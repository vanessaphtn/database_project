import psycopg2
import csv
import os

# --- Database connection ---
conn = psycopg2.connect(
    host="db",                 
    port=5432,
    database=os.environ["POSTGRES_DB"],
    user=os.environ["POSTGRES_USER"],
    password=os.environ["POSTGRES_PASSWORD"]
)

cur = conn.cursor()

# --- Helper functions ---

def clean_value(v):
    if v is None:
        return None
    v = str(v).strip()
    if v in ("", "null", "[null]", "NaN"):
        return None
    return v

def load_artists(csv_file):
    print("Inserting artists...")

    with open(csv_file, newline='', encoding="utf-8") as f:
        reader = csv.DictReader(f)

        for row in reader:
            cur.execute("""
                INSERT INTO artists (name, nationality, birth, death, gender)
                VALUES (%s, %s, %s, %s, %s)
                ON CONFLICT (name) DO NOTHING;
            """, (
                clean_value(row["Artist Display Name"]),
                clean_value(row["Artist Nationality"]),
                int(row["Artist Begin Date"]) if row["Artist Begin Date"].isdigit() else None,
                int(row["Artist End Date"]) if row["Artist End Date"].isdigit() else None,
                clean_value(row["Artist Gender"])
            ))
    conn.commit()
    print("Done: artists")

def load_departments(csv_file):
    print("Inserting departments...")

    with open(csv_file, newline='', encoding="utf-8") as f:
        reader = csv.DictReader(f)

        for row in reader:
            dept = row["Department"]
            if not dept:
                continue

            cur.execute("""
                INSERT INTO departments (name)
                VALUES (%s)
                ON CONFLICT (name) DO NOTHING;
            """, (dept,))
    conn.commit()
    print("Done: departments")

def load_origins(csv_file):
    print("Inserting origins...")

    with open(csv_file, newline='', encoding="utf-8") as f:
        reader = csv.DictReader(f)

        for row in reader:

            cur.execute("""
                INSERT INTO origins (city, country, region, culture)
                VALUES (%s, %s, %s, %s)
                ON CONFLICT (city, country, region, culture) DO NOTHING; 
            """, (
                clean_value(row["City"]),
                clean_value(row["Country"]),
                clean_value(row["Region"]),
                clean_value(row["Culture"])
            ))

    conn.commit()
    print("Done: origins")

def load_periods(csv_file):
    print("Inserting periods...")

    with open(csv_file, newline='', encoding="utf-8") as f:
        reader = csv.DictReader(f)

        for row in reader:
            cur.execute("""
                INSERT INTO periods (period, dynasty, reign)
                VALUES (%s, %s, %s)
                ON CONFLICT (period, dynasty, reign) DO NOTHING;
            """, (
                clean_value(row["Period"]),
                clean_value(row["Dynasty"]),
                clean_value(row["Reign"])
            ))
    conn.commit()
    print("Done: periods")

def load_mediums(csv_file):
    print("Inserting mediums...")

    with open(csv_file, newline='', encoding="utf-8") as f:
        reader = csv.DictReader(f)

        for row in reader:
            dept = row["Medium"]
            if not dept:
                continue

            cur.execute("""
                INSERT INTO mediums (medium)
                VALUES (%s)
                ON CONFLICT (medium) DO NOTHING;
            """, (dept,))
    conn.commit()
    print("Done: mediums")

