import streamlit as st

packages = [
    "joblib",
    "pandas",
    "numpy",
    "plotly",
    "lightgbm",
    "sklearn"
]

for p in packages:
    try:
        __import__(p)
        st.success(f"{p} OK")
    except Exception as e:
        st.error(f"{p} FAILED: {e}")
from pathlib import Path

st.write("APP STARTED")

req = Path("requirements.txt")

st.write("requirements.txt exists:", req.exists())

if req.exists():
    st.code(req.read_text())

st.write("START")

try:
    import joblib
    st.write("JOBLIB OK")
except Exception as e:
    st.write("JOBLIB ERROR")
    st.write(repr(e))
    st.stop()
import pandas as pd
import lightgbm as lgb
import plotly.graph_objects as go
import pkgutil



# ---------------------------------------------------
# PAGE CONFIG
# ---------------------------------------------------

st.set_page_config(
    page_title="Customer Risk Intelligence",
    page_icon="🎯",
    layout="wide"
)

model = lgb.Booster(model_file="churn_model.txt")
feature_columns = joblib.load("feature_columns.pkl")

# ---------------------------------------------------
# CUSTOM CSS
# ---------------------------------------------------

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Syne:wght@400;600;700;800&family=DM+Sans:wght@300;400;500;600&display=swap');

/* ---- Reset & Base ---- */
*, *::before, *::after { box-sizing: border-box; }

html, body, .stApp {
    font-family: 'DM Sans', sans-serif;
    background: #0A0F1E;
    color: #E2E8F0;
}

/* ---- Hide Streamlit chrome ---- */
#MainMenu, footer, header { visibility: hidden; }
.block-container {
    padding: 2rem 2.5rem 4rem 2.5rem !important;
    max-width: 1400px !important;
}

/* ---- Animated background ---- */
.stApp::before {
    content: '';
    position: fixed;
    inset: 0;
    background:
        radial-gradient(ellipse 80% 50% at 20% 10%, rgba(99,102,241,0.12) 0%, transparent 60%),
        radial-gradient(ellipse 60% 40% at 80% 80%, rgba(236,72,153,0.08) 0%, transparent 55%),
        radial-gradient(ellipse 50% 60% at 60% 30%, rgba(16,185,129,0.06) 0%, transparent 50%);
    pointer-events: none;
    z-index: 0;
}

/* ---- Hero Header ---- */
.hero {
    display: flex;
    align-items: center;
    gap: 16px;
    margin-bottom: 2rem;
    padding: 2rem 2.5rem;
    background: linear-gradient(135deg, rgba(99,102,241,0.15) 0%, rgba(16,185,129,0.08) 100%);
    border: 1px solid rgba(99,102,241,0.25);
    border-radius: 20px;
    position: relative;
    overflow: hidden;
}

.hero::after {
    content: 'RISK INTELLIGENCE';
    position: absolute;
    right: -10px;
    top: 50%;
    transform: translateY(-50%);
    font-family: 'Syne', sans-serif;
    font-size: 80px;
    font-weight: 800;
    color: rgba(99,102,241,0.06);
    letter-spacing: 4px;
    pointer-events: none;
    white-space: nowrap;
}

.hero-icon {
    font-size: 42px;
    filter: drop-shadow(0 0 16px rgba(99,102,241,0.6));
}

