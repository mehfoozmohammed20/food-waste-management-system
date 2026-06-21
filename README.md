# Local Food Wastage Management System

A data analytics and web application project that connects food providers (restaurants, grocery stores, supermarkets, catering services) with receivers (NGOs, shelters, individuals, charities) to reduce food wastage and fight hunger.

## Live App

[Add your Streamlit Cloud link here after deployment]

## Project Overview

Surplus food from restaurants and stores often goes to waste while many people face food insecurity. This system provides a centralized platform where:

- Providers list surplus food
- Receivers claim available food
- Every claim is tracked from pending to completed or cancelled
- Data is analyzed to find patterns in food donation and wastage

## Tech Stack

- **Python** — data cleaning, exploratory data analysis (pandas, matplotlib, seaborn)
- **MySQL** — relational database for providers, receivers, food listings, and claims
- **Streamlit** — interactive web application

## Project Structure

```
food_wastage_project/
├── app.py                      # Main Streamlit application
├── food_cleaning.py            # Phase 1: Data cleaning script
├── food_mysql_load.py          # Phase 2: MySQL database creation and load
├── food_queries.py             # Phase 2: 18 SQL queries, results saved as CSV
├── food_eda.py                 # Phase 3: 16 EDA charts generation
├── requirements.txt            # Python dependencies
├── data/
│   ├── raw/                    # Original uploaded CSVs
│   ├── cleaned/                # Cleaned CSVs (used by the app)
│   ├── query_results/          # 18 SQL query result CSVs
│   └── eda_charts/              # 16 generated chart PNGs
└── README.md
```

## Features

- **Overview Dashboard** — key metrics, filters by city, provider type, meal type, and food type
- **Query Analysis** — all 18 SQL queries with results and plain-language explanations
- **Visualizations** — 16 charts across univariate, bivariate, multivariate, and claim analysis
- **CRUD Operations** — add, view, update, and delete food listings directly from the app
- **Provider and Receiver Directory** — searchable contact directory
- **Insights and Recommendations** — key findings paired with specific recommended actions

## Running Locally

```bash
pip install -r requirements.txt
streamlit run app.py
```

The app reads from the `data/cleaned`, `data/query_results`, and `data/eda_charts` folders, so no live database connection is required to run the Streamlit app — these folders must be present alongside `app.py`.

## Data Pipeline (Run Once, In Order)

```bash
python food_cleaning.py       # Step 1: Clean raw CSVs
python food_mysql_load.py     # Step 2: Load into MySQL
python food_queries.py        # Step 3: Run 18 SQL queries, export results
python food_eda.py            # Step 4: Generate 16 EDA charts
streamlit run app.py          # Step 5: Launch the app
```

## Key Findings

- Only ~34% of all claims are actually completed; the rest are cancelled or pending
- Around 35% of food listings are never claimed at all
- Restaurants are the largest contributor of food by quantity
- NGOs are the most active and reliable receiver type

## Author

GUVI x HCL Data Analytics Training Project
