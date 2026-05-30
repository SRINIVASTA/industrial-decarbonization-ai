import streamlit as st
import pandas as pd
import numpy as np
import requests
import time
from datetime import datetime
import pytz
from sklearn.linear_model import LinearRegression
from streamlit_autorefresh import st_autorefresh

st.set_page_config(page_title="Industrial Decarbonization AI Engine", layout="wide")

# --- CONFIGURE AUTOMATED UI REFRESH (Every 2000ms / 2 Seconds) ---
st_autorefresh(interval=2000, limit=None, key="scada_telemetry_counter")

st.title("🏭 Industrial Decarbonization AI Platform")
st.subheader("Interactive Continuous SCADA Telemetry Logging & Cost Audit")

USD_TO_INR = 83.50  # 1 USD = ₹83.50 INR

# ====================================================
# 🎛️ INTERACTIVE SIDEBAR SLIDERS & CONTROLS
# ====================================================
st.sidebar.header("Regulatory & Economic Inputs")
CARBON_TAX_PER_TON = st.sidebar.slider("Global Carbon Tax ($ / Metric Ton)", 0.0, 250.0, 85.0, 5.0)
ENERGY_COST_PER_KWH = st.sidebar.slider("Grid Electricity Rate ($ / kWh)", 0.05, 0.40, 0.12, 0.01)

st.sidebar.markdown("---")
st.sidebar.header("Operational Constraints")
LOAD_REDUCTION_PCT = st.sidebar.slider("AI Load Shifting Target (%)", 5, 40, 15, 5)
LEAK_THRESHOLD_KG = st.sidebar.slider("AI Alarm Leak Sensitivity (kg CO2)", 20, 200, 100, 10)

# ----------------------------------------------------
# STAGE 1: Live Data Baseline Fetching (with Fallback)
# ----------------------------------------------------
st.sidebar.markdown("---")
try:
    df_global = pd.read_csv("https://githubusercontent.com", timeout=5)
    recent_global = df_global[df_global['country'] == 'World'][['year', 'cement_co2', 'industry_co2']].tail(5)
    st.sidebar.success("✅ Connected to Our World in Data live feed")
except:
    st.sidebar.warning("⚠️ Using local baseline data (Live URL unreachable)")
    recent_global = pd.DataFrame({
        'year': [2021, 2022, 2023, 2024, 2025],
        'cement_co2': [1610.4, 1615.1, 1622.3, 1630.0, 1635.8],
        'industry_co2': [11450.2, 11520.8, 11600.1, 11580.4, 11610.2]
    })
st.sidebar.dataframe(recent_global.set_index('year'))

# ----------------------------------------------------
# STAGE 2: Machine Learning Process Calibration
# ----------------------------------------------------
extended_time_index = pd.date_range(start="2026-04-28 00:00", periods=720, freq="h")
np.random.seed(42)
historical_throughput = np.random.normal(loc=50, scale=5, size=720)
historical_power = np.random.normal(loc=500, scale=50, size=720)
historical_emissions = 50 + (historical_power * 0.6) + (historical_throughput * 2.0) + np.random.normal(loc=0, scale=5, size=720)

training_df = pd.DataFrame({
    "throughput_tons": historical_throughput,
    "power_draw_kw": historical_power,
    "direct_emissions_kg": historical_emissions
}, index=extended_time_index)

optimizer_model = LinearRegression()
optimizer_model.fit(training_df[['throughput_tons', 'power_draw_kw']], training_df['direct_emissions_kg'])

# ====================================================
# 💾 PERSISTENT ROW-BASED DATA LOGGER STORAGE
# ====================================================
# Creates a continuous rolling table that stores fresh rows every 2 seconds
if "scada_logger_db" not in st.session_state:
    st.session_state.scada_logger_db = pd.DataFrame(columns=[
        "Timestamp (IST)", "Live Throughput (T/h)", "Live Power Demand (kW)", 
        "Measured Emissions (kg CO2)", "AI Predicted Baseline (kg)", 
        "Emissions Residual Gap (kg)", "Carbon Tax ($/Ton)", 
        "Electricity Rate ($/kWh)", "Hourly Savings (USD)", "Hourly Savings (INR)"
    ])

# ----------------------------------------------------
# STAGE 3: Telemetry Stream Dashboard Setup
# ----------------------------------------------------
col_btn1, col_btn2 = st.columns(2)
with col_btn1:
    st.success("🔄 **System Active:** Appending a fresh data row every 2 seconds.")
with col_btn2:
    trigger_leak = st.toggle("🚨 Force Simulated Hardware Failure / Leak Event", value=False)

ist_timezone = pytz.timezone('Asia/Kolkata')
current_ist_time = datetime.now(ist_timezone).strftime('%Y-%m-%d %H:%M:%S')