def load_artworks(csv_file):
    print("Inserting artworks...")
    with open(csv_file, newline='', encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            object_id = row["Object ID"]
            is_highlight = row["Is Highlight"].strip().lower() == "true"
            is_public_domain = row["Is Public Domain"].strip().lower() == "true"
            department_name = clean_value(row["Department"])
            city = clean_value(row["City"])
            country = clean_value(row["Country"])
            region = clean_value(row["Region"])
            culture_name = clean_value(row["Culture"])
            period_name = clean_value(row["Period"])
            dynasty = clean_value(row["Dynasty"])
            reign = clean_value(row["Reign"])
            object_name = clean_value(row["Object Name"])
            classification = clean_value(row["Classification"])
            title = clean_value(row["Title"])
            accession_year = int(row["AccessionYear"]) if row["AccessionYear"].isdigit() else None
            object_date = clean_value(row["Object Date"])
            object_begin_date = int(row["Object Begin Date"]) if row["Object Begin Date"].isdigit() else None
            object_end_date = int(row["Object End Date"]) if row["Object End Date"].isdigit() else None
            dimensions = clean_value(row["Dimensions"])

            # --- Lookup foreign keys ---
            # Department
            cur.execute("SELECT departmentId FROM departments WHERE name=%s", (department_name,))
            department_id_row = cur.fetchone()
            department_id = department_id_row[0] if department_id_row else None

            # connections to origins table
            origin_id = get_origin_id(city, country, region, culture_name)

            # connections to periods table
            period_id = get_period_id(period_name, dynasty, reign)

            # --- Insert artwork ---
            cur.execute("""
                INSERT INTO artworks (
                    objectId, departmentId, originId, periodId,
                    isHighlight, isPublicDomain, objectName,
                    classification, title, accessionYear, objectDate,
                    objectBeginDate, objectEndDate, dimensions
                )
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                ON CONFLICT (objectId) DO NOTHING;
            """, (
                object_id, department_id, origin_id, period_id,
                is_highlight, is_public_domain, object_name,
                classification, title, accession_year, object_date,
                object_begin_date, object_end_date, dimensions
            ))
    conn.commit()
    print("Done: artworks")

def get_origin_id(city, country, region, culture):
    query = """
        SELECT originId FROM origins
        WHERE city IS NOT DISTINCT FROM %s
          AND country IS NOT DISTINCT FROM %s
          AND region IS NOT DISTINCT FROM %s
          AND culture IS NOT DISTINCT FROM %s
    """
    cur.execute(query, (city, country, region, culture))
    row = cur.fetchone()
    return row[0] if row else None

def get_period_id(period,dynasty,reign):
    query = """
        SELECT periodId FROM periods
        WHERE period IS NOT DISTINCT FROM %s
          AND dynasty IS NOT DISTINCT FROM %s
          AND reign IS NOT DISTINCT FROM %s
    """
    cur.execute(query, (period,dynasty,reign))
    row = cur.fetchone()
    return row[0] if row else None

def load_artwork_artists(csv_file):
    print("Inserting artwork–artist relations...")

    with open(csv_file, newline='', encoding="utf-8") as f:
        reader = csv.DictReader(f)

        for row in reader:
            object_id = row["Object ID"]
            artist_name = clean_value(row["Artist Display Name"])

            # --- find artistId ---
            cur.execute("SELECT artistId FROM artists WHERE name = %s", (artist_name,))
            artist_row = cur.fetchone()
            if not artist_row:
                continue
            artist_id = artist_row[0]

            # --- Insert junction ---
            cur.execute("""
                INSERT INTO artworkArtist (objectId, artistId)
                VALUES (%s, %s)
                ON CONFLICT DO NOTHING;
            """, (object_id, artist_id))

    conn.commit()
    print("Done: artwork–artist")

def load_artwork_mediums(csv_file):
    print("Inserting artwork–medium relations...")

    with open(csv_file, newline='', encoding="utf-8") as f:
        reader = csv.DictReader(f)

        for row in reader:
            object_id = row["Object ID"]
            medium = clean_value(row["Medium"])

            # --- find artistId ---
            cur.execute("SELECT mediumId FROM mediums WHERE medium = %s", (medium,))
            medium_row = cur.fetchone()
            if not medium_row:
                continue
            medium_id = medium_row[0]

            # --- Insert junction ---
            cur.execute("""
                INSERT INTO artworkMedium (objectId, mediumId)
                VALUES (%s, %s)
                ON CONFLICT DO NOTHING;
            """, (object_id, medium_id))

    conn.commit()
    print("Done: artwork–medium")

# --- Load lookup tables ---
load_artists("data/artists_unique.csv")
load_departments("data/departments.csv")
load_origins("data/origins.csv")
load_periods("data/periods.csv")
load_mediums("data/mediums.csv")
load_artworks("data/artworks.csv")
#load_artwork_artists("data/artwork_artist.csv")
#load_artwork_mediums("data/artwork_medium.csv")
cur.close()
conn.close()
print("All lookup tables inserted")
