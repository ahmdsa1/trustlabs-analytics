"""
Trust Labs Healthcare Analytics Dashboard
v4.0 — Authentication + Mobile + Keep-Alive + Security fixes
"""

import streamlit as st
import pandas as pd
import sqlite3
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta
import io
import numpy as np
from sklearn.linear_model import LinearRegression
import yaml
from yaml.loader import SafeLoader
import streamlit_authenticator as stauth
from streamlit_autorefresh import st_autorefresh

# ============================================================
# PAGE CONFIG — must be first Streamlit call
# ============================================================

st.set_page_config(
    page_title="Trust Labs Analytics",
    page_icon="🏥",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ============================================================
# AUTHENTICATION
# ============================================================

# 1. Load configuration: Priority to st.secrets, fallback to config.yaml
if "credentials" in st.secrets:
    config = st.secrets.to_dict()
else:
    try:
        with open("config.yaml") as f:
            config = yaml.load(f, Loader=SafeLoader)
    except (FileNotFoundError, yaml.YAMLError):
        st.error("Configuration not found. Please set up Streamlit Secrets or provide a valid config.yaml.")
        st.stop()

# 2. Initialize authenticator
try:
    authenticator = stauth.Authenticate(
        config["credentials"],
        config["cookie"]["name"],
        config["cookie"]["key"],
        config["cookie"]["expiry_days"],
        config.get("preauthorized", {"emails": []})
    )
except Exception as e:
    st.error(f"Error initializing authenticator: {e}")
    st.stop()

# 3. Render login widget
# Returns name, status, and username
name, authentication_status, username = authenticator.login(location='main')

# 4. Handle authentication status
if authentication_status:
    # User is logged in
    st.session_state["name"] = name
    st.session_state["username"] = username
elif authentication_status == False:
    st.error("Incorrect username or password. Please try again.")
    st.stop()
elif authentication_status == None:
    st.markdown("""
    <div style="max-width:400px;margin:100px auto 40px;text-align:center;padding:40px;border:1px solid #dadce0;border-radius:8px;background:#ffffff">
        <div style="font-size:2.5rem;margin-bottom:16px">🏥</div>
        <div style="font-size:1.5rem;font-weight:400;color:#202124;margin-bottom:8px;font-family:'Google Sans',sans-serif">Sign in</div>
        <div style="font-size:1rem;color:#202124;margin-bottom:32px;font-family:'Roboto',sans-serif">to continue to Trust Labs Analytics</div>
    </div>
    """, unsafe_allow_html=True)
    st.stop()

# ── Authenticated past this point ──────────────────────────

# Keep-alive: silently re-runs every 10 minutes so Streamlit
# Cloud never marks the app as inactive and puts it to sleep.
st_autorefresh(interval=600_000, limit=None, key="keepalive")

# ============================================================
# CSS — Material Design + Mobile Responsive
# ============================================================

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Google+Sans:wght@300;400;500;600;700&family=Google+Sans+Display:wght@400;500;700&family=Roboto:wght@300;400;500;700&display=swap');

html, body, [class*="css"], .stApp {
  background: #ffffff !important;
  color: #202124 !important;
  font-family: 'Roboto', sans-serif !important;
}
.main .block-container {
  padding: 1rem 2.5rem !important;
  max-width: 1400px !important;
}

/* ── SIDEBAR GOOGLE STYLE ─────────────────────────────────── */
[data-testid="stSidebar"] {
  background: #ffffff !important;
  border-right: 1px solid #dadce0 !important;
  width: 280px !important;
}
[data-testid="stSidebar"] .stRadio > div { gap: 4px !important; }
[data-testid="stSidebar"] .stRadio label {
  display: flex !important; align-items: center !important;
  gap: 12px !important; padding: 12px 24px !important;
  border-radius: 0 24px 24px 0 !important; color: #3c4043 !important;
  font-weight: 500 !important; font-size: 0.875rem !important;
  cursor: pointer !important; transition: background .2s !important;
  margin-right: 12px !important;
  font-family: 'Google Sans', sans-serif !important;
}
[data-testid="stSidebar"] .stRadio label:hover {
  background: #f1f3f4 !important;
}
[data-testid="stSidebar"] .stRadio [data-testid="stMarkdownContainer"] p {
    color: inherit !important;
}

/* ── BUTTONS & INPUTS ────────────────────────────────────── */
.stButton > button {
  font-family: 'Google Sans', sans-serif !important; font-weight: 500 !important;
  font-size: 0.875rem !important; background: #1a73e8 !important;
  color: #ffffff !important; border: 1px solid transparent !important;
  border-radius: 24px !important; padding: 0.6rem 1.5rem !important;
  transition: all .2s !important;
  box-shadow: none !important;
}
.stButton > button:hover {
  background: #1765cc !important;
  box-shadow: 0 1px 2px 0 rgba(60,64,67,.3), 0 1px 3px 1px rgba(60,64,67,.15) !important;
}

.stTextInput input {
  border-radius: 8px !important;
  border: 1px solid #dadce0 !important;
  padding: 10px 14px !important;
}

/* ── CARDS & SECTIONS ─────────────────────────────────────── */
.kpi-card {
  background: #ffffff; border-radius: 12px; padding: 24px;
  border: 1px solid #dadce0;
  transition: box-shadow .2s ease-in-out;
}
.kpi-card:hover {
  box-shadow: 0 1px 2px 0 rgba(60,64,67,.30), 0 1px 3px 1px rgba(60,64,67,.15);
}
.kpi-label {
  font-size: 0.8rem; color: #5f6368; font-weight: 500;
  font-family: 'Google Sans', sans-serif; margin-bottom: 8px;
}
.kpi-value {
  font-size: 2.25rem; font-weight: 400; color: #202124;
  font-family: 'Google Sans Display', sans-serif; margin-bottom: 4px;
}

.section-title {
  font-family: 'Google Sans', sans-serif !important; font-size: 1.25rem !important;
  font-weight: 400 !important; color: #202124 !important;
  margin: 2rem 0 1rem 0 !important;
}

/* ── HIDE STREAMLIT ELEMENTS ──────────────────────────────── */
#MainMenu, footer { visibility: hidden; }
.stDeployButton { display: none; }

# ============================================================
# PLOTLY THEME
# ============================================================

def google_theme(fig, height=350):
    fig.update_layout(
        plot_bgcolor="rgba(0,0,0,0)",
        paper_bgcolor="rgba(0,0,0,0)",
        xaxis=dict(showgrid=False, showline=True, linecolor="#dadce0",
                   tickfont=dict(size=12, color="#5f6368", family="Roboto"),
                   title_font=dict(size=12, color="#5f6368", family="Google Sans")),
        yaxis=dict(showgrid=True, gridcolor="#f1f3f4", showline=False,
                   tickfont=dict(size=12, color="#5f6368", family="Roboto"),
                   title_font=dict(size=12, color="#5f6368", family="Google Sans")),
        font=dict(family="Roboto, sans-serif", size=12, color="#202124"),
        margin=dict(t=20, b=30, l=40, r=20),
        height=height,
        hoverlabel=dict(bgcolor="#ffffff", font_size=12, font_family="Roboto", bordercolor="#dadce0"),
        legend=dict(font=dict(size=12, color="#5f6368"), bgcolor="rgba(0,0,0,0)",
                   orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
    )
    return fig

def google_donut(vals, names, colors, hole=0.7):
    fig = px.pie(values=vals, names=names, color=names,
                 color_discrete_map=dict(zip(names, colors)))
    fig.update_traces(hole=hole, textposition="outside", textinfo="percent+label",
                      textfont=dict(size=12, color="#202124"),
                      marker=dict(line=dict(color="#ffffff", width=2)))
    fig.update_layout(height=300, paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
                      showlegend=False, margin=dict(t=10, b=10, l=10, r=10),
                      font=dict(family="Google Sans, sans-serif", size=12, color="#202124"))
    return fig

def safe_vline(fig, x_datetime):
    xs = x_datetime.strftime("%Y-%m-%d")
    fig.add_shape(type="line", x0=xs, x1=xs, y0=0, y1=1, xref="x", yref="paper",
                  line=dict(color="#9aa0a6", width=1, dash="solid"))

# ============================================================
# CARD HELPERS
# ============================================================

def sec_title(title, subtitle=""):
    html = f'<div class="section-title">{title}</div>'
    if subtitle:
        html += f'<div style="font-size:0.875rem;color:#5f6368;margin:-8px 0 24px 0">{subtitle}</div>'
    st.markdown(html, unsafe_allow_html=True)

def kpi_card(label, value, trend_text, trend_dir="neutral", icon="📊", accent="#1a73e8"):
    return f"""
<div class="kpi-card">
  <div class="kpi-label">{label}</div>
  <div class="kpi-value">{value}</div>
  <div style="font-size:0.8rem;color:#5f6368;display:flex;align-items:center;gap:4px">
    <span>{icon}</span> {trend_text}
  </div>
</div>"""

def kpi_row(cards, cols=5):
    return (f'<div class="kpi-grid" style="grid-template-columns:repeat({cols},1fr)">'
            + "".join(cards) + "</div>")

# ============================================================
# DATABASE — single cached connection
# ============================================================

@st.cache_resource
def get_connection():
    conn = sqlite3.connect("trust_labs.db", check_same_thread=False)
    conn.execute("PRAGMA journal_mode=WAL")
    conn.execute("PRAGMA synchronous=NORMAL")
    
    # Initialize tables if they don't exist
    conn.execute("""
    CREATE TABLE IF NOT EXISTS patients (
        patient_id TEXT PRIMARY KEY,
        gender TEXT,
        age_group TEXT,
        patient_tier TEXT,
        loyalty_points INTEGER,
        churn_risk_category TEXT,
        churn_risk_score INTEGER,
        days_since_last_visit INTEGER
    )""")
    conn.execute("""
    CREATE TABLE IF NOT EXISTS visits (
        visit_date TEXT,
        visit_month TEXT,
        patient_id TEXT,
        branch_name TEXT,
        visit_time TEXT,
        visit_day_name TEXT
    )""")
    conn.execute("""
    CREATE TABLE IF NOT EXISTS doctors (
        doctor_id TEXT PRIMARY KEY,
        actual_referrals INTEGER
    )""")
    conn.execute("""
    CREATE TABLE IF NOT EXISTS corporates (
        corporate_id TEXT PRIMARY KEY,
        actual_visits INTEGER
    )""")
    conn.execute("""
    CREATE TABLE IF NOT EXISTS branches (
        branch_name TEXT PRIMARY KEY,
        total_visits INTEGER
    )""")
    conn.execute("""
    CREATE TABLE IF NOT EXISTS monthly_trends (
        visit_month TEXT PRIMARY KEY,
        total_visits INTEGER
    )""")
    conn.execute("""
    CREATE TABLE IF NOT EXISTS monthly_revenue (
        visit_month TEXT PRIMARY KEY,
        total_revenue REAL,
        total_profit REAL
    )""")
    return conn

conn = get_connection()

# ============================================================
# DATA LOADERS — lazy, cached per page
# ============================================================

@st.cache_data(ttl=3600)
def load_patients():
    try:
        return pd.read_sql("SELECT * FROM patients", conn)
    except Exception:
        return pd.DataFrame(columns=["patient_id", "gender", "age_group", "patient_tier", "loyalty_points", "churn_risk_category", "churn_risk_score", "days_since_last_visit"])

@st.cache_data(ttl=3600)
def load_visits():
    try:
        df = pd.read_sql("SELECT * FROM visits", conn)
        df["visit_date"]  = pd.to_datetime(df["visit_date"],  errors="coerce")
        df["visit_month"] = pd.to_datetime(df["visit_month"], errors="coerce")
        return df
    except Exception:
        return pd.DataFrame(columns=["visit_date", "visit_month", "patient_id", "branch_name", "visit_time", "visit_day_name"])

@st.cache_data(ttl=3600)
def load_doctors():
    try:
        return pd.read_sql("SELECT * FROM doctors", conn)
    except Exception:
        return pd.DataFrame(columns=["doctor_id", "actual_referrals"])

@st.cache_data(ttl=3600)
def load_corporates():
    try:
        return pd.read_sql("SELECT * FROM corporates", conn)
    except Exception:
        return pd.DataFrame(columns=["corporate_id", "actual_visits"])

@st.cache_data(ttl=3600)
def load_branches():
    try:
        return pd.read_sql("SELECT * FROM branches", conn)
    except Exception:
        return pd.DataFrame(columns=["branch_name", "total_visits"])

@st.cache_data(ttl=3600)
def load_monthly_trends():
    try:
        df = pd.read_sql("SELECT * FROM monthly_trends", conn)
        df["visit_month"] = pd.to_datetime(df["visit_month"], errors="coerce")
        return df
    except Exception:
        return pd.DataFrame(columns=["visit_month", "total_visits"])

@st.cache_data(ttl=3600)
def load_monthly_revenue():
    try:
        df = pd.read_sql("SELECT * FROM monthly_revenue", conn)
        df["visit_month"] = pd.to_datetime(df["visit_month"], errors="coerce")
        return df
    except Exception:
        return pd.DataFrame(columns=["visit_month", "total_revenue", "total_profit"])

# ============================================================
# SEARCH HELPERS — parameterised queries (no SQL injection)
# ============================================================

def search_patient_by_id(pid: str):
    df = pd.read_sql(
        "SELECT * FROM patients WHERE LOWER(patient_id) = LOWER(?)",
        conn, params=(pid.strip(),)
    )
    return df if not df.empty else None

def search_doctor_by_id(did: str):
    df = pd.read_sql(
        "SELECT * FROM doctors WHERE LOWER(doctor_id) = LOWER(?)",
        conn, params=(did.strip(),)
    )
    return df if not df.empty else None

def search_corporate_by_id(cid: str):
    df = pd.read_sql(
        "SELECT * FROM corporates WHERE LOWER(corporate_id) = LOWER(?)",
        conn, params=(cid.strip(),)
    )
    return df if not df.empty else None

def get_patient_visits(pid: str):
    df = pd.read_sql(
        """SELECT visit_date, branch_name, visit_time, visit_day_name
           FROM visits WHERE LOWER(patient_id) = LOWER(?)
           ORDER BY visit_date DESC""",
        conn, params=(pid.strip(),)
    )
    df["visit_date"] = pd.to_datetime(df["visit_date"], errors="coerce")
    return df

# ============================================================
# EXPORT HELPERS
# ============================================================

def export_to_excel(df: pd.DataFrame) -> bytes:
    out = io.BytesIO()
    with pd.ExcelWriter(out, engine="openpyxl") as w:
        df.to_excel(w, index=False)
    return out.getvalue()

def export_to_csv(df: pd.DataFrame) -> bytes:
    return df.to_csv(index=False).encode("utf-8")

# ============================================================
# ANALYTICS HELPERS
# ============================================================

@st.cache_data(ttl=3600)
def predict_visits(_monthly_trends_df: pd.DataFrame, months_ahead: int = 3):
    """Linear regression forecast. Underscore prefix skips DataFrame hashing."""
    df = _monthly_trends_df.copy().sort_values("visit_month").reset_index(drop=True)
    df["month_num"] = range(len(df))
    X = df[["month_num"]].values
    y = df["total_visits"].values
    model = LinearRegression().fit(X, y)
    residuals = y - model.predict(X)
    std_err = np.std(residuals)
    last_num = df["month_num"].max()
    future_nums = np.array([[last_num + i] for i in range(1, months_ahead + 1)])
    preds = model.predict(future_nums).astype(int)
    last_date = df["visit_month"].max()
    future_dates = [last_date + timedelta(days=30 * i) for i in range(1, months_ahead + 1)]
    return pd.DataFrame({
        "visit_month": future_dates,
        "predicted_visits": preds,
        "lower": (preds - std_err).astype(int),
        "upper": (preds + std_err).astype(int),
    }), std_err

def compute_cagr(initial, final, months):
    if initial <= 0 or final <= 0 or months <= 0:
        return 0.0
    try:
        return ((final / initial) ** (1.0 / (months / 12.0)) - 1.0) * 100.0
    except Exception:
        return 0.0

def build_real_revenue_from_visits(visits_df, annual_inflation=0.33):
    avg_rev = 150
    monthly = (visits_df.groupby("visit_month")
               .agg({"visit_date": "count"}).reset_index()
               .rename(columns={"visit_date": "total_visits"})
               .sort_values("visit_month").reset_index(drop=True))
    monthly["total_revenue"] = monthly["total_visits"] * avg_rev
    monthly["total_profit"]  = monthly["total_revenue"] * 0.65
    if len(monthly) < 2:
        return pd.DataFrame()
    n = len(monthly)
    deflators = [(1 + annual_inflation) ** (i / 12.0) for i in range(n)]
    monthly["deflator"]      = deflators
    monthly["real_revenue"]  = monthly["total_revenue"] / monthly["deflator"]
    monthly["real_profit"]   = monthly["total_profit"]  / monthly["deflator"]
    monthly["inflation_tax"] = monthly["total_revenue"] - monthly["real_revenue"]
    monthly["real_index"]    = monthly["real_revenue"]  / monthly["real_revenue"].iloc[0] * 100
    monthly["nominal_index"] = monthly["total_revenue"] / monthly["total_revenue"].iloc[0] * 100
    monthly["month_label"]   = monthly["visit_month"].dt.strftime("%b %Y")
    return monthly

def build_real_revenue(mr_df, annual_inflation=0.33):
    df = (mr_df.sort_values("visit_month").dropna(subset=["total_revenue"])
          .copy().reset_index(drop=True))
    if len(df) < 2:
        return df
    n = len(df)
    deflators = [(1 + annual_inflation) ** (i / 12.0) for i in range(n)]
    df["deflator"]      = deflators
    df["real_revenue"]  = df["total_revenue"] / df["deflator"]
    if "total_profit" in df.columns:
        df["real_profit"] = df["total_profit"] / df["deflator"]
    df["inflation_tax"] = df["total_revenue"] - df["real_revenue"]
    df["real_index"]    = df["real_revenue"]  / df["real_revenue"].iloc[0] * 100
    df["nominal_index"] = df["total_revenue"] / df["total_revenue"].iloc[0] * 100
    df["month_label"]   = df["visit_month"].dt.strftime("%b %Y")
    return df

# ============================================================
# LOAD SHARED DATA
# ============================================================

patients_data   = load_patients()
branches_data   = load_branches()
monthly_trends  = load_monthly_trends()
high_risk_count = int((patients_data["churn_risk_category"] == "High Risk").sum())

# ============================================================
# SIDEBAR
# ============================================================

with st.sidebar:
    st.markdown("""
<div style="padding:16px 24px">
    <div style="display:flex;align-items:center;gap:12px">
        <span style="font-size:2rem">🏥</span>
        <div style="font-family:'Google Sans',sans-serif;font-size:1.15rem;font-weight:500;color:#202124">Trust Labs</div>
    </div>
</div>""", unsafe_allow_html=True)

    # Logged-in user info
    user_name = st.session_state.get("name", "User")
    st.markdown(f"""
<div style="padding:0 24px 16px;font-size:0.875rem;color:#5f6368">
  Logged in as <b>{user_name}</b>
</div>""", unsafe_allow_html=True)

    st.markdown('<hr style="margin:0 0 12px;border:none;border-top:1px solid #dadce0">', unsafe_allow_html=True)

    page = st.radio("nav",
        ["Home", "Patient Search", "Doctor Search",
         "Corporate Search", "Analytics", "Export"],
        label_visibility="collapsed")

    st.markdown('<hr style="margin:12px 0;border:none;border-top:1px solid #dadce0">', unsafe_allow_html=True)
    st.markdown("""<div style="font-size:.7rem;font-weight:600;text-transform:uppercase;
letter-spacing:.8px;color:#5f6368;margin-bottom:10px;font-family:'Google Sans',sans-serif">Quick Stats</div>""",
                unsafe_allow_html=True)

    visits_count = len(load_visits())
    doctors_data_sidebar = load_doctors()
    active_docs_sidebar  = int((doctors_data_sidebar["actual_referrals"] > 0).sum())

    st.markdown(kpi_row([
        kpi_card("Patients", f"{len(patients_data):,}", "", "neutral", "👥", "#1a73e8"),
        kpi_card("Visits",   f"{visits_count:,}",       "", "neutral", "📊", "#34a853")
    ], 2), unsafe_allow_html=True)
    st.markdown(kpi_row([
        kpi_card("Doctors",  f"{active_docs_sidebar}", "", "neutral", "👨‍⚕️", "#fbbc04"),
        kpi_card("At Risk",  f"{high_risk_count}",     "", "down",    "⚠️", "#ea4335")
    ], 2), unsafe_allow_html=True)

    st.markdown('<hr style="margin:12px 0;border:none;border-top:1px solid #dadce0">', unsafe_allow_html=True)
    st.markdown(f"""<div style="text-align:center;font-size:0.7rem;color:#9aa0a6">
Updated {datetime.now().strftime("%b %d, %Y • %H:%M")}</div>""", unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)
    authenticator.logout("Logout", "sidebar")

# ============================================================
# PAGE: HOME
# ============================================================

if page == "Home":
    st.markdown("""<div class="page-header">
<h1>Analytics Dashboard</h1>
<p>Professional healthcare intelligence platform</p>
</div>""", unsafe_allow_html=True)

    visits_data   = load_visits()
    avg_visits    = len(visits_data) / len(patients_data)
    avg_loyalty   = patients_data["loyalty_points"].mean()
    high_risk_pct = high_risk_count / len(patients_data) * 100

    st.markdown(kpi_row([
        kpi_card("Total Patients",    f"{len(patients_data):,}", "+5.2%", "up",      "👥", "#1a73e8"),
        kpi_card("Total Visits",      f"{len(visits_data):,}",   "+8.1%", "up",      "📊", "#34a853"),
        kpi_card("Avg Visits/Patient", f"{avg_visits:.1f}",       "+0.3",  "up",      "📈", "#fbbc04"),
        kpi_card("High Risk %",        f"{high_risk_pct:.1f}%",  "-2.1%", "down",    "⚠️", "#ea4335"),
        kpi_card("Avg Loyalty",        f"{avg_loyalty:.0f}",      "+3.5",  "up",      "🏆", "#9334e6")
    ], 5), unsafe_allow_html=True)

    c1, c2 = st.columns(2)
    with c1:
        sec_title("Gender Distribution")
        gender_counts = patients_data["gender"].value_counts()
        fig = google_donut(gender_counts.values, gender_counts.index, ["#1a73e8", "#ea4335"])
        st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": False})
            with c2:
        sec_title("Churn Risk Levels")
        risk_counts = patients_data["churn_risk_category"].value_counts()
        fig = google_donut(risk_counts.values, risk_counts.index, ["#34a853", "#fbbc04", "#ea4335"])
        st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": False})
        
    sec_title("Monthly Visit Trends")
    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=monthly_trends["visit_month"], y=monthly_trends["total_visits"],
        mode="lines+markers", name="Total Visits",
        line=dict(color="#1a73e8", width=3), marker=dict(size=10)
    ))
    google_theme(fig, height=320)
    st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": False})

    gold_count = len(patients_data[patients_data["patient_tier"] == "Gold"])
    corporates_data = load_corporates()
    doctors_data    = load_doctors()
    active_docs     = int((doctors_data["actual_referrals"] > 0).sum())
    active_corps    = int((corporates_data["actual_visits"] > 0).sum())

    st.markdown(kpi_row([
        kpi_card("Gold Tier",        f"{gold_count:,}",
                 f"{gold_count/len(patients_data)*100:.1f}%", "neutral", "🥇", "#fbbc04"),
        kpi_card("Active Doctors",   f"{active_docs}/{len(doctors_data)}", "active", "up",      "👨‍⚕️", "#34a853"),
        kpi_card("Active Contracts", f"{active_corps}/{len(corporates_data)}", "active", "up",  "🏢", "#1a73e8"),
        kpi_card("Top Branch",
                 branches_data.nlargest(1, "total_visits")["branch_name"].values[0] if not branches_data.empty else "N/A",
                 "Leading", "neutral", "🏆", "#9334e6")
    ], 4), unsafe_allow_html=True)
