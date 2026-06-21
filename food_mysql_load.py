import pandas as pd
import mysql.connector
from mysql.connector import Error

# ── Config ─────────────────────────────────────────────────────────────────
DB_CONFIG = {
    "host": "localhost",
    "port": 3306,
    "user": "root",
    "password": "Admin@1234"
}
DB_NAME = "food_wastage_db"
CLEANED_DIR = "data/cleaned"

# ── Connect ─────────────────────────────────────────────────────────────────
def get_connection(database=None):
    cfg = DB_CONFIG.copy()
    if database:
        cfg["database"] = database
    return mysql.connector.connect(**cfg)

print("=" * 60)
print("LOCAL FOOD WASTAGE MANAGEMENT SYSTEM - MYSQL LOAD")
print("=" * 60)

# ── Step 1: Create Database ─────────────────────────────────────────────────
print("\n[1/6] Creating database...")
conn = get_connection()
cursor = conn.cursor()
cursor.execute(f"DROP DATABASE IF EXISTS {DB_NAME}")
cursor.execute(f"CREATE DATABASE {DB_NAME}")
cursor.close()
conn.close()
print(f"  ✔ Database '{DB_NAME}' created")

# ── Step 2: Create Tables ───────────────────────────────────────────────────
print("\n[2/6] Creating tables...")
conn = get_connection(DB_NAME)
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE providers (
    Provider_ID   INT PRIMARY KEY,
    Name          VARCHAR(255) NOT NULL,
    Type          VARCHAR(100),
    Address       VARCHAR(500),
    City          VARCHAR(100),
    Contact       VARCHAR(100)
)
""")

cursor.execute("""
CREATE TABLE receivers (
    Receiver_ID   INT PRIMARY KEY,
    Name          VARCHAR(255) NOT NULL,
    Type          VARCHAR(100),
    City          VARCHAR(100),
    Contact       VARCHAR(100)
)
""")

cursor.execute("""
CREATE TABLE food_listings (
    Food_ID       INT PRIMARY KEY,
    Food_Name     VARCHAR(255),
    Quantity      INT,
    Expiry_Date   DATE,
    Provider_ID   INT,
    Provider_Type VARCHAR(100),
    Location      VARCHAR(255),
    Food_Type     VARCHAR(50),
    Meal_Type     VARCHAR(50),
    FOREIGN KEY (Provider_ID) REFERENCES providers(Provider_ID)
)
""")

cursor.execute("""
CREATE TABLE claims (
    Claim_ID     INT PRIMARY KEY,
    Food_ID      INT,
    Receiver_ID  INT,
    Status       VARCHAR(50),
    Timestamp    DATETIME,
    FOREIGN KEY (Food_ID)     REFERENCES food_listings(Food_ID),
    FOREIGN KEY (Receiver_ID) REFERENCES receivers(Receiver_ID)
)
""")

conn.commit()
cursor.close()
conn.close()
print("  ✔ Tables created: providers, receivers, food_listings, claims")

# ── Step 3: Load CSVs ───────────────────────────────────────────────────────
print("\n[3/6] Loading cleaned CSVs...")

providers = pd.read_csv(f"{CLEANED_DIR}/providers_cleaned.csv")
receivers = pd.read_csv(f"{CLEANED_DIR}/receivers_cleaned.csv")
food      = pd.read_csv(f"{CLEANED_DIR}/food_listings_cleaned.csv")
claims    = pd.read_csv(f"{CLEANED_DIR}/claims_cleaned.csv")

# Fix date formats
food['Expiry_Date']    = pd.to_datetime(food['Expiry_Date'], errors='coerce').dt.strftime('%Y-%m-%d')
claims['Timestamp']    = pd.to_datetime(claims['Timestamp'], errors='coerce').dt.strftime('%Y-%m-%d %H:%M:%S')

print(f"  providers : {len(providers)} rows")
print(f"  receivers : {len(receivers)} rows")
print(f"  food      : {len(food)} rows")
print(f"  claims    : {len(claims)} rows")

# ── Step 4: Insert Data ─────────────────────────────────────────────────────
print("\n[4/6] Inserting data into MySQL...")
conn = get_connection(DB_NAME)
cursor = conn.cursor()

# Providers
for _, row in providers.iterrows():
    cursor.execute("""
        INSERT INTO providers (Provider_ID, Name, Type, Address, City, Contact)
        VALUES (%s, %s, %s, %s, %s, %s)
    """, tuple(row))
print(f"  ✔ providers → {len(providers)} rows inserted")

# Receivers
for _, row in receivers.iterrows():
    cursor.execute("""
        INSERT INTO receivers (Receiver_ID, Name, Type, City, Contact)
        VALUES (%s, %s, %s, %s, %s)
    """, tuple(row))
print(f"  ✔ receivers → {len(receivers)} rows inserted")

# Food Listings
for _, row in food.iterrows():
    cursor.execute("""
        INSERT INTO food_listings
        (Food_ID, Food_Name, Quantity, Expiry_Date, Provider_ID, Provider_Type, Location, Food_Type, Meal_Type)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
    """, tuple(row))
print(f"  ✔ food_listings → {len(food)} rows inserted")

# Claims
for _, row in claims.iterrows():
    cursor.execute("""
        INSERT INTO claims (Claim_ID, Food_ID, Receiver_ID, Status, Timestamp)
        VALUES (%s, %s, %s, %s, %s)
    """, tuple(row))
print(f"  ✔ claims → {len(claims)} rows inserted")

conn.commit()
cursor.close()
conn.close()

# ── Step 5: Verify ──────────────────────────────────────────────────────────
print("\n[5/6] Verifying row counts...")
conn = get_connection(DB_NAME)
cursor = conn.cursor()
for table in ["providers", "receivers", "food_listings", "claims"]:
    cursor.execute(f"SELECT COUNT(*) FROM {table}")
    count = cursor.fetchone()[0]
    print(f"  {table:20s} → {count} rows")
cursor.close()
conn.close()

# ── Step 6: Done ────────────────────────────────────────────────────────────
print("\n" + "=" * 60)
print("MYSQL LOAD SUMMARY")
print("=" * 60)
print(f"  Database : {DB_NAME}")
print(f"  Host     : localhost:3306")
print(f"  Tables   : providers, receivers, food_listings, claims")
print("\n✔ Phase 2 Complete — Ready for SQL Queries")
