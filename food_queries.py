import pandas as pd
import mysql.connector
import os

# ── Config ──────────────────────────────────────────────────────────────────
DB_CONFIG = {
    "host": "localhost",
    "port": 3306,
    "user": "root",
    "password": "Admin@1234",
    "database": "food_wastage_db"
}
OUTPUT_DIR = "data/query_results"
os.makedirs(OUTPUT_DIR, exist_ok=True)

print("=" * 60)
print("LOCAL FOOD WASTAGE MANAGEMENT SYSTEM - SQL QUERIES")
print("=" * 60)

conn = mysql.connector.connect(**DB_CONFIG)

QUERIES = {

    # ── FROM DOC (mandatory questions) ──────────────────────────────────────

    "Q01_providers_receivers_by_city": {
        "title": "Number of Providers and Receivers by City",
        "sql": """
            SELECT p.City,
                   COUNT(DISTINCT p.Provider_ID) AS Total_Providers,
                   COUNT(DISTINCT r.Receiver_ID) AS Total_Receivers
            FROM providers p
            LEFT JOIN receivers r ON p.City = r.City
            GROUP BY p.City
            ORDER BY Total_Providers DESC
            LIMIT 20
        """
    },

    "Q02_provider_type_most_food": {
        "title": "Which Provider Type Contributes Most Food",
        "sql": """
            SELECT p.Type AS Provider_Type,
                   COUNT(f.Food_ID)   AS Total_Listings,
                   SUM(f.Quantity)    AS Total_Quantity
            FROM providers p
            JOIN food_listings f ON p.Provider_ID = f.Provider_ID
            GROUP BY p.Type
            ORDER BY Total_Quantity DESC
        """
    },

    "Q03_provider_contact_by_city": {
        "title": "Provider Contact Information by City",
        "sql": """
            SELECT p.City, p.Name AS Provider_Name,
                   p.Type, p.Address, p.Contact
            FROM providers p
            ORDER BY p.City, p.Name
        """
    },

    "Q04_receivers_most_claimed": {
        "title": "Receivers Who Claimed the Most Food",
        "sql": """
            SELECT r.Name AS Receiver_Name, r.Type, r.City,
                   COUNT(c.Claim_ID)  AS Total_Claims,
                   SUM(CASE WHEN c.Status = 'Completed' THEN 1 ELSE 0 END) AS Completed_Claims
            FROM receivers r
            JOIN claims c ON r.Receiver_ID = c.Receiver_ID
            GROUP BY r.Receiver_ID, r.Name, r.Type, r.City
            ORDER BY Total_Claims DESC
            LIMIT 10
        """
    },

    "Q05_total_food_quantity": {
        "title": "Total Quantity of Food Available from All Providers",
        "sql": """
            SELECT p.Name AS Provider_Name, p.Type, p.City,
                   SUM(f.Quantity) AS Total_Quantity_Donated
            FROM providers p
            JOIN food_listings f ON p.Provider_ID = f.Provider_ID
            GROUP BY p.Provider_ID, p.Name, p.Type, p.City
            ORDER BY Total_Quantity_Donated DESC
            LIMIT 15
        """
    },

    "Q06_city_highest_food_listings": {
        "title": "City with Highest Number of Food Listings",
        "sql": """
            SELECT f.Location AS City,
                   COUNT(f.Food_ID)  AS Total_Listings,
                   SUM(f.Quantity)   AS Total_Quantity
            FROM food_listings f
            GROUP BY f.Location
            ORDER BY Total_Listings DESC
            LIMIT 15
        """
    },

    "Q07_most_common_food_types": {
        "title": "Most Commonly Available Food Types",
        "sql": """
            SELECT Food_Type,
                   COUNT(*)       AS Total_Items,
                   SUM(Quantity)  AS Total_Quantity,
                   ROUND(COUNT(*) * 100.0 / (SELECT COUNT(*) FROM food_listings), 2) AS Percentage
            FROM food_listings
            GROUP BY Food_Type
            ORDER BY Total_Items DESC
        """
    },

    "Q08_claims_per_food_item": {
        "title": "Number of Claims per Food Item",
        "sql": """
            SELECT f.Food_ID, f.Food_Name, f.Food_Type, f.Meal_Type,
                   COUNT(c.Claim_ID) AS Total_Claims
            FROM food_listings f
            LEFT JOIN claims c ON f.Food_ID = c.Food_ID
            GROUP BY f.Food_ID, f.Food_Name, f.Food_Type, f.Meal_Type
            ORDER BY Total_Claims DESC
            LIMIT 15
        """
    },

    "Q09_provider_most_successful_claims": {
        "title": "Provider with Highest Successful Food Claims",
        "sql": """
            SELECT p.Name AS Provider_Name, p.Type, p.City,
                   COUNT(c.Claim_ID) AS Total_Claims,
                   SUM(CASE WHEN c.Status = 'Completed' THEN 1 ELSE 0 END) AS Successful_Claims
            FROM providers p
            JOIN food_listings f ON p.Provider_ID = f.Provider_ID
            JOIN claims c        ON f.Food_ID = c.Food_ID
            GROUP BY p.Provider_ID, p.Name, p.Type, p.City
            ORDER BY Successful_Claims DESC
            LIMIT 10
        """
    },

    "Q10_claim_status_percentage": {
        "title": "Claim Status Percentage (Completed vs Pending vs Cancelled)",
        "sql": """
            SELECT Status,
                   COUNT(*) AS Total_Claims,
                   ROUND(COUNT(*) * 100.0 / (SELECT COUNT(*) FROM claims), 2) AS Percentage
            FROM claims
            GROUP BY Status
            ORDER BY Total_Claims DESC
        """
    },

    "Q11_avg_quantity_per_receiver": {
        "title": "Average Quantity of Food Claimed per Receiver",
        "sql": """
            SELECT r.Name AS Receiver_Name, r.Type, r.City,
                   COUNT(c.Claim_ID) AS Total_Claims,
                   ROUND(AVG(f.Quantity), 2) AS Avg_Quantity_Claimed
            FROM receivers r
            JOIN claims c        ON r.Receiver_ID = c.Receiver_ID
            JOIN food_listings f ON c.Food_ID = f.Food_ID
            GROUP BY r.Receiver_ID, r.Name, r.Type, r.City
            ORDER BY Avg_Quantity_Claimed DESC
            LIMIT 10
        """
    },

    "Q12_most_claimed_meal_type": {
        "title": "Most Claimed Meal Type (Breakfast/Lunch/Dinner/Snacks)",
        "sql": """
            SELECT f.Meal_Type,
                   COUNT(c.Claim_ID) AS Total_Claims,
                   SUM(f.Quantity)   AS Total_Quantity,
                   ROUND(COUNT(c.Claim_ID) * 100.0 / (SELECT COUNT(*) FROM claims), 2) AS Claim_Percentage
            FROM food_listings f
            JOIN claims c ON f.Food_ID = c.Food_ID
            GROUP BY f.Meal_Type
            ORDER BY Total_Claims DESC
        """
    },

    "Q13_total_donated_qty_by_provider": {
        "title": "Total Donated Quantity by Each Provider",
        "sql": """
            SELECT p.Name AS Provider_Name, p.Type, p.City,
                   SUM(f.Quantity) AS Total_Donated_Quantity
            FROM providers p
            JOIN food_listings f ON p.Provider_ID = f.Provider_ID
            GROUP BY p.Provider_ID, p.Name, p.Type, p.City
            ORDER BY Total_Donated_Quantity DESC
            LIMIT 15
        """
    },

    # ── ADDITIONAL (insights & trends) ──────────────────────────────────────

    "Q14_unclaimed_food_waste": {
        "title": "Unclaimed Food Items (Potential Waste)",
        "sql": """
            SELECT f.Food_ID, f.Food_Name, f.Quantity,
                   f.Expiry_Date, f.Food_Type, f.Meal_Type,
                   p.Name AS Provider_Name, p.City
            FROM food_listings f
            JOIN providers p ON f.Provider_ID = p.Provider_ID
            LEFT JOIN claims c ON f.Food_ID = c.Food_ID
            WHERE c.Claim_ID IS NULL
            ORDER BY f.Quantity DESC
            LIMIT 20
        """
    },

    "Q15_daily_claims_trend": {
        "title": "Daily Claims Trend Over Time",
        "sql": """
            SELECT DATE(Timestamp) AS Claim_Date,
                   COUNT(*) AS Total_Claims,
                   SUM(CASE WHEN Status = 'Completed' THEN 1 ELSE 0 END) AS Completed,
                   SUM(CASE WHEN Status = 'Cancelled' THEN 1 ELSE 0 END) AS Cancelled,
                   SUM(CASE WHEN Status = 'Pending'   THEN 1 ELSE 0 END) AS Pending
            FROM claims
            GROUP BY DATE(Timestamp)
            ORDER BY Claim_Date ASC
        """
    },

    "Q16_food_type_vs_meal_type_matrix": {
        "title": "Food Type vs Meal Type Quantity Matrix",
        "sql": """
            SELECT Food_Type, Meal_Type,
                   COUNT(*)                    AS Total_Items,
                   SUM(Quantity)               AS Total_Quantity,
                   ROUND(AVG(Quantity), 2)     AS Avg_Quantity
            FROM food_listings
            GROUP BY Food_Type, Meal_Type
            ORDER BY Food_Type, Total_Quantity DESC
        """
    },

    "Q17_receiver_type_claim_success": {
        "title": "Claim Success Rate by Receiver Type",
        "sql": """
            SELECT r.Type AS Receiver_Type,
                   COUNT(c.Claim_ID) AS Total_Claims,
                   SUM(CASE WHEN c.Status = 'Completed' THEN 1 ELSE 0 END) AS Completed,
                   SUM(CASE WHEN c.Status = 'Cancelled' THEN 1 ELSE 0 END) AS Cancelled,
                   ROUND(SUM(CASE WHEN c.Status = 'Completed' THEN 1 ELSE 0 END) * 100.0 / COUNT(*), 2) AS Success_Rate_Pct
            FROM claims c
            JOIN receivers r ON c.Receiver_ID = r.Receiver_ID
            GROUP BY r.Type
            ORDER BY Success_Rate_Pct DESC
        """
    },

    "Q18_full_claim_details": {
        "title": "Full Claim Details — Food + Provider + Receiver",
        "sql": """
            SELECT c.Claim_ID, c.Status, c.Timestamp,
                   f.Food_Name, f.Food_Type, f.Meal_Type,
                   f.Quantity, f.Expiry_Date,
                   p.Name AS Provider_Name, p.Type AS Provider_Type,
                   p.City AS Provider_City, p.Contact AS Provider_Contact,
                   r.Name AS Receiver_Name, r.Type AS Receiver_Type,
                   r.City AS Receiver_City
            FROM claims c
            JOIN food_listings f ON c.Food_ID = f.Food_ID
            JOIN providers p     ON f.Provider_ID = p.Provider_ID
            JOIN receivers r     ON c.Receiver_ID = r.Receiver_ID
            ORDER BY c.Timestamp DESC
        """
    }

}

# ── Run & Save ───────────────────────────────────────────────────────────────
print(f"\nRunning {len(QUERIES)} queries...\n")

for key, q in QUERIES.items():
    try:
        df = pd.read_sql(q["sql"], conn)
        out_path = f"{OUTPUT_DIR}/{key}.csv"
        df.to_csv(out_path, index=False)
        print(f"  ✔ {key} → {len(df)} rows")
    except Exception as e:
        print(f"  ✘ {key} FAILED: {e}")

conn.close()

print("\n" + "=" * 60)
print("QUERY SUMMARY")
print("=" * 60)
print(f"  Total Queries  : {len(QUERIES)}")
print(f"  Doc Questions  : Q01 - Q13 (13 mandatory)")
print(f"  Extra Insights : Q14 - Q18 (5 additional)")
print(f"  Results saved  : {OUTPUT_DIR}/")
print("\n✔ Phase 2 Queries Complete — Ready for EDA (Phase 3)")