# ============================================================
# PAGE: PATIENT SEARCH
# ============================================================

elif page == "Patient Search":
    st.markdown("""<div class="page-header">
<h1>Patient Search</h1>
<p>Search and analyze patient records in the Trust Labs database</p>
</div>""", unsafe_allow_html=True)

    tab1, tab2 = st.tabs(["🆔 ID Lookup", "🔎 Advanced Search"])

    with tab1:
        c1, c2 = st.columns([3, 1])
        with c1:
            patient_id = st.text_input("Patient ID", placeholder="e.g., P0000000001")
        with c2:
            st.markdown("<br>", unsafe_allow_html=True)
            search_btn = st.button("🔍 Search", type="primary", use_container_width=True)

        if search_btn and patient_id:
            patient = search_patient_by_id(patient_id)
            if patient is None:
                st.error(f"Patient ID '{patient_id}' not found.")
            else:
                st.success(f"Patient found: **{patient_id.upper()}**")
                tier    = patient["patient_tier"].values[0]
                loyalty = int(patient["loyalty_points"].values[0])
                risk    = int(patient["churn_risk_score"].values[0])
                visits  = int(patient["total_visits"].values[0])
                days    = int(patient["days_since_last_visit"].values[0])

                st.markdown(kpi_row([
                    kpi_card("Tier",       tier,      "",        "neutral",                               "🏆", "#1a73e8"),
                    kpi_card("Loyalty",    str(loyalty), "points", "up",                                  "⭐", "#fbbc04"),
                    kpi_card("Risk Score", str(risk),
                             "Low" if risk < 30 else "Medium" if risk < 60 else "High",
                             "neutral" if risk < 30 else "down",                                          "⚠️",
                             "#ea4335" if risk >= 60 else "#fbbc04"),
                    kpi_card("Visits",     str(visits), "",        "neutral",                             "📊", "#34a853"),
                    kpi_card("Days Since", str(days),   "last visit", "neutral",                          "📅", "#9334e6")
                ], 5), unsafe_allow_html=True)

                info_card_start("Patient Information")
                st.dataframe(patient.T, use_container_width=True)
                
                patient_visits = get_patient_visits(patient_id)
                if not patient_visits.empty:
                    info_card_start(f"Visit History ({len(patient_visits)} visits)")
                    st.dataframe(patient_visits, hide_index=True, use_container_width=True, height=300)
                    c1, c2 = st.columns(2)
                    with c1:
                        st.download_button("📊 Download Excel",
                                           export_to_excel(patient_visits),
                                           f"patient_{patient_id}_visits.xlsx",
                                           use_container_width=True)
                    with c2:
                        st.download_button("📄 Download CSV",
                                           export_to_csv(patient_visits),
                                           f"patient_{patient_id}_visits.csv",
                                           use_container_width=True)
                    
    with tab2:
        info_card_start("🔎 Advanced Filters")
        c1, c2, c3 = st.columns(3)
        with c1:
            tier_filter   = st.multiselect("Tier", ["Gold", "Silver", "Bronze"])
            risk_filter   = st.multiselect("Risk", ["Low Risk", "Medium Risk", "High Risk"])
        with c2:
            age_filter    = st.multiselect("Age Group", sorted(patients_data["age_group"].unique()))
            gender_filter = st.selectbox("Gender", ["All", "Male", "Female"])
        with c3:
            min_visits  = st.number_input("Min Visits", 0, step=1)
            min_loyalty = st.number_input("Min Loyalty", 0, step=10)

        if st.button("🔎 Apply Filters", type="primary"):
            results = patients_data.copy()
            if tier_filter:            results = results[results["patient_tier"].isin(tier_filter)]
            if risk_filter:            results = results[results["churn_risk_category"].isin(risk_filter)]
            if age_filter:             results = results[results["age_group"].isin(age_filter)]
            if gender_filter != "All": results = results[results["gender"] == gender_filter]
            if min_visits > 0:         results = results[results["total_visits"] >= min_visits]
            if min_loyalty > 0:        results = results[results["loyalty_points"] >= min_loyalty]

            st.markdown(f'<p style="color:#5f6368;font-size:.85rem">Found {len(results):,} patients</p>',
                        unsafe_allow_html=True)
            st.dataframe(results[["patient_id", "age_group", "gender", "patient_tier",
                                   "loyalty_points", "churn_risk_category", "total_visits"]],
                         hide_index=True, use_container_width=True, height=400)
            st.download_button("📊 Export Results", export_to_excel(results), "search_results.xlsx")
        
