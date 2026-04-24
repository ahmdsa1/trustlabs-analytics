"""
Trust Labs Healthcare Analytics Dashboard
Material Design 3 + Google Analytics 4 Aesthetic
FIXED VERSION - All Issues Resolved
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

st.set_page_config(
    page_title="Trust Labs Analytics",
    page_icon="🏥",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ============================================================
# FULL MATERIAL DESIGN 3 CSS
# ============================================================

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Google+Sans:wght@300;400;500;600;700&family=Google+Sans+Display:wght@400;500;700&family=Roboto:wght@300;400;500;700&display=swap');

/* ── FORCE LIGHT THEME ───────────────────────────────────── */
html, body, [class*="css"], .stApp {
  background: #f8f9fa !important;
  color: #202124 !important;
}
.main .block-container {
  padding: 1.5rem 2rem !important;
  max-width: 1600px !important;
}
.stMarkdown, .stMarkdown *, .stText,
[data-testid="stMarkdownContainer"],
[data-testid="stMarkdownContainer"] *,
[data-testid="stText"], .element-container,
p, span, li, h1, h2, h3, h4, h5, h6 {
  color: #202124 !important;
}

/* ── SIDEBAR COLLAPSE BUTTON — ALWAYS VISIBLE ────────────── */
[data-testid="collapsedControl"],
[data-testid="stSidebarCollapseButton"],
section[data-testid="stSidebarCollapsedControl"],
button[data-testid="baseButton-headerNoPadding"] {
  visibility: visible !important;
  display: flex !important;
  opacity: 1 !important;
}

/* ── SIDEBAR ─────────────────────────────────────────────── */
[data-testid="stSidebar"] {
  background: #ffffff !important;
  border-right: 1px solid #dadce0 !important;
}
[data-testid="stSidebar"] * { color: #202124 !important; }
[data-testid="stSidebar"] .stRadio > div { gap: 2px !important; }
[data-testid="stSidebar"] .stRadio label {
  display: flex !important; align-items: center !important;
  gap: 10px !important; padding: 10px 14px !important;
  border-radius: 8px !important; color: #5f6368 !important;
  font-weight: 500 !important; font-size: 0.875rem !important;
  cursor: pointer !important; transition: background .2s, color .2s !important;
  font-family: 'Google Sans', sans-serif !important;
}
[data-testid="stSidebar"] .stRadio label:hover {
  background: #e8f0fe !important; color: #1a73e8 !important;
}
[data-testid="stSidebar"] .stRadio [data-baseweb="radio"] > div:first-child {
  display: none !important;
}

/* ── TABS ────────────────────────────────────────────────── */
.stTabs [data-baseweb="tab-list"] {
  background: #ffffff !important; border-radius: 16px 16px 0 0 !important;
  padding: 0 16px !important; border-bottom: 1px solid #dadce0 !important;
  gap: 0 !important;
}
.stTabs [data-baseweb="tab"] {
  height: 52px !important;
  font-family: 'Google Sans', sans-serif !important;
  font-weight: 500 !important; font-size: 0.875rem !important;
  color: #5f6368 !important; border-bottom: 3px solid transparent !important;
  padding: 0 20px !important; background: transparent !important;
}
.stTabs [aria-selected="true"] {
  color: #1a73e8 !important; border-bottom-color: #1a73e8 !important;
}
.stTabs [data-baseweb="tab-panel"] {
  background: #ffffff !important; border-radius: 0 0 16px 16px !important;
  padding: 20px !important; border: 1px solid #dadce0 !important;
  border-top: none !important;
}

/* ── INPUTS ───────────────────────────────────────────────── */
.stTextInput label, .stSelectbox label, .stMultiSelect label,
.stNumberInput label, .stRadio label, .stCheckbox label {
  color: #5f6368 !important; font-size: 0.8125rem !important;
  font-weight: 500 !important; font-family: 'Google Sans', sans-serif !important;
}
.stTextInput input, .stTextInput > div > div > input {
  color: #202124 !important; background: #ffffff !important;
  border: 1px solid #dadce0 !important; border-radius: 8px !important;
}
.stSelectbox *, .stMultiSelect * { color: #202124 !important; }
.stSelectbox > div > div, .stMultiSelect > div > div {
  background: #ffffff !important;
}
[data-baseweb="select"] > div,
[data-baseweb="popover"] > div,
[role="listbox"], [role="option"] {
  background: #ffffff !important; color: #202124 !important;
}
[role="option"]:hover { background: #e8f0fe !important; }
[data-baseweb="tag"] { background: #e8f0fe !important; color: #1a73e8 !important; }
.stNumberInput input {
  color: #202124 !important; background: #ffffff !important;
  border: 1px solid #dadce0 !important;
}

/* ── BUTTONS ─────────────────────────────────────────────── */
.stButton > button {
  font-family: 'Google Sans', sans-serif !important; font-weight: 500 !important;
  font-size: 0.875rem !important; background: #1a73e8 !important;
  color: #ffffff !important; border: none !important;
  border-radius: 8px !important; padding: 0.625rem 1.5rem !important;
  box-shadow: 0 1px 3px rgba(60,64,67,.15) !important;
  transition: box-shadow .2s, transform .15s !important;
}
.stButton > button:hover {
  box-shadow: 0 4px 12px rgba(60,64,67,.15) !important;
  transform: translateY(-1px) !important;
}
.stDownloadButton > button {
  background: #ffffff !important; color: #1a73e8 !important;
  border: 1px solid #dadce0 !important; border-radius: 8px !important;
  font-weight: 500 !important; font-family: 'Google Sans', sans-serif !important;
}
.stDownloadButton > button:hover { background: #e8f0fe !important; }

/* ── DATAFRAME ───────────────────────────────────────────── */
[data-testid="stDataFrame"] {
  border-radius: 12px !important; border: 1px solid #dadce0 !important;
  overflow: hidden !important;
}

/* ── HIDE STREAMLIT CHROME ───────────────────────────────── */
#MainMenu, footer { visibility: hidden; }
.stDeployButton { display: none; }
[data-testid="stMetric"] { display: none !important; }

/* ── CUSTOM COMPONENTS ───────────────────────────────────── */
.page-header { margin-bottom: 1.5rem; }
.page-header h1 {
  font-family: 'Google Sans Display', sans-serif !important;
  font-size: 1.75rem !important; font-weight: 500 !important;
  color: #202124 !important; margin: 0 0 4px 0 !important;
}
.page-header p { font-size: 0.875rem; color: #5f6368; margin: 0; }

.kpi-grid { display: grid; gap: 12px; margin-bottom: 1.25rem; }
.kpi-card {
  background: #ffffff; border-radius: 16px; padding: 20px 22px;
  box-shadow: 0 1px 3px rgba(60,64,67,.15),0 1px 2px rgba(60,64,67,.12);
  border: 1px solid #dadce0; position: relative; overflow: hidden;
  transition: box-shadow .2s;
}
.kpi-card:hover { box-shadow: 0 4px 12px rgba(60,64,67,.15); }
.kpi-card::before {
  content: ''; position: absolute; top: 0; left: 0; right: 0; height: 3px;
  background: var(--acc, #1a73e8); border-radius: 16px 16px 0 0;
}
.kpi-label {
  font-size: 0.72rem; font-weight: 600; text-transform: uppercase;
  letter-spacing: 0.8px; color: var(--acc, #1a73e8);
  font-family: 'Google Sans', sans-serif; margin-bottom: 6px;
}
.kpi-value {
  font-size: 1.9rem; font-weight: 500; color: #202124;
  font-family: 'Google Sans Display', sans-serif; line-height: 1.1; margin-bottom: 8px;
}
.kpi-trend {
  display: inline-flex; align-items: center; gap: 4px;
  font-size: 0.72rem; font-weight: 500; padding: 3px 10px;
  border-radius: 100px; font-family: 'Google Sans', sans-serif;
}
.kpi-trend.up     { background: #e6f4ea; color: #137333; }
.kpi-trend.down   { background: #fce8e6; color: #c5221f; }
.kpi-trend.neutral{ background: #fef7e0; color: #b06000; }
.kpi-icon { position: absolute; top: 16px; right: 18px; font-size: 1.75rem; opacity: 0.1; }

/* ── CHART SECTION CARD ─────────────────────────────────── */
.section-title {
  font-family: 'Google Sans', sans-serif !important; font-size: 0.9375rem !important;
  font-weight: 600 !important; color: #202124 !important;
  margin: 0 0 14px 0 !important; display: flex; align-items: center; gap: 8px;
  padding: 18px 20px 0 20px;
  background: #ffffff;
  border-radius: 16px 16px 0 0;
  border: 1px solid #dadce0;
  border-bottom: none;
}
.section-subtitle {
  font-size: 0.8rem; color: #5f6368; margin: -10px 0 14px 0;
  padding: 0 20px 12px 20px;
  background: #ffffff;
  border-left: 1px solid #dadce0;
  border-right: 1px solid #dadce0;
}
.chart-body {
  background: #ffffff;
  border-radius: 0 0 16px 16px;
  border: 1px solid #dadce0;
  border-top: none;
  padding: 0 16px 16px 16px;
  margin-bottom: 12px;
  box-shadow: 0 1px 3px rgba(60,64,67,.15);
}

/* Stand-alone cards (no chart inside — just text/table) */
.info-card {
  background: #ffffff; border-radius: 16px; padding: 20px 22px;
  box-shadow: 0 1px 3px rgba(60,64,67,.15); border: 1px solid #dadce0;
  margin-bottom: 12px;
}
.info-card-title {
  font-family: 'Google Sans', sans-serif; font-size: 0.9375rem;
  font-weight: 600; color: #202124; margin: 0 0 14px 0;
}

.infl-banner {
  background: linear-gradient(90deg,#fef7e0 0%,#e8f0fe 100%);
  border-left: 4px solid #fbbc04; padding: 14px 18px;
  border-radius: 8px; margin-bottom: 16px; font-size: 0.86rem; color: #3c4043;
}
</style>
""", unsafe_allow_html=True)

# ============================================================
# PLOTLY GOOGLE THEME
# ============================================================

