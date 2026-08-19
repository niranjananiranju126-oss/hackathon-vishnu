import sqlite3
import pandas as pd
import streamlit as st

st.set_page_config(page_title="ScamShield AI Console", page_icon="🛡️", layout="wide")

st.title("🛡️ ScamShield AI — Control Panel & Real-Time Telemetry")
st.caption("Live threat monitoring, dynamic intent analysis, and automated call interception")

# SQLite Database Functions
def init_db():
    conn = sqlite3.connect("call_logs.db")
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS logs 
        (id INTEGER PRIMARY KEY AUTOINCREMENT, 
         caller TEXT, 
         status TEXT, 
         details TEXT, 
         timestamp DATETIME DEFAULT CURRENT_TIMESTAMP)
    """)
    conn.commit()
    conn.close()

def log_call(caller, status, details):
    conn = sqlite3.connect("call_logs.db")
    cursor = conn.cursor()
    cursor.execute("INSERT INTO logs (caller, status, details) VALUES (?, ?, ?)", (caller, status, details))
    conn.commit()
    conn.close()

def get_logs():
    try:
        conn = sqlite3.connect("call_logs.db")
        df = pd.read_sql_query("SELECT * FROM logs ORDER BY timestamp DESC", conn)
        conn.close()
        return df
    except Exception:
        return pd.DataFrame()

# Initialize DB on Startup
init_db()
df = get_logs()

# Telemetry Header Metrics
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

# Interactive Threat Simulator
st.subheader("⚡ Live Scam & Threat Detection Simulator")
st.write("Simulate incoming calls and real-time speech transcripts directly to test the threat engine.")

col_sim1, col_sim2 = st.columns(2)

with col_sim1:
    sim_phone = st.text_input("Incoming Caller Number:", value="+917538879631")
    sim_type = st.radio("Select Test Scenario:", ["Speech Intent Analysis", "Blacklist Number Screening"])

with col_sim2:
    if sim_type == "Speech Intent Analysis":
        speech_input = st.text_area(
            "Caller Speech Transcript:",
            value="I need you to buy gift cards for bank account verification",
            height=100
        )
    else:
        blacklisted_phone = st.selectbox("Select Known Malicious Number:", ["+18005550199", "+18001234567"])

st.write("")
if st.button("🚀 Run Live Threat Check", use_container_width=True):
    if sim_type == "Speech Intent Analysis":
        scam_keywords = ["bank", "gift card", "social security", "urgent", "verify account", "tax", "irs"]
        speech_text = speech_input.lower()
        
        if any(word in speech_text for word in scam_keywords):
            log_call(sim_phone, "BLOCKED", f"Scam Intent Detected: '{speech_input}'")
            st.error("🚨 ALERT: Scam Speech Pattern Intercepted and Blocked!")
        else:
            log_call(sim_phone, "PASSED", f"Verified Safe Speech: '{speech_input}'")
            st.success("✅ Safe Call Approved and Connected.")
    else:
        log_call(blacklisted_phone, "BLOCKED", "High Risk: Flagged in Fraud Database")
        st.error(f"🚨 CRITICAL: Intercepted Blacklisted Call from {blacklisted_phone}!")
        
    st.rerun()

st.divider()

# Live Telemetry Data Table
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
