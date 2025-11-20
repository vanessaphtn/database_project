# Database Project: The Metropolitan Museum of Art Collection Database
## Project Setup Guide
### 1. Install Requirements

Before starting, make sure you have these installed on your computer:

- **Git** → [https://git-scm.com/downloads](https://git-scm.com/downloads)  
- **Docker** and **Docker Compose** → [https://www.docker.com/get-started](https://www.docker.com/get-started)   

---

### 2. Download the Project

Open a terminal (Command Prompt / Powershell / Terminal) and run the following commands:

```
git clone https://github.com/vanessaphtn/database_project.git
cd database_project
```

### 3. Prepare the Data
The main `artworks.csv` file is too large for GitHub. You need to download it manually: [artworks.csv](https://drive.google.com/file/d/1tFtoqr3KCXUvyb7vB4aDfdaEesj7rhdx/view?usp=share_link)
Place the downloaded file into the `data/` folder of your project (`database_project/data/artworks.csv`)
Make sure the file name and location are correct.

### 4. Start the Database
From the project folder in your terminal, run:
```
docker compose up --build
```
This will start all necessary services (PostgreSQL database, loaders, etc.) in Docker.

### 5. Open PgAdmin
Open PgAdmin in your browser at:
```
http://localhost:5050
```
Log in using the credentials:
```
Email: admin@admin.com
Password: root
```
These credentials are also stored in the `.env` file in the project.

### 6. Add a New Server in PgAdmin
Click Add New Server. <br>
Give it any **Name** you like (e.g., Database Project).<br>
Fill in the **Connection** fields as follows:<br>
**Host**: db<br>
**Port**: 5432<br>
**Maintenance database**: met_museum_db (or as defined in .env)<br>
**Username**: user (or as defined in .env)<br>
**Password**: password (or as defined in .env)<br>
Save the server.<br>
<img width="696" height="549" alt="Screenshot 2025-11-20 at 09 49 01" src="https://github.com/user-attachments/assets/4a2d6c7d-63dd-4e4c-85ae-1a2eb6ca5857" />

### 7. Database & Data Insertion
The database and all tables are automatically created and populated when Docker starts.<br>
It may take 1–2 minutes for all data to appear.<br>
You should see a screen like this when everything is ready:<br>
<img width="832" height="173" alt="Screenshot 2025-11-20 at 09 48 10" src="https://github.com/user-attachments/assets/af6cf980-6500-4770-b440-9d9a74eb3171" />
<img width="696" height="312" alt="Screenshot 2025-11-20 at 09 50 57" src="https://github.com/user-attachments/assets/bc941af4-484f-40a1-b29d-a03f56812ec4" />

### 8. Working with the Database
You can now browse tables in PgAdmin.<br>
You can run SQL queries, explore the data, and connect scripts to the database.<br>