# ============================================================
# PAGE: DOCTOR SEARCH
# ============================================================

elif page == "Doctor Search":
    st.markdown("""<div class="page-header">
<h1>Doctor Referrals</h1>
<p>Analyze referral performance and doctor engagement</p>
</div>""", unsafe_allow_html=True)

    doctors_data = load_doctors()

    c1, c2 = st.columns([3, 1])
    with c1:
        doctor_id = st.text_input("Doctor ID", placeholder="e.g., DOC00096")
    with c2:
        st.markdown("<br>", unsafe_allow_html=True)
        search_btn = st.button("🔍 Search", type="primary", use_container_width=True)

    if search_btn and doctor_id:
        doctor = search_doctor_by_id(doctor_id)
        if doctor is None or doctor.empty:
            st.error(f"Doctor ID '{doctor_id}' not found.")
        else:
            st.success(f"Doctor found: **{doctor['doctor_name'].values[0]}**")
            refs     = int(doctor["actual_referrals"].values[0])
            patients = int(doctor["unique_patients_referred"].values[0])
            revenue  = float(doctor["total_revenue_generated"].values[0])
            perf     = doctor["performance_category"].values[0]

            st.markdown(kpi_row([
                kpi_card("Specialty",  doctor["specialty"].values[0], "", "neutral", "🩺", "#1a73e8"),
                kpi_card("Referrals",  f"{refs:,}",                   "", "up",      "📊", "#34a853"),
                kpi_card("Patients",   f"{patients:,}",    "unique",  "up",          "👥", "#fbbc04"),
                kpi_card("Revenue",    f"{revenue/1000:.1f}K EGP", "generated", "up", "💰", "#9334e6"),
                kpi_card("Performance", perf, "",
                         "up" if perf == "Exceeds Expectations" else "neutral", "⭐",
                         "#34a853" if perf == "Exceeds Expectations" else "#fbbc04")
            ], 5), unsafe_allow_html=True)

            st.dataframe(doctor.T, use_container_width=True)
            
    display_doctors = doctors_data[[
        "doctor_id", "doctor_name", "specialty", "actual_referrals",
        "unique_patients_referred", "total_revenue_generated", "performance_category"
    ]].sort_values("actual_referrals", ascending=False)
    st.dataframe(display_doctors, hide_index=True, use_container_width=True, height=400)
    st.download_button("📊 Export Doctors", export_to_excel(display_doctors), "doctors_performance.xlsx")
    