def google_theme(fig, height=350):
    fig.update_layout(
        plot_bgcolor="rgba(0,0,0,0)",
        paper_bgcolor="rgba(0,0,0,0)",
        xaxis=dict(showgrid=False, showline=True, linecolor="#dadce0",
                   tickfont=dict(size=11, color="#5f6368", family="Roboto"),
                   title_font=dict(size=11, color="#5f6368", family="Google Sans")),
        yaxis=dict(showgrid=True, gridcolor="#f1f3f4", showline=False,
                   tickfont=dict(size=11, color="#5f6368", family="Roboto"),
                   title_font=dict(size=11, color="#5f6368", family="Google Sans")),
        font=dict(family="Roboto, sans-serif", size=11, color="#202124"),
        margin=dict(t=20, b=30, l=40, r=20),
        height=height,
        hoverlabel=dict(bgcolor="#ffffff", font_size=11,
                       font_family="Roboto", bordercolor="#dadce0"),
        legend=dict(font=dict(size=11, color="#5f6368"),
                   bgcolor="rgba(0,0,0,0)", orientation="h",
                   yanchor="bottom", y=1.02, xanchor="right", x=1)
    )
    return fig

def google_donut(vals, names, colors, hole=0.6):
    fig = px.pie(values=vals, names=names, color=names,
                 color_discrete_map=dict(zip(names, colors)))
    fig.update_traces(hole=hole, textposition="outside",
                      textinfo="percent+label",
                      textfont=dict(size=11, color="#202124"),
                      marker=dict(line=dict(color="#ffffff", width=3)))
    fig.update_layout(height=300, paper_bgcolor="rgba(0,0,0,0)",
                      plot_bgcolor="rgba(0,0,0,0)", showlegend=False,
                      margin=dict(t=10, b=10, l=10, r=10),
                      font=dict(family="Google Sans, sans-serif", size=11, color="#202124"))
    return fig

def safe_vline(fig, x_datetime):
    xs = x_datetime.strftime("%Y-%m-%d")
    fig.add_shape(type="line", x0=xs, x1=xs, y0=0, y1=1,
                  xref="x", yref="paper",
                  line=dict(color="#9aa0a6", width=1.5, dash="solid"))
    fig.add_annotation(x=xs, y=0.97, xref="x", yref="paper",
                       text="Forecast →", showarrow=False, xanchor="left",
                       font=dict(size=10, color="#5f6368"),
                       bgcolor="rgba(255,255,255,0.85)", borderpad=3)

# ============================================================
# CHART SECTION CARD HELPERS
# ============================================================

def sec_title(title, subtitle=""):
    html = f'<div class="section-title">{title}</div>'
    if subtitle:
        html += f'<div class="section-subtitle">{subtitle}</div>'
    st.markdown(html, unsafe_allow_html=True)

def chart_start():
    st.markdown('<div class="chart-body">', unsafe_allow_html=True)

def chart_end():
    st.markdown('</div>', unsafe_allow_html=True)

def info_card_start(title):
    st.markdown(f'<div class="info-card"><div class="info-card-title">{title}</div>', unsafe_allow_html=True)

def info_card_end():
    st.markdown('</div>', unsafe_allow_html=True)

# ============================================================
# KPI CARD HELPERS
# ============================================================

def kpi_card(label, value, trend_text, trend_dir="neutral", icon="📊", accent="#1a73e8"):
    cls   = {"up":"up","down":"down","neutral":"neutral"}.get(trend_dir, "neutral")
    arrow = {"up":"↑","down":"↓","neutral":"→"}.get(trend_dir, "→")
    return f"""
<div class="kpi-card" style="--acc:{accent}">
  <div class="kpi-icon">{icon}</div>
  <div class="kpi-label">{label}</div>
  <div class="kpi-value">{value}</div>
  <span class="kpi-trend {cls}">{arrow}&nbsp;{trend_text}</span>
</div>"""

def kpi_row(cards, cols=5):
    return (f'<div class="kpi-grid" style="grid-template-columns:repeat({cols},1fr)">'
            + "".join(cards) + "</div>")

# ============================================================
# DATABASE CONNECTION
# ============================================================

@st.cache_resource
def get_connection():
    return sqlite3.connect("trust_labs.db", check_same_thread=False)

conn = get_connection()

# ============================================================
# DATA LOADERS
# ============================================================

@st.cache_data(ttl=3600)
def load_patients():
    return pd.read_sql("SELECT * FROM patients", conn)

@st.cache_data(ttl=3600)
def load_visits():
    df = pd.read_sql("SELECT * FROM visits", conn)
    df["visit_date"]  = pd.to_datetime(df["visit_date"],  errors="coerce")
    df["visit_month"] = pd.to_datetime(df["visit_month"], errors="coerce")
    return df

@st.cache_data(ttl=3600)
def load_doctors():
    return pd.read_sql("SELECT * FROM doctors", conn)

@st.cache_data(ttl=3600)
def load_corporates():
    return pd.read_sql("SELECT * FROM corporates", conn)

@st.cache_data(ttl=3600)
def load_branches():
    return pd.read_sql("SELECT * FROM branches", conn)

@st.cache_data(ttl=3600)
def load_monthly_trends():
    df = pd.read_sql("SELECT * FROM monthly_trends", conn)
    df["visit_month"] = pd.to_datetime(df["visit_month"], errors="coerce")
    return df

@st.cache_data(ttl=3600)
def load_monthly_revenue():
    df = pd.read_sql("SELECT * FROM monthly_revenue", conn)
    df["visit_month"] = pd.to_datetime(df["visit_month"], errors="coerce")
    return df

@st.cache_data(ttl=3600)
def load_revenue_by_test():
    return pd.read_sql(
        "SELECT * FROM revenue_by_test ORDER BY total_revenue DESC LIMIT 20", conn)

@st.cache_data(ttl=3600)
def load_hourly_patterns():
    try:
        return pd.read_sql("SELECT * FROM hourly_patterns", conn)
    except Exception:
        return pd.DataFrame()

@st.cache_data(ttl=3600)
def load_dow_patterns():
    try:
        return pd.read_sql("SELECT * FROM dow_patterns", conn)
    except Exception:
        return pd.DataFrame()

@st.cache_data(ttl=3600)
def load_daily_stats():
    try:
        df = pd.read_sql("SELECT * FROM daily_stats", conn)
        df["visit_date"] = pd.to_datetime(df["visit_date"], errors="coerce")
        return df
    except Exception:
        return pd.DataFrame()

@st.cache_data(ttl=3600)
def load_branch_comparison():
    try:
        return pd.read_sql("SELECT * FROM branch_comparison", conn)
    except Exception:
        return pd.DataFrame()

@st.cache_data(ttl=3600)
def load_doctor_branch():
    try:
        return pd.read_sql("SELECT * FROM doctor_branch", conn)
    except Exception:
        return pd.DataFrame()

# ============================================================
# SEARCH HELPERS
# ============================================================

def search_patient_by_id(pid):
    q = f"SELECT * FROM patients WHERE LOWER(patient_id)=LOWER('{pid}')"
    r = pd.read_sql(q, conn)
    return r if not r.empty else None

def search_doctor_by_id(did):
    q = f"SELECT * FROM doctors WHERE LOWER(doctor_id)=LOWER('{did}')"
    r = pd.read_sql(q, conn)
    return r if not r.empty else None

def search_corporate_by_id(cid):
    q = f"SELECT * FROM corporates WHERE LOWER(corporate_id)=LOWER('{cid}')"
    r = pd.read_sql(q, conn)
    return r if not r.empty else None

def get_patient_visits(pid):
    q = f"""SELECT visit_date, branch_name, visit_time, visit_day_name
            FROM visits WHERE LOWER(patient_id)=LOWER('{pid}')
            ORDER BY visit_date DESC"""
    df = pd.read_sql(q, conn)
    df["visit_date"] = pd.to_datetime(df["visit_date"], errors="coerce")
    return df

# ============================================================
# EXPORT HELPERS
# ============================================================

def export_to_excel(df):
    out = io.BytesIO()
    with pd.ExcelWriter(out, engine="openpyxl") as w:
        df.to_excel(w, index=False)
    return out.getvalue()

def export_to_csv(df):
    return df.to_csv(index=False).encode("utf-8")

# ============================================================
# ANALYTICS HELPERS
# ============================================================

def predict_visits(monthly_trends_df, months_ahead=3):
    df = monthly_trends_df.copy().sort_values("visit_month").reset_index(drop=True)
    df["month_num"] = range(len(df))
    X = df[["month_num"]].values
    y = df["total_visits"].values
    model = LinearRegression()
    model.fit(X, y)
    # Compute residuals std for confidence band
    residuals = y - model.predict(X)
    std_err = np.std(residuals)
    last_num = df["month_num"].max()
    future_nums = np.array([[last_num + i] for i in range(1, months_ahead + 1)])
    preds = model.predict(future_nums).astype(int)
    last_date = df["visit_month"].max()
    future_dates = [last_date + timedelta(days=30*i) for i in range(1, months_ahead + 1)]
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
        years = months / 12.0
        return ((final / initial) ** (1.0 / years) - 1.0) * 100.0
    except Exception:
        return 0.0

def build_real_revenue_from_visits(visits_df, annual_inflation=0.33):
    avg_revenue_per_visit = 150
    monthly = visits_df.groupby("visit_month").agg({"visit_date": "count"}).reset_index()
    monthly.columns = ["visit_month", "total_visits"]
    monthly = monthly.sort_values("visit_month").reset_index(drop=True)
    monthly["total_revenue"] = monthly["total_visits"] * avg_revenue_per_visit
    monthly["total_profit"]  = monthly["total_revenue"] * 0.65
    if monthly.empty or len(monthly) < 2:
        return pd.DataFrame()
    n = len(monthly)
    deflators = [(1 + annual_inflation) ** (i / 12.0) for i in range(n)]
    monthly["deflator"]      = deflators
    monthly["real_revenue"]  = monthly["total_revenue"] / monthly["deflator"]
    monthly["real_profit"]   = monthly["total_profit"]  / monthly["deflator"]
    monthly["inflation_tax"] = monthly["total_revenue"] - monthly["real_revenue"]
    rv0 = monthly["real_revenue"].iloc[0]
    nv0 = monthly["total_revenue"].iloc[0]
    monthly["real_index"]    = monthly["real_revenue"]  / rv0 * 100
    monthly["nominal_index"] = monthly["total_revenue"] / nv0 * 100
    monthly["month_label"]   = monthly["visit_month"].dt.strftime("%b %Y")
    return monthly

