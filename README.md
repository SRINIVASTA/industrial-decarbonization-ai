# 🏭 Industrial Decarbonization AI Platform

An enterprise-grade, interactive machine learning platform designed to **track, optimize, and reduce carbon emissions** across heavy manufacturing sectors and supply chain networks. 

This platform leverages data-driven **Physics-Enforced Process Control (PEPC)** models to analyze factory telemetry, flag mechanical degradation anomalies, optimize fuel-to-power parameters via simulated closed-loop feedback, and automate dual-currency ESG regulatory compliance auditing.

---

## 👥 Project Information & Leadership

* **Created & Developed By**: **Srinivasa**
* **Project Scope**: Industrial AI Solution for ESG Compliance and Real-Time SCADA Optimization
* **Version**: 11.0 (Production Stable Release)

---

## 🗺️ Architectural Evolution History (Why v11.0?)

This platform has undergone 11 major structural and architectural rewrites during its development lifecycle to reach a production-ready edge state:


| Major Version | Architectural Shift | Key Engineering Milestone |
| :--- | :--- | :--- |
| **v1.0** | Initial Concept | Basic Python tracking connecting to live web dataset structures. |
| **v2.0** | Network Resilience | Added a `try/except` network fallback layer to prevent internet timeouts. |
| **v3.0** | Operational Physics | Corrected randomized synthetic metrics to follow true industrial physical scaling laws. |
| **v4.0** | Data Cleansing | Automated the extraction of unscaled anomalies out of model calibration loops. |
| **v5.0** | UI Layout Engine | Shifted from terminal outputs to a live dashboard interface using Streamlit. |
| **v6.0** | Market Adaptability | Programmed dynamic hourly grid utility spikes instead of using fixed power rates. |
| **v7.0** | High-Precision ML | Dropped blind unsupervised isolation arrays for a **Physics-Enforced Residual Error Check**. |
| **v8.0** | Hardware Messaging | Integrated network sockets using a multi-threaded **Live MQTT Broker** framework. |
| **v9.0** | Industrial PLC Context | Integrated standard 16-bit physical register memory maps via **Modbus TCP Loops**. |
| **v10.0** | Version Futureproofing | Rewrote the core using loopback abstractions to handle breaking third-party API updates. |
| **v11.0** | **Production Immutable Audit** | Tied in an **SQLite persistence database engine** to store unalterable audit histories. |

---

## 📈 Platform Architecture Flow

The system coordinates continuous, automated workflows split across three distinct operational layers:

1. **Dynamic Tracking Layer**: Pulls live historical industrial benchmarks from **Our World in Data (OWID)** [🎯]. It screens real-time plant SCADA registers using a physics-informed model, evaluating actual outputs against statistical operation limits.
2. **Process Optimization Layer**: Evaluates multivariate data points (Throughput vs. Grid Power Demand) using Linear Regression to determine optimal production targets. It identifies load-shifting opportunities to balance fluctuating energy markets.
3. **Automated Reduction & SCADA Override Layer**: If actual factory emissions exceed expected physics baselines, the engine triggers an automated loop override, simulating PLC throttling commands to mitigate excess carbon tax penalties.

---

## ✨ Core System Features

* 📊 **Live SCADA Ingest Dashboard**: Interactive visualization tracking live raw metrics (Throughput in T/h, Power Demand in kW, and Measured Emissions in kg CO2).
* 🚨 **Physics-Enforced Anomaly Intercept**: Eliminates false negatives from unscaled models by validating actual emissions against historical regression memory to catch physical asset leaks instantly.
* 💵 **Dual-Currency Financial Audit Fabric**: Translates environmental waste and optimization savings metrics simultaneously into **US Dollars ($)** and **Indian Rupees (₹)** in real-time.
* 📈 **Time-Series Trend Profiler**: Interactive 24-hour historical grid trend charts plotting operational loads against carbon emissions tracking lines.
* 📥 **One-Click Regulatory Compliance Export**: Generates unalterable, structured audit sheets downloadable as standard `.CSV` payloads to back up annual corporate ESG tax reporting.

---

## 🛠️ Step-by-Step Installation & Deployment

You can run this platform locally or deploy it to a live cloud web server in under 5 minutes.

### 1. Prerequisites & Cloning
Ensure you have Python 3.9+ installed. Clone this repository onto your workstation machine or cloud server environment:
```bash
git clone https://github.com
cd industrial-decarbonization-ai
```

### 2. Install Dependencies
Install the required analytical and user interface packages using pip:
```bash
pip install -r requirements.txt
```
*(Your `requirements.txt` must contain: `pandas`, `numpy`, `scikit-learn`, and `streamlit`)*

### 3. Run the Application Locally
Launch the application server on your localhost loopback interface:
```bash
streamlit run app.py
```
This command automatically runs a background web container and drops a live link (`http://localhost:8501`) directly inside your standard internet browser windows.

---

## 🚀 Cloud Deployment (Streamlit Community Cloud)

To make your system live on a public web server:
1. Push your completed files (`app.py`, `requirements.txt`, and `README.md`) to your GitHub repository.
2. Head to [share.streamlit.io](https://industrial-decarbonization-ai-augymefrzm4gyhyikn6x3z.streamlit.app/) and authorize access using your GitHub credentials.
3. Click **"New App"**, pick your repository, specify the branch (`main`), and target your UI application script path (`app.py`).
4. Click **"Deploy!"**

Streamlit Cloud will configure the network dependencies and assign a permanent public URL (`https://streamlit.app`) to your analytics console dashboard.

---

## 💼 Stress-Test Evaluation Guide

To demonstrate the real-time closed-loop decision capabilities of the AI platform:
1. Open your live app dashboard web page.
2. Toggle the sidebar inputs to alter variables like **Global Carbon Taxes**, **Grid Utility Rates**, or **AI Load Shifting Target Pcts**. Notice the immediate changes in financial output yields.
3. Turn on the **"🚨 Force Simulated Hardware Failure / Leak Event"** switch on the central control hub.
4. The system will immediately flag a **Mechanical Breakdown Alert**, log the unexpected carbon leakage rate, and calculate the exact dollar and rupee tax penalty liabilities.
5. Review the updated line chart graph and click **"📥 Download Custom Stress-Test Audit Report (.CSV)"** to pull the system sheet straight onto your machine hardware storage.

---

## 📊 Data Transparency Notes
Historical baseline data streams loaded within this application are compiled from the **Our World in Data (OWID)** public global greenhouse gas database repository [🎯], derived from consensus metrics published by the *Global Carbon Project* and *Jones et al. (2024)*. If network barriers isolate your environment, the code activates local data frames to preserve continuous uptime.
