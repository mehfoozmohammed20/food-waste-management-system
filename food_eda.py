import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors
import seaborn as sns
import os
import warnings
warnings.filterwarnings("ignore")

CLEANED_DIR = "data/cleaned"
OUTPUT_DIR  = "data/eda_charts"
os.makedirs(OUTPUT_DIR, exist_ok=True)

providers = pd.read_csv(f"{CLEANED_DIR}/providers_cleaned.csv")
receivers = pd.read_csv(f"{CLEANED_DIR}/receivers_cleaned.csv")
food      = pd.read_csv(f"{CLEANED_DIR}/food_listings_cleaned.csv")
claims    = pd.read_csv(f"{CLEANED_DIR}/claims_cleaned.csv")
claims['Timestamp'] = pd.to_datetime(claims['Timestamp'], errors='coerce')
claims['Date']      = claims['Timestamp'].dt.date

BG     = "#0a1018"
COLORS = ["#2dd4bf","#fb923c","#a78bfa","#facc15","#34d399","#f87171"]
sns.set_style("dark")

def shades_of(hex_color, n, light_to_dark=True):
    """Generate n shades of a single color, from light to dark (or reverse)."""
    base_rgb = mcolors.to_rgb(hex_color)
    shades = []
    for i in range(n):
        # interpolate between a light version and the base/dark version
        factor = i / max(n-1, 1)
        if light_to_dark:
            # lighter at start, base color at end
            light = tuple(min(1, c + (1-c)*0.65) for c in base_rgb)
            r = tuple(light[j] + (base_rgb[j]-light[j])*factor for j in range(3))
        else:
            light = tuple(min(1, c + (1-c)*0.65) for c in base_rgb)
            r = tuple(base_rgb[j] + (light[j]-base_rgb[j])*factor for j in range(3))
        shades.append(r)
    return shades

def style_ax(ax):
    ax.set_facecolor(BG)
    ax.tick_params(colors='#ffffff', labelsize=10)
    ax.xaxis.label.set_color('#ffffff')
    ax.yaxis.label.set_color('#ffffff')
    for spine in ax.spines.values():
        spine.set_color('#22344a')
    ax.grid(axis='y', color='#22344a', linewidth=0.6, alpha=0.7)

def save(fig, name):
    fig.patch.set_facecolor(BG)
    fig.savefig(f"{OUTPUT_DIR}/{name}.png", dpi=160, bbox_inches='tight', facecolor=BG)
    plt.close(fig)
    print(f"  OK {name}.png")

print("Generating EDA charts with shaded single-color bars...")

# U1 - multi category, keep multi color
fig, ax = plt.subplots(figsize=(7,4.3)); style_ax(ax)
vc = providers['Type'].value_counts()
bars = ax.bar(vc.index, vc.values, color=COLORS[:len(vc)], edgecolor=BG, linewidth=1.5, width=0.6)
for b in bars: ax.text(b.get_x()+b.get_width()/2, b.get_height()+2, str(int(b.get_height())), ha='center', color='white', fontsize=10, fontweight='bold')
ax.set_ylabel("Count")
plt.tight_layout()
save(fig, "U1_provider_type_distribution")

# U2 - pie (keep multi color, pies are fine)
fig, ax = plt.subplots(figsize=(4.2,2.8)); ax.set_facecolor(BG)
vc = receivers['Type'].value_counts()
w,t,a = ax.pie(vc.values, labels=vc.index, autopct='%1.1f%%', colors=COLORS[:len(vc)], startangle=140, wedgeprops=dict(edgecolor=BG, linewidth=2), textprops={'fontsize':8,'color':'white'})
for x in a: x.set_color('white'); x.set_fontweight('bold')
plt.tight_layout()
save(fig, "U2_receiver_type_distribution")

# U3 - multi category keep
fig, ax = plt.subplots(figsize=(7,4.3)); style_ax(ax)
vc = food['Food_Type'].value_counts()
bars = ax.barh(vc.index, vc.values, color=COLORS[:len(vc)], edgecolor=BG, linewidth=1.5, height=0.55)
for b in bars: ax.text(b.get_width()+2, b.get_y()+b.get_height()/2, str(int(b.get_width())), va='center', color='white', fontsize=10, fontweight='bold')
ax.set_xlabel("Count")
plt.tight_layout()
save(fig, "U3_food_type_distribution")

