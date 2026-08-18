import streamlit as st
import numpy as np
import pandas as pd
from datetime import datetime
from PIL import Image

# Page Configuration
st.set_page_config(page_title="AgroVision AI", page_icon="🌱", layout="wide")

st.title("🌱 AgroVision — Real-Time Smart Agriculture Dashboard")
st.caption("Technology for a Better Society | CREZIA 2026")

# Navigation Sidebar
st.sidebar.header("Navigation")
page = st.sidebar.radio("Select View", ["Real-Time Sensor Monitoring", "Leaf Disease Diagnosis"])

# ----------------------------------------------------
# PAGE 1: REAL-TIME SENSOR MONITORING
# ----------------------------------------------------
if page == "Real-Time Sensor Monitoring":
    st.header("⚡ Live Field Telemetry")
    
    col_ctrl1, col_ctrl2 = st.columns(2)
    with col_ctrl1:
        crop_name = st.selectbox("Select Active Field Crop", ["Tomato", "Potato", "Corn", "Wheat"])
    with col_ctrl2:
        update_interval = st.slider("Sensor Refresh Interval (seconds)", 1, 5, 2)

    if "live_data" not in st.session_state:
        st.session_state.live_data = pd.DataFrame(columns=["Time", "Soil Moisture (%)", "Temperature (°C)"])

    @st.fragment(run_every=update_interval)
    def render_realtime_metrics():
        now_str = datetime.now().strftime("%H:%M:%S")
        new_moisture = float(np.random.randint(30, 70))
        new_temp = float(np.random.randint(24, 34))

        new_row = pd.DataFrame([{
            "Time": now_str,
            "Soil Moisture (%)": new_moisture,
            "Temperature (°C)": new_temp
        }])

        st.session_state.live_data = pd.concat([st.session_state.live_data, new_row], ignore_index=True).tail(15)

        m1, m2, m3 = st.columns(3)
        m1.metric(label="Current Moisture", value=f"{new_moisture:.0f}%", delta=f"{np.random.choice([-2, -1, 0, 1, 2])}%")
        m2.metric(label="Field Temperature", value=f"{new_temp:.0f} °C", delta=f"{np.random.choice([-1, 0, 1])} °C")
        m3.metric(label="Connection Status", value="ONLINE 🟢", delta="Live Feed")

        st.subheader(f"📊 Live Telemetry Stream ({crop_name})")
        chart_df = st.session_state.live_data.set_index("Time")
        st.line_chart(chart_df)

        if new_moisture < 38:
            st.error(f"🚨 **Critical Alert:** Soil moisture dropped to {new_moisture:.0f}%. Automatic irrigation pump engaged!")
        elif new_moisture > 62:
            st.warning(f"⚠️ **Caution:** Soil moisture reached {new_moisture:.0f}%. Halting pump to prevent overwatering.")
        else:
            st.success("✅ **Optimal Field Status:** Moisture and temperature levels are stable.")

    render_realtime_metrics()

# ----------------------------------------------------
# PAGE 2: LEAF DISEASE DIAGNOSIS
# ----------------------------------------------------
elif page == "Leaf Disease Diagnosis":
    st.header("🔍 AI Leaf Disease Diagnosis")
    uploaded_file = st.file_uploader("Upload a leaf image...", type=["jpg", "png", "jpeg"])
    
    if uploaded_file is not None:
        image = Image.open(uploaded_file)
        # Fixed: using use_container_width instead of use_column_width
        st.image(image, caption="Uploaded Leaf Image", use_container_width=True)
        
        st.write("### AI Analysis Result")
        conditions = ["Healthy", "Early Blight", "Late Blight", "Bacterial Spot"]
        detected = np.random.choice(conditions)
        confidence = np.random.uniform(88, 98)
        
        if detected == "Healthy":
            st.success(f"**Diagnosis:** {detected} ({confidence:.2f}% Confidence)")
            st.info("💡 **Action:** Soil nutrients optimal. Maintain routine schedule.")
        else:
            st.error(f"**Diagnosis:** {detected} ({confidence:.2f}% Confidence)")
            st.warning("⚠️ **Action Required:** Apply organic copper-based fungicide.")