.hero-title {
    font-family: 'Syne', sans-serif;
    font-size: 32px;
    font-weight: 800;
    background: linear-gradient(135deg, #A5B4FC 0%, #34D399 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
    margin: 0;
    line-height: 1.1;
}

.hero-sub {
    font-size: 14px;
    color: #64748B;
    margin: 4px 0 0 0;
    letter-spacing: 0.5px;
}

/* ---- KPI Cards ---- */
.kpi-grid {
    display: grid;
    grid-template-columns: repeat(5, 1fr);
    gap: 14px;
    margin-bottom: 1.8rem;
}

.kpi-card {
    background: rgba(15,23,42,0.8);
    border: 1px solid rgba(255,255,255,0.07);
    border-radius: 16px;
    padding: 20px 18px;
    position: relative;
    overflow: hidden;
    transition: transform 0.2s, border-color 0.2s;
    backdrop-filter: blur(12px);
}

.kpi-card::before {
    content: '';
    position: absolute;
    top: 0; left: 0; right: 0;
    height: 2px;
    background: var(--accent, linear-gradient(90deg, #6366F1, #8B5CF6));
    border-radius: 16px 16px 0 0;
}

.kpi-card:hover {
    transform: translateY(-2px);
    border-color: rgba(99,102,241,0.3);
}

.kpi-label {
    font-size: 11px;
    font-weight: 600;
    letter-spacing: 1.2px;
    text-transform: uppercase;
    color: #475569;
    margin-bottom: 10px;
}

.kpi-value {
    font-family: 'Syne', sans-serif;
    font-size: 28px;
    font-weight: 800;
    color: #F1F5F9;
    line-height: 1;
    margin-bottom: 6px;
}

.kpi-badge {
    display: inline-flex;
    align-items: center;
    gap: 5px;
    font-size: 11px;
    font-weight: 600;
    padding: 3px 10px;
    border-radius: 999px;
}

.badge-low    { background: rgba(16,185,129,0.15); color: #34D399; }
.badge-medium { background: rgba(245,158,11,0.15); color: #FBBF24; }
.badge-high   { background: rgba(239,68,68,0.15);  color: #F87171; }
.badge-vip      { background: rgba(16,185,129,0.15); color: #34D399; }
.badge-monitor  { background: rgba(99,102,241,0.15); color: #A5B4FC; }
.badge-at-risk  { background: rgba(245,158,11,0.15); color: #FBBF24; }
.badge-critical { background: rgba(239,68,68,0.15);  color: #F87171; }

/* ---- Section Cards ---- */
.section-card {
    background: rgba(15,23,42,0.8);
    border: 1px solid rgba(255,255,255,0.07);
    border-radius: 20px;
    padding: 28px;
    margin-bottom: 1.5rem;
    backdrop-filter: blur(12px);
}

.section-title {
    font-family: 'Syne', sans-serif;
    font-size: 16px;
    font-weight: 700;
    letter-spacing: 0.5px;
    color: #94A3B8;
    text-transform: uppercase;
    margin-bottom: 18px;
    display: flex;
    align-items: center;
    gap: 8px;
}

.section-title::after {
    content: '';
    flex: 1;
    height: 1px;
    background: rgba(255,255,255,0.06);
}

/* ---- Risk Driver Tags ---- */
.driver-tag {
    display: inline-flex;
    align-items: center;
    gap: 8px;
    background: rgba(245,158,11,0.1);
    border: 1px solid rgba(245,158,11,0.2);
    color: #FCD34D;
    padding: 8px 16px;
    border-radius: 10px;
    font-size: 13px;
    font-weight: 500;
    margin: 4px;
}

/* ---- Recommendation Box ---- */
.rec-critical {
    background: linear-gradient(135deg, rgba(239,68,68,0.1) 0%, rgba(220,38,38,0.05) 100%);
    border: 1px solid rgba(239,68,68,0.3);
    border-left: 4px solid #EF4444;
    border-radius: 16px;
    padding: 24px;
}
.rec-at-risk {
    background: linear-gradient(135deg, rgba(245,158,11,0.1) 0%, rgba(217,119,6,0.05) 100%);
    border: 1px solid rgba(245,158,11,0.3);
    border-left: 4px solid #F59E0B;
    border-radius: 16px;
    padding: 24px;
}
.rec-vip {
    background: linear-gradient(135deg, rgba(16,185,129,0.1) 0%, rgba(5,150,105,0.05) 100%);
    border: 1px solid rgba(16,185,129,0.3);
    border-left: 4px solid #10B981;
    border-radius: 16px;
    padding: 24px;
}
.rec-monitor {
    background: linear-gradient(135deg, rgba(99,102,241,0.1) 0%, rgba(79,70,229,0.05) 100%);
    border: 1px solid rgba(99,102,241,0.3);
    border-left: 4px solid #6366F1;
    border-radius: 16px;
    padding: 24px;
}

.rec-title {
    font-family: 'Syne', sans-serif;
    font-size: 18px;
    font-weight: 700;
    margin-bottom: 14px;
    display: flex;
    align-items: center;
    gap: 10px;
}

.rec-item {
    display: flex;
    align-items: center;
    gap: 10px;
    padding: 10px 0;
    border-bottom: 1px solid rgba(255,255,255,0.05);
    font-size: 14px;
    color: #CBD5E1;
}

.rec-item:last-child { border-bottom: none; }

.rec-dot {
    width: 6px; height: 6px;
    border-radius: 50%;
    flex-shrink: 0;
}

/* ---- Churn Gauge ---- */
.gauge-wrap {
    display: flex;
    justify-content: center;
    align-items: center;
}

/* ---- Sidebar Styling ---- */
[data-testid="stSidebar"] {
    background: #080D1A !important;
    border-right: 1px solid rgba(255,255,255,0.06) !important;
}

[data-testid="stSidebar"] .stSelectbox label,
[data-testid="stSidebar"] .stSlider label,
[data-testid="stSidebar"] .stNumberInput label {
    color: #94A3B8 !important;
    font-size: 12px !important;
    font-weight: 500 !important;
    letter-spacing: 0.5px !important;
}

[data-testid="stSidebar"] h3 {
    font-family: 'Syne', sans-serif !important;
    font-size: 11px !important;
    font-weight: 700 !important;
    letter-spacing: 2px !important;
    text-transform: uppercase !important;
    color: #6366F1 !important;
    margin-top: 20px !important;
    margin-bottom: 10px !important;
}

[data-testid="stSidebar"] h2 {
    font-family: 'Syne', sans-serif !important;
    color: #E2E8F0 !important;
    font-size: 18px !important;
}

/* Sidebar button */
[data-testid="stSidebar"] .stButton > button {
    background: linear-gradient(135deg, #6366F1 0%, #8B5CF6 100%) !important;
    color: white !important;
    border: none !important;
    border-radius: 12px !important;
    font-family: 'Syne', sans-serif !important;
    font-weight: 700 !important;
    font-size: 14px !important;
    letter-spacing: 0.5px !important;
    padding: 14px !important;
    transition: opacity 0.2s, transform 0.2s !important;
    box-shadow: 0 4px 20px rgba(99,102,241,0.4) !important;
}

[data-testid="stSidebar"] .stButton > button:hover {
    opacity: 0.9 !important;
    transform: translateY(-1px) !important;
}

/* ---- Empty state ---- */
.empty-state {
    text-align: center;
    padding: 60px 20px;
    color: #334155;
}

.empty-icon {
    font-size: 56px;
    margin-bottom: 16px;
    filter: grayscale(0.5);
}

.empty-text {
    font-family: 'Syne', sans-serif;
    font-size: 18px;
    font-weight: 700;
    color: #475569;
    margin-bottom: 8px;
}

.empty-sub {
    font-size: 14px;
    color: #334155;
}

/* ---- Progress bar ---- */
.prob-bar-wrap {
    margin-top: 12px;
}
.prob-bar-label {
    display: flex;
    justify-content: space-between;
    font-size: 11px;
    color: #64748B;
    margin-bottom: 6px;
}
.prob-bar-bg {
    height: 6px;
    background: rgba(255,255,255,0.06);
    border-radius: 99px;
    overflow: hidden;
}
.prob-bar-fill {
    height: 100%;
    border-radius: 99px;
    transition: width 0.8s cubic-bezier(0.4,0,0.2,1);
}

/* ---- Divider ---- */
.styled-divider {
    border: none;
    height: 1px;
    background: linear-gradient(90deg, transparent, rgba(99,102,241,0.3), transparent);
    margin: 1.5rem 0;
}

</style>
""", unsafe_allow_html=True)

# ---------------------------------------------------
# SIDEBAR
# ---------------------------------------------------

with st.sidebar:
    st.header("Customer Intel")
    st.markdown("### Profile")

    gender = st.selectbox("Gender", ["Male", "Female"])
    senior = st.selectbox("Senior Citizen", ["Yes", "No"])
    partner = st.selectbox("Partner", ["Yes", "No"])
    dependents = st.selectbox("Dependents", ["Yes", "No"])

    st.markdown("### Billing")
    tenure = st.slider("Tenure (Months)", 0, 72, 12)
    monthly_charges = st.number_input("Monthly Charges (₹)", min_value=0.0, value=50.0, step=5.0)

    st.markdown("### Services")
    phone_service = st.selectbox("Phone Service", ["Yes", "No"])
    multiple_lines = st.selectbox("Multiple Lines", ["No", "Yes", "No phone service"])
    internet_service = st.selectbox("Internet Service", ["DSL", "Fiber optic", "No"])
    online_security = st.selectbox("Online Security", ["Yes", "No", "No internet service"])
    online_backup = st.selectbox("Online Backup", ["Yes", "No", "No internet service"])
    device_protection = st.selectbox("Device Protection", ["Yes", "No", "No internet service"])
    tech_support = st.selectbox("Tech Support", ["Yes", "No", "No internet service"])
    streaming_tv = st.selectbox("Streaming TV", ["Yes", "No", "No internet service"])
    streaming_movies = st.selectbox("Streaming Movies", ["Yes", "No", "No internet service"])

    st.markdown("### Contract")
    contract = st.selectbox("Contract Type", ["Month-to-month", "One year", "Two year"])
    paperless_billing = st.selectbox("Paperless Billing", ["Yes", "No"])
    payment_method = st.selectbox("Payment Method", [
        "Bank transfer", "Credit card (automatic)", "Electronic check", "Mailed check"
    ])

    st.divider()
    analyze = st.button("⚡  Assess Customer", use_container_width=True)

# ---------------------------------------------------
# HERO HEADER
# ---------------------------------------------------

st.markdown("""
<div class="hero">
    <div class="hero-icon">🎯</div>
    <div>
        <div class="hero-title">Customer Risk Intelligence</div>
        <div class="hero-sub">Predictive churn analysis · Real-time scoring · Retention strategy</div>
    </div>
</div>
""", unsafe_allow_html=True)

# ---------------------------------------------------
# PREDICTION LOGIC
# ---------------------------------------------------

churn_probability = None
ltv = None
revenue_at_risk = None
segment = "--"
fig = None
risk_level = "--"
confidence = None
reasons = []

if analyze:
    input_data = {col: 0 for col in feature_columns}

    input_data["SeniorCitizen"] = 1 if senior == "Yes" else 0
    input_data["tenure"] = tenure
    input_data["MonthlyCharges"] = monthly_charges
    input_data["TotalCharges"] = tenure * monthly_charges

    input_data["gender_Male"] = 1 if gender == "Male" else 0
    input_data["Partner_Yes"] = 1 if partner == "Yes" else 0
    input_data["Dependents_Yes"] = 1 if dependents == "Yes" else 0
    input_data["PhoneService_Yes"] = 1 if phone_service == "Yes" else 0

    if multiple_lines == "No phone service":
        input_data["MultipleLines_No phone service"] = 1
    elif multiple_lines == "Yes":
        input_data["MultipleLines_Yes"] = 1

    if internet_service == "Fiber optic":
        input_data["InternetService_Fiber optic"] = 1
    elif internet_service == "No":
        input_data["InternetService_No"] = 1

    if online_security == "No internet service":
        input_data["OnlineSecurity_No internet service"] = 1
    elif online_security == "Yes":
        input_data["OnlineSecurity_Yes"] = 1

    if online_backup == "No internet service":
        input_data["OnlineBackup_No internet service"] = 1
    elif online_backup == "Yes":
        input_data["OnlineBackup_Yes"] = 1

    if device_protection == "No internet service":
        input_data["DeviceProtection_No internet service"] = 1
    elif device_protection == "Yes":
        input_data["DeviceProtection_Yes"] = 1

    if tech_support == "No internet service":
        input_data["TechSupport_No internet service"] = 1
    elif tech_support == "Yes":
        input_data["TechSupport_Yes"] = 1

    if streaming_tv == "No internet service":
        input_data["StreamingTV_No internet service"] = 1
    elif streaming_tv == "Yes":
        input_data["StreamingTV_Yes"] = 1

    if streaming_movies == "No internet service":
        input_data["StreamingMovies_No internet service"] = 1
    elif streaming_movies == "Yes":
        input_data["StreamingMovies_Yes"] = 1

    if contract == "One year":
        input_data["Contract_One year"] = 1
    elif contract == "Two year":
        input_data["Contract_Two year"] = 1

    input_data["PaperlessBilling_Yes"] = 1 if paperless_billing == "Yes" else 0

    if payment_method == "Credit card (automatic)":
        input_data["PaymentMethod_Credit card (automatic)"] = 1
    elif payment_method == "Electronic check":
        input_data["PaymentMethod_Electronic check"] = 1
    elif payment_method == "Mailed check":
        input_data["PaymentMethod_Mailed check"] = 1

    customer_df = pd.DataFrame([input_data])[feature_columns]
    proba = model.predict(customer_df)
    churn_probability = float(proba[0])
    confidence = max(churn_probability, 1 - churn_probability)

    if churn_probability < 0.15:
        risk_level = "Low"
    elif churn_probability < 0.40:
        risk_level = "Medium"
    else:
        risk_level = "High"

    ltv = tenure * monthly_charges
    revenue_at_risk = ltv * churn_probability

    ltv_threshold = 1397.475
    churn_threshold = 0.14985

    if churn_probability > churn_threshold and ltv > ltv_threshold:
        segment = "Critical"
    elif churn_probability > churn_threshold and ltv <= ltv_threshold:
        segment = "At Risk"
    elif churn_probability <= churn_threshold and ltv > ltv_threshold:
        segment = "VIP"
    else:
        segment = "Monitor"

    if contract == "Month-to-month":
        reasons.append(("📋", "Month-to-month contract"))
    if internet_service == "Fiber optic":
        reasons.append(("🌐", "Fiber optic internet service"))
    if payment_method == "Electronic check":
        reasons.append(("💳", "Electronic check payment"))
    if paperless_billing == "Yes":
        reasons.append(("📧", "Paperless billing enabled"))
    if tenure < 12:
        reasons.append(("🕐", "Low tenure — new customer"))
    if monthly_charges > 70:
        reasons.append(("💰", "High monthly charges"))

    # --- Plotly Risk Matrix ---
    segment_colors = {
        "Critical": "#EF4444",
        "At Risk":  "#F59E0B",
        "VIP":      "#10B981",
        "Monitor":  "#6366F1",
    }
    dot_color = segment_colors.get(segment, "#6366F1")

    fig = go.Figure()

    # Quadrant fills
    fig.add_shape(type="rect", x0=0, y0=churn_threshold, x1=ltv_threshold, y1=1,
        fillcolor="rgba(239,68,68,0.05)", line=dict(width=0))
    fig.add_shape(type="rect", x0=ltv_threshold, y0=churn_threshold, x1=5000, y1=1,
        fillcolor="rgba(245,158,11,0.05)", line=dict(width=0))
    fig.add_shape(type="rect", x0=ltv_threshold, y0=0, x1=5000, y1=churn_threshold,
        fillcolor="rgba(16,185,129,0.05)", line=dict(width=0))
    fig.add_shape(type="rect", x0=0, y0=0, x1=ltv_threshold, y1=churn_threshold,
        fillcolor="rgba(99,102,241,0.05)", line=dict(width=0))

    # Threshold lines
    fig.add_vline(x=ltv_threshold, line_dash="dot", line_color="rgba(255,255,255,0.15)", line_width=1)
    fig.add_hline(y=churn_threshold, line_dash="dot", line_color="rgba(255,255,255,0.15)", line_width=1)

    # Customer dot
    fig.add_trace(go.Scatter(
        x=[ltv], y=[churn_probability],
        mode="markers",
        marker=dict(
            size=18,
            color=dot_color,
            line=dict(color="white", width=2),
            symbol="circle",
        ),
        hovertemplate=(
            f"<b>LTV:</b> ₹{ltv:,.0f}<br>"
            f"<b>Churn Risk:</b> {churn_probability:.1%}<br>"
            f"<b>Segment:</b> {segment}<extra></extra>"
        ),
        name="Customer"
    ))

    # Quadrant labels
    for (x, y, txt, col) in [
        (200, 0.85, "🚨 Critical",      "rgba(239,68,68,0.7)"),
        (2500, 0.85, "⚠️ High Value At Risk", "rgba(245,158,11,0.7)"),
        (200, 0.05, "🔵 Monitor",       "rgba(99,102,241,0.7)"),
        (2500, 0.05, "🌟 VIP",           "rgba(16,185,129,0.7)"),
    ]:
        fig.add_annotation(x=x, y=y, text=txt, showarrow=False,
            font=dict(color=col, size=11, family="DM Sans"),
            bgcolor="rgba(0,0,0,0)")

    fig.update_layout(
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font=dict(family="DM Sans", color="#94A3B8"),
        xaxis=dict(
            title="Lifetime Value (₹)",
            gridcolor="rgba(255,255,255,0.04)",
            zeroline=False,
            tickfont=dict(size=11),
            range=[0, max(5000, ltv * 1.3)]
        ),
        yaxis=dict(
            title="Churn Probability",
            gridcolor="rgba(255,255,255,0.04)",
            zeroline=False,
            tickformat=".0%",
            tickfont=dict(size=11),
            range=[0, 1]
        ),
        height=340,
        margin=dict(l=10, r=10, t=10, b=10),
        showlegend=False,
        hoverlabel=dict(
            bgcolor="#0F172A",
            bordercolor="#6366F1",
            font=dict(color="white", size=13)
        )
    )

# ---------------------------------------------------
# KPI CARDS
# ---------------------------------------------------

churn_display     = f"{churn_probability*100:.1f}%" if churn_probability is not None else "--"
ltv_display       = f"₹{ltv:,.0f}" if ltv is not None else "--"
revenue_display   = f"₹{revenue_at_risk:,.0f}" if revenue_at_risk is not None else "--"
confidence_display = f"{confidence*100:.1f}%" if confidence is not None else "--"

risk_badge_class = {
    "Low": "badge-low",
    "Medium": "badge-medium",
    "High": "badge-high",
}.get(risk_level, "badge-monitor")

seg_badge_class = {
    "VIP": "badge-vip",
    "Monitor": "badge-monitor",
    "At Risk": "badge-at-risk",
    "Critical": "badge-critical",
}.get(segment, "badge-monitor")

bar_pct = f"{churn_probability*100:.1f}" if churn_probability is not None else "0"
bar_color = "#EF4444" if risk_level == "High" else "#F59E0B" if risk_level == "Medium" else "#10B981"

st.markdown(f"""
<div class="kpi-grid">

  <div class="kpi-card" style="--accent: linear-gradient(90deg, {bar_color}, {bar_color}88);">
    <div class="kpi-label">Churn Risk Score</div>
    <div class="kpi-value">{churn_display}</div>
    <span class="kpi-badge {risk_badge_class}">{risk_level} Risk</span>
    <div class="prob-bar-wrap">
      <div class="prob-bar-bg">
        <div class="prob-bar-fill" style="width:{bar_pct}%; background:{bar_color};"></div>
      </div>
    </div>
  </div>

  <div class="kpi-card" style="--accent: linear-gradient(90deg, #6366F1, #8B5CF6);">
    <div class="kpi-label">Lifetime Value</div>
    <div class="kpi-value">{ltv_display}</div>
    <span class="kpi-badge badge-monitor">Expected value</span>
  </div>

  <div class="kpi-card" style="--accent: linear-gradient(90deg, #F59E0B, #EF4444);">
    <div class="kpi-label">Revenue Exposure</div>
    <div class="kpi-value">{revenue_display}</div>
    <span class="kpi-badge badge-at-risk">Revenue at risk</span>
  </div>

  <div class="kpi-card" style="--accent: linear-gradient(90deg, #10B981, #6366F1);">
    <div class="kpi-label">Customer Segment</div>
    <div class="kpi-value" style="font-size:22px; padding-top:4px;">{segment}</div>
    <span class="kpi-badge {seg_badge_class}">Strategic class</span>
  </div>

  <div class="kpi-card" style="--accent: linear-gradient(90deg, #8B5CF6, #6366F1);">
    <div class="kpi-label">Model Confidence</div>
    <div class="kpi-value">{confidence_display}</div>
    <span class="kpi-badge badge-monitor">Prediction score</span>
  </div>

</div>
""", unsafe_allow_html=True)

# ---------------------------------------------------
# MAIN CONTENT
# ---------------------------------------------------

if not analyze:
    st.markdown("""
    <div class="section-card">
      <div class="empty-state">
        <div class="empty-icon">🎯</div>
        <div class="empty-text">No Assessment Yet</div>
        <div class="empty-sub">Configure customer details in the sidebar and click <strong>Assess Customer</strong> to generate the risk intelligence report.</div>
      </div>
    </div>
    """, unsafe_allow_html=True)

else:
    col_chart, col_rec = st.columns([3, 2], gap="large")

    with col_chart:
        st.markdown("""
        <div class="section-card" style="padding-bottom: 8px;">
            <div class="section-title">📍 Risk Matrix Position</div>
        """, unsafe_allow_html=True)
        st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": False})
        st.markdown("</div>", unsafe_allow_html=True)

    with col_rec:
        # Risk drivers
        st.markdown('<div class="section-card">', unsafe_allow_html=True)
        st.markdown('<div class="section-title">⚡ Risk Drivers</div>', unsafe_allow_html=True)

        if reasons:
            drivers_html = "".join([
                f'<div class="driver-tag"><span>{icon}</span><span>{label}</span></div>'
                for icon, label in reasons
            ])
            st.markdown(f'<div style="display:flex; flex-wrap:wrap; gap:4px;">{drivers_html}</div>', unsafe_allow_html=True)
        else:
            st.markdown('<p style="color:#475569; font-size:14px;">✅ No major risk drivers detected.</p>', unsafe_allow_html=True)

        st.markdown('<hr class="styled-divider">', unsafe_allow_html=True)

        # Recommendation
        if segment == "Critical":
            st.markdown(f"""
            <div class="rec-critical">
              <div class="rec-title" style="color:#F87171;">🚨 Critical Risk Customer</div>
              <div class="rec-item"><div class="rec-dot" style="background:#EF4444;"></div>Immediate retention call required</div>
              <div class="rec-item"><div class="rec-dot" style="background:#EF4444;"></div>Offer special loyalty discount</div>
              <div class="rec-item"><div class="rec-dot" style="background:#EF4444;"></div>Assign dedicated account manager</div>
              <div class="rec-item"><div class="rec-dot" style="background:#EF4444;"></div>Escalate to customer success team</div>
            </div>
            """, unsafe_allow_html=True)

        elif segment == "At Risk":
            st.markdown(f"""
            <div class="rec-at-risk">
              <div class="rec-title" style="color:#FBBF24;">⚠️ Elevated Churn Risk</div>
              <div class="rec-item"><div class="rec-dot" style="background:#F59E0B;"></div>Launch targeted retention campaign</div>
              <div class="rec-item"><div class="rec-dot" style="background:#F59E0B;"></div>Offer loyalty incentives or discounts</div>
              <div class="rec-item"><div class="rec-dot" style="background:#F59E0B;"></div>Upgrade to annual contract offer</div>
              <div class="rec-item"><div class="rec-dot" style="background:#F59E0B;"></div>Follow up within 30 days</div>
            </div>
            """, unsafe_allow_html=True)

        elif segment == "VIP":
            st.markdown(f"""
            <div class="rec-vip">
              <div class="rec-title" style="color:#34D399;">🌟 High Value Customer</div>
              <div class="rec-item"><div class="rec-dot" style="background:#10B981;"></div>Upsell premium plans & add-ons</div>
              <div class="rec-item"><div class="rec-dot" style="background:#10B981;"></div>Introduce referral reward program</div>
              <div class="rec-item"><div class="rec-dot" style="background:#10B981;"></div>Provide exclusive VIP benefits</div>
              <div class="rec-item"><div class="rec-dot" style="background:#10B981;"></div>Maintain proactive relationship</div>
            </div>
            """, unsafe_allow_html=True)

        else:
            st.markdown(f"""
            <div class="rec-monitor">
              <div class="rec-title" style="color:#A5B4FC;">✅ Stable Customer</div>
              <div class="rec-item"><div class="rec-dot" style="background:#6366F1;"></div>Continue standard engagement</div>
              <div class="rec-item"><div class="rec-dot" style="background:#6366F1;"></div>Monitor account periodically</div>
              <div class="rec-item"><div class="rec-dot" style="background:#6366F1;"></div>Watch for behavioral changes</div>
              <div class="rec-item"><div class="rec-dot" style="background:#6366F1;"></div>Eligible for upsell exploration</div>
            </div>
            """, unsafe_allow_html=True)

        st.markdown('</div>', unsafe_allow_html=True)
