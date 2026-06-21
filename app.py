import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import os
import warnings
warnings.filterwarnings("ignore")

st.set_page_config(
    page_title="Local Food Wastage Management System",
    page_icon="🥗",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');

    html, body, .stApp {
        background: radial-gradient(circle at 15% 10%, #14233a 0%, #0a1018 45%),
                    radial-gradient(circle at 85% 90%, #1a2a42 0%, #0a1018 55%),
                    #0a1018 !important;
        color: #e8eaf0 !important;
        font-family: 'Inter', sans-serif !important;
    }

    section[data-testid="stSidebar"] {
        background: rgba(13, 20, 32, 0.55) !important;
        backdrop-filter: blur(18px) saturate(140%);
        -webkit-backdrop-filter: blur(18px) saturate(140%);
        border-right: 1px solid rgba(255,255,255,0.06) !important;
    }

    .main-title { font-size: 2.15rem; font-weight: 800; color: #ffffff; text-align:center; letter-spacing:-0.5px; margin-bottom:0.2rem; }
    .main-title span { color: #2dd4bf; }
    .sub-title { font-size: 0.9rem; color: #8b99ad; text-align:center; margin-bottom: 0.4rem; }

    /* Glass section header - floating glass strip */
    .sec-header {
        font-size: 1.05rem; font-weight: 700; color: #ffffff;
        margin: 1.7rem 0 1rem 0;
        padding: 0.7rem 1.1rem;
        background: rgba(255,255,255,0.035);
        backdrop-filter: blur(14px);
        -webkit-backdrop-filter: blur(14px);
        border: 1px solid rgba(255,255,255,0.08);
        border-left: 3px solid rgba(45,212,191,0.7);
        border-radius: 12px;
        box-shadow: 0 4px 20px rgba(0,0,0,0.25);
    }

    /* Glassmorphic KPI cards */
    .kpi-grid { display:flex; gap:14px; flex-wrap:wrap; margin-bottom: 0.5rem; }
    .kpi-card {
        background: rgba(255,255,255,0.045);
        backdrop-filter: blur(16px) saturate(160%);
        -webkit-backdrop-filter: blur(16px) saturate(160%);
        border: 1px solid rgba(255,255,255,0.09);
        border-radius: 18px;
        padding: 1.15rem 1.3rem;
        flex:1; min-width:140px;
        box-shadow: 0 8px 24px rgba(0,0,0,0.35), inset 0 1px 0 rgba(255,255,255,0.08);
        position: relative;
        transition: all 0.25s ease;
    }
    .kpi-card::before {
        content: ""; position:absolute; inset:0; border-radius:18px; padding:1px;
        background: linear-gradient(135deg, rgba(45,212,191,0.4), rgba(255,255,255,0.02) 40%);
        -webkit-mask: linear-gradient(#fff 0 0) content-box, linear-gradient(#fff 0 0);
        -webkit-mask-composite: xor; mask-composite: exclude;
        pointer-events: none;
    }
    .kpi-value { font-size: 1.65rem; font-weight: 800; color:#fff; line-height:1.1; }
    .kpi-label { font-size: 0.73rem; color:#8b99ad; margin-top:0.3rem; text-transform:uppercase; letter-spacing:0.6px; }

    /* Glass insight strip */
    .insight-box {
        background: rgba(45,212,191,0.045);
        backdrop-filter: blur(12px);
        -webkit-backdrop-filter: blur(12px);
        border: 1px solid rgba(45,212,191,0.18);
        border-radius: 14px; padding: 1rem 1.2rem; color:#a8b6c8;
        font-size: 0.87rem; margin: 0.5rem 0 1.9rem 0; line-height:1.7;
        box-shadow: 0 4px 18px rgba(0,0,0,0.2);
    }
    .insight-box b { color:#2dd4bf; }

    /* Combined insight + recommendation glass card */
    .biz-insight {
        background: rgba(255,255,255,0.04);
        backdrop-filter: blur(18px) saturate(150%);
        -webkit-backdrop-filter: blur(18px) saturate(150%);
        border: 1px solid rgba(255,255,255,0.09);
        border-radius:16px; padding:1.2rem 1.4rem; margin-bottom:1rem;
        color:#a8b6c8; font-size:0.9rem; line-height:1.75;
        box-shadow: 0 8px 28px rgba(0,0,0,0.3), inset 0 1px 0 rgba(255,255,255,0.06);
        position: relative; overflow: hidden;
    }
    .biz-insight::after {
        content: ""; position:absolute; top:-40%; right:-20%; width:180px; height:180px;
        background: radial-gradient(circle, rgba(45,212,191,0.10), transparent 70%);
        pointer-events: none;
    }
    .biz-insight b { color:#ffffff; font-size:0.96rem; }

    .rec-card {
        background: rgba(251,146,60,0.04);
        backdrop-filter: blur(16px);
        -webkit-backdrop-filter: blur(16px);
        border: 1px solid rgba(251,146,60,0.18);
        border-radius:16px; padding:1.1rem 1.3rem; margin-bottom:0.85rem;
        color:#a8b6c8; font-size:0.9rem; line-height:1.75;
        box-shadow: 0 6px 22px rgba(0,0,0,0.25);
    }
    .rec-card b { color:#fb923c; font-size:0.96rem; }

    .prog-wrap { background:rgba(255,255,255,0.08); border-radius:20px; height:8px; width:100%; margin:8px 0 4px 0; overflow:hidden; backdrop-filter: blur(4px); }
    .prog-fill { height:8px; border-radius:20px; box-shadow: 0 0 8px rgba(45,212,191,0.5); }

    .stat-pill-label { color:#8b99ad; font-size:0.74rem; text-transform:uppercase; letter-spacing:0.6px; }
    .stat-pill-value { font-size:1.3rem; font-weight:800; }

    .fancy-divider { border:none; border-top:1px solid rgba(255,255,255,0.08); margin:1.5rem 0; }

    div[data-testid="stRadio"] > label { color:#8b99ad !important; font-size:0.78rem !important; text-transform:uppercase; letter-spacing:1.2px; }
    div[data-testid="stRadio"] div[role="radiogroup"] label { color:#c4d0e0 !important; font-size:0.95rem !important; }

    /* Glass expanders */
    div[data-testid="stExpander"] {
        background: rgba(255,255,255,0.035) !important;
        backdrop-filter: blur(14px) !important;
        -webkit-backdrop-filter: blur(14px) !important;
        border:1px solid rgba(255,255,255,0.08) !important; border-radius:14px !important; margin-bottom:10px !important;
        box-shadow: 0 4px 16px rgba(0,0,0,0.2);
    }
    div[data-testid="stExpander"] summary { color:#c4d0e0 !important; font-weight:600 !important; font-size:0.88rem !important; }

    div[data-testid="stMultiSelect"] label, div[data-testid="stSelectbox"] label,
    div[data-testid="stTextInput"] label, div[data-testid="stNumberInput"] label,
    div[data-testid="stDateInput"] label {
        color:#8b99ad !important; font-size:0.76rem !important; text-transform:uppercase; letter-spacing:0.6px;
    }

    /* Glass input boxes */
    div[data-testid="stTextInput"] input, div[data-testid="stNumberInput"] input,
    div[data-baseweb="select"] > div {
        background: rgba(255,255,255,0.04) !important;
        border: 1px solid rgba(255,255,255,0.1) !important;
        border-radius: 10px !important;
        backdrop-filter: blur(10px);
    }

    h1,h2,h3,h4,h5 { color:#ffffff !important; }
    p, li { color:#a8b6c8 !important; }

    .stTabs [data-baseweb="tab-list"] {
        background: rgba(255,255,255,0.035) !important;
        backdrop-filter: blur(12px);
        border-radius:12px; border:1px solid rgba(255,255,255,0.08);
    }
    .stTabs [data-baseweb="tab"] { color:#8b99ad !important; font-weight:600; }
    .stTabs [aria-selected="true"] { color:#2dd4bf !important; border-bottom:2px solid #2dd4bf !important; }

    /* Glass dataframe wrapper */
    div[data-testid="stDataFrame"] {
        background: rgba(255,255,255,0.02) !important;
        border-radius: 12px;
        border: 1px solid rgba(255,255,255,0.06);
    }
</style>
""", unsafe_allow_html=True)

# ── Load Data ────────────────────────────────────────────────────────────────
@st.cache_data
def load_data():
    base = "data/cleaned"
    providers = pd.read_csv(f"{base}/providers_cleaned.csv")
    receivers = pd.read_csv(f"{base}/receivers_cleaned.csv")
    food      = pd.read_csv(f"{base}/food_listings_cleaned.csv")
    claims    = pd.read_csv(f"{base}/claims_cleaned.csv")
    claims['Timestamp'] = pd.to_datetime(claims['Timestamp'], errors='coerce')
    claims['Date']      = claims['Timestamp'].dt.date
    food['Expiry_Date'] = pd.to_datetime(food['Expiry_Date'], errors='coerce')
    return providers, receivers, food, claims

@st.cache_data
def load_query_results():
    qdir = "data/query_results"
    results = {}
    if os.path.exists(qdir):
        for f in sorted(os.listdir(qdir)):
            if f.endswith(".csv"):
                results[f.replace(".csv","")] = pd.read_csv(f"{qdir}/{f}")
    return results

providers, receivers, food, claims = load_data()
query_results = load_query_results()
os.makedirs("data", exist_ok=True)
BG = "#0a1018"
COLORS = ["#2dd4bf","#fb923c","#a78bfa","#facc15","#34d399","#f87171"]

def show_chart_small(path, width_pct=55):
    if os.path.exists(path):
        c1, c2, c3 = st.columns([(100-width_pct)/2, width_pct, (100-width_pct)/2])
        with c2:
            st.image(path, use_container_width=True)
    else:
        st.warning(f"Chart not found: {path}")

def show_fig(fig, width_pct=55):
    """Render a matplotlib figure directly with no disk I/O - avoids stale file issues."""
    c1, c2, c3 = st.columns([(100-width_pct)/2, width_pct, (100-width_pct)/2])
    with c2:
        st.pyplot(fig, use_container_width=True)
    plt.close(fig)

def dark_fig(w=6.5, h=3.3):
    fig, ax = plt.subplots(figsize=(w, h), facecolor=BG)
    ax.set_facecolor(BG)
    ax.tick_params(colors='#6e7d92', labelsize=8)
    ax.xaxis.label.set_color('#6e7d92')
    ax.yaxis.label.set_color('#6e7d92')
    for spine in ax.spines.values():
        spine.set_color('#1a2638')
    ax.grid(axis='y', color='#1a2638', linewidth=0.5, alpha=0.7)
    return fig, ax

# ── Sidebar ──────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("### Food Wastage MS")
    st.markdown('<hr class="fancy-divider">', unsafe_allow_html=True)
    st.markdown("**NAVIGATE**")
    page = st.radio("", [
        "Overview",
        "Query Analysis",
        "Visualizations",
        "CRUD Operations",
        "Provider and Receiver Directory",
        "Insights & Recommendations"
    ])
    st.markdown('<hr class="fancy-divider">', unsafe_allow_html=True)
    st.markdown('<p style="color:#2e3d52;font-size:0.72rem;">Local Food Wastage Management System<br>GUVI x HCL Training Project</p>', unsafe_allow_html=True)

# ════════════════════════════════════════════════════════════════════════════
# OVERVIEW
# ════════════════════════════════════════════════════════════════════════════
if page == "Overview":
    st.markdown('<div class="main-title">Local Food Wastage <span>Management System</span></div>', unsafe_allow_html=True)
    st.markdown('<div class="sub-title">Connecting Food Providers with Receivers — Reducing Waste, Fighting Hunger</div>', unsafe_allow_html=True)
    st.markdown('<hr class="fancy-divider">', unsafe_allow_html=True)

    st.markdown('<div class="sec-header">Key Metrics — All Data</div>', unsafe_allow_html=True)

    total_listings_all = len(food)
    total_quantity_all  = food['Quantity'].sum()
    total_claims_all    = len(claims)
    completed_all       = len(claims[claims['Status']=='Completed'])
    success_rate_all    = round(completed_all/total_claims_all*100,1) if total_claims_all>0 else 0
    unclaimed_all        = len(food[~food['Food_ID'].isin(claims['Food_ID'])])

    st.markdown(f"""
    <div class="kpi-grid">
        <div class="kpi-card"><div class="kpi-value">{total_listings_all:,}</div><div class="kpi-label">Food Listings</div></div>
        <div class="kpi-card"><div class="kpi-value">{total_quantity_all:,}</div><div class="kpi-label">Total Quantity</div></div>
        <div class="kpi-card"><div class="kpi-value">{total_claims_all:,}</div><div class="kpi-label">Total Claims</div></div>
        <div class="kpi-card"><div class="kpi-value">{completed_all:,}</div><div class="kpi-label">Completed</div></div>
        <div class="kpi-card">
            <div class="kpi-value">{success_rate_all}%</div><div class="kpi-label">Success Rate</div>
            <div class="prog-wrap"><div class="prog-fill" style="width:{success_rate_all}%;background:linear-gradient(90deg,#2dd4bf,#0d9488);"></div></div>
        </div>
        <div class="kpi-card"><div class="kpi-value">{unclaimed_all:,}</div><div class="kpi-label">Unclaimed Items</div></div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown('<hr class="fancy-divider">', unsafe_allow_html=True)

    st.markdown('<div class="sec-header">Dashboard Filters</div>', unsafe_allow_html=True)
    fc1, fc2, fc3, fc4 = st.columns(4)
    with fc1: sel_cities    = st.multiselect("City", sorted(food['Location'].dropna().unique()))
    with fc2: sel_providers = st.multiselect("Provider Type", sorted(food['Provider_Type'].dropna().unique()))
    with fc3: sel_meal      = st.multiselect("Meal Type", sorted(food['Meal_Type'].dropna().unique()))
    with fc4: sel_food_type = st.multiselect("Food Type", sorted(food['Food_Type'].dropna().unique()))

    filtered_food = food.copy()
    if sel_cities:      filtered_food = filtered_food[filtered_food['Location'].isin(sel_cities)]
    if sel_providers:   filtered_food = filtered_food[filtered_food['Provider_Type'].isin(sel_providers)]
    if sel_meal:        filtered_food = filtered_food[filtered_food['Meal_Type'].isin(sel_meal)]
    if sel_food_type:   filtered_food = filtered_food[filtered_food['Food_Type'].isin(sel_food_type)]
    filtered_claims = claims[claims['Food_ID'].isin(filtered_food['Food_ID'])]

    st.markdown('<hr class="fancy-divider">', unsafe_allow_html=True)

    st.markdown('<div class="sec-header">Food Quantity by Provider Type</div>', unsafe_allow_html=True)
    pt = filtered_food.groupby('Provider_Type')['Quantity'].sum().sort_values(ascending=False)
    if len(pt) > 0:
        fig, ax = dark_fig(6.5, 3.3)
        bars = ax.bar(pt.index, pt.values, color=COLORS[:len(pt)], edgecolor=BG, linewidth=1.2, width=0.6, zorder=3)
        for bar in bars:
            ax.text(bar.get_x()+bar.get_width()/2, bar.get_height()+15, f"{int(bar.get_height()):,}", ha='center', fontsize=8, color='white', fontweight='700')
        ax.set_ylabel("Total Quantity", fontsize=9)
        plt.xticks(fontsize=8)
        plt.tight_layout()
        show_fig(fig, 50)
        top_pt = pt.idxmax()
        pct_share = round(pt.max()/pt.sum()*100,1)
        st.markdown(f'<div class="insight-box">{top_pt} contributes the highest food quantity, making up <b>{pct_share}%</b> of all donated food in the current filter. This shows {top_pt}s are the most valuable type of partner in this system right now. Strengthening relationships with more {top_pt}s — for example through regular pickup schedules or recognition programs — would create the biggest improvement in total food collected and redistributed.</div>', unsafe_allow_html=True)
    else:
        st.info("No data matches the current filter selection. Try removing one or more filters above.")

    st.markdown('<div class="sec-header">Food Type Distribution</div>', unsafe_allow_html=True)
    ft = filtered_food['Food_Type'].value_counts()
    if len(ft) > 0:
        fig, ax = plt.subplots(figsize=(4.2,2.8), facecolor=BG)
        w,t,a = ax.pie(ft.values, labels=ft.index, autopct='%1.1f%%', colors=COLORS[:len(ft)], startangle=140, wedgeprops=dict(edgecolor=BG, linewidth=2), textprops={'fontsize':8})
        for x in t: x.set_color('white')
        for x in a: x.set_color('white'); x.set_fontweight('bold')
        plt.tight_layout()
        show_fig(fig, 35)
        top_ft = ft.idxmax()
        st.markdown(f'<div class="insight-box">{top_ft} is the most commonly listed food type, but all three categories (Vegetarian, Non-Vegetarian, Vegan) are fairly close in proportion. This balance is a good sign — it means the system is not overly dependent on one diet type, and receivers with different dietary needs or restrictions all have a reasonable chance of finding suitable food.</div>', unsafe_allow_html=True)

    st.markdown('<div class="sec-header">Meal Type vs Total Quantity</div>', unsafe_allow_html=True)
    mt = filtered_food.groupby('Meal_Type')['Quantity'].sum().sort_values(ascending=True)
    if len(mt) > 0:
        fig, ax = dark_fig(6.5, 3.3)
        bars = ax.barh(mt.index, mt.values, color=COLORS[:len(mt)], edgecolor=BG, linewidth=1.2, height=0.55, zorder=3)
        for bar in bars:
            ax.text(bar.get_width()+15, bar.get_y()+bar.get_height()/2, f"{int(bar.get_width()):,}", va='center', fontsize=8, color='white', fontweight='700')
        ax.set_xlabel("Total Quantity", fontsize=9)
        plt.tight_layout()
        show_fig(fig, 50)
        top_mt = mt.idxmax()
        st.markdown(f'<div class="insight-box"><b>{top_mt}</b> has the highest total quantity of food listed among all meal types. This typically happens because providers tend to have more surplus during this meal period. If claim rates for {top_mt} are lower than other meal types, this becomes the single biggest source of preventable food waste — so outreach campaigns timed around {top_mt} collection windows could meaningfully reduce wastage.</div>', unsafe_allow_html=True)

    st.markdown('<div class="sec-header">Claim Status Distribution</div>', unsafe_allow_html=True)
    cs = filtered_claims['Status'].value_counts()
    if len(cs) > 0:
        fig, ax = plt.subplots(figsize=(4.2,2.8), facecolor=BG)
        w,t,a = ax.pie(cs.values, labels=cs.index, autopct='%1.1f%%', colors=["#2dd4bf","#fb923c","#a78bfa"], startangle=140, wedgeprops=dict(edgecolor=BG, linewidth=2), textprops={'fontsize':8})
        for x in t: x.set_color('white')
        for x in a: x.set_color('white'); x.set_fontweight('bold')
        plt.tight_layout()
        show_fig(fig, 35)

        comp_pct = round(cs.get('Completed',0)/cs.sum()*100,1)
        canc_pct = round(cs.get('Cancelled',0)/cs.sum()*100,1)
        pend_pct = round(cs.get('Pending',0)/cs.sum()*100,1)
        st.markdown(f'<div class="insight-box">Out of all claims in the current filter, only <b>{comp_pct}%</b> are actually completed. <b>{canc_pct}%</b> get cancelled and <b>{pend_pct}%</b> are still pending. This means a majority of claimed food may never actually reach the receiver — the food gets reserved but then falls through due to logistics, timing, or communication issues. This is the single biggest leakage point in the entire food distribution pipeline and should be the top priority to fix.</div>', unsafe_allow_html=True)

        cc1, cc2, cc3 = st.columns(3)
        with cc1:
            st.markdown(f'<div class="stat-pill-label">Completed</div><div class="stat-pill-value" style="color:#2dd4bf;">{comp_pct}%</div><div class="prog-wrap"><div class="prog-fill" style="width:{comp_pct}%;background:linear-gradient(90deg,#2dd4bf,#0d9488);"></div></div>', unsafe_allow_html=True)
        with cc2:
            st.markdown(f'<div class="stat-pill-label">Cancelled</div><div class="stat-pill-value" style="color:#fb923c;">{canc_pct}%</div><div class="prog-wrap"><div class="prog-fill" style="width:{canc_pct}%;background:linear-gradient(90deg,#fb923c,#c2410c);"></div></div>', unsafe_allow_html=True)
        with cc3:
            st.markdown(f'<div class="stat-pill-label">Pending</div><div class="stat-pill-value" style="color:#a78bfa;">{pend_pct}%</div><div class="prog-wrap"><div class="prog-fill" style="width:{pend_pct}%;background:linear-gradient(90deg,#a78bfa,#7c3aed);"></div></div>', unsafe_allow_html=True)
    else:
        st.info("No claims match the current filter selection.")

    st.markdown('<hr class="fancy-divider">', unsafe_allow_html=True)
    st.markdown('<div class="sec-header">Filtered Food Listings</div>', unsafe_allow_html=True)
    st.dataframe(filtered_food.head(50), use_container_width=True)

# ════════════════════════════════════════════════════════════════════════════
# SQL QUERY RESULTS
# ════════════════════════════════════════════════════════════════════════════
elif page == "Query Analysis":
    st.markdown('<div class="main-title">SQL Query <span>Results</span></div>', unsafe_allow_html=True)
    st.markdown('<div class="sub-title">18 SQL queries executed on MySQL — food_wastage_db</div>', unsafe_allow_html=True)
    st.markdown('<hr class="fancy-divider">', unsafe_allow_html=True)

    QUERY_META = {
        "Q01_providers_receivers_by_city": ("1. Number of Providers and Receivers by City",
            "This shows how providers and receivers are spread out geographically. Cities with many providers but few or no receivers are at high risk of food going unclaimed simply because there's nobody nearby to collect it. These mismatched cities should be the first target for new NGO partnerships."),
        "Q02_provider_type_most_food": ("2. Which Provider Type Contributes Most Food",
            "This ranks provider categories by total contribution. Whichever type comes out on top is effectively carrying the system — losing even one or two large contributors from this group would have an outsized impact on total food availability, so retention matters more here than for any other provider type."),
        "Q03_provider_contact_by_city": ("3. Provider Contact Information by City",
            "This is a ready-to-use directory letting receivers find and directly contact providers in their own city without needing a middleman. It removes a major friction point in the donation process — speed of contact often determines whether food gets collected before it spoils."),
        "Q04_receivers_most_claimed": ("4. Receivers Who Claimed the Most Food",
            "These are the most active and reliable receivers in the system. Because they already collect food consistently, they're the safest organizations to route new or large food listings to, since the probability of an actual successful pickup is highest with them."),
        "Q05_total_food_quantity": ("5. Total Food Quantity by Provider",
            "This ranks individual providers, not just provider types, by total quantity donated. It helps identify the specific top contributors who deserve recognition and also flags which single providers the system would be most exposed to losing."),
        "Q06_city_highest_food_listings": ("6. City with Highest Number of Food Listings",
            "The city at the top of this list has the most food supply concentrated in one place. If claim numbers from that same city are low, it's a strong signal that demand-side infrastructure (more receivers, easier pickup logistics) needs to be built there urgently."),
        "Q07_most_common_food_types": ("7. Most Commonly Available Food Types",
            "This tells us whether the food supply matches the variety receivers might need. If one food type heavily dominates, receivers with different dietary requirements (for example strictly vegan recipients) may struggle to find enough suitable food even when overall quantity looks healthy."),
        "Q08_claims_per_food_item": ("8. Number of Claims per Food Item",
            "Items at the top of this list are in high demand and get claimed quickly — sometimes even multiple times. Items at the bottom may indicate food types that are unpopular or simply not visible enough to receivers, both of which increase wastage risk."),
        "Q09_provider_most_successful_claims": ("9. Provider with Most Successful Claims",
            "Unlike just counting donations, this tracks providers whose food is actually successfully collected and used — not just claimed and then cancelled. These are the providers whose food has the most real-world impact, and they should be the model others are encouraged to follow."),
        "Q10_claim_status_percentage": ("10. Claim Status Percentage",
            "This is the single most important health metric for the whole system. A high cancelled or pending percentage relative to completed claims means the matching process between providers and receivers is fundamentally broken somewhere — most likely due to timing, distance, or lack of confirmation reminders."),
        "Q11_avg_quantity_per_receiver": ("11. Average Quantity Claimed per Receiver",
            "This shows which receivers are claiming large amounts per transaction versus small ones. Receivers with high averages might be feeding many people at once (like shelters), while low averages may indicate individuals — this helps with planning food batch sizes for different receiver types."),
        "Q12_most_claimed_meal_type": ("12. Most Claimed Meal Type",
            "This reveals which meal type receivers actually want most, which can be compared against which meal type providers donate most. A mismatch between the two (for example providers donate mostly Snacks but receivers claim mostly Dinner) points directly to where supply and demand are out of sync."),
        "Q13_total_donated_qty_by_provider": ("13. Total Donated Quantity by Provider",
            "Similar to Q05 but focused purely on volume donated regardless of whether it was claimed. This is useful for recognizing generosity and effort even in cases where the food ultimately wasn't claimed — the issue there lies on the demand side, not the provider's contribution."),
        "Q14_unclaimed_food_waste": ("14. Unclaimed Food Items (Potential Waste)",
            "This is the most direct evidence of food wastage in the entire system — items that were listed but never claimed by anyone at all. Every row here represents food that went to waste. Reducing the size of this list should be treated as the core success metric for the whole platform."),
        "Q15_daily_claims_trend": ("15. Daily Claims Trend",
            "This shows how claim activity changes day by day. Spikes might align with weekends or paydays when receivers are more active, while dips could indicate days when outreach or awareness was low. Recognizing this pattern helps with planning targeted reminder campaigns on slow days."),
        "Q16_food_type_vs_meal_type_matrix": ("16. Food Type vs Meal Type Matrix",
            "This cross-tab reveals specific combinations — for example, whether Vegan food is mostly donated for Breakfast or Dinner. These patterns help receivers anticipate what kind of food they're likely to find at certain times of day, improving planning on both sides."),
        "Q17_receiver_type_claim_success": ("17. Claim Success Rate by Receiver Type",
            "This compares how reliably each receiver category actually follows through on their claims. If one receiver type (for example Individuals) has a much lower completion rate than organizations like NGOs or Shelters, the system may want to prioritize routing food toward more organized receiver types."),
        "Q18_full_claim_details": ("18. Full Claim Details",
            "This is the complete combined record joining every claim with its food, provider, and receiver information. It acts as the master audit trail for the whole system — useful for manually investigating specific cases, disputes, or unusual patterns that the summary queries above might miss."),
    }

    for key, (title, insight) in QUERY_META.items():
        with st.expander(f"**{title}**"):
            if key in query_results:
                df = query_results[key]
                st.dataframe(df, use_container_width=True)
                st.caption(f"{len(df)} rows returned")
                st.markdown(f'<div class="insight-box">{insight}</div>', unsafe_allow_html=True)
            else:
                st.warning("Result not found. Run food_queries.py first.")

# ════════════════════════════════════════════════════════════════════════════
# EDA CHARTS
# ════════════════════════════════════════════════════════════════════════════
elif page == "Visualizations":
    st.markdown('<div class="main-title">Exploratory <span>Data Analysis</span></div>', unsafe_allow_html=True)
    st.markdown('<div class="sub-title">16 charts — Univariate, Bivariate, Multivariate and Claim Analysis</div>', unsafe_allow_html=True)
    st.markdown('<hr class="fancy-divider">', unsafe_allow_html=True)

    CHART_DIR = "data/eda_charts"

    SECTIONS = {
        "Univariate Analysis": [
            ("U1_provider_type_distribution",  "Provider Type Distribution", 60,
             "All four provider categories — Restaurant, Supermarket, Grocery Store, and Catering Service — appear in roughly equal numbers. This even spread means the system isn't fragile to losing any single type of provider, since no one category is carrying a disproportionate share of total participation."),
            ("U2_receiver_type_distribution",  "Receiver Type Distribution", 38,
             "Receivers are distributed across NGOs, Shelters, Individuals, and Charities fairly evenly. This diversity is healthy because it means the platform serves multiple kinds of need at once — emergency shelters, ongoing charity work, and direct individual hunger relief — rather than over-serving just one group."),
            ("U3_food_type_distribution",      "Food Type Distribution", 60,
             "Vegetarian, Non-Vegetarian, and Vegan listings are close in number, with no single category overwhelmingly dominant. This balance matters because it means receivers with specific dietary restrictions are not systematically underserved compared to others."),
            ("U4_meal_type_distribution",      "Meal Type Distribution", 60,
             "Breakfast, Lunch, Dinner, and Snacks are all represented in similar volume. This tells us food becomes available fairly consistently throughout the day rather than being concentrated around just one meal window, which is good for receivers with flexible pickup schedules."),
        ],
        "Bivariate Analysis": [
            ("B1_city_vs_food_listings",       "Top 10 Cities by Food Listings", 65,
             "A handful of cities clearly account for the bulk of listings compared to the rest. These high-supply cities are the most urgent candidates for expanding receiver presence, because right now they likely have more food available than there are organizations to collect it."),
            ("B2_provider_type_vs_quantity",   "Provider Type vs Total Quantity", 60,
             "When looking at total quantity rather than just count of listings, Grocery Stores and Supermarkets tend to donate in bulk more than Restaurants, which donate more frequently but in smaller amounts per listing. This distinction matters for planning transport and storage capacity needed at pickup."),
            ("B3_food_type_vs_quantity",       "Food Type vs Total Quantity", 60,
             "Total quantity is fairly evenly split across food types, meaning the system isn't accidentally over-producing one category at the expense of others. This is a reassuring sign that the donation pipeline as a whole is balanced, not skewed toward a single diet type."),
            ("B4_meal_type_vs_quantity",       "Meal Type vs Total Quantity", 60,
             "Snacks and Breakfast show slightly higher total quantities than Lunch and Dinner. This could mean providers tend to have more leftover inventory from these meal categories specifically, possibly due to how they're packaged or how demand fluctuates for them commercially."),
        ],
        "Multivariate Analysis": [
            ("M1_city_provider_type_quantity", "City + Provider Type + Quantity", 90,
             "Most top-performing cities have multiple provider types active simultaneously rather than relying on just one. Cities that show only a single dominant provider type are more vulnerable — if that one provider type pulls back, the city's entire food supply could collapse rather than just shrink."),
            ("M2_food_type_meal_type_quantity","Food Type + Meal Type + Quantity", 80,
             "Specific combinations stand out — for instance Non-Vegetarian food tends to peak for Dinner while Vegan food appears more for Breakfast. Receivers can use this pattern to plan exactly when to check listings depending on what dietary type of food they need most."),
            ("M3_provider_claims_quantity",    "Provider Type + Claim Status", 80,
             "Across all provider types, the ratio of completed versus cancelled claims stays fairly consistent. This tells us the high cancellation problem is not isolated to any specific provider category — it's a system-wide logistics or communication issue that needs a platform-level fix, not a provider-specific one."),
            ("M4_receiver_claims_quantity",    "Receiver Type + Claim Status", 80,
             "Organized receiver types like NGOs and Shelters tend to complete claims more reliably than Individuals. This suggests that routing larger or time-sensitive food listings toward organizational receivers first, before opening them to individuals, could reduce the overall cancellation rate."),
        ],
        "Claim Analysis": [
            ("C1_claim_status_distribution",   "Claim Status Distribution", 38,
             "Roughly only a third of all claims end up fully completed, while the rest are split between cancelled and pending. This single chart captures the core inefficiency of the whole system — the majority of claimed food may never actually reach a person in need, even though on paper it looks 'claimed'."),
            ("C2_top_receivers_by_claims",     "Top 10 Receivers by Total Claims", 65,
             "A small core group of receivers accounts for a disproportionate share of all claims. These organizations have clearly built trust and reliable processes — onboarding similar organizations using the same model as these top receivers would likely boost overall completion rates."),
            ("C3_top_providers_by_claims",     "Top 10 Providers by Total Claims", 65,
             "These providers see the most receiver interest in their listings, meaning their food gets used effectively rather than wasted. Studying what makes their listings attractive — location, quantity per listing, timing — could help less successful providers improve their own claim rates."),
            ("C4_daily_claims_trend",          "Daily Claims Trend", 70,
             "Claim activity shows clear peaks and dips across the observed weeks rather than staying flat. This kind of weekly rhythm — likely tied to weekends or specific days when receivers are more available — can be used to time reminder notifications or promotional pushes for maximum effect."),
        ],
    }

    for section_title, charts in SECTIONS.items():
        st.markdown(f'<div class="sec-header">{section_title}</div>', unsafe_allow_html=True)
        for fname, title, w, insight in charts:
            st.markdown(f"**{title}**")
            path = f"{CHART_DIR}/{fname}.png"
            show_chart_small(path, w)
            st.markdown(f'<div class="insight-box">{insight}</div>', unsafe_allow_html=True)
        st.markdown('<hr class="fancy-divider">', unsafe_allow_html=True)

# ════════════════════════════════════════════════════════════════════════════
# CRUD OPERATIONS
# ════════════════════════════════════════════════════════════════════════════
elif page == "CRUD Operations":
    st.markdown('<div class="main-title">CRUD Operations</div>', unsafe_allow_html=True)
    st.markdown('<div class="sub-title">Add, View, Update and Delete Food Listings</div>', unsafe_allow_html=True)
    st.markdown('<hr class="fancy-divider">', unsafe_allow_html=True)

    FOOD_CSV  = "data/cleaned/food_listings_cleaned.csv"
    food_live = pd.read_csv(FOOD_CSV)

    tabs = st.tabs(["Add Listing", "View & Search", "Update Listing", "Delete Listing"])

    with tabs[0]:
        st.markdown("### Add New Food Listing")
        with st.form("add_form"):
            c1, c2 = st.columns(2)
            with c1:
                new_name     = st.text_input("Food Name")
                new_qty      = st.number_input("Quantity", min_value=1, max_value=500, value=10)
                new_expiry   = st.date_input("Expiry Date")
                new_provider = st.selectbox("Provider ID", sorted(providers['Provider_ID'].tolist()))
            with c2:
                new_ptype    = st.selectbox("Provider Type", food['Provider_Type'].unique().tolist())
                new_location = st.text_input("Location (City)")
                new_ftype    = st.selectbox("Food Type", food['Food_Type'].unique().tolist())
                new_mtype    = st.selectbox("Meal Type", food['Meal_Type'].unique().tolist())
            if st.form_submit_button("Add Listing", use_container_width=True):
                if not new_name or not new_location:
                    st.error("Food Name and Location are required.")
                else:
                    new_id = int(food_live['Food_ID'].max()) + 1
                    new_row = {'Food_ID':new_id,'Food_Name':new_name,'Quantity':new_qty,
                               'Expiry_Date':str(new_expiry),'Provider_ID':new_provider,
                               'Provider_Type':new_ptype,'Location':new_location,
                               'Food_Type':new_ftype,'Meal_Type':new_mtype}
                    food_live = pd.concat([food_live, pd.DataFrame([new_row])], ignore_index=True)
                    food_live.to_csv(FOOD_CSV, index=False)
                    st.success(f"Added! Food ID: {new_id}")
                    st.dataframe(pd.DataFrame([new_row]), use_container_width=True)

    with tabs[1]:
        st.markdown("### View & Search Food Listings")
        search = st.text_input("Search by Food Name or Location")
        df_view = food_live.copy()
        if search:
            df_view = df_view[df_view['Food_Name'].str.contains(search,case=False,na=False)|
                              df_view['Location'].str.contains(search,case=False,na=False)]
        st.dataframe(df_view, use_container_width=True)
        st.caption(f"Showing {len(df_view)} of {len(food_live)} records")

    with tabs[2]:
        st.markdown("### Update Food Listing")
        sel_id = st.selectbox("Select Food ID", sorted(food_live['Food_ID'].tolist()))
        row = food_live[food_live['Food_ID']==sel_id].iloc[0]
        with st.form("update_form"):
            c1, c2 = st.columns(2)
            with c1:
                upd_name  = st.text_input("Food Name", value=str(row['Food_Name']))
                upd_qty   = st.number_input("Quantity", min_value=1, max_value=500, value=int(row['Quantity']))
                upd_ftype = st.selectbox("Food Type", food['Food_Type'].unique().tolist(),
                    index=list(food['Food_Type'].unique()).index(row['Food_Type']) if row['Food_Type'] in food['Food_Type'].unique() else 0)
            with c2:
                upd_mtype = st.selectbox("Meal Type", food['Meal_Type'].unique().tolist(),
                    index=list(food['Meal_Type'].unique()).index(row['Meal_Type']) if row['Meal_Type'] in food['Meal_Type'].unique() else 0)
                upd_loc   = st.text_input("Location", value=str(row['Location']))
            if st.form_submit_button("Save Changes", use_container_width=True):
                food_live.loc[food_live['Food_ID']==sel_id,'Food_Name']  = upd_name
                food_live.loc[food_live['Food_ID']==sel_id,'Quantity']   = upd_qty
                food_live.loc[food_live['Food_ID']==sel_id,'Food_Type']  = upd_ftype
                food_live.loc[food_live['Food_ID']==sel_id,'Meal_Type']  = upd_mtype
                food_live.loc[food_live['Food_ID']==sel_id,'Location']   = upd_loc
                food_live.to_csv(FOOD_CSV, index=False)
                st.success(f"Food ID {sel_id} updated!")

    with tabs[3]:
        st.markdown("### Delete Food Listing")
        del_id = st.selectbox("Select Food ID to Delete", sorted(food_live['Food_ID'].tolist()))
        st.dataframe(food_live[food_live['Food_ID']==del_id], use_container_width=True)
        if st.button("Confirm Delete", use_container_width=True):
            food_live = food_live[food_live['Food_ID']!=del_id]
            food_live.to_csv(FOOD_CSV, index=False)
            st.success(f"Food ID {del_id} deleted.")
            st.rerun()

# ════════════════════════════════════════════════════════════════════════════
# PROVIDER DIRECTORY
# ════════════════════════════════════════════════════════════════════════════
elif page == "Provider and Receiver Directory":
    st.markdown('<div class="main-title">Provider and Receiver <span>Directory</span></div>', unsafe_allow_html=True)
    st.markdown('<div class="sub-title">Find and contact food providers and receivers directly</div>', unsafe_allow_html=True)
    st.markdown('<hr class="fancy-divider">', unsafe_allow_html=True)

    st.markdown('<div class="sec-header">Provider Search</div>', unsafe_allow_html=True)
    c1, c2, c3 = st.columns(3)
    with c1: search_name = st.text_input("Provider Name")
    with c2: search_city = st.selectbox("City", ["All"]+sorted(providers['City'].dropna().unique().tolist()))
    with c3: filter_type = st.selectbox("Type", ["All"]+sorted(providers['Type'].unique().tolist()))

    df_prov = providers.copy()
    if search_name: df_prov = df_prov[df_prov['Name'].str.contains(search_name,case=False,na=False)]
    if search_city!="All": df_prov = df_prov[df_prov['City']==search_city]
    if filter_type!="All": df_prov = df_prov[df_prov['Type']==filter_type]

    st.caption(f"{len(df_prov)} providers found")
    st.dataframe(df_prov[['Provider_ID','Name','Type','City','Address','Contact']], use_container_width=True)

    st.markdown('<hr class="fancy-divider">', unsafe_allow_html=True)
    st.markdown('<div class="sec-header">Receiver Search</div>', unsafe_allow_html=True)
    r1, r2, r3 = st.columns(3)
    with r1: recv_name = st.text_input("Receiver Name")
    with r2: recv_city = st.selectbox("Receiver City", ["All"]+sorted(receivers['City'].dropna().unique().tolist()))
    with r3: recv_type = st.selectbox("Receiver Type", ["All"]+sorted(receivers['Type'].dropna().unique().tolist()))

    df_recv = receivers.copy()
    if recv_name: df_recv = df_recv[df_recv['Name'].str.contains(recv_name,case=False,na=False)]
    if recv_city!="All": df_recv = df_recv[df_recv['City']==recv_city]
    if recv_type!="All": df_recv = df_recv[df_recv['Type']==recv_type]

    st.caption(f"{len(df_recv)} receivers found")
    st.dataframe(df_recv, use_container_width=True)

# ════════════════════════════════════════════════════════════════════════════
# INSIGHTS & RECOMMENDATIONS
# ════════════════════════════════════════════════════════════════════════════
elif page == "Insights & Recommendations":
    st.markdown('<div class="main-title">Insights & <span>Recommendations</span></div>', unsafe_allow_html=True)
    st.markdown('<div class="sub-title">What the data shows, and what should be done about it</div>', unsafe_allow_html=True)
    st.markdown('<hr class="fancy-divider">', unsafe_allow_html=True)

    top_city      = food.groupby('Location')['Quantity'].sum().idxmax()
    top_city_qty  = food.groupby('Location')['Quantity'].sum().max()
    top_prov_type = food.groupby('Provider_Type')['Quantity'].sum().idxmax()
    top_meal      = food.groupby('Meal_Type')['Quantity'].sum().idxmax()
    unclaimed_cnt = len(food[~food['Food_ID'].isin(claims['Food_ID'])])
    unclaimed_pct = round(unclaimed_cnt/len(food)*100,1)
    completed_pct = round(len(claims[claims['Status']=='Completed'])/len(claims)*100,1)
    cancelled_pct = round(len(claims[claims['Status']=='Cancelled'])/len(claims)*100,1)
    top_recv_type = claims.merge(receivers[['Receiver_ID','Type']],on='Receiver_ID')['Type'].value_counts().idxmax()
    top_demand    = claims.merge(receivers[['Receiver_ID','City']],on='Receiver_ID')['City'].value_counts().idxmax()

    combined = [
        ("1. City with Most Food Available",
         f"<b>{top_city}</b> has the highest food available with <b>{top_city_qty:,} units</b>. This city clearly has very active providers, but it likely doesn't have enough receivers nearby to match that level of supply. Unless more NGOs or shelters are added here, a large share of this food risks expiring before anyone claims it.",
         f"Actively identify and onboard NGOs, shelters, and community centers specifically in {top_city} so the existing food supply doesn't go to waste simply due to lack of receivers nearby."),
        ("2. Most Donated Meal Type",
         f"<b>{top_meal}</b> is the meal type with the highest quantity donated overall. If claim rates for {top_meal} specifically turn out to be lower than other meal types, it becomes the single biggest contributor to wastage in the entire system, simply because there's more of it sitting around unclaimed.",
         f"Run targeted outreach campaigns timed specifically around {top_meal} collection windows, so receivers are reminded to check listings exactly when this surplus is highest."),
        ("3. Top Provider Type",
         f"<b>{top_prov_type}s</b> contribute the most food quantity of any provider category. This makes them the most important group to retain and grow — losing engagement from {top_prov_type}s would have a bigger negative effect on total food supply than losing any other single provider type.",
         f"Give {top_prov_type}s visible recognition through badges, leaderboards, or featured placement in the app, which keeps them motivated and encourages other providers of the same type to contribute more."),
        ("4. Most Active Receiver Type",
         f"<b>{top_recv_type}s</b> make the most food claims of any receiver category. They've clearly built reliable collection habits, which makes them the safest option to prioritize when listing time-sensitive or large quantities of food that need to be picked up quickly.",
         f"Prioritize routing large or time-sensitive food listings toward {top_recv_type}s first, before opening them up to other receiver types, to reduce the risk of the food going unclaimed."),
        ("5. Low Claim Completion Rate",
         f"Only <b>{completed_pct}%</b> of all claims actually get completed, while <b>{cancelled_pct}%</b> end up cancelled. This is the most serious issue in the whole system — food gets reserved by a receiver but then never actually collected, which means it still goes to waste even though it appeared to be 'successfully claimed' on paper.",
         "Send automated SMS or in-app reminders to receivers as soon as a claim is made and again closer to the expiry date, so claimed food is actually picked up instead of being forgotten."),
        ("6. City with Highest Food Demand",
         f"<b>{top_demand}</b> shows the highest number of food claims, meaning demand here is outpacing what's typically available. Recruiting more providers specifically in this city would directly close the gap between how much food people need and how much is actually being offered.",
         f"Actively recruit new food providers in {top_demand} and improve pickup logistics for receivers already operating there, since this is where additional supply will have the highest impact."),
        ("7. Unclaimed Food Waste",
         f"<b>{unclaimed_cnt} food items ({unclaimed_pct}%)</b> have never been claimed by anyone at all. This is the most direct and measurable form of food waste in the dataset — these are not failed attempts, they are items nobody even tried to collect, which usually points to a visibility problem rather than a logistics one.",
         "Improve in-app visibility for new listings — such as push notifications when new food matching a receiver's usual preferences becomes available — so unclaimed items become rare rather than common."),
    ]

    for title, insight, rec in combined:
        st.markdown(f'''<div class="biz-insight">
            <b>{title}</b><br><br>
            <span style="color:#9aa8bc;">{insight}</span><br><br>
            <b style="color:#fb923c;">Recommendation:</b> <span style="color:#9aa8bc;">{rec}</span>
        </div>''', unsafe_allow_html=True)

    st.markdown('<hr class="fancy-divider">', unsafe_allow_html=True)
    st.markdown('<div class="sec-header">Summary</div>', unsafe_allow_html=True)
    c1,c2,c3,c4 = st.columns(4)
    c1.metric("Total Providers",  f"{len(providers):,}")
    c2.metric("Total Receivers",  f"{len(receivers):,}")
    c3.metric("Total Food Items", f"{len(food):,}")
    c4.metric("Total Claims",     f"{len(claims):,}")