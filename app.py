import streamlit as st
import pandas as pd
import numpy as np
import requests
from sklearn.linear_model import LinearRegression

st.set_page_config(page_title="Industrial Decarbonization AI Engine", layout="wide")
st.title("🏭 Industrial Decarbonization AI Platform")
st.subheader("Interactive Stress-Testing: Tracking, Optimization, & Financial Cost Audit")

# ====================================================
# EXCHANGE RATE LAYER (Static baseline for dual-currency)
# ====================================================
USD_TO_INR = 83.50  # 1 USD = ₹83.50 INR

# ====================================================
# 🎛️ INTERACTIVE SIDEBAR SLIDERS & CONTROLS
# ====================================================
st.sidebar.header("Regulatory & Economic Inputs")
CARBON_TAX_PER_TON = st.sidebar.slider(
    "Global Carbon Tax ($ / Metric Ton)", 
    min_value=0.0, max_value=250.0, value=85.0, step=5.0
)
ENERGY_COST_PER_KWH = st.sidebar.slider(
    "Grid Electricity Rate ($ / kWh)", 
    min_value=0.05, max_value=0.40, value=0.12, step=0.01
)

st.sidebar.markdown("---")
st.sidebar.header("Operational Constraints")
LOAD_REDUCTION_PCT = st.sidebar.slider(
    "AI Load Shifting Target (%)", 
    min_value=5, max_value=40, value=15, step=5
)
LEAK_THRESHOLD_KG = st.sidebar.slider(
    "AI Alarm Leak Sensitivity (kg CO2)", 
    min_value=20, max_value=200, value=100, step=10
)

# ----------------------------------------------------
# STAGE 1: Live Data Baseline Fetching (with Fallback)
# ----------------------------------------------------
st.sidebar.markdown("---")
owid_url = "https://githubusercontent.com"
try:
    df_global = pd.read_csv(owid_url, timeout=5)
    recent_global = df_global[df_global['country'] == 'World'][['year', 'cement_co2', 'industry_co2']].tail(5)
    st.sidebar.success("✅ Connected to Our World in Data live feed")
except:
    st.sidebar.warning("⚠️ Using local baseline data (Live URL unreachable)")
    fallback_data = {
        'year': [2021, 2022, 2023, 2024, 2025],
        'cement_co2': [1610.4, 1615.1, 1622.3, 1630.0, 1635.8],
        'industry_co2': [11450.2, 11520.8, 11600.1, 11580.4, 11610.2]
    }
    recent_global = pd.DataFrame(fallback_data)

st.sidebar.markdown("**Global Industrial Baselines:**")
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

# ----------------------------------------------------
# STAGE 3: Telemetry Stream Dashboard Setup
# ----------------------------------------------------
col_btn1, col_btn2 = st.columns(2)
with col_btn1:
    if st.button("🔄 Poll Live SCADA Sensors"):
        st.rerun()
with col_btn2:
    trigger_leak = st.toggle("🚨 Force Simulated Hardware Failure / Leak Event", value=False)

# Simulate current streaming values
current_throughput = float(np.random.normal(loc=53, scale=2))
current_power = float(np.random.normal(loc=515, scale=25))

if trigger_leak:
    current_emissions = 999.0
else:
    current_emissions = float(50 + (current_power * 0.6) + (current_throughput * 2.0) + np.random.normal(loc=0, scale=2))

# Run the AI Optimization Math using the Sliders' Inputs
input_features = pd.DataFrame([[current_throughput, current_power]], columns=['throughput_tons', 'power_draw_kw'])
normal_predicted = float(optimizer_model.predict(input_features))
residual_error = current_emissions - normal_predicted

# Calculate dynamic reduction using the user's slider input
reduction_factor = 1.0 - (LOAD_REDUCTION_PCT / 100.0)
optimized_features = pd.DataFrame([[current_throughput, current_power * reduction_factor]], columns=['throughput_tons', 'power_draw_kw'])
optimized_predicted = float(optimizer_model.predict(optimized_features))

carbon_saved_kg = normal_predicted - optimized_predicted

# FINANCIAL DUAL-CURRENCY ENGINE CORE
financial_savings_usd = ((current_power * (LOAD_REDUCTION_PCT / 100.0)) * ENERGY_COST_PER_KWH) + ((carbon_saved_kg / 1000.0) * CARBON_TAX_PER_TON)
financial_savings_inr = financial_savings_usd * USD_TO_INR

# Layout Metrics Display
m1, m2, m3 = st.columns(3)
m1.metric("Live Throughput", f"{current_throughput:.1f} T/h")
m2.metric("Live Power Demand", f"{current_power:.1f} kW")
m3.metric("Measured Emissions", f"{current_emissions:.1f} kg CO2")

st.markdown("---")

# Conditional Layout Alerts with Dual-Currency Output
if residual_error > LEAK_THRESHOLD_KG:
    penalty_usd = (residual_error / 1000.0) * CARBON_TAX_PER_TON
    penalty_inr = penalty_usd * USD_TO_INR
    st.error(f"🚨 **CRITICAL ALARM: Mechanical Breakdown Isolated!**  \n"
             f"-> Unexplained Emissions Leak: +{residual_error:.2f} kg CO2  \n"
             f"-> Added Financial Liability: **${penalty_usd:.2f} / hr** (approx. **    ₹{penalty_inr:.2f} / hr**) under a **${CARBON_TAX_PER_TON:.2f}/Ton** tax scheme.")
else:
    st.success("✅ **Operations Stable**: Carbon footprint conforms directly to physical parameters.")

st.info(f"💡 **AI Load Shifting Recommendation ({LOAD_REDUCTION_PCT}% Power Drop Target):**  \n"
        f"By shifting hardware parameters by **{LOAD_REDUCTION_PCT}%**, you will mitigate **{carbon_saved_kg:.2f} kg CO2/hr**.  \n"
        f"This yields a combined financial savings of **${financial_savings_usd:.2f} / hr** (approx. **₹{financial_savings_inr:.2f} / hr**) through reduced utility bills and avoided carbon taxes.")

# ====================================================
# 📈 FEATURE A: INTERACTIVE TIME-SERIES LINE CHART
# ====================================================
st.markdown("### 📈 24-Hour Historical Shift Trend Tracking")

# Generate mock data for the last 24 hours of plant runtime
chart_time_index = pd.date_range(end=pd.Timestamp.now(), periods=24, freq="h")
np.random.seed(101)
chart_throughput = np.random.normal(loc=52, scale=2, size=24)
chart_power = np.random.normal(loc=510, scale=30, size=24)
chart_emissions = 50 + (chart_power * 0.6) + (chart_throughput * 2.0) + np.random.normal(loc=0, scale=3, size=24)

# Inject the leak event into the chart history if the user toggled it
if trigger_leak:
    chart_emissions[-1] = 999.0  # Force the final data point to match the leak alert

# Package into clean chart rendering dataframe
chart_df = pd.DataFrame({
    "Power Draw (kW)": chart_power,
    "Actual Emissions (kg CO2)": chart_emissions
}, index=chart_time_index)

# Render interactive line graph
st.line_chart(chart_df)


# ====================================================
# 💾 FEATURE B: AUTOMATED AUDIT SHEET DATA EXPORT
# ====================================================
st.markdown("### 💾 Regulatory Compliance & ESG Data Export")

# Compile current running parameters into a downloadable pandas layout
export_df = pd.DataFrame({
    "Metric/Parameter Name": [
        "Timestamp", "Live Throughput (T/h)", "Live Power Demand (kW)", 
        "Measured Emissions (kg CO2)", "AI Predicted Emissions Baseline (kg)", 
        "Emissions Residual Gap (kg)", "Carbon Tax Setting ($/Ton)", 
        "Electricity Rate Setting ($/kWh)", "Hourly Dynamic Financial Savings (USD)", 
        "Hourly Dynamic Financial Savings (INR)"
    ],
    "Recorded System Value": [
        pd.Timestamp.now().strftime('%Y-%m-%d %H:%M:%S'), f"{current_throughput:.2f}", f"{current_power:.2f}",
        f"{current_emissions:.2f}", f"{normal_predicted:.2f}", f"{residual_error:.2f}", 
        f"{CARBON_TAX_PER_TON:.2f}", f"{ENERGY_COST_PER_KWH:.2f}", f"{financial_savings_usd:.2f}", 
        f"{financial_savings_inr:.2f}"
    ]
})

# Display a preview of the audit spreadsheet
st.dataframe(export_df, use_container_width=True)

# Convert dataframe to standard download string encoding
csv_data = export_df.to_csv(index=False).encode('utf-8')

# Render the native Streamlit file download button interface
st.download_button(
    label="📥 Download Custom Stress-Test Audit Report (.CSV)",
    data=csv_data,
    file_name=f"esg_decarbonization_audit_{pd.Timestamp.now().strftime('%Y%m%d_%H%M%S')}.csv",
    mime="text/csv",
    help="Click to download an unalterable system sheet mapping your custom economic and physical stress tests for ESG audits."
)