# U4 - multi category keep
fig, ax = plt.subplots(figsize=(7,4.3)); style_ax(ax)
vc = food['Meal_Type'].value_counts()
bars = ax.bar(vc.index, vc.values, color=COLORS[:len(vc)], edgecolor=BG, linewidth=1.5, width=0.6)
for b in bars: ax.text(b.get_x()+b.get_width()/2, b.get_height()+1, str(int(b.get_height())), ha='center', color='white', fontsize=10, fontweight='bold')
ax.set_ylabel("Count")
plt.tight_layout()
save(fig, "U4_meal_type_distribution")

# B1 - SINGLE COLOR -> use shades (teal)
fig, ax = plt.subplots(figsize=(8.5,4.5)); style_ax(ax)
city_food = food.groupby('Location')['Food_ID'].count().sort_values(ascending=False).head(10)
shades = shades_of("#2dd4bf", len(city_food), light_to_dark=False)
bars = ax.bar(city_food.index, city_food.values, color=shades, edgecolor=BG, linewidth=1.5, width=0.6)
for b in bars: ax.text(b.get_x()+b.get_width()/2, b.get_height()+0.1, str(int(b.get_height())), ha='center', color='white', fontsize=9, fontweight='bold')
ax.set_ylabel("Listings")
plt.xticks(rotation=30, ha='right')
plt.tight_layout()
save(fig, "B1_city_vs_food_listings")

# B2 - multi category keep
fig, ax = plt.subplots(figsize=(7,4.3)); style_ax(ax)
pt_qty = food.groupby('Provider_Type')['Quantity'].sum().sort_values(ascending=False)
bars = ax.bar(pt_qty.index, pt_qty.values, color=COLORS[:len(pt_qty)], edgecolor=BG, linewidth=1.5, width=0.6)
for b in bars: ax.text(b.get_x()+b.get_width()/2, b.get_height()+10, f"{int(b.get_height()):,}", ha='center', color='white', fontsize=10, fontweight='bold')
ax.set_ylabel("Total Quantity")
plt.tight_layout()
save(fig, "B2_provider_type_vs_quantity")

# B3 - multi category keep
fig, ax = plt.subplots(figsize=(7,4.3)); style_ax(ax)
ft_qty = food.groupby('Food_Type')['Quantity'].sum().sort_values(ascending=False)
bars = ax.bar(ft_qty.index, ft_qty.values, color=COLORS[:len(ft_qty)], edgecolor=BG, linewidth=1.5, width=0.6)
for b in bars: ax.text(b.get_x()+b.get_width()/2, b.get_height()+10, f"{int(b.get_height()):,}", ha='center', color='white', fontsize=10, fontweight='bold')
ax.set_ylabel("Total Quantity")
plt.tight_layout()
save(fig, "B3_food_type_vs_quantity")

# B4 - multi category keep
fig, ax = plt.subplots(figsize=(7,4.3)); style_ax(ax)
mt_qty = food.groupby('Meal_Type')['Quantity'].sum().sort_values(ascending=False)
bars = ax.bar(mt_qty.index, mt_qty.values, color=COLORS[:len(mt_qty)], edgecolor=BG, linewidth=1.5, width=0.6)
for b in bars: ax.text(b.get_x()+b.get_width()/2, b.get_height()+10, f"{int(b.get_height()):,}", ha='center', color='white', fontsize=10, fontweight='bold')
ax.set_ylabel("Total Quantity")
plt.tight_layout()
save(fig, "B4_meal_type_vs_quantity")

# M1 - multi category (provider type legend) keep
fig, ax = plt.subplots(figsize=(12,6)); style_ax(ax)
top_cities = food.groupby('Location')['Quantity'].sum().nlargest(8).index
city_pt = food[food['Location'].isin(top_cities)].groupby(['Location','Provider_Type'])['Quantity'].sum().unstack(fill_value=0)
city_pt.plot(kind='bar', ax=ax, color=COLORS[:4], edgecolor=BG, linewidth=1, width=0.78)
ax.set_ylabel("Total Quantity", fontsize=11)
leg = ax.legend(title="Provider Type", bbox_to_anchor=(1.01,1), loc='upper left', facecolor=BG, edgecolor='#22344a', fontsize=9, labelcolor='white')
leg.get_title().set_color('white')
plt.xticks(rotation=30, ha='right', fontsize=10)
plt.tight_layout()
save(fig, "M1_city_provider_type_quantity")