# ============================================================
# PAGE: CORPORATE SEARCH
# ============================================================

elif page == "Corporate Search":
    st.markdown("""<div class="page-header">
<h1>Corporate Performance</h1>
<p>Monitor contract utilization and corporate patient visits</p>
</div>""", unsafe_allow_html=True)

    corporates_data = load_corporates()

    c1, c2 = st.columns([3, 1])
    with c1:
        corp_id = st.text_input("Corporate ID", placeholder="e.g., CORP023")
    with c2:
        st.markdown("<br>", unsafe_allow_html=True)
        search_btn = st.button("🔍 Search", type="primary", use_container_width=True)

    if search_btn and corp_id:
        corp = search_corporate_by_id(corp_id)
        if corp is None or corp.empty:
            st.error(f"Corporate ID '{corp_id}' not found.")
        else:
            st.success(f"Contract found: **{corp['company_name'].values[0]}**")
            emp     = int(corp["employee_count"].values[0])
            active  = int(corp["unique_employees"].values[0])
            util    = float(corp["actual_utilization_rate"].values[0]) * 100
            revenue = float(corp["total_revenue"].values[0])
            health  = corp["contract_health"].values[0]

            st.markdown(kpi_row([
                kpi_card("Employees",    f"{emp:,}",    "total",  "neutral",                         "👥", "#1a73e8"),
                kpi_card("Active",       f"{active:,}", f"{active/emp*100:.0f}%", "up",              "✅", "#34a853"),
                kpi_card("Utilization",  f"{util:.1f}%", "rate",
                         "up" if util > 50 else "neutral",                                            "📊", "#fbbc04"),
                kpi_card("Revenue",      f"{revenue/1000:.1f}K EGP", "total", "up",                  "💰", "#9334e6"),
                kpi_card("Health",       health, "",
                         "up" if health == "Excellent" else "neutral" if health == "Good" else "down","❤️",
                         "#34a853" if health == "Excellent" else "#fbbc04")
            ], 5), unsafe_allow_html=True)

            st.dataframe(corp.T, use_container_width=True)
            
    display_corps = corporates_data[[
        "corporate_id", "company_name", "industry", "employee_count",
        "unique_employees", "total_revenue", "contract_health"
    ]].sort_values("total_revenue", ascending=False)
    st.dataframe(display_corps, hide_index=True, use_container_width=True, height=400)
    st.download_button("📊 Export Contracts", export_to_excel(display_corps), "corporate_contracts.xlsx")
    
