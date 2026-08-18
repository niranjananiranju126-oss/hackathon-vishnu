# -*- coding: utf-8 -*-
"""
Created on Tue Aug 18 10:56:06 2026

@author: niran
"""

import streamlit as st
import numpy as np
import pandas as pd
from PIL import Image

st.set_page_config(page_title="AgroVision AI", page_icon="🌱", layout="wide")

st.title("🌱 AgroVision — AI Crop Health Optimizer")
st.subheader("Technology for a Better Society | Smart Agriculture & AI")

# Sidebar - Input Selection
st.sidebar.header("Navigation")
page = st.sidebar.radio("Go to", ["Disease Detection", "Crop Analytics"])

if page == "Disease Detection":
    st.header("🔍 Leaf Disease Diagnosis")
    uploaded_file = st.file_uploader("Upload a leaf image...", type=["jpg", "png", "jpeg"])
    
    if uploaded_file is not None:
        image = Image.open(uploaded_file)
        st.image(image, caption="Uploaded Leaf Image", use_column_width=True)
        
        # Simulated AI Classification Model Logic
        st.write("### AI Analysis Result")
        
        # Placeholder prediction logic
        conditions = ["Healthy", "Early Blight", "Late Blight", "Bacterial Spot"]
        detected = np.random.choice(conditions)
        confidence = np.random.uniform(85, 98)
        
        if detected == "Healthy":
            st.success(f"**Diagnosis:** {detected} ({confidence:.2f}% Confidence)")
            st.info("💡 **Recommendation:** Keep maintaining normal water and fertilizer schedules.")
        else:
            st.error(f"**Diagnosis:** {detected} ({confidence:.2f}% Confidence)")
            st.warning("⚠️ **Recommended Action:**")
            st.write("* Apply targeted organic fungicide.")
            st.write("* Ensure adequate spacing between crops to reduce humidity.")

elif page == "Crop Analytics":
    st.header("📊 Dynamic Farm Health & Soil Analytics")
    
    # 1. Interactive Inputs for Live Field Simulation
    st.subheader("⚙️ Field Parameters")
    col1, col2 = st.columns(2)
    
    with col1:
        selected_crop = st.selectbox(
            "Select Crop Type", 
            ["Tomato", "Potato", "Corn", "Wheat"]
        )
        base_moisture = st.slider("Target Moisture Level (%)", 20, 80, 50)

    with col2:
        days_to_predict = st.slider("Forecast Range (Days)", 3, 14, 7)
        weather_condition = st.selectbox(
            "Expected Weather Trend", 
            ["Normal", "Sunny/Dry", "Rainy"]
        )

    # 2. Dynamic Data Generation based on user inputs
    np.random.seed(42)  # For consistent relative variance
    days = [f"Day {i}" for i in range(1, days_to_predict + 1)]
    
    # Adjust moisture and temperature trends based on selected weather
    if weather_condition == "Sunny/Dry":
        moisture = [max(10, base_moisture - (i * 3) + np.random.randint(-2, 3)) for i in range(days_to_predict)]
        temp = [30 + np.random.randint(0, 5) for _ in range(days_to_predict)]
    elif weather_condition == "Rainy":
        moisture = [min(100, base_moisture + (i * 2) + np.random.randint(1, 6)) for i in range(days_to_predict)]
        temp = [24 + np.random.randint(-2, 2) for _ in range(days_to_predict)]
    else:
        moisture = [base_moisture + np.random.randint(-5, 6) for _ in range(days_to_predict)]
        temp = [27 + np.random.randint(-2, 3) for _ in range(days_to_predict)]

    df = pd.DataFrame({
        "Day": days,
        "Soil Moisture (%)": moisture,
        "Temperature (°C)": temp
    })

    # 3. Dynamic Visualizations
    st.write(f"### {selected_crop} Field Trends ({days_to_predict}-Day Analysis)")
    st.line_chart(df.set_index("Day"))

    # 4. Live Automated Insights & Actionable Alerts
    st.subheader("💡 Real-time Automated Recommendations")
    avg_moisture = np.mean(moisture)
    
    if avg_moisture < 35:
        st.error(f"🚨 **Alert:** Average moisture ({avg_moisture:.1f}%) is low for **{selected_crop}**. Immediate irrigation scheduled.")
    elif avg_moisture > 65:
        st.warning(f"⚠️ **Warning:** Soil moisture ({avg_moisture:.1f}%) is high. Halt automated irrigation to prevent root rot.")
    else:
        st.success(f"✅ **Optimal Conditions:** Soil moisture ({avg_moisture:.1f}%) is ideal for **{selected_crop}** growth.")
