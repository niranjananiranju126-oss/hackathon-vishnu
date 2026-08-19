import sqlite3
import requests
from flask import Flask, request
from twilio.rest import Client
from twilio.twiml.voice_response import VoiceResponse, Gather

app = Flask(__name__)

# Twilio Credentials
TWILIO_ACCOUNT_SID = 'AC8142462f381367b68da02e386f8c4cdb'
TWILIO_AUTH_TOKEN = 'de49a32fb69c8b4f59497b5e1df1e0af'

# Replace with your actual Twilio virtual phone number (e.g., '+1833XXX...')
TWILIO_PHONE_NUMBER = '+917538879631'

# SQLite Database Setup
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

# Initialize DB on startup
init_db()

# Risk Engine Logic
def check_risk_score(phone_number):
    known_spams = ["+18005550199", "+18001234567"]
    if phone_number in known_spams:
        return True, "Flagged in Fraud Database"
    return False, "Clean Profile"

# Webhook for Incoming Calls
@app.route('/voice-incoming', methods=['POST'])
def voice_incoming():
    caller = request.form.get('From', '').replace(' ', '+').strip() or "Unknown"
    response = VoiceResponse()
    
    is_scam, reason = check_risk_score(caller)
    if is_scam:
        log_call(caller, "BLOCKED", f"High Risk: {reason}")
        print(f"🚨 CRITICAL: Intercepted Scam Call from {caller}")
        response.say("Security Alert: Call blocked due to suspected fraud.")
        response.reject()
        return str(response)

    log_call(caller, "PENDING", "Routing to Dynamic Speech Analysis")
    gather = Gather(input='speech', action='/analyze-speech', timeout=4)
    gather.say("Please state the reason for your call after the prompt.")
    response.append(gather)
    return str(response)

# Webhook for Transcribed Speech Analysis
@app.route('/analyze-speech', methods=['POST'])
def analyze_speech():
    caller = request.form.get('From', '').replace(' ', '+').strip() or "Unknown"
    speech_text = request.form.get('SpeechResult', '').lower()
    response = VoiceResponse()

    scam_keywords = ["bank", "gift card", "social security", "urgent", "verify account", "tax", "irs"]
    
    if any(word in speech_text for word in scam_keywords):
        log_call(caller, "BLOCKED", f"Scam Intent Detected: '{speech_text}'")
        print(f"🚨 ALERT: Blocked Scam Speech Pattern from {caller}")
        response.say("Scam speech patterns detected. Call terminated.")
        response.reject()
    else:
        log_call(caller, "PASSED", f"Verified Safe Speech: '{speech_text}'")
        print(f"✅ Safe Call Approved from {caller}")
        response.say("Thank you. Connecting your call now.")

    return str(response)

# Route to Initiate Outbound Calls
@app.route('/make-call', methods=['POST'])
def make_call():
    target_number = request.form.get('to_number', '').replace(' ', '+').strip()
    
    if not target_number:
        return {"status": "error", "message": "Phone number is required"}, 400

    try:
        client = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)
        call = client.calls.create(
            to=target_number,
            from_=TWILIO_PHONE_NUMBER,
            url='https://rippling-casino-gamma.ngrok-free.dev/voice-incoming'
        )
        log_call(target_number, "OUTBOUND_INITIATED", f"Call SID: {call.sid}")
        return {"status": "success", "call_sid": call.sid}, 200
    except Exception as e:
        return {"status": "error", "message": str(e)}, 500

if __name__ == '__main__':
    print("🚀 ScamShield Server active on http://localhost:5000...")
    app.run(port=5000, debug=True)