# Generate live metric drift
live_drift = (time.time() % 10) - 5  
current_throughput = float(np.random.uniform(51.0, 55.0) + (live_drift * 0.1))
current_power = float(np.random.uniform(490.0, 540.0) + live_drift)

if trigger_leak:
    current_emissions = 999.0
else:
    current_emissions = float(50 + (current_power * 0.6) + (current_throughput * 2.0) + np.random.uniform(-3, 3))

# Core Machine Learning Inferences
input_features = pd.DataFrame([[current_throughput, current_power]], columns=['throughput_tons', 'power_draw_kw'])
normal_predicted = float(optimizer_model.predict(input_features)[0])
residual_error = current_emissions - normal_predicted

reduction_factor = 1.0 - (LOAD_REDUCTION_PCT / 100.0)
optimized_features = pd.DataFrame([[current_throughput, current_power * reduction_factor]], columns=['throughput_tons', 'power_draw_kw'])
optimized_predicted = float(optimizer_model.predict(optimized_features)[0])
carbon_saved_kg = normal_predicted - optimized_predicted

# Financial Formulations
financial_savings_usd = ((current_power * (LOAD_REDUCTION_PCT / 100.0)) * ENERGY_COST_PER_KWH) + ((carbon_saved_kg / 1000.0) * CARBON_TAX_PER_TON)
financial_savings_inr = financial_savings_usd * USD_TO_INR

# --- APPEND RECENT ROW HORIZONTALLY TO MEMORY STORAGE ---
new_audit_row = pd.DataFrame([{
    "Timestamp (IST)": current_ist_time,
    "Live Throughput (T/h)": round(current_throughput, 2),
    "Live Power Demand (kW)": round(current_power, 2),
    "Measured Emissions (kg CO2)": round(current_emissions, 2),
    "AI Predicted Baseline (kg)": round(normal_predicted, 2),
    "Emissions Residual Gap (kg)": round(residual_error, 2),
    "Carbon Tax ($/Ton)": CARBON_TAX_PER_TON,
    "Electricity Rate ($/kWh)": ENERGY_COST_PER_KWH,
    "Hourly Savings (USD)": round(financial_savings_usd, 2),
    "Hourly Savings (INR)": round(financial_savings_inr, 2)
}])

st.session_state.scada_logger_db = pd.concat([st.session_state.scada_logger_db, new_audit_row], ignore_index=True)

# Keep only the latest 50 entries to keep memory usage balanced
if len(st.session_state.scada_logger_db) > 50:
    st.session_state.scada_logger_db = st.session_state.scada_logger_db.tail(50)

# Layout KPI Card Deck Display
m_time, m1, m2, m3 = st.columns(4)
m_time.metric("Indian Local Time (IST)", current_ist_time)
m1.metric("Live Throughput", f"{current_throughput:.1f} T/h")
m2.metric("Live Power Demand", f"{current_power:.1f} kW")
m3.metric("Measured Emissions", f"{current_emissions:.1f} kg CO2")

st.markdown("---")

if residual_error > LEAK_THRESHOLD_KG:
    penalty_usd = (residual_error / 1000.0) * CARBON_TAX_PER_TON
    penalty_inr = penalty_usd * USD_TO_INR
    st.error(f"🚨 **CRITICAL ALARM: Leakage Detected!** Liability: **${penalty_usd:.2f}/hr** (approx. **₹{penalty_inr:.2f}/hr**)")
else:
    st.success("✅ **Operations Stable**: Footprint conforms to physics parameters.")

# ====================================================
# 📈 FEATURE A: DYNAMIC REAL-TIME LINE CHART
# ====================================================
st.markdown("### 📈 Real-Time Rolling Shift Trend Tracking")
# This chart maps your live session's exact data history directly from the logging database
chart_df = st.session_state.scada_logger_db.set_index("Timestamp (IST)")[["Live Power Demand (kW)", "Measured Emissions (kg CO2)"]]
st.line_chart(chart_df)

# ====================================================
# 💾 FEATURE B: ROW-BASED COMPLIANCE EXPORT LEDGER
# ====================================================
st.markdown("### 💾 Regulatory Compliance & ESG Data Export (Horizontal Registry)")

# Display the horizontal logging database directly on the UI screen
st.dataframe(st.session_state.scada_logger_db, use_container_width=True)

csv_data = st.session_state.scada_logger_db.to_csv(index=False).encode('utf-8')

st.download_button(
    label="📥 Download Continuous Row-Based Audit Report (.CSV)",
    data=csv_data,
    file_name=f"esg_rolling_compliance_audit.csv",
    mime="text/csv",
    use_container_width=True
)