# M2 - multi category keep
fig, ax = plt.subplots(figsize=(10,5.5)); style_ax(ax)
ft_mt = food.groupby(['Food_Type','Meal_Type'])['Quantity'].sum().unstack(fill_value=0)
ft_mt.plot(kind='bar', ax=ax, color=COLORS[:4], edgecolor=BG, linewidth=1, width=0.75)
ax.set_ylabel("Total Quantity", fontsize=11)
leg = ax.legend(title="Meal Type", bbox_to_anchor=(1.01,1), loc='upper left', facecolor=BG, edgecolor='#22344a', fontsize=9, labelcolor='white')
leg.get_title().set_color('white')
plt.xticks(rotation=0, fontsize=10)
plt.tight_layout()
save(fig, "M2_food_type_meal_type_quantity")

# M3 - multi category (status legend) keep
fig, ax = plt.subplots(figsize=(10,5.5)); style_ax(ax)
merged = claims.merge(food[['Food_ID','Provider_Type','Quantity']], on='Food_ID')
pt_claims = merged.groupby(['Provider_Type','Status'])['Claim_ID'].count().unstack(fill_value=0)
pt_claims.plot(kind='bar', ax=ax, color=COLORS[:3], edgecolor=BG, linewidth=1, width=0.75)
ax.set_ylabel("Number of Claims", fontsize=11)
leg = ax.legend(title="Claim Status", bbox_to_anchor=(1.01,1), loc='upper left', facecolor=BG, edgecolor='#22344a', fontsize=9, labelcolor='white')
leg.get_title().set_color('white')
plt.xticks(rotation=15, ha='right', fontsize=10)
plt.tight_layout()
save(fig, "M3_provider_claims_quantity")

# M4 - multi category keep
fig, ax = plt.subplots(figsize=(10,5.5)); style_ax(ax)
merged_r = claims.merge(receivers[['Receiver_ID','Type']], on='Receiver_ID')
rt_claims = merged_r.groupby(['Type','Status'])['Claim_ID'].count().unstack(fill_value=0)
rt_claims.plot(kind='bar', ax=ax, color=COLORS[:3], edgecolor=BG, linewidth=1, width=0.75)
ax.set_ylabel("Number of Claims", fontsize=11)
leg = ax.legend(title="Claim Status", bbox_to_anchor=(1.01,1), loc='upper left', facecolor=BG, edgecolor='#22344a', fontsize=9, labelcolor='white')
leg.get_title().set_color('white')
plt.xticks(rotation=15, ha='right', fontsize=10)
plt.tight_layout()
save(fig, "M4_receiver_claims_quantity")

# C1 - pie keep
fig, ax = plt.subplots(figsize=(4.2,2.8)); ax.set_facecolor(BG)
cs = claims['Status'].value_counts()
w,t,a = ax.pie(cs.values, labels=cs.index, autopct='%1.1f%%', colors=["#2dd4bf","#fb923c","#a78bfa"], startangle=140, wedgeprops=dict(edgecolor=BG, linewidth=2), textprops={'fontsize':8,'color':'white'})
for x in a: x.set_color('white'); x.set_fontweight('bold')
plt.tight_layout()
save(fig, "C1_claim_status_distribution")

# C2 - SINGLE COLOR -> shades (orange)
fig, ax = plt.subplots(figsize=(8.5,4.5)); style_ax(ax)
top_recv = claims.merge(receivers[['Receiver_ID','Name']], on='Receiver_ID')
top_recv = top_recv.groupby('Name')['Claim_ID'].count().sort_values(ascending=False).head(10)
shades = shades_of("#fb923c", len(top_recv), light_to_dark=False)[::-1]
bars = ax.barh(top_recv.index[::-1], top_recv.values[::-1], color=shades[::-1], edgecolor=BG, height=0.6)
for b in bars: ax.text(b.get_width()+0.05, b.get_y()+b.get_height()/2, str(int(b.get_width())), va='center', color='white', fontsize=9, fontweight='bold')
ax.set_xlabel("Total Claims")
plt.tight_layout()
save(fig, "C2_top_receivers_by_claims")

