import pandas as pd
from sqlalchemy import create_engine, text

# ---------- CONFIG ----------
DB_USER = "postgres"
DB_PASS = "your_password"
DB_NAME = "your_db"
DB_HOST = "localhost"   # because you're connecting from your Mac
DB_PORT = 5432

CSV_FILE = "MetObjects_clean.csv"

# ---------- CONNECT ----------
engine = create_engine(f"postgresql://{DB_USER}:{DB_PASS}@{DB_HOST}:{DB_PORT}/{DB_NAME}")

df = pd.read_csv(CSV_FILE)

# Replace NaN with None for SQL inserts
df = df.where(pd.notnull(df), None)

# ---------- HELPERS ----------
def split_field(value):
    if value is None:
        return []
    return [v.strip() for v in str(value).split("|") if v.strip()]

# ---------- 1. Insert unique artists ----------
artist_dict = {}   # name -> artistId mapping

with engine.begin() as conn:
    for _, row in df.iterrows():
        artist_names = split_field(row["Artist Display Name"])
        artist_bios = split_field(row["Artist Display Bio"])
        artist_nation = split_field(row["Artist Nationality"])
        artist_birth = split_field(row["Artist Begin Date"])
        artist_death = split_field(row["Artist End Date"])
        artist_gender = split_field(row["Artist Gender"])

        # Align lengths (example: 2 artists → 2 bios, etc.)
        max_len = len(artist_names)
        artist_bios += [None] * (max_len - len(artist_bios))
        artist_nation += [None] * (max_len - len(artist_nation))
        artist_birth += [None] * (max_len - len(artist_birth))
        artist_death += [None] * (max_len - len(artist_death))
        artist_gender += [None] * (max_len - len(artist_gender))

        for i in range(len(artist_names)):
            name = artist_names[i]
            if name in artist_dict:
                continue

            result = conn.execute(
                text("""
                    INSERT INTO artists (artistDisplayName, artistDisplayBio, nationality,
                                         birth, death, gender)
                    VALUES (:name, :bio, :nation, :birth, :death, :gender)
                    RETURNING artistId;
                """),
                {
                    "name": name,
                    "bio": artist_bios[i],
                    "nation": artist_nation[i],
                    "birth": int(artist_birth[i]) if artist_birth[i] else None,
                    "death": int(artist_death[i]) if artist_death[i] else None,
                    "gender": artist_gender[i],
                }
            )
            artist_id = result.scalar()
            artist_dict[name] = artist_id

print("Artists inserted:", len(artist_dict))

# ---------- 2. Insert artworks + many-to-many mapping ----------
with engine.begin() as conn:
    for _, row in df.iterrows():
        object_id = int(row["Object ID"])

        # Insert artwork
        conn.execute(
            text("""
                INSERT INTO artworks (
                    objectId, artistId, medium, departmentId,
                    isHighlight, isPublicDomain, objectName,
                    classification, title, accessionYear,
                    objectDate, objectBeginDate, objectEndDate,
                    dimensions
                )
                VALUES (
                    :objectId, NULL, NULL, 1,
                    :isHighlight, :isPublicDomain, :objectName,
                    :classification, :title, :accessionYear,
                    :objectDate, :beginDate, :endDate,
                    :dimensions
                )
                ON CONFLICT (objectId) DO NOTHING;
            """),
            {
                "objectId": object_id,
                "isHighlight": row["Is Highlight"],
                "isPublicDomain": row["Is Public Domain"],
                "objectName": row["Object Name"],
                "classification": row["Classification"],
                "title": row["Title"],
                "accessionYear": row["AccessionYear"],
                "objectDate": row["Object Date"],
                "beginDate": row["Object Begin Date"],
                "endDate": row["Object End Date"],
                "dimensions": row["Dimensions"],
            }
        )

        # Link artists to artwork
        artist_names = split_field(row["Artist Display Name"])

        for name in artist_names:
            conn.execute(
                text("""
                    INSERT INTO artworkArtist (objectId, artistId)
                    VALUES (:objectId, :artistId)
                    ON CONFLICT DO NOTHING;
                """),
                {
                    "objectId": object_id,
                    "artistId": artist_dict[name]
                }
            )

print("Artworks + mappings inserted successfully!")