# ============================================================
# PAGE: ANALYTICS
# ============================================================

elif page == "Analytics":
    st.markdown("""<div class="page-header">
<h1>Platform Analytics</h1>
<p>Deep dive into operational and clinical metrics</p>
</div>""", unsafe_allow_html=True)

    visits_data  = load_visits()
    doctors_data = load_doctors()

    tab1, tab2, tab3, tab4 = st.tabs(
        ["📊 Overview", "⚠️ Churn", "💰 Revenue & Inflation (CAGR)", "🔮 Predictive Trends"])

    with tab1:
        n      = len(patients_data)
        gold   = len(patients_data[patients_data["patient_tier"] == "Gold"])
        silver = len(patients_data[patients_data["patient_tier"] == "Silver"])
        bronze = len(patients_data[patients_data["patient_tier"] == "Bronze"])

        st.markdown(kpi_row([
            kpi_card("🥇 Gold",      f"{gold:,}",   f"{gold/n*100:.1f}%",   "neutral", "🥇", "#fbbc04"),
            kpi_card("🥈 Silver",    f"{silver:,}", f"{silver/n*100:.1f}%", "neutral", "🥈", "#9aa0a6"),
            kpi_card("🥉 Bronze",    f"{bronze:,}", f"{bronze/n*100:.1f}%", "neutral", "🥉", "#cd7f32"),
            kpi_card("Avg Loyalty",  f"{patients_data['loyalty_points'].mean():.0f}", "points", "up", "⭐", "#1a73e8")
        ], 4), unsafe_allow_html=True)

        c1, c2 = st.columns(2)
        with c1:
            sec_title("🏆 Patient Tiers")
            tier_counts = patients_data["patient_tier"].value_counts()
            fig = google_donut(tier_counts.values, tier_counts.index, ["#fbbc04", "#9aa0a6", "#cd7f32"])
            st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": False})
        with c2:
            sec_title("🏥 Top 5 Branches")
            top5 = branches_data.nlargest(5, "total_visits")
            fig = px.bar(top5, x="total_visits", y="branch_name", orientation="h",
                         color="performance_score", color_continuous_scale="Blues")
            google_theme(fig, height=280)
            fig.update_layout(showlegend=False, yaxis_title=None, xaxis_title="Total Visits")
            st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": False})
            
        sec_title("👥 Age Distribution")
        age_dist = patients_data["age_group"].value_counts().sort_index()
        fig = px.bar(x=age_dist.index, y=age_dist.values,
                     color=age_dist.values, color_continuous_scale="Viridis")
        google_theme(fig, height=300)
        fig.update_layout(showlegend=False, xaxis_title="Age Group", yaxis_title="Count")
        st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": False})
        
    with tab2:
        hi = patients_data[patients_data["churn_risk_category"] == "High Risk"]
        me = patients_data[patients_data["churn_risk_category"] == "Medium Risk"]
        lo = patients_data[patients_data["churn_risk_category"] == "Low Risk"]
        n  = len(patients_data)

        st.markdown(kpi_row([
            kpi_card("🔴 High Risk",   f"{len(hi):,}", f"{len(hi)/n*100:.1f}%", "down",    "🔴", "#ea4335"),
            kpi_card("🟡 Medium Risk", f"{len(me):,}", f"{len(me)/n*100:.1f}%", "neutral", "🟡", "#fbbc04"),
            kpi_card("🟢 Low Risk",    f"{len(lo):,}", f"{len(lo)/n*100:.1f}%", "up",      "🟢", "#34a853")
        ], 3), unsafe_allow_html=True)

        c1, c2 = st.columns(2)
        with c1:
            sec_title("👥 Risk Level by Patient Tier", "How each tier breaks down across risk categories")
            cross = (patients_data.groupby(["churn_risk_category", "patient_tier"])
                     .size().reset_index(name="count"))
            fig = px.bar(cross, x="churn_risk_category", y="count", color="patient_tier",
                         color_discrete_map={"Gold": "#fbbc04", "Silver": "#9aa0a6", "Bronze": "#cd7f32"},
                         barmode="group",
                         category_orders={"churn_risk_category": ["Low Risk", "Medium Risk", "High Risk"]},
                         text="count")
            fig.update_traces(textposition="outside", textfont_size=11)
            google_theme(fig, height=300)
            fig.update_layout(xaxis_title=None, yaxis_title="Patients", legend_title="Tier")
            st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": False})
            
        with c2:
            sec_title("🔥 Patient Engagement Status", "Current engagement level across all patients")
            if "engagement_status" in patients_data.columns:
                eng = patients_data["engagement_status"].value_counts().reset_index()
                eng.columns = ["Status", "Count"]
                color_map = {"Highly Engaged": "#34a853", "Engaged": "#1a73e8",
                             "At Risk": "#fbbc04", "Inactive": "#ea4335"}
                fig = px.bar(eng, x="Status", y="Count", color="Status",
                             color_discrete_map=color_map, text="Count")
                fig.update_traces(textposition="outside", textfont_size=12)
                google_theme(fig, height=300)
                fig.update_layout(xaxis_title=None, yaxis_title="Patients", showlegend=False)
                st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": False})
            else:
                st.info("Engagement status column not available in this dataset.")
            
        sec_title("📋 Average Profile by Risk Category", "What distinguishes high-risk from low-risk patients")
        summary_cols = ["churn_risk_category", "total_visits", "days_since_last_visit", "loyalty_points"]
        available    = [c for c in summary_cols if c in patients_data.columns]
        if len(available) > 1:
            summary = (patients_data[available].groupby("churn_risk_category").mean().round(1).reset_index())
            summary.columns = [c.replace("_", " ").title() for c in summary.columns]
            order_map = {"Low Risk": 0, "Medium Risk": 1, "High Risk": 2}
            summary["_sort"] = summary.iloc[:, 0].map(order_map)
            summary = summary.sort_values("_sort").drop(columns=["_sort"])
            st.dataframe(summary, hide_index=True, use_container_width=True)
        
        st.dataframe(hi.nlargest(20, "churn_risk_score")[["patient_id", "churn_risk_score", "days_since_last_visit",
             "total_visits", "loyalty_points", "patient_tier"]],
                     hide_index=True, use_container_width=True)
        st.download_button("📊 Export High-Risk List", export_to_excel(hi), "high_risk.xlsx")
        
    with tab3:
        monthly_revenue = load_monthly_revenue()
        INFL = 0.33
        mr = build_real_revenue(monthly_revenue, annual_inflation=INFL)
        if len(mr) < 2:
            st.info("📊 Building revenue analysis from visits data...")
            mr = build_real_revenue_from_visits(visits_data, annual_inflation=INFL)

        if len(mr) < 2:
            st.warning("Need ≥ 2 months of data to compute CAGR.")
        else:
            fd   = mr["visit_month"].iloc[0]
            ld   = mr["visit_month"].iloc[-1]
            span = max(1, (ld.year - fd.year) * 12 + (ld.month - fd.month))
            cagr_nom  = compute_cagr(mr["total_revenue"].iloc[0], mr["total_revenue"].iloc[-1], span)
            cagr_real = compute_cagr(mr["real_revenue"].iloc[0],  mr["real_revenue"].iloc[-1],  span)
            gap        = cagr_nom - cagr_real
            total_nom  = mr["total_revenue"].sum()
            total_real = mr["real_revenue"].sum()
            total_tax  = mr["inflation_tax"].sum()

            st.markdown(kpi_row([
                kpi_card("Total Revenue (Nominal)", f"{total_nom/1e6:.2f}M EGP", "Actual EGP received",         "neutral", "💵", "#1a73e8"),
                kpi_card("Total Revenue (Real)",    f"{total_real/1e6:.2f}M EGP", "Base-month purchasing power", "neutral", "🏦", "#34a853"),
                kpi_card("Inflation Erosion",       f"{total_tax/1e6:.2f}M EGP", f"Lost to {INFL*100:.0f}%/yr", "down",    "🔥", "#ea4335"),
                kpi_card("Nominal CAGR",            f"{cagr_nom:+.1f}%",          f"Over {span} months",         "up" if cagr_nom > 0 else "neutral", "🚀", "#1a73e8"),
                kpi_card("Real CAGR",               f"{cagr_real:+.1f}%",          "After inflation",             "up" if cagr_real > 0 else "down",   "📉",
                         "#34a853" if cagr_real > 0 else "#ea4335"),
            ], 5), unsafe_allow_html=True)

            note = (f"Nominal CAGR = <b>{cagr_nom:+.1f}%</b> over {span} months. "
                    f"After Egypt's ~{INFL*100:.0f}%/yr inflation, real CAGR = "
                    f"<b>{cagr_real:+.1f}%</b> (gap = {gap:+.1f} pp). "
                    f"Total inflation erosion = <b>{total_tax/1e6:.2f}M EGP</b>.")
            st.markdown(f'<div class="infl-banner">📌 <b>Inflation Note:</b> {note}</div>',
                        unsafe_allow_html=True)

            sec_title("📊 Nominal vs Real Revenue",
                      "Real revenue = what those EGPs are actually worth in base-month purchasing power.")
            fig = go.Figure()
            fig.add_trace(go.Scatter(x=mr["visit_month"], y=mr["total_revenue"],
                name="Nominal Revenue", mode="lines+markers",
                line=dict(color="#1a73e8", width=2.5), marker=dict(size=8)))
            fig.add_trace(go.Scatter(x=mr["visit_month"], y=mr["real_revenue"],
                name="Real Revenue (base-month EGP)", mode="lines+markers",
                line=dict(color="#ea4335", width=2.5, dash="dot"), marker=dict(size=8)))
            fig.add_trace(go.Scatter(
                x=pd.concat([mr["visit_month"], mr["visit_month"][::-1]]),
                y=pd.concat([mr["total_revenue"], mr["real_revenue"][::-1]]),
                fill="toself", fillcolor="rgba(234,67,53,0.08)",
                line=dict(color="rgba(0,0,0,0)"), name="Inflation Erosion", hoverinfo="skip"))
            if "total_profit" in mr.columns:
                fig.add_trace(go.Scatter(x=mr["visit_month"], y=mr["total_profit"],
                    name="Nominal Profit", mode="lines+markers",
                    line=dict(color="#34a853", width=2), marker=dict(size=6)))
            google_theme(fig, height=380)
            fig.update_layout(yaxis_title="EGP")
            st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": False})
            
            c1b, c2b = st.columns(2)
            with c1b:
                sec_title("📈 Month-on-Month Growth")
                mr2 = mr.copy()
                mr2["nom_g"]  = mr2["total_revenue"].pct_change() * 100
                mr2["real_g"] = mr2["real_revenue"].pct_change() * 100
                mr2 = mr2.dropna(subset=["nom_g"])
                fig = go.Figure()
                fig.add_trace(go.Bar(x=mr2["visit_month"], y=mr2["nom_g"], name="Nominal MoM %",
                    marker_color=["#34a853" if v >= 0 else "#ea4335" for v in mr2["nom_g"]]))
                fig.add_trace(go.Scatter(x=mr2["visit_month"], y=mr2["real_g"], name="Real MoM %",
                    mode="lines+markers", line=dict(color="#1a73e8", width=2, dash="dot"), marker=dict(size=6)))
                fig.add_shape(type="line",
                              x0=mr2["visit_month"].min(), x1=mr2["visit_month"].max(), y0=0, y1=0,
                              xref="x", yref="y", line=dict(color="#dadce0", width=1))
                google_theme(fig, height=280)
                fig.update_layout(yaxis_title="Growth (%)")
                st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": False})
                
            with c2b:
                sec_title("💸 Cumulative Inflation Erosion")
                mr["cum_tax"] = mr["inflation_tax"].cumsum()
                fig = go.Figure()
                fig.add_trace(go.Scatter(x=mr["visit_month"], y=mr["cum_tax"] / 1e6,
                    mode="lines+markers", fill="tozeroy",
                    line=dict(color="#ea4335", width=2.5), marker=dict(size=7),
                    fillcolor="rgba(234,67,53,0.15)", name="Cumulative Loss"))
                google_theme(fig, height=280)
                fig.update_layout(yaxis_title="Million EGP")
                st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": False})
                
            sec_title("🏢 Branch-Level CAGR Analysis", "Growth rates by branch, adjusted for inflation")
            branch_cagr_data = []
            for bname in branches_data["branch_name"].unique():
                bv = visits_data[visits_data["branch_name"] == bname]
                bm = bv.groupby("visit_month").size().reset_index(name="visits")
                if len(bm) >= 2:
                    bm = bm.sort_values("visit_month").reset_index(drop=True)
                    sr  = bm.iloc[0]["visits"] * 150
                    er  = bm.iloc[-1]["visits"] * 150
                    mth = len(bm)
                    nc  = compute_cagr(sr, er, mth)
                    branch_cagr_data.append({
                        "Branch": bname, "Nominal CAGR (%)": round(nc, 2),
                        "Inflation Rate (%)": INFL * 100,
                        "Real CAGR (%)": round(nc - INFL * 100, 2), "Months": mth
                    })
            if branch_cagr_data:
                cdf = pd.DataFrame(branch_cagr_data).sort_values("Real CAGR (%)", ascending=False)
                st.dataframe(cdf, hide_index=True, use_container_width=True)
                fig = go.Figure()
                fig.add_trace(go.Bar(x=cdf["Branch"], y=cdf["Nominal CAGR (%)"],
                                     name="Nominal CAGR", marker_color="#1a73e8"))
                fig.add_trace(go.Bar(x=cdf["Branch"], y=cdf["Real CAGR (%)"],
                                     name="Real CAGR (Inflation-Adjusted)", marker_color="#34a853"))
                fig.add_shape(type="line", x0=-0.5, x1=len(cdf) - 0.5, y0=0, y1=0,
                              line=dict(color="#ea4335", width=1, dash="dash"))
                google_theme(fig, height=320)
                fig.update_layout(barmode="group", yaxis_title="CAGR (%)", xaxis_title=None)
                st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": False})
            
    with tab4:
        predictions, std_err = predict_visits(monthly_trends, months_ahead=3)
        historical = monthly_trends[["visit_month", "total_visits"]].copy()

        sec_title("🔮 3-Month Visit Forecast",
                  "Historical visits vs AI-predicted future visits (linear trend + confidence band)")
        fig = go.Figure()
        band_x = predictions["visit_month"].tolist() + predictions["visit_month"].tolist()[::-1]
        band_y = predictions["upper"].tolist() + predictions["lower"].tolist()[::-1]
        fig.add_trace(go.Scatter(x=band_x, y=band_y, fill="toself",
            fillcolor="rgba(52,168,83,0.12)", line=dict(color="rgba(0,0,0,0)"),
            name="Confidence Range", hoverinfo="skip"))
        fig.add_trace(go.Scatter(x=historical["visit_month"], y=historical["total_visits"],
            name="Historical Visits", mode="lines+markers+text",
            line=dict(color="#1a73e8", width=3), marker=dict(size=10, color="#1a73e8"),
            text=[f"{v:,}" for v in historical["total_visits"]],
            textposition="top center", textfont=dict(size=10, color="#1a73e8")))
        fig.add_trace(go.Scatter(x=predictions["visit_month"], y=predictions["predicted_visits"],
            name="Predicted Visits", mode="lines+markers+text",
            line=dict(color="#34a853", width=3, dash="dash"),
            marker=dict(size=12, color="#34a853", symbol="diamond"),
            text=[f"{v:,}" for v in predictions["predicted_visits"]],
            textposition="top center", textfont=dict(size=10, color="#34a853")))
        safe_vline(fig, historical["visit_month"].max())
        google_theme(fig, height=420)
        fig.update_layout(yaxis_title="Number of Visits",
                          xaxis=dict(tickformat="%b %Y", dtick="M1",
                                     showgrid=False, showline=True, linecolor="#dadce0"),
                          hovermode="x unified")
        st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": False})
        
        next_val   = int(predictions.iloc[0]["predicted_visits"])
        last_val   = int(historical.iloc[-1]["total_visits"])
        total_3m   = int(predictions["predicted_visits"].sum())
        avg_growth = (predictions["predicted_visits"].mean() / historical["total_visits"].mean() - 1) * 100
        st.markdown(kpi_row([
            kpi_card("Next Month Forecast", f"{next_val:,}",
                     f"{((next_val/last_val)-1)*100:+.1f}% vs last month",
                     "up" if next_val >= last_val else "down", "📈", "#1a73e8"),
            kpi_card("3-Month Total", f"{total_3m:,}", "predicted visits", "neutral", "📊", "#34a853"),
            kpi_card("Trend vs Avg", f"{avg_growth:+.1f}%", "vs historical avg",
                     "up" if avg_growth > 0 else "down", "📈",
                     "#34a853" if avg_growth > 0 else "#ea4335")
        ], 3), unsafe_allow_html=True)

        pred_display = predictions[["visit_month", "predicted_visits", "lower", "upper"]].copy()
        pred_display["visit_month"] = pred_display["visit_month"].dt.strftime("%B %Y")
        pred_display.columns = ["Month", "Predicted Visits", "Lower Bound", "Upper Bound"]
        st.dataframe(pred_display, hide_index=True, use_container_width=True)
        
        st.info("""
**How to read this forecast:**
- Blue line = actual historical visit data
- Green dashed line = AI-predicted visits for next 3 months
- Green band = confidence range (±1 standard deviation)
- Vertical line = divides past from future
        """)

