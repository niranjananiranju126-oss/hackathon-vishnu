import sqlite3
import pandas as pd
import requests
import streamlit as st

st.set_page_config(page_title="ScamShield AI Console", page_icon="🛡️", layout="wide")

st.title("🛡️ ScamShield AI — Control Panel & Real-Time Telemetry")
st.caption("Live threat monitoring, dynamic intent analysis, and automated call interception")

# Fetch SQLite database logs
def get_logs():
    try:
        conn = sqlite3.connect("call_logs.db")
        df = pd.read_sql_query("SELECT * FROM logs ORDER BY timestamp DESC", conn)
        conn.close()
        return df
    except Exception:
        return pd.DataFrame()

df = get_logs()

# Telemetry Metrics Header
col_metric1, col_metric2, col_metric3 = st.columns(3)
with col_metric1:
    st.metric(label="Total Calls Intercepted", value=len(df))
with col_metric2:
    blocked_calls = len(df[df["status"] == "BLOCKED"]) if not df.empty else 0
    st.metric(label="Scam Threats Blocked", value=blocked_calls)
with col_metric3:
    passed_calls = len(df[df["status"] == "PASSED"]) if not df.empty else 0
    st.metric(label="Safe Calls Approved", value=passed_calls)

st.divider()

# Interactive Testing Panel
st.subheader("⚡ Live Scam & Threat Detection Simulator")
st.write("Simulate incoming calls and real-time speech transcripts directly to test your backend engine.")

col_sim1, col_sim2 = st.columns(2)

with col_sim1:
    sim_phone = st.text_input("Incoming Caller Number:", value="+917538879631")
    sim_type = st.radio("Select Test Scenario:", ["Speech Speech Analysis", "Blacklist Number Screening"])

with col_sim2:
    if sim_type == "Speech Speech Analysis":
        speech_input = st.text_area(
            "Caller Speech Transcript:",
            value="I need you to buy gift cards for bank account verification",
            height=100
        )
    else:
        blacklisted_phone = st.selectbox("Select Known Malicious Number:", ["+18005550199", "+18001234567"])

st.write("")
if st.button("🚀 Run Live Threat Check", use_container_width=True):
    try:
        if sim_type == "Speech Speech Analysis":
            res = requests.post("http://localhost:5000/analyze-speech", data={
                "From": sim_phone,
                "SpeechResult": speech_input
            })
        else:
            res = requests.post("http://localhost:5000/voice-incoming", data={
                "From": blacklisted_phone
            })

        if res.status_code == 200:
            st.success("Test executed successfully! Check updated logs below.")
            st.rerun()
        else:
            st.error(f"Error executing test: {res.status_code}")
    except Exception as e:
        st.error(f"Could not connect to Flask backend: {e}")

st.divider()

# Live Telemetry Table
st.subheader("📊 Real-Time Call Telemetry Logs")

if not df.empty:
    def highlight_status(val):
        if val == "BLOCKED":
            return "background-color: #ff4b4b; color: white; font-weight: bold;"
        elif val == "PASSED":
            return "background-color: #28a745; color: white; font-weight: bold;"
        return "background-color: #ffc107; color: black;"

    styled_df = df.style.map(highlight_status, subset=["status"])
    st.dataframe(styled_df, use_container_width=True, height=350)
else:
    st.info("No calls logged yet. Run a scenario above to test!")

if st.button("🔄 Refresh Logs"):
    st.rerun()