def build_real_revenue(mr_df, annual_inflation=0.33):
    df = (mr_df.sort_values("visit_month").dropna(subset=["total_revenue"])
          .copy().reset_index(drop=True))
    if df.empty or len(df) < 2:
        return df
    n = len(df)
    deflators           = [(1 + annual_inflation) ** (i / 12.0) for i in range(n)]
    df["deflator"]      = deflators
    df["real_revenue"]  = df["total_revenue"] / df["deflator"]
    if "total_profit" in df.columns:
        df["real_profit"] = df["total_profit"] / df["deflator"]
    df["inflation_tax"] = df["total_revenue"] - df["real_revenue"]
    rv0 = df["real_revenue"].iloc[0]
    nv0 = df["total_revenue"].iloc[0]
    df["real_index"]    = df["real_revenue"]  / rv0 * 100
    df["nominal_index"] = df["total_revenue"] / nv0 * 100
    df["month_label"]   = df["visit_month"].dt.strftime("%b %Y")
    return df

# ============================================================
# LOAD EVERYTHING
# ============================================================

patients_data   = load_patients()
visits_data     = load_visits()
doctors_data    = load_doctors()
corporates_data = load_corporates()
branches_data   = load_branches()
monthly_trends  = load_monthly_trends()
monthly_revenue = load_monthly_revenue()
hourly_data     = load_hourly_patterns()
dow_data        = load_dow_patterns()
daily_data      = load_daily_stats()
branch_comp     = load_branch_comparison()
doctor_branch   = load_doctor_branch()
high_risk_count = int((patients_data["churn_risk_category"] == "High Risk").sum())
active_docs     = int((doctors_data["actual_referrals"] > 0).sum())
active_corps    = int((corporates_data["actual_visits"] > 0).sum())

# ============================================================
# SIDEBAR
# ============================================================

with st.sidebar:
    st.markdown("""
<div style="padding:12px 6px 20px 6px">
  <div style="display:flex;align-items:center;gap:10px">
    <span style="font-size:1.6rem">🏥</span>
    <div>
      <div style="font-family:'Google Sans Display',sans-serif;font-size:1rem;
                  font-weight:700;color:#202124;line-height:1.2">Trust Labs</div>
      <div style="font-size:.7rem;color:#5f6368">Healthcare Analytics</div>
    </div>
  </div>
</div>""", unsafe_allow_html=True)

    st.markdown('<hr style="margin:0 0 12px;border:none;border-top:1px solid #dadce0">',
                unsafe_allow_html=True)

    page = st.radio("nav",
        ["🏠  Home","🌅  Branch View","🔍  Patient Search",
         "👨‍⚕️  Doctor Search","🏢  Corporate Search",
         "📊  Analytics","📥  Export"],
        label_visibility="collapsed")

    st.markdown('<hr style="margin:12px 0;border:none;border-top:1px solid #dadce0">',
                unsafe_allow_html=True)
    st.markdown("""<div style="font-size:.7rem;font-weight:600;text-transform:uppercase;
letter-spacing:.8px;color:#5f6368;margin-bottom:10px;font-family:'Google Sans',sans-serif"
>Quick Stats</div>""", unsafe_allow_html=True)

    st.markdown(kpi_row([
        kpi_card("Patients",f"{len(patients_data):,}","","neutral","👥","#1a73e8"),
        kpi_card("Visits",f"{len(visits_data):,}","","neutral","📊","#34a853")
    ],2), unsafe_allow_html=True)
    st.markdown(kpi_row([
        kpi_card("Doctors",f"{active_docs}","","neutral","👨‍⚕️","#fbbc04"),
        kpi_card("At Risk",f"{high_risk_count}","","down","⚠️","#ea4335")
    ],2), unsafe_allow_html=True)

    st.markdown('<hr style="margin:12px 0;border:none;border-top:1px solid #dadce0">',
                unsafe_allow_html=True)
    st.markdown(f"""<div style="text-align:center;font-size:0.7rem;color:#9aa0a6">
Updated {datetime.now().strftime("%b %d, %Y • %H:%M")}</div>""",
                unsafe_allow_html=True)

# ============================================================
# PAGE: HOME
# ============================================================

if page == "🏠  Home":
    st.markdown("""<div class="page-header">
<h1>Analytics Dashboard</h1>
<p>Professional healthcare intelligence platform</p>
</div>""", unsafe_allow_html=True)

    avg_visits  = len(visits_data) / len(patients_data)
    avg_loyalty = patients_data["loyalty_points"].mean()
    high_risk_pct = high_risk_count / len(patients_data) * 100

    st.markdown(kpi_row([
        kpi_card("Total Patients", f"{len(patients_data):,}", "+5.2%", "up", "👥", "#1a73e8"),
        kpi_card("Total Visits", f"{len(visits_data):,}", "+8.1%", "up", "📊", "#34a853"),
        kpi_card("Avg Visits/Patient", f"{avg_visits:.1f}", "+0.3", "up", "📈", "#fbbc04"),
        kpi_card("High Risk %", f"{high_risk_pct:.1f}%", "-2.1%", "down", "⚠️", "#ea4335"),
        kpi_card("Avg Loyalty", f"{avg_loyalty:.0f}", "+3.5", "up", "🏆", "#9334e6")
    ], 5), unsafe_allow_html=True)

    c1, c2 = st.columns(2)
    with c1:
        sec_title("👥 Gender Distribution")
        chart_start()
        gender_counts = patients_data["gender"].value_counts()
        fig = google_donut(gender_counts.values, gender_counts.index, ["#1a73e8", "#ea4335"])
        st.plotly_chart(fig, width='stretch', config={"displayModeBar": False})
        chart_end()

    with c2:
        sec_title("⚠️ Churn Risk Levels")
        chart_start()
        risk_counts = patients_data["churn_risk_category"].value_counts()
        fig = google_donut(risk_counts.values, risk_counts.index,
                          ["#34a853", "#fbbc04", "#ea4335"])
        st.plotly_chart(fig, width='stretch', config={"displayModeBar": False})
        chart_end()

    sec_title("📈 Monthly Visit Trends")
    chart_start()
    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=monthly_trends["visit_month"], y=monthly_trends["total_visits"],
        mode="lines+markers", name="Total Visits",
        line=dict(color="#1a73e8", width=3), marker=dict(size=10)
    ))
    google_theme(fig, height=320)
    st.plotly_chart(fig, width='stretch', config={"displayModeBar": False})
    chart_end()

    st.markdown(kpi_row([
        kpi_card("Gold Tier", f"{len(patients_data[patients_data['patient_tier']=='Gold']):,}",
                f"{len(patients_data[patients_data['patient_tier']=='Gold'])/len(patients_data)*100:.1f}%",
                "neutral", "🥇", "#fbbc04"),
        kpi_card("Active Doctors", f"{active_docs}/{len(doctors_data)}", "active", "up", "👨‍⚕️", "#34a853"),
        kpi_card("Active Contracts", f"{active_corps}/{len(corporates_data)}", "active", "up", "🏢", "#1a73e8"),
        kpi_card("Top Branch", branches_data.nlargest(1, "total_visits")["branch_name"].values[0],
                "Leading", "neutral", "🏆", "#9334e6")
    ], 4), unsafe_allow_html=True)

# ============================================================
# PAGE: BRANCH VIEW  ← Manager's daily operational dashboard
# ============================================================

