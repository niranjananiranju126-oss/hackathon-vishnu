import time
import requests
import streamlit as st

# Page Configuration
st.set_page_config(page_title="Real-Time Call Threat Detector", page_icon="📞", layout="centered")

st.title("📞 Incoming Call Scam Detector")
st.caption("Simulate or receive live incoming calls to evaluate scam risk based on number metadata.")

# Simulated Blacklist Database (For offline demo)
KNOWN_SPAM_DATABASE = {
    "+18005550199": {"reports": 450, "category": "Bank Phishing Fraud", "risk": 95},
    "+919876543210": {"reports": 120, "category": "Lottery / KYC Scam", "risk": 85},
    "+442079460912": {"reports": 15, "category": "Robocall Tech Support", "risk": 60},
}

def analyze_phone_number(phone_number: str):
    """Analyzes phone number against local databases and metadata patterns."""
    clean_number = phone_number.strip().replace(" ", "")
    
    # Check 1: Known Scam Database Lookup
    if clean_number in KNOWN_SPAM_DATABASE:
        data = KNOWN_SPAM_DATABASE[clean_number]
        return data["risk"], f"Flagged in database ({data['reports']} user reports for {data['category']})", "HIGH"
    
    # Check 2: Pattern & Line-Type Analysis Rules
    # VoIP, Toll-Free, or invalid country formats often carry elevated fraud risks
    if clean_number.startswith("+1800") or clean_number.startswith("+1888"):
        return 55, "Toll-Free line: Potential spoofed corporate caller.", "MEDIUM"
    
    if len(clean_number) < 10 or not clean_number.startswith("+"):
        return 75, "Suspicious formatting or missing international country code.", "HIGH"
        
    # Default Safe Result
    return 10, "Clean number. No reported scam records found.", "LOW"

# --- USER INTERFACE ---
st.subheader("📲 Incoming Call Simulator")

incoming_number = st.text_input(
    "Incoming Phone Number:", 
    value="+18005550199", 
    help="Enter a phone number with country code (e.g., +18005550199 or +919876543210)"
)

if st.button("Simulate Incoming Call"):
    with st.spinner("Incoming call ringing... Fetching caller metadata..."):
        time.sleep(1)  # Simulate network latency
        
    risk_score, reason, severity = analyze_phone_number(incoming_number)
    
    st.write("---")
    
    # --- CRITICAL THREAT NOTIFICATIONS ---
    if severity == "HIGH":
        st.error(f"🚨 **CRITICAL ALERT: HIGH RISK SCAM CALL!**")
        st.toast("🚨 ALERT: Incoming Scam Call Detected!", icon="🛑")
        st.metric(label="Threat Risk Score", value=f"{risk_score}%", delta="CRITICAL", delta_color="inverse")
        st.warning(f"⚠️ **Reason:** {reason}")
        st.info("🛑 **Recommended Action:** Decline call immediately or do not share sensitive information.")
        
    elif severity == "MEDIUM":
        st.warning(f"⚠️ **CAUTION: SUSPICIOUS CALLER**")
        st.toast("⚠️ Warning: Suspicious caller detected.", icon="⚠️")
        st.metric(label="Threat Risk Score", value=f"{risk_score}%", delta="SUSPICIOUS", delta_color="off")
        st.write(f"**Details:** {reason}")
        st.info("💡 **Recommended Action:** Verify the identity of the caller before sharing details.")
        
    else:
        st.success(f"✅ **SAFE CALLER DETECTED**")
        st.toast("✅ Incoming call checked. Safe to answer.", icon="✅")
        st.metric(label="Threat Risk Score", value=f"{risk_score}%", delta="SAFE")
        st.write(f"**Details:** {reason}")