# ============================================================
# PAGE: EXPORT
# ============================================================

elif page == "Export":
    st.markdown("""<div class="page-header">
<h1>Export Data</h1>
<p>Download analytics data for external use</p>
</div>""", unsafe_allow_html=True)

    table_options = {
        "Patients":            "patients",
        "Doctors":             "doctors",
        "Corporate Contracts": "corporates",
        "Branches":            "branches",
        "High Risk Patients":  "high_risk"
    }
    selected = st.selectbox("Select table to export", list(table_options.keys()))

    if selected == "High Risk Patients":
        export_data = patients_data[patients_data["churn_risk_category"] == "High Risk"]
    else:
        export_data = pd.read_sql(f"SELECT * FROM {table_options[selected]}", conn)

    info_card_start(f"Preview: {selected}")
    st.markdown(f'<p style="color:#5f6368;font-size:.85rem">Total records: {len(export_data):,}</p>',
                unsafe_allow_html=True)
    st.dataframe(export_data.head(10), hide_index=True, use_container_width=True)
    c1, c2 = st.columns(2)
    with c1:
        st.download_button("📊 Download as Excel",
                           export_to_excel(export_data),
                           f"{selected.lower().replace(' ', '_')}.xlsx",
                           use_container_width=True)
    with c2:
        st.download_button("📄 Download as CSV",
                           export_to_csv(export_data),
                           f"{selected.lower().replace(' ', '_')}.csv",
                           use_container_width=True)
    
# ============================================================
# FOOTER
# ============================================================

st.markdown(f"""
<div style="text-align:center;margin-top:3rem;padding:1.5rem 0;
     border-top:1px solid #dadce0;color:#5f6368;font-size:0.8125rem;
     font-family:'Google Sans',sans-serif;line-height:1.8;">
  <div style="font-weight:600;color:#202124;font-size:0.875rem;margin-bottom:4px;">
    Trust Labs Healthcare Analytics &nbsp;·&nbsp; v4.0
  </div>
  <div>Data Analysis for Health Care Systems &nbsp;·&nbsp; <strong>Ahmed Mustafa</strong></div>
  <div style="margin-top:4px;">
    📱 <a href="https://wa.me/201143575727" style="color:#1a73e8;text-decoration:none;">01143575727</a>
    &nbsp;&nbsp;
    📧 <a href="mailto:ahmedsm2727@gmail.com" style="color:#1a73e8;text-decoration:none;">ahmedsm2727@gmail.com</a>
  </div>
  <div style="margin-top:6px;color:#9aa0a6;font-size:0.75rem;">
    Last updated: {datetime.now().strftime("%B %d, %Y at %H:%M")}
  </div>
</div>
""", unsafe_allow_html=True)