elif page == "🌅  Branch View":
    st.markdown("""<div class="page-header">
<h1>🌅 Branch Manager View</h1>
<p>Daily operations · Patient flow · Branch comparison · Doctor activity</p>
</div>""", unsafe_allow_html=True)

    # ── Branch selector ──────────────────────────────────────────────────────
    all_branches = sorted(visits_data["branch_name"].dropna().unique().tolist())
    sel_branch   = st.selectbox("Select your branch", all_branches, key="bv_branch")

    has_hourly  = not hourly_data.empty
    has_dow     = not dow_data.empty
    has_daily   = not daily_data.empty
    has_bcomp   = not branch_comp.empty
    has_db      = not doctor_branch.empty

    # ── Use latest date in data as "today" ──────────────────────────────────
    ref_date = visits_data["visit_date"].max()
    ref_label= ref_date.strftime("%A, %d %b %Y") if pd.notna(ref_date) else "Latest date"

    st.markdown(f'<p style="color:#5f6368;font-size:.85rem">📅 Reference date: <b>{ref_label}</b> '
                f'(latest date in dataset — used as "today")</p>', unsafe_allow_html=True)

    tab1, tab2, tab3, tab4 = st.tabs([
        "📋 Today at a Glance",
        "⏰ When Do Patients Come?",
        "🆚 Branch Comparison",
        "👨‍⚕️ Doctor Activity"
    ])

    # ── TAB 1: TODAY AT A GLANCE ─────────────────────────────────────────────
    with tab1:
        if has_daily:
            branch_daily = daily_data[daily_data["branch_name"] == sel_branch].copy()
            branch_daily = branch_daily.sort_values("visit_date")

            # Today and last week same day
            today_row = branch_daily[branch_daily["visit_date"] == ref_date]
            last_wk   = ref_date - timedelta(days=7)
            lastw_row = branch_daily[branch_daily["visit_date"] == last_wk]
            avg_30d   = branch_daily.tail(30)["total_visits"].mean()

            today_v = int(today_row["total_visits"].values[0])   if not today_row.empty else 0
            lastw_v = int(lastw_row["total_visits"].values[0])   if not lastw_row.empty else None
            today_new = int(today_row["new_patients"].values[0]) if not today_row.empty and "new_patients" in today_row.columns else 0
            today_ret = int(today_row["return_patients"].values[0]) if not today_row.empty and "return_patients" in today_row.columns else 0
            today_ref = int(today_row["referral_visits"].values[0]) if not today_row.empty and "referral_visits" in today_row.columns else 0
            today_wlk = int(today_row["walkin_visits"].values[0])   if not today_row.empty and "walkin_visits"  in today_row.columns else 0

            delta_wk  = f"{((today_v/lastw_v)-1)*100:+.0f}% vs last week" if lastw_v and lastw_v > 0 else "—"
            delta_avg = f"{((today_v/avg_30d)-1)*100:+.0f}% vs 30-day avg" if avg_30d > 0 else "—"

            st.markdown(kpi_row([
                kpi_card("Today's Visits",   f"{today_v}",     delta_wk,  "up" if lastw_v and today_v >= lastw_v else "down", "📊", "#1a73e8"),
                kpi_card("vs 30-day Avg",    f"{avg_30d:.0f}", delta_avg, "up" if today_v >= avg_30d else "down",             "📈", "#34a853"),
                kpi_card("New Patients",      f"{today_new}",  "today",   "up",     "🆕", "#fbbc04"),
                kpi_card("Returning Patients",f"{today_ret}",  "today",   "up",     "🔁", "#9334e6"),
                kpi_card("Walk-ins Today",    f"{today_wlk}",  f"Referrals: {today_ref}", "neutral", "🚶", "#ea4335"),
            ], 5), unsafe_allow_html=True)

            # ── Last 30 days trend for this branch ──
            sec_title("📈 Last 30 Days — Daily Visits", f"{sel_branch}")
            chart_start()
            tail30 = branch_daily.tail(30)
            fig = go.Figure()
            # 7-day rolling average
            tail30 = tail30.copy()
            tail30["rolling7"] = tail30["total_visits"].rolling(7, min_periods=1).mean()
            fig.add_trace(go.Bar(
                x=tail30["visit_date"], y=tail30["total_visits"],
                name="Daily Visits", marker_color="#c5ddf8"
            ))
            fig.add_trace(go.Scatter(
                x=tail30["visit_date"], y=tail30["rolling7"],
                name="7-Day Avg", mode="lines",
                line=dict(color="#1a73e8", width=2.5)
            ))
            # Mark today — use safe_vline to avoid Plotly int+str TypeError
            if not today_row.empty and pd.notna(ref_date):
                safe_vline(fig, ref_date)
            google_theme(fig, height=320)
            fig.update_layout(xaxis_title=None, yaxis_title="Visits", barmode="overlay")
            st.plotly_chart(fig, width='stretch', config={"displayModeBar": False})
            chart_end()

            # ── New vs Returning trend ──
            if "new_patients" in branch_daily.columns and "return_patients" in branch_daily.columns:
                sec_title("🆕 New vs Returning Patients — Last 30 Days")
                chart_start()
                fig = go.Figure()
                fig.add_trace(go.Scatter(
                    x=tail30["visit_date"], y=tail30["new_patients"],
                    name="New", mode="lines+markers",
                    line=dict(color="#34a853", width=2), marker=dict(size=6)
                ))
                fig.add_trace(go.Scatter(
                    x=tail30["visit_date"], y=tail30["return_patients"],
                    name="Returning", mode="lines+markers",
                    line=dict(color="#1a73e8", width=2), marker=dict(size=6)
                ))
                google_theme(fig, height=260)
                fig.update_layout(yaxis_title="Patients")
                st.plotly_chart(fig, width='stretch', config={"displayModeBar": False})
                chart_end()
        else:
            st.info("⚠️ Daily stats table not found. Re-run trust_labs_complete_analysis.R "
                    "then export_to_sqlite.R to generate it.")

    # ── TAB 2: WHEN DO PATIENTS COME? ───────────────────────────────────────
    with tab2:
        col_a, col_b = st.columns(2)

        # Hour of day chart
        with col_a:
            if has_hourly:
                bh = hourly_data[hourly_data["branch_name"] == sel_branch].copy()
                if not bh.empty:
                    bh = bh.sort_values("visit_hour")
                    bh["color"] = bh["visit_hour"].apply(
                        lambda h: "#1a73e8" if h in [9,10,11,14,15,16] else "#c5ddf8"
                    )
                    sec_title("⏰ Visits by Hour of Day",
                              "Blue bars = peak hours (9–11am, 2–4pm)")
                    chart_start()
                    fig = go.Figure(go.Bar(
                        x=bh["visit_hour"],
                        y=bh["avg_visits_per_day"],
                        marker_color=bh["color"],
                        text=bh["avg_visits_per_day"].round(1),
                        textposition="outside"
                    ))
                    google_theme(fig, height=320)
                    fig.update_layout(
                        xaxis=dict(tickmode="linear", dtick=1,
                                   title="Hour of Day (0–23)"),
                        yaxis_title="Avg Visits / Day",
                        showlegend=False
                    )
                    st.plotly_chart(fig, width='stretch', config={"displayModeBar": False})
                    chart_end()

                    # staffing advice
                    if not bh.empty:
                        peak = bh.nlargest(1,"avg_visits_per_day")
                        peak_h = int(peak["visit_hour"].values[0])
                        peak_v = float(peak["avg_visits_per_day"].values[0])
                        st.info(f"💡 **Staffing tip:** Busiest hour is **{peak_h:02d}:00** "
                                f"({peak_v:.1f} avg visits). Ensure full staff coverage "
                                f"from {peak_h-1:02d}:00–{peak_h+2:02d}:00.")
                else:
                    st.info("No hourly data for this branch.")
            else:
                st.info("⚠️ Hourly patterns table not found. Re-run the R scripts.")

        # Day of week chart
        with col_b:
            if has_dow:
                bd = dow_data[dow_data["branch_name"] == sel_branch].copy()
                if not bd.empty and "visit_dow_num" in bd.columns:
                    bd = bd.sort_values("visit_dow_num")
                    sec_title("📅 Visits by Day of Week",
                              "Plan staffing around your busiest days")
                    chart_start()
                    fig = px.bar(
                        bd, x="visit_day_name", y="avg_visits_per_week",
                        color="avg_visits_per_week",
                        color_continuous_scale=["#c5ddf8", "#1a73e8"],
                        text=bd["avg_visits_per_week"].round(1)
                    )
                    fig.update_traces(textposition="outside")
                    google_theme(fig, height=320)
                    fig.update_layout(
                        xaxis_title=None, yaxis_title="Avg Visits / Week",
                        showlegend=False, coloraxis_showscale=False
                    )
                    st.plotly_chart(fig, width='stretch', config={"displayModeBar": False})
                    chart_end()

                    busiest = bd.nlargest(1,"avg_visits_per_week")["visit_day_name"].values[0]
                    quietest= bd.nsmallest(1,"avg_visits_per_week")["visit_day_name"].values[0]
                    st.info(f"💡 **Busiest day:** {busiest} — consider booking slots in advance.  \n"
                            f"**Quietest day:** {quietest} — ideal for equipment maintenance, staff training.")
                else:
                    st.info("No day-of-week data for this branch.")
            else:
                st.info("⚠️ Day-of-week patterns table not found. Re-run the R scripts.")

        # Walk-in vs Referral breakdown
        if has_daily:
            bd2 = daily_data[daily_data["branch_name"] == sel_branch].copy()
            if "referral_visits" in bd2.columns and "walkin_visits" in bd2.columns:
                sec_title("🚶 Walk-in vs Referral — Monthly Trend",
                          "Understanding your patient acquisition mix")
                chart_start()
                bd2_m = bd2.copy()
                bd2_m["month"] = pd.to_datetime(bd2_m["visit_date"]).dt.to_period("M").astype(str)
                mly = bd2_m.groupby("month")[["referral_visits","walkin_visits"]].sum().reset_index()
                mly["total"] = mly["referral_visits"] + mly["walkin_visits"]
                mly["ref_pct"] = (mly["referral_visits"] / mly["total"] * 100).round(1)
                fig = go.Figure()
                fig.add_trace(go.Bar(x=mly["month"], y=mly["walkin_visits"],
                                     name="Walk-in", marker_color="#c5ddf8"))
                fig.add_trace(go.Bar(x=mly["month"], y=mly["referral_visits"],
                                     name="Referral", marker_color="#1a73e8"))
                google_theme(fig, height=280)
                fig.update_layout(barmode="stack", xaxis_title=None, yaxis_title="Visits")
                st.plotly_chart(fig, width='stretch', config={"displayModeBar": False})
                chart_end()

    # ── TAB 3: BRANCH COMPARISON ─────────────────────────────────────────────
    with tab3:
        if has_bcomp:
            # Highlight the selected branch
            bc = branch_comp.copy()
            bc["is_mine"] = bc["branch_name"] == sel_branch

            # KPIs for MY branch vs network avg
            mine = bc[bc["branch_name"] == sel_branch]
            if not mine.empty:
                net_avg_daily = bc["avg_daily_visits"].mean()
                net_avg_ref   = bc["referral_rate"].mean()   if "referral_rate" in bc.columns else 0
                net_avg_ret   = bc["return_rate"].mean()     if "return_rate"   in bc.columns else 0
                my_daily = float(mine["avg_daily_visits"].values[0])
                my_ref   = float(mine["referral_rate"].values[0])   if "referral_rate" in mine.columns else 0
                my_ret   = float(mine["return_rate"].values[0])     if "return_rate"   in mine.columns else 0
                my_rank  = int(bc["avg_daily_visits"].rank(ascending=False)[bc["branch_name"]==sel_branch].values[0])

                st.markdown(kpi_row([
                    kpi_card("My Avg Daily Visits", f"{my_daily:.0f}",
                             f"Network avg: {net_avg_daily:.0f}",
                             "up" if my_daily >= net_avg_daily else "down", "📊", "#1a73e8"),
                    kpi_card("My Referral Rate", f"{my_ref:.1f}%",
                             f"Network avg: {net_avg_ref:.1f}%",
                             "up" if my_ref >= net_avg_ref else "down", "👨‍⚕️", "#34a853"),
                    kpi_card("My Return Rate", f"{my_ret:.1f}%",
                             f"Network avg: {net_avg_ret:.1f}%",
                             "up" if my_ret >= net_avg_ret else "down", "🔁", "#fbbc04"),
                    kpi_card("My Network Rank", f"#{my_rank}",
                             f"of {len(bc)} branches",
                             "up" if my_rank <= len(bc)//2 else "down", "🏆", "#9334e6"),
                ], 4), unsafe_allow_html=True)

            # Bar: Avg daily visits — all branches, mine highlighted
            sec_title("📊 Avg Daily Visits — All Branches",
                      f"Your branch ({sel_branch}) highlighted in blue")
            chart_start()
            bc_s = bc.sort_values("avg_daily_visits", ascending=True)
            bc_s["color"] = bc_s["branch_name"].apply(
                lambda b: "#1a73e8" if b == sel_branch else "#dadce0"
            )
            fig = go.Figure(go.Bar(
                x=bc_s["avg_daily_visits"], y=bc_s["branch_name"],
                orientation="h", marker_color=bc_s["color"],
                text=bc_s["avg_daily_visits"].round(1),
                textposition="outside"
            ))
            google_theme(fig, height=max(300, len(bc_s)*32))
            fig.update_layout(xaxis_title="Avg Daily Visits", yaxis_title=None)
            st.plotly_chart(fig, width='stretch', config={"displayModeBar": False})
            chart_end()

            # Head-to-head comparison — pick any branch to compare
            st.markdown("---")
            sec_title("🆚 Head-to-Head Comparison",
                      "Compare your branch against any other branch in the network")
            chart_start()
            other_branches = [b for b in all_branches if b != sel_branch]
            comp_branch = st.selectbox("Compare against", other_branches, key="bv_comp")

            comp_metrics = ["avg_daily_visits","referral_rate","return_rate",
                            "new_patient_rate","peak_utilization","weekend_rate"]
            comp_labels  = ["Avg Daily Visits","Referral Rate %","Return Rate %",
                            "New Patient Rate %","Peak Hour Util %","Weekend Rate %"]

            mine_row  = bc[bc["branch_name"] == sel_branch].iloc[0]   if not bc[bc["branch_name"]==sel_branch].empty   else None
            other_row = bc[bc["branch_name"] == comp_branch].iloc[0]  if not bc[bc["branch_name"]==comp_branch].empty  else None

            if mine_row is not None and other_row is not None:
                avail = [(m, l) for m, l in zip(comp_metrics, comp_labels) if m in bc.columns]
                if avail:
                    avail_m, avail_l = zip(*avail)
                    mine_vals  = [float(mine_row[m])  for m in avail_m]
                    other_vals = [float(other_row[m]) for m in avail_m]

                    fig = go.Figure()
                    fig.add_trace(go.Bar(name=sel_branch,  x=list(avail_l), y=mine_vals,
                                         marker_color="#1a73e8", text=[f"{v:.1f}" for v in mine_vals],
                                         textposition="outside"))
                    fig.add_trace(go.Bar(name=comp_branch, x=list(avail_l), y=other_vals,
                                         marker_color="#dadce0", text=[f"{v:.1f}" for v in other_vals],
                                         textposition="outside"))
                    google_theme(fig, height=340)
                    fig.update_layout(barmode="group", xaxis_title=None, yaxis_title="Value")
                    st.plotly_chart(fig, width='stretch', config={"displayModeBar": False})

                    # Insight: where you're losing
                    gaps = [(l, mv, ov) for l, mv, ov in zip(avail_l, mine_vals, other_vals) if ov > mv]
                    if gaps:
                        worst = sorted(gaps, key=lambda x: x[2]-x[1], reverse=True)[0]
                        st.warning(f"📌 **Biggest gap:** {worst[0]} — you have {worst[1]:.1f}, "
                                   f"{comp_branch} has {worst[2]:.1f}. This is your priority to close.")
            chart_end()

            # Full network table
            info_card_start("📋 Full Network Comparison Table")
            display_bc = bc.drop(columns=["is_mine"], errors="ignore")
            st.dataframe(display_bc.sort_values("avg_daily_visits", ascending=False),
                        hide_index=True, width='stretch')
            st.download_button("📊 Export Table", export_to_excel(display_bc),
                               "branch_comparison.xlsx")
            info_card_end()
        else:
            st.info("⚠️ Branch comparison table not found. Re-run the R scripts.")

    # ── TAB 4: DOCTOR ACTIVITY ───────────────────────────────────────────────
    with tab4:
        if has_db:
            bdr = doctor_branch[doctor_branch["branch_name"] == sel_branch].copy()

            if not bdr.empty:
                # Top KPIs
                total_ref   = int(bdr["referrals"].sum())
                active_docs_b = int((bdr["days_since_last"] <= 30).sum()) if "days_since_last" in bdr.columns else len(bdr)
                at_risk_docs  = int(((bdr["days_since_last"] > 30) & (bdr["days_since_last"] <= 90)).sum()) if "days_since_last" in bdr.columns else 0
                lost_docs     = int((bdr["days_since_last"] > 90).sum()) if "days_since_last" in bdr.columns else 0

                st.markdown(kpi_row([
                    kpi_card("Total Referrals",      f"{total_ref:,}",     "to this branch", "up",      "📊","#1a73e8"),
                    kpi_card("Active Doctors",        f"{active_docs_b}",   "sent in 30d",    "up",      "🟢","#34a853"),
                    kpi_card("At-Risk Doctors",       f"{at_risk_docs}",    "31–90 days ago", "neutral", "🟡","#fbbc04"),
                    kpi_card("Lost Doctors",          f"{lost_docs}",       ">90 days ago",   "down",    "🔴","#ea4335"),
                ], 4), unsafe_allow_html=True)

                # Top 15 doctors for this branch
                sec_title("🏆 Top Referring Doctors", f"Ranked by referrals sent to {sel_branch}")
                chart_start()
                top_docs = bdr.nlargest(15, "referrals")
                if "doctor_name" in top_docs.columns:
                    top_docs["label"] = top_docs["doctor_name"].fillna(top_docs["referring_doctor_id"])
                else:
                    top_docs["label"] = top_docs["referring_doctor_id"]

                # Color by recency
                def doc_color(days):
                    if pd.isna(days): return "#dadce0"
                    if days <= 30:  return "#34a853"
                    if days <= 90:  return "#fbbc04"
                    return "#ea4335"

                top_docs["color"] = top_docs["days_since_last"].apply(doc_color) if "days_since_last" in top_docs.columns else "#1a73e8"

                fig = go.Figure(go.Bar(
                    x=top_docs["referrals"],
                    y=top_docs["label"],
                    orientation="h",
                    marker_color=top_docs["color"],
                    text=top_docs["referrals"],
                    textposition="outside"
                ))
                google_theme(fig, height=400)
                fig.update_layout(
                    xaxis_title="Referrals", yaxis_title=None,
                    yaxis=dict(autorange="reversed")
                )
                st.plotly_chart(fig, width='stretch', config={"displayModeBar": False})
                st.markdown("🟢 Active (≤30 days)&nbsp;&nbsp;"
                            "🟡 At Risk (31–90 days)&nbsp;&nbsp;"
                            "🔴 Lost (>90 days)", unsafe_allow_html=False)
                chart_end()

                # At-risk action list
                if "days_since_last" in bdr.columns:
                    at_risk_list = bdr[(bdr["days_since_last"] > 30) & (bdr["days_since_last"] <= 90)].copy()
                    if not at_risk_list.empty:
                        info_card_start("🟡 At-Risk Doctors — Call This Week")
                        if "doctor_name" in at_risk_list.columns:
                            at_risk_list["Name"] = at_risk_list["doctor_name"].fillna(at_risk_list["referring_doctor_id"])
                        else:
                            at_risk_list["Name"] = at_risk_list["referring_doctor_id"]
                        disp = at_risk_list[["Name","referrals","days_since_last","last_referral"]].copy()
                        disp.columns = ["Doctor", "Total Referrals", "Days Since Last", "Last Referral"]
                        disp = disp.sort_values("Days Since Last")
                        st.dataframe(disp, hide_index=True, width='stretch')
                        st.download_button("📞 Export Call List",
                                          export_to_excel(disp), "at_risk_doctors.xlsx")
                        info_card_end()

                    # Full doctor table
                    info_card_start("📋 All Doctors for This Branch")
                    full_disp = bdr.sort_values("referrals", ascending=False)
                    st.dataframe(full_disp, hide_index=True, width='stretch', height=350)
                    st.download_button("📊 Export Full List",
                                      export_to_excel(full_disp), "branch_doctors.xlsx")
                    info_card_end()
            else:
                st.info(f"No doctor referral data found for {sel_branch}.")
        else:
            st.info("⚠️ Doctor-branch table not found. Re-run the R scripts.")

# ============================================================
# PAGE: PATIENT SEARCH
# ============================================================

elif page == "🔍  Patient Search":
    st.markdown("""<div class="page-header">
<h1>Patient Search</h1>
<p>Search and analyze patient records</p>
</div>""", unsafe_allow_html=True)

    tab1, tab2 = st.tabs(["🆔 ID Lookup", "🔎 Advanced Search"])

    with tab1:
        c1, c2 = st.columns([3, 1])
        with c1:
            patient_id = st.text_input("Patient ID", placeholder="e.g., P0000000001")
        with c2:
            st.markdown("<br>", unsafe_allow_html=True)
            search_btn = st.button("🔍 Search", type="primary", width='stretch')

        if search_btn and patient_id:
            patient = search_patient_by_id(patient_id)
            if patient is None:
                st.error(f"❌ Patient ID '{patient_id}' not found!")
            else:
                st.success(f"✅ Patient Found: **{patient_id.upper()}**")

                tier    = patient["patient_tier"].values[0]
                loyalty = int(patient["loyalty_points"].values[0])
                risk    = int(patient["churn_risk_score"].values[0])
                visits  = int(patient["total_visits"].values[0])
                days    = int(patient["days_since_last_visit"].values[0])

                st.markdown(kpi_row([
                    kpi_card("Tier", tier, "", "neutral", "🏆", "#1a73e8"),
                    kpi_card("Loyalty", str(loyalty), "points", "up", "⭐", "#fbbc04"),
                    kpi_card("Risk Score", str(risk),
                            "Low" if risk<30 else "Medium" if risk<60 else "High",
                            "neutral" if risk<30 else "down", "⚠️",
                            "#ea4335" if risk>=60 else "#fbbc04"),
                    kpi_card("Visits", str(visits), "", "neutral", "📊", "#34a853"),
                    kpi_card("Days Since", str(days), "last visit", "neutral", "📅", "#9334e6")
                ], 5), unsafe_allow_html=True)

                info_card_start("Patient Information")
                st.dataframe(patient.T, width='stretch')
                info_card_end()

                patient_visits = get_patient_visits(patient_id)
                if not patient_visits.empty:
                    info_card_start(f"Visit History ({len(patient_visits)} visits)")
                    st.dataframe(patient_visits, hide_index=True,
                                width='stretch', height=300)
                    c1, c2 = st.columns(2)
                    with c1:
                        st.download_button("📊 Download Excel",
                                         export_to_excel(patient_visits),
                                         f"patient_{patient_id}_visits.xlsx",
                                         width='stretch')
                    with c2:
                        st.download_button("📄 Download CSV",
                                         export_to_csv(patient_visits),
                                         f"patient_{patient_id}_visits.csv",
                                         width='stretch')
                    info_card_end()

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
            if tier_filter:   results = results[results["patient_tier"].isin(tier_filter)]
            if risk_filter:   results = results[results["churn_risk_category"].isin(risk_filter)]
            if age_filter:    results = results[results["age_group"].isin(age_filter)]
            if gender_filter != "All": results = results[results["gender"] == gender_filter]
            if min_visits > 0:  results = results[results["total_visits"] >= min_visits]
            if min_loyalty > 0: results = results[results["loyalty_points"] >= min_loyalty]

            st.markdown(f'<p style="color:#5f6368;font-size:.85rem">Found {len(results):,} patients</p>',
                       unsafe_allow_html=True)
            st.dataframe(results[["patient_id", "age_group", "gender", "patient_tier",
                                 "loyalty_points", "churn_risk_category", "total_visits"]],
                        hide_index=True, width='stretch', height=400)
            st.download_button("📊 Export Results", export_to_excel(results), "search_results.xlsx")
        info_card_end()

# ============================================================
# PAGE: DOCTOR SEARCH
# ============================================================

elif page == "👨‍⚕️  Doctor Search":
    st.markdown("""<div class="page-header">
<h1>Doctor Performance</h1>
<p>Track and analyze doctor referral metrics</p>
</div>""", unsafe_allow_html=True)

    c1, c2 = st.columns([3, 1])
    with c1:
        doctor_id = st.text_input("Doctor ID", placeholder="e.g., DOC00096")
    with c2:
        st.markdown("<br>", unsafe_allow_html=True)
        search_btn = st.button("🔍 Search", type="primary", width='stretch')

    if search_btn and doctor_id:
        doctor = search_doctor_by_id(doctor_id)
        if doctor is None or doctor.empty:
            st.error(f"❌ Doctor ID '{doctor_id}' not found!")
        else:
            st.success(f"✅ Doctor Found: **{doctor['doctor_name'].values[0]}**")
            refs    = int(doctor["actual_referrals"].values[0])
            patients = int(doctor["unique_patients_referred"].values[0])
            revenue = float(doctor["total_revenue_generated"].values[0])
            perf    = doctor["performance_category"].values[0]
            st.markdown(kpi_row([
                kpi_card("Specialty", doctor["specialty"].values[0], "", "neutral", "🩺", "#1a73e8"),
                kpi_card("Referrals", f"{refs:,}", "", "up", "📊", "#34a853"),
                kpi_card("Patients", f"{patients:,}", "unique", "up", "👥", "#fbbc04"),
                kpi_card("Revenue", f"{revenue/1000:.1f}K EGP", "generated", "up", "💰", "#9334e6"),
                kpi_card("Performance", perf, "",
                        "up" if perf=="Exceeds Expectations" else "neutral",
                        "⭐", "#34a853" if perf=="Exceeds Expectations" else "#fbbc04")
            ], 5), unsafe_allow_html=True)
            info_card_start("Complete Doctor Profile")
            st.dataframe(doctor.T, width='stretch')
            info_card_end()

    info_card_start("All Doctors Performance")
    display_doctors = doctors_data[[
        "doctor_id", "doctor_name", "specialty", "actual_referrals",
        "unique_patients_referred", "total_revenue_generated", "performance_category"
    ]].sort_values("actual_referrals", ascending=False)
    st.dataframe(display_doctors, hide_index=True, width='stretch', height=400)
    st.download_button("📊 Export Doctors", export_to_excel(display_doctors), "doctors_performance.xlsx")
    info_card_end()

# ============================================================
# PAGE: CORPORATE SEARCH
# ============================================================

elif page == "🏢  Corporate Search":
    st.markdown("""<div class="page-header">
<h1>Corporate Contracts</h1>
<p>Manage and analyze corporate partnerships</p>
</div>""", unsafe_allow_html=True)

    c1, c2 = st.columns([3, 1])
    with c1:
        corp_id = st.text_input("Corporate ID", placeholder="e.g., CORP023")
    with c2:
        st.markdown("<br>", unsafe_allow_html=True)
        search_btn = st.button("🔍 Search", type="primary", width='stretch')

    if search_btn and corp_id:
        corp = search_corporate_by_id(corp_id)
        if corp is None or corp.empty:
            st.error(f"❌ Corporate ID '{corp_id}' not found!")
        else:
            st.success(f"✅ Contract Found: **{corp['company_name'].values[0]}**")
            emp     = int(corp["employee_count"].values[0])
            active  = int(corp["unique_employees"].values[0])
            util    = float(corp["actual_utilization_rate"].values[0]) * 100
            revenue = float(corp["total_revenue"].values[0])
            health  = corp["contract_health"].values[0]
            st.markdown(kpi_row([
                kpi_card("Employees", f"{emp:,}", "total", "neutral", "👥", "#1a73e8"),
                kpi_card("Active", f"{active:,}", f"{active/emp*100:.0f}%", "up", "✅", "#34a853"),
                kpi_card("Utilization", f"{util:.1f}%", "rate",
                        "up" if util > 50 else "neutral", "📊", "#fbbc04"),
                kpi_card("Revenue", f"{revenue/1000:.1f}K EGP", "total", "up", "💰", "#9334e6"),
                kpi_card("Health", health, "",
                        "up" if health=="Excellent" else "neutral" if health=="Good" else "down",
                        "❤️", "#34a853" if health=="Excellent" else "#fbbc04")
            ], 5), unsafe_allow_html=True)
            info_card_start("Contract Details")
            st.dataframe(corp.T, width='stretch')
            info_card_end()

    info_card_start("All Corporate Contracts")
    display_corps = corporates_data[[
        "corporate_id", "company_name", "industry", "employee_count",
        "unique_employees", "total_revenue", "contract_health"
    ]].sort_values("total_revenue", ascending=False)
    st.dataframe(display_corps, hide_index=True, width='stretch', height=400)
    st.download_button("📊 Export Contracts", export_to_excel(display_corps), "corporate_contracts.xlsx")
    info_card_end()

# ============================================================
# PAGE: ANALYTICS
# ============================================================

elif page == "📊  Analytics":
    st.markdown("""<div class="page-header">
<h1>Analytics Dashboard</h1>
<p>Patients • Revenue • Inflation-adjusted CAGR • 3-month forecast</p>
</div>""", unsafe_allow_html=True)

    tab1, tab2, tab3, tab4 = st.tabs(
        ["📊 Overview", "⚠️ Churn", "💰 Revenue & Inflation (CAGR)", "🔮 Predictive Trends"])

    # ── TAB 1: OVERVIEW ──
    with tab1:
        n      = len(patients_data)
        gold   = len(patients_data[patients_data["patient_tier"]=="Gold"])
        silver = len(patients_data[patients_data["patient_tier"]=="Silver"])
        bronze = len(patients_data[patients_data["patient_tier"]=="Bronze"])

        st.markdown(kpi_row([
            kpi_card("🥇 Gold",   f"{gold:,}",   f"{gold/n*100:.1f}%",   "neutral","🥇","#fbbc04"),
            kpi_card("🥈 Silver", f"{silver:,}", f"{silver/n*100:.1f}%", "neutral","🥈","#9aa0a6"),
            kpi_card("🥉 Bronze", f"{bronze:,}", f"{bronze/n*100:.1f}%", "neutral","🥉","#cd7f32"),
            kpi_card("Avg Loyalty", f"{patients_data['loyalty_points'].mean():.0f}", "points","up","⭐","#1a73e8")
        ], 4), unsafe_allow_html=True)

        c1, c2 = st.columns(2)
        with c1:
            sec_title("🏆 Patient Tiers")
            chart_start()
            tier_counts = patients_data["patient_tier"].value_counts()
            fig = google_donut(tier_counts.values, tier_counts.index,
                              ["#fbbc04", "#9aa0a6", "#cd7f32"])
            st.plotly_chart(fig, width='stretch', config={"displayModeBar": False})
            chart_end()

        with c2:
            sec_title("🏥 Top 5 Branches")
            chart_start()
            top5 = branches_data.nlargest(5, "total_visits")
            fig = px.bar(top5, x="total_visits", y="branch_name", orientation="h",
                        color="performance_score", color_continuous_scale="Blues")
            google_theme(fig, height=280)
            fig.update_layout(showlegend=False, yaxis_title=None, xaxis_title="Total Visits")
            st.plotly_chart(fig, width='stretch', config={"displayModeBar": False})
            chart_end()

        sec_title("👥 Age Distribution")
        chart_start()
        age_dist = patients_data["age_group"].value_counts().sort_index()
        fig = px.bar(x=age_dist.index, y=age_dist.values,
                    color=age_dist.values, color_continuous_scale="Viridis")
        google_theme(fig, height=300)
        fig.update_layout(showlegend=False, xaxis_title="Age Group", yaxis_title="Count")
        st.plotly_chart(fig, width='stretch', config={"displayModeBar": False})
        chart_end()

    # ── TAB 2: CHURN (REDESIGNED) ──
    with tab2:
        hi = patients_data[patients_data["churn_risk_category"]=="High Risk"]
        me = patients_data[patients_data["churn_risk_category"]=="Medium Risk"]
        lo = patients_data[patients_data["churn_risk_category"]=="Low Risk"]
        n  = len(patients_data)

        st.markdown(kpi_row([
            kpi_card("🔴 High Risk",   f"{len(hi):,}", f"{len(hi)/n*100:.1f}%", "down",    "🔴","#ea4335"),
            kpi_card("🟡 Medium Risk", f"{len(me):,}", f"{len(me)/n*100:.1f}%", "neutral", "🟡","#fbbc04"),
            kpi_card("🟢 Low Risk",    f"{len(lo):,}", f"{len(lo)/n*100:.1f}%", "up",      "🟢","#34a853")
        ], 3), unsafe_allow_html=True)

        # ── CHART 1: Patients by Risk Level & Tier (stacked bar — easy, actionable) ──
        c1, c2 = st.columns(2)
        with c1:
            sec_title("👥 Risk Level by Patient Tier",
                      "How each tier breaks down across risk categories")
            chart_start()
            cross = (patients_data.groupby(["churn_risk_category","patient_tier"])
                     .size().reset_index(name="count"))
            fig = px.bar(
                cross, x="churn_risk_category", y="count", color="patient_tier",
                color_discrete_map={"Gold":"#fbbc04","Silver":"#9aa0a6","Bronze":"#cd7f32"},
                barmode="group",
                category_orders={"churn_risk_category":["Low Risk","Medium Risk","High Risk"]},
                text="count"
            )
            fig.update_traces(textposition="outside", textfont_size=11)
            google_theme(fig, height=300)
            fig.update_layout(xaxis_title=None, yaxis_title="Patients",
                              legend_title="Tier")
            st.plotly_chart(fig, width='stretch', config={"displayModeBar": False})
            chart_end()

        # ── CHART 2: Engagement status breakdown ──
        with c2:
            sec_title("🔥 Patient Engagement Status",
                      "Current engagement level across all patients")
            chart_start()
            if "engagement_status" in patients_data.columns:
                eng = patients_data["engagement_status"].value_counts().reset_index()
                eng.columns = ["Status", "Count"]
                color_map = {
                    "Highly Engaged": "#34a853",
                    "Engaged":        "#1a73e8",
                    "At Risk":        "#fbbc04",
                    "Inactive":       "#ea4335"
                }
                fig = px.bar(
                    eng, x="Status", y="Count",
                    color="Status", color_discrete_map=color_map,
                    text="Count"
                )
                fig.update_traces(textposition="outside", textfont_size=12)
                google_theme(fig, height=300)
                fig.update_layout(xaxis_title=None, yaxis_title="Patients",
                                  showlegend=False)
                st.plotly_chart(fig, width='stretch',
                               config={"displayModeBar": False})
            else:
                st.info("Engagement status column not available in this dataset.")
            chart_end()

        # ── Key metrics summary per risk group ──
        sec_title("📋 Average Profile by Risk Category",
                  "What distinguishes high-risk patients from low-risk ones")
        chart_start()
        summary_cols = ["churn_risk_category", "total_visits",
                        "days_since_last_visit", "loyalty_points"]
        available    = [c for c in summary_cols if c in patients_data.columns]
        if len(available) > 1:
            summary = (patients_data[available]
                       .groupby("churn_risk_category")
                       .mean().round(1).reset_index())
            summary.columns = [c.replace("_"," ").title() for c in summary.columns]
            category_order  = ["Low Risk", "Medium Risk", "High Risk"]
            order_map       = {v: i for i, v in enumerate(category_order)}
            sort_col        = summary.columns[0]
            summary["_sort"] = summary[sort_col].map(order_map)
            summary = summary.sort_values("_sort").drop(columns=["_sort"])
            st.dataframe(summary, hide_index=True, width='stretch')
        chart_end()

        # ── Top 20 high-risk patients ──
        info_card_start("🚨 Top 20 High-Risk Patients — Prioritise for Outreach")
        display_cols = [c for c in
            ["patient_id","churn_risk_score","days_since_last_visit",
             "total_visits","loyalty_points","patient_tier"]
            if c in hi.columns]
        st.dataframe(hi.nlargest(20, "churn_risk_score")[display_cols],
                    hide_index=True, width='stretch')
        st.download_button("📊 Export High-Risk List", export_to_excel(hi), "high_risk.xlsx")
        info_card_end()

    # ── TAB 3: REVENUE + INFLATION + CAGR ──
    with tab3:
        INFL = 0.33

        mr = build_real_revenue(monthly_revenue, annual_inflation=INFL)
        if len(mr) < 2:
            st.info("📊 Building revenue analysis from visits data...")
            mr = build_real_revenue_from_visits(visits_data, annual_inflation=INFL)

        if len(mr) < 2:
            st.warning("⚠️ Need ≥ 2 months of data to compute CAGR.")
        else:
            fd   = mr["visit_month"].iloc[0]
            ld   = mr["visit_month"].iloc[-1]
            span = max(1, (ld.year - fd.year)*12 + (ld.month - fd.month))

            nom0, nomF = mr["total_revenue"].iloc[0],  mr["total_revenue"].iloc[-1]
            re0,  reF  = mr["real_revenue"].iloc[0],   mr["real_revenue"].iloc[-1]

            cagr_nom  = compute_cagr(nom0, nomF, span)
            cagr_real = compute_cagr(re0,  reF,  span)
            gap       = cagr_nom - cagr_real

            total_nom  = mr["total_revenue"].sum()
            total_real = mr["real_revenue"].sum()
            total_tax  = mr["inflation_tax"].sum()

            st.markdown(kpi_row([
                kpi_card("Total Revenue (Nominal)", f"{total_nom/1e6:.2f}M EGP",
                         "Actual EGP received",         "neutral","💵","#1a73e8"),
                kpi_card("Total Revenue (Real)",    f"{total_real/1e6:.2f}M EGP",
                         "Base-month purchasing power", "neutral","🏦","#34a853"),
                kpi_card("Inflation Erosion",       f"{total_tax/1e6:.2f}M EGP",
                         f"Lost to {INFL*100:.0f}%/yr","down","🔥","#ea4335"),
                kpi_card("Nominal CAGR",            f"{cagr_nom:+.1f}%",
                         f"Over {span} months",         "up" if cagr_nom>0 else "neutral","🚀","#1a73e8"),
                kpi_card("Real CAGR",               f"{cagr_real:+.1f}%",
                         "After inflation",              "up" if cagr_real>0 else "down","📉",
                         "#34a853" if cagr_real>0 else "#ea4335"),
            ],5), unsafe_allow_html=True)

            if cagr_nom == 0.0:
                note = (f"Nominal revenue was <b>flat</b> across the {span}-month window. "
                        f"With Egypt's ~{INFL*100:.0f}%/yr inflation, real purchasing-power CAGR = "
                        f"<b>{cagr_real:+.1f}%</b> — meaning the lab silently lost "
                        f"<b>{total_tax/1e6:.2f}M EGP</b> in real value.")
            else:
                note = (f"Nominal CAGR = <b>{cagr_nom:+.1f}%</b> over {span} months. "
                        f"After Egypt's ~{INFL*100:.0f}%/yr inflation, real CAGR = "
                        f"<b>{cagr_real:+.1f}%</b> (gap = {gap:+.1f} pp). "
                        f"Total inflation erosion = <b>{total_tax/1e6:.2f}M EGP</b>.")
            st.markdown(f'<div class="infl-banner">📌 <b>Inflation Note:</b> {note}</div>',
                        unsafe_allow_html=True)

            # Chart 1
            sec_title("📊 Nominal vs Real Revenue",
                      "Real revenue = what those EGPs are actually worth in base-month purchasing power.")
            chart_start()
            fig = go.Figure()
            fig.add_trace(go.Scatter(x=mr["visit_month"],y=mr["total_revenue"],
                name="Nominal Revenue",mode="lines+markers",
                line=dict(color="#1a73e8",width=2.5),marker=dict(size=8)))
            fig.add_trace(go.Scatter(x=mr["visit_month"],y=mr["real_revenue"],
                name="Real Revenue (base-month EGP)",mode="lines+markers",
                line=dict(color="#ea4335",width=2.5,dash="dot"),marker=dict(size=8)))
            fig.add_trace(go.Scatter(
                x=pd.concat([mr["visit_month"],mr["visit_month"][::-1]]),
                y=pd.concat([mr["total_revenue"],mr["real_revenue"][::-1]]),
                fill="toself",fillcolor="rgba(234,67,53,0.08)",
                line=dict(color="rgba(0,0,0,0)"),name="Inflation Erosion",hoverinfo="skip"))
            if "total_profit" in mr.columns:
                fig.add_trace(go.Scatter(x=mr["visit_month"],y=mr["total_profit"],
                    name="Nominal Profit",mode="lines+markers",
                    line=dict(color="#34a853",width=2),marker=dict(size=6)))
            google_theme(fig, height=380)
            fig.update_layout(yaxis_title="EGP")
            st.plotly_chart(fig, width='stretch', config={"displayModeBar": False})
            chart_end()

            # Chart 2
            sec_title("📈 Purchasing-Power Index (Base Month = 100)",
                      "When the Real Index drops below 100 your revenue buys less than at launch.")
            chart_start()
            fig = go.Figure()
            fig.add_trace(go.Scatter(x=mr["visit_month"],y=mr["nominal_index"],
                name="Nominal Index",mode="lines+markers",
                line=dict(color="#1a73e8",width=2.5),marker=dict(size=8)))
            fig.add_trace(go.Scatter(x=mr["visit_month"],y=mr["real_index"],
                name="Real Index",mode="lines+markers",
                line=dict(color="#ea4335",width=2.5,dash="dot"),marker=dict(size=8)))
            fig.add_shape(type="line",
                          x0=mr["visit_month"].min(),x1=mr["visit_month"].max(),
                          y0=100,y1=100,xref="x",yref="y",
                          line=dict(color="#9aa0a6",width=1,dash="dot"))
            fig.add_annotation(x=mr["visit_month"].max(),y=100,xref="x",yref="y",
                               text="Breakeven (100)",showarrow=False,
                               xanchor="right",font=dict(size=10,color="#9aa0a6"))
            google_theme(fig, height=300)
            fig.update_layout(yaxis_title="Index (base = 100)")
            st.plotly_chart(fig, width='stretch', config={"displayModeBar": False})
            chart_end()

            c1b, c2b = st.columns(2)
            with c1b:
                sec_title("📈 Month-on-Month Growth")
                chart_start()
                mr2          = mr.copy()
                mr2["nom_g"] = mr2["total_revenue"].pct_change()*100
                mr2["real_g"]= mr2["real_revenue"].pct_change()*100
                mr2          = mr2.dropna(subset=["nom_g"])
                fig = go.Figure()
                fig.add_trace(go.Bar(x=mr2["visit_month"],y=mr2["nom_g"],
                    name="Nominal MoM %",
                    marker_color=["#34a853" if v>=0 else "#ea4335" for v in mr2["nom_g"]]))
                fig.add_trace(go.Scatter(x=mr2["visit_month"],y=mr2["real_g"],
                    name="Real MoM %",mode="lines+markers",
                    line=dict(color="#1a73e8",width=2,dash="dot"),marker=dict(size=6)))
                fig.add_shape(type="line",
                              x0=mr2["visit_month"].min(),x1=mr2["visit_month"].max(),
                              y0=0,y1=0,xref="x",yref="y",
                              line=dict(color="#dadce0",width=1))
                google_theme(fig, height=280)
                fig.update_layout(yaxis_title="Growth (%)")
                st.plotly_chart(fig, width='stretch', config={"displayModeBar": False})
                chart_end()

            with c2b:
                sec_title("💸 Cumulative Inflation Erosion")
                chart_start()
                mr["cum_tax"] = mr["inflation_tax"].cumsum()
                fig = go.Figure()
                fig.add_trace(go.Scatter(x=mr["visit_month"],y=mr["cum_tax"]/1e6,
                    mode="lines+markers",fill="tozeroy",
                    line=dict(color="#ea4335",width=2.5),marker=dict(size=7),
                    fillcolor="rgba(234,67,53,0.15)",name="Cumulative Loss"))
                google_theme(fig, height=280)
                fig.update_layout(yaxis_title="Million EGP")
                st.plotly_chart(fig, width='stretch', config={"displayModeBar": False})
                chart_end()

            # Branch CAGR
            sec_title("🏢 Branch-Level CAGR Analysis",
                      "Growth rates by branch, adjusted for inflation")
            chart_start()
            branch_cagr_data = []
            for bname in branches_data["branch_name"].unique():
                bv = visits_data[visits_data["branch_name"] == bname]
                bm = bv.groupby("visit_month").size().reset_index(name="visits")
                if len(bm) >= 2:
                    bm = bm.sort_values("visit_month").reset_index(drop=True)
                    avg_rev = 150
                    sr  = bm.iloc[0]["visits"] * avg_rev
                    er  = bm.iloc[-1]["visits"] * avg_rev
                    mth = len(bm)
                    nc  = compute_cagr(sr, er, mth)
                    rc  = nc - (INFL * 100)
                    branch_cagr_data.append({
                        "Branch": bname, "Nominal CAGR (%)": round(nc, 2),
                        "Inflation Rate (%)": INFL*100,
                        "Real CAGR (%)": round(rc, 2), "Months": mth
                    })
            if branch_cagr_data:
                cdf = pd.DataFrame(branch_cagr_data).sort_values("Real CAGR (%)", ascending=False)
                st.dataframe(cdf, hide_index=True, width='stretch')
                fig = go.Figure()
                fig.add_trace(go.Bar(x=cdf["Branch"],y=cdf["Nominal CAGR (%)"],
                                    name="Nominal CAGR",marker_color="#1a73e8"))
                fig.add_trace(go.Bar(x=cdf["Branch"],y=cdf["Real CAGR (%)"],
                                    name="Real CAGR (Inflation-Adjusted)",marker_color="#34a853"))
                fig.add_shape(type="line",x0=-0.5,x1=len(cdf)-0.5,y0=0,y1=0,
                             line=dict(color="#ea4335",width=1,dash="dash"))
                google_theme(fig, height=320)
                fig.update_layout(barmode="group",yaxis_title="CAGR (%)",xaxis_title=None)
                st.plotly_chart(fig, width='stretch', config={"displayModeBar": False})
            chart_end()

    # ── TAB 4: PREDICTIVE TRENDS (IMPROVED) ──
    with tab4:
        predictions, std_err = predict_visits(monthly_trends, months_ahead=3)
        historical = monthly_trends[["visit_month","total_visits"]].copy()

        # ── Main forecast chart ──
        sec_title("🔮 3-Month Visit Forecast",
                  "Historical visits vs AI-predicted future visits (linear trend + confidence band)")
        chart_start()

        fig = go.Figure()

        # Confidence band
        upper_band = predictions["upper"].tolist()
        lower_band = predictions["lower"].tolist()
        band_x = predictions["visit_month"].tolist() + predictions["visit_month"].tolist()[::-1]
        band_y = upper_band + lower_band[::-1]
        fig.add_trace(go.Scatter(
            x=band_x, y=band_y,
            fill="toself",
            fillcolor="rgba(52,168,83,0.12)",
            line=dict(color="rgba(0,0,0,0)"),
            name="Confidence Range",
            hoverinfo="skip"
        ))

        # Historical line
        fig.add_trace(go.Scatter(
            x=historical["visit_month"],
            y=historical["total_visits"],
            name="Historical Visits",
            mode="lines+markers+text",
            line=dict(color="#1a73e8", width=3),
            marker=dict(size=10, color="#1a73e8"),
            text=[f"{v:,}" for v in historical["total_visits"]],
            textposition="top center",
            textfont=dict(size=10, color="#1a73e8")
        ))

        # Forecast line
        fig.add_trace(go.Scatter(
            x=predictions["visit_month"],
            y=predictions["predicted_visits"],
            name="Predicted Visits",
            mode="lines+markers+text",
            line=dict(color="#34a853", width=3, dash="dash"),
            marker=dict(size=12, color="#34a853", symbol="diamond"),
            text=[f"{v:,}" for v in predictions["predicted_visits"]],
            textposition="top center",
            textfont=dict(size=10, color="#34a853")
        ))

        # Divider line
        safe_vline(fig, historical["visit_month"].max())

        google_theme(fig, height=420)
        fig.update_layout(
            yaxis_title="Number of Visits",
            xaxis=dict(
                tickformat="%b %Y",
                dtick="M1",
                showgrid=False, showline=True, linecolor="#dadce0"
            ),
            hovermode="x unified"
        )
        st.plotly_chart(fig, width='stretch', config={"displayModeBar": False})
        chart_end()

        # KPI summary
        next_val = int(predictions.iloc[0]["predicted_visits"])
        last_val = int(historical.iloc[-1]["total_visits"])
        total_3m = int(predictions["predicted_visits"].sum())
        avg_growth = (predictions["predicted_visits"].mean() / historical["total_visits"].mean() - 1) * 100

        st.markdown(kpi_row([
            kpi_card("Next Month Forecast", f"{next_val:,}",
                    f"{((next_val/last_val)-1)*100:+.1f}% vs last month",
                    "up" if next_val >= last_val else "down", "📈", "#1a73e8"),
            kpi_card("3-Month Total", f"{total_3m:,}",
                    "predicted visits", "neutral", "📊", "#34a853"),
            kpi_card("Trend vs Avg", f"{avg_growth:+.1f}%",
                    "vs historical avg",
                    "up" if avg_growth > 0 else "down", "📈",
                    "#34a853" if avg_growth > 0 else "#ea4335")
        ], 3), unsafe_allow_html=True)

        # Detailed table
        info_card_start("📅 Detailed Monthly Forecast")
        pred_display = predictions[["visit_month","predicted_visits","lower","upper"]].copy()
        pred_display["visit_month"] = pred_display["visit_month"].dt.strftime("%B %Y")
        pred_display.columns = ["Month", "Predicted Visits", "Lower Bound", "Upper Bound"]
        st.dataframe(pred_display, hide_index=True, width='stretch')
        info_card_end()

        st.info("""
**How to read this forecast:**
- 🔵 **Blue line** = actual historical visit data
- 🟢 **Green dashed line** = AI-predicted visits for next 3 months
- 🟩 **Green band** = confidence range (±1 standard deviation)
- **Vertical line** = divides past from future
- Model uses linear regression on historical trends — best used for short-term planning
        """)

# ============================================================
# PAGE: EXPORT
# ============================================================

elif page == "📥  Export":
    st.markdown("""<div class="page-header">
<h1>Export Data</h1>
<p>Download analytics data for external use</p>
</div>""", unsafe_allow_html=True)

    table_options = {
        "Patients":           "patients",
        "Doctors":            "doctors",
        "Corporate Contracts":"corporates",
        "Branches":           "branches",
        "High Risk Patients": "high_risk"
    }

    selected = st.selectbox("Select table to export", list(table_options.keys()))

    if selected == "High Risk Patients":
        export_data = patients_data[patients_data["churn_risk_category"] == "High Risk"]
    else:
        export_data = pd.read_sql(f"SELECT * FROM {table_options[selected]}", conn)

    info_card_start(f"Preview: {selected}")
    st.markdown(f'<p style="color:#5f6368;font-size:.85rem">Total records: {len(export_data):,}</p>',
                unsafe_allow_html=True)
    st.dataframe(export_data.head(10), hide_index=True, width='stretch')
    c1, c2 = st.columns(2)
    with c1:
        st.download_button("📊 Download as Excel",
                          export_to_excel(export_data),
                          f"{selected.lower().replace(' ', '_')}.xlsx",
                          width='stretch')
    with c2:
        st.download_button("📄 Download as CSV",
                          export_to_csv(export_data),
                          f"{selected.lower().replace(' ', '_')}.csv",
                          width='stretch')
    info_card_end()

# ============================================================
# FOOTER
# ============================================================

st.markdown(f"""
<div style="text-align:center; margin-top:3rem; padding:1.5rem 0;
     border-top:1px solid #dadce0; color:#5f6368; font-size:0.8125rem;
     font-family:'Google Sans',sans-serif; line-height:1.8;">
  <div style="font-weight:600; color:#202124; font-size:0.875rem; margin-bottom:4px;">
    Trust Labs Healthcare Analytics &nbsp;·&nbsp; v3.0
  </div>
  <div>
    Data Analysis for Health Care Systems &nbsp;·&nbsp;
    <strong>Ahmed Mustafa</strong>
  </div>
  <div style="margin-top:4px;">
    📱 <a href="https://wa.me/201143575727" style="color:#1a73e8;text-decoration:none;">01143575727</a>
    &nbsp;&nbsp;
    📧 <a href="mailto:ahmdsa1@proton.com" style="color:#1a73e8;text-decoration:none;">ahmdsa1@proton.com</a>
  </div>
  <div style="margin-top:6px; color:#9aa0a6; font-size:0.75rem;">
    Last updated: {datetime.now().strftime("%B %d, %Y at %H:%M")}
  </div>
</div>
""", unsafe_allow_html=True)
