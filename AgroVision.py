import io
import re
import streamlit as st
import speech_recognition as sr

# ---------------------------------------------------------
# 1. PAGE & STYLING CONFIGURATION
# ---------------------------------------------------------
st.set_page_config(
    page_title="ScamGuard - Real-Time Call Scam Detector",
    page_icon="🛡️",
    layout="wide"
)

st.title("🛡️ ScamGuard: Real-Time Call Threat Analyzer")
st.caption("AI-powered voice call monitoring to protect users against phishing and financial scams.")

# ---------------------------------------------------------
# 2. SCAM KEYWORDS & THREAT WEIGHTS
# ---------------------------------------------------------
SCAM_TRIGGERS = {
    "otp": 40,
    "one time password": 40,
    "bank account suspended": 35,
    "verify your identity": 25,
    "cvv": 35,
    "credit card": 30,
    "gift card": 40,
    "police warrant": 35,
    "lottery prize": 35,
    "wire transfer": 30,
    "urgent action required": 25,
    "department of revenue": 30,
    "blocked": 15,
}

def analyze_transcript(transcript: str):
    """Calculates threat score based on keyword matches and returns detected triggers."""
    text_lower = transcript.lower()
    matched = []
    score = 0
    
    for phrase, weight in SCAM_TRIGGERS.items():
        if re.search(r'\b' + re.escape(phrase) + r'\b', text_lower):
            matched.append(phrase)
            score += weight
            
    final_score = min(score, 100)
    return final_score, matched

def process_audio_file(audio_bytes):
    """Transcribes audio bytes into text using Google Speech Recognition."""
    recognizer = sr.Recognizer()
    try:
        audio_file = io.BytesIO(audio_bytes)
        with sr.AudioFile(audio_file) as source:
            audio_data = recognizer.record(source)
            transcript = recognizer.recognize_google(audio_data)
            return transcript, None
    except sr.UnknownValueError:
        return None, "Speech was unintelligible or silent. Please try speaking clearly."
    except sr.RequestError as e:
        return None, f"Speech Recognition API Error: {e}"
    except Exception as e:
        return None, f"Error reading audio file format: {e}"

# ---------------------------------------------------------
# 3. USER INTERFACE (LIVE MIC + FILE UPLOAD)
# ---------------------------------------------------------
tab1, tab2 = st.tabs(["🎤 Live Mic Capture", "📁 Upload Call Recording"])

audio_source = None

with tab1:
    st.write("Record spoken audio directly through your web browser:")
    # Native Streamlit Microphone Widget
    mic_audio = st.audio_input("Record Call Audio")
    if mic_audio:
        audio_source = mic_audio.read()

with tab2:
    st.write("Upload a pre-recorded call audio file (.wav format recommended):")
    uploaded_file = st.file_uploader("Choose a WAV audio file", type=["wav"])
    if uploaded_file:
        audio_source = uploaded_file.read()

# ---------------------------------------------------------
# 4. PROCESSING & NOTIFICATION ALERTS
# ---------------------------------------------------------
if audio_source is not None:
    st.write("---")
    st.subheader("🔍 Analysis Output")
    
    with st.spinner("Processing audio and scanning for scam patterns..."):
        transcript, error = process_audio_file(audio_source)

    if error:
        st.error(f"⚠️ {error}")
    else:
        st.write(f"**Speech Transcript:** *\"{transcript}\"*")
        
        risk_score, matched_triggers = analyze_transcript(transcript)
        
        # Threat level progress bar
        st.write(f"**Calculated Threat Risk:** `{risk_score}%`")
        st.progress(risk_score / 100)

        # TRIGGER NOTIFICATIONS BASED ON RISK LEVEL
        if risk_score >= 50:
            # High-Level Alert
            st.error("🚨 **CRITICAL ALERT: HIGH RISK SCAM DETECTED!**")
            st.toast("🚨 ALERT: High Risk Scam Call Detected!", icon="🛑")
            st.warning(f"⚠️ **Detected Suspicious Phrase Triggers:** {', '.join(matched_triggers)}")
            st.info("💡 **Security Advice:** End the call immediately! Do NOT disclose OTPs, PINs, or financial info.")
            
        elif risk_score >= 25:
            # Medium-Level Caution Alert
            st.warning("⚠️ **WARNING: SUSPICIOUS ACTIVITY DETECTED**")
            st.toast("⚠️ Warning: Suspicious call pattern detected.", icon="⚠️")
            st.write(f"**Flagged Keywords:** {', '.join(matched_triggers)}")
            
        else:
            # Low Risk Confirmation
            st.success("✅ **CALL APPEARS SAFE**")
            st.toast("✅ Call analyzed. No threat patterns found.", icon="✅")
            st.write("No high-risk financial or urgency phrases were found in this audio sample.")