# C3 - SINGLE COLOR -> shades (purple)
fig, ax = plt.subplots(figsize=(8.5,4.5)); style_ax(ax)
top_prov = claims.merge(food[['Food_ID','Provider_ID']], on='Food_ID')
top_prov = top_prov.merge(providers[['Provider_ID','Name']], on='Provider_ID')
top_prov = top_prov.groupby('Name')['Claim_ID'].count().sort_values(ascending=False).head(10)
shades = shades_of("#a78bfa", len(top_prov), light_to_dark=False)[::-1]
bars = ax.barh(top_prov.index[::-1], top_prov.values[::-1], color=shades[::-1], edgecolor=BG, height=0.6)
for b in bars: ax.text(b.get_width()+0.05, b.get_y()+b.get_height()/2, str(int(b.get_width())), va='center', color='white', fontsize=9, fontweight='bold')
ax.set_xlabel("Total Claims")
plt.tight_layout()
save(fig, "C3_top_providers_by_claims")

# C4 - line chart, keep as is
fig, ax = plt.subplots(figsize=(9.5,4.5)); style_ax(ax)
daily = claims.groupby('Date')['Claim_ID'].count().reset_index()
ax.plot(daily['Date'], daily['Claim_ID'], color=COLORS[0], linewidth=2.5, marker='o', markersize=5)
ax.fill_between(daily['Date'], daily['Claim_ID'], alpha=0.15, color=COLORS[0])
ax.set_ylabel("Total Claims")
plt.xticks(rotation=30, ha='right')
plt.tight_layout()
save(fig, "C4_daily_claims_trend")

print("All 16 charts regenerated with shaded bars + white text.")

# ── ADDITIONAL DEMAND & WASTAGE CHARTS (closes business-question gaps) ──────
print("\nGenerating 3 additional demand and wastage charts...")

# D1 - Top 10 cities by claim demand
recv_claims = claims.merge(receivers[['Receiver_ID','City']], on='Receiver_ID')
city_demand = recv_claims['City'].value_counts().head(10)
fig, ax = plt.subplots(figsize=(8.5,4.5)); style_ax(ax)
shades = shades_of("#fb923c", len(city_demand), light_to_dark=False)
bars = ax.bar(city_demand.index, city_demand.values, color=shades, edgecolor=BG, linewidth=1.5, width=0.6)
for b in bars: ax.text(b.get_x()+b.get_width()/2, b.get_height()+0.05, str(int(b.get_height())), ha='center', color='white', fontsize=9, fontweight='bold')
ax.set_ylabel("Total Claims")
plt.xticks(rotation=30, ha='right')
plt.tight_layout()
save(fig, "D1_top_cities_by_claim_demand")

# D2 - Top 10 receivers by name (claims)
recv_claims2 = claims.merge(receivers[['Receiver_ID','Name']], on='Receiver_ID')
top_recv_names = recv_claims2.groupby('Name')['Claim_ID'].count().sort_values(ascending=False).head(10)
fig, ax = plt.subplots(figsize=(8.5,4.5)); style_ax(ax)
shades = shades_of("#a78bfa", len(top_recv_names), light_to_dark=False)[::-1]
bars = ax.barh(top_recv_names.index[::-1], top_recv_names.values[::-1], color=shades[::-1], edgecolor=BG, height=0.6)
for b in bars: ax.text(b.get_width()+0.05, b.get_y()+b.get_height()/2, str(int(b.get_width())), va='center', color='white', fontsize=9, fontweight='bold')
ax.set_xlabel("Total Claims")
plt.tight_layout()
save(fig, "D2_top_receivers_by_name")

# D3 - Meal type wastage rate (unclaimed %) - answers "which meal wasted most"
food_claimed = food.copy()
food_claimed['Is_Claimed'] = food_claimed['Food_ID'].isin(claims['Food_ID'])
meal_waste = food_claimed.groupby('Meal_Type').agg(
    Total=('Food_ID','count'),
    Unclaimed=('Is_Claimed', lambda x: (~x).sum())
)
meal_waste['Waste_Pct'] = round(meal_waste['Unclaimed']/meal_waste['Total']*100,1)
meal_waste = meal_waste.sort_values('Waste_Pct', ascending=False)

fig, ax = plt.subplots(figsize=(7,4.3)); style_ax(ax)
bars = ax.bar(meal_waste.index, meal_waste['Waste_Pct'], color=COLORS[:len(meal_waste)], edgecolor=BG, linewidth=1.5, width=0.6)
for b in bars: ax.text(b.get_x()+b.get_width()/2, b.get_height()+0.5, f"{b.get_height()}%", ha='center', color='white', fontsize=10, fontweight='bold')
ax.set_ylabel("Unclaimed Rate (%)")
plt.tight_layout()
save(fig, "D3_meal_type_wastage_rate")

print("All 3 additional charts generated.")
print("\nTotal charts: 19 (16 original + 3 new)")