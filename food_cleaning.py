import pandas as pd
import os

# ── Config ─────────────────────────────────────────────────────────────────
INPUT_DIR = "data/raw"
OUTPUT_DIR = "data/cleaned"
os.makedirs(OUTPUT_DIR, exist_ok=True)

print("=" * 60)
print("LOCAL FOOD WASTAGE MANAGEMENT SYSTEM - DATA CLEANING")
print("=" * 60)

# ══════════════════════════════════════════════════════════════
# 1. PROVIDERS
# ══════════════════════════════════════════════════════════════
print("\n[1/4] Cleaning providers_data...")
providers = pd.read_csv(f"{INPUT_DIR}/providers_data.csv")

print(f"  Shape         : {providers.shape}")
print(f"  Null values   :\n{providers.isnull().sum().to_string()}")
print(f"  Duplicates    : {providers.duplicated().sum()}")

# Drop duplicates
providers.drop_duplicates(inplace=True)

# Fill missing Contact/Address with 'Not Available'
providers['Contact'] = providers['Contact'].fillna('Not Available')
providers['Address'] = providers['Address'].fillna('Not Available')

# Strip whitespace
providers['Name'] = providers['Name'].str.strip()
providers['City'] = providers['City'].str.strip()
providers['Type'] = providers['Type'].str.strip()

print(f"  Provider Types: {providers['Type'].unique().tolist()}")
print(f"  Cities        : {providers['City'].nunique()} unique")
print(f"  Final Shape   : {providers.shape}")

providers.to_csv(f"{OUTPUT_DIR}/providers_cleaned.csv", index=False)
print("  ✔ Saved → providers_cleaned.csv")

# ══════════════════════════════════════════════════════════════
# 2. RECEIVERS
# ══════════════════════════════════════════════════════════════
print("\n[2/4] Cleaning receivers_data...")
receivers = pd.read_csv(f"{INPUT_DIR}/receivers_data.csv")

print(f"  Shape         : {receivers.shape}")
print(f"  Null values   :\n{receivers.isnull().sum().to_string()}")
print(f"  Duplicates    : {receivers.duplicated().sum()}")

receivers.drop_duplicates(inplace=True)

# Fill missing contact
receivers['Contact'] = receivers['Contact'].fillna('Not Available')

# Strip whitespace
receivers['Name'] = receivers['Name'].str.strip()
receivers['City'] = receivers['City'].str.strip()
receivers['Type'] = receivers['Type'].str.strip()

print(f"  Receiver Types: {receivers['Type'].unique().tolist()}")
print(f"  Cities        : {receivers['City'].nunique()} unique")
print(f"  Final Shape   : {receivers.shape}")

receivers.to_csv(f"{OUTPUT_DIR}/receivers_cleaned.csv", index=False)
print("  ✔ Saved → receivers_cleaned.csv")

# ══════════════════════════════════════════════════════════════
# 3. FOOD LISTINGS
# ══════════════════════════════════════════════════════════════
print("\n[3/4] Cleaning food_listings_data...")
food = pd.read_csv(f"{INPUT_DIR}/food_listings_data.csv")

print(f"  Shape         : {food.shape}")
print(f"  Null values   :\n{food.isnull().sum().to_string()}")
print(f"  Duplicates    : {food.duplicated().sum()}")

food.drop_duplicates(inplace=True)

# Fill missing Quantity with median
if food['Quantity'].isnull().sum() > 0:
    median_qty = food['Quantity'].median()
    food['Quantity'] = food['Quantity'].fillna(median_qty)
    print(f"  Filled Quantity nulls with median: {median_qty}")

# Fill missing Expiry_Date with 'Unknown'
food['Expiry_Date'] = food['Expiry_Date'].fillna('Unknown')

# Convert Expiry_Date to datetime
food['Expiry_Date'] = pd.to_datetime(food['Expiry_Date'], errors='coerce')

# Strip whitespace
food['Food_Name'] = food['Food_Name'].str.strip()
food['Food_Type'] = food['Food_Type'].str.strip()
food['Meal_Type'] = food['Meal_Type'].str.strip()
food['Location'] = food['Location'].str.strip()
food['Provider_Type'] = food['Provider_Type'].str.strip()

# Ensure Quantity is integer
food['Quantity'] = food['Quantity'].astype(int)

print(f"  Food Types    : {food['Food_Type'].unique().tolist()}")
print(f"  Meal Types    : {food['Meal_Type'].unique().tolist()}")
print(f"  Quantity Range: {food['Quantity'].min()} - {food['Quantity'].max()}")
print(f"  Final Shape   : {food.shape}")

food.to_csv(f"{OUTPUT_DIR}/food_listings_cleaned.csv", index=False)
print("  ✔ Saved → food_listings_cleaned.csv")

# ══════════════════════════════════════════════════════════════
# 4. CLAIMS
# ══════════════════════════════════════════════════════════════
print("\n[4/4] Cleaning claims_data...")
claims = pd.read_csv(f"{INPUT_DIR}/claims_data.csv")

print(f"  Shape         : {claims.shape}")
print(f"  Null values   :\n{claims.isnull().sum().to_string()}")
print(f"  Duplicates    : {claims.duplicated().sum()}")

claims.drop_duplicates(inplace=True)

# Fill missing Status with 'Pending'
claims['Status'] = claims['Status'].fillna('Pending')

# Convert Timestamp to datetime
claims['Timestamp'] = pd.to_datetime(claims['Timestamp'], errors='coerce')

# Fill missing Timestamp with NaT (keep as unknown)
print(f"  Status Values : {claims['Status'].unique().tolist()}")
print(f"  Timestamp Range: {claims['Timestamp'].min()} → {claims['Timestamp'].max()}")
print(f"  Final Shape   : {claims.shape}")

claims.to_csv(f"{OUTPUT_DIR}/claims_cleaned.csv", index=False)
print("  ✔ Saved → claims_cleaned.csv")

# ══════════════════════════════════════════════════════════════
# SUMMARY
# ══════════════════════════════════════════════════════════════
print("\n" + "=" * 60)
print("CLEANING SUMMARY")
print("=" * 60)
print(f"  providers_cleaned.csv  → {providers.shape[0]} rows, {providers.shape[1]} cols")
print(f"  receivers_cleaned.csv  → {receivers.shape[0]} rows, {receivers.shape[1]} cols")
print(f"  food_listings_cleaned.csv → {food.shape[0]} rows, {food.shape[1]} cols")
print(f"  claims_cleaned.csv     → {claims.shape[0]} rows, {claims.shape[1]} cols")
print("\n✔ All files saved to data/cleaned/")
print("✔ Phase 1 Complete — Ready for MySQL load")
