from flask import Flask, request
from twilio.twiml.voice_response import VoiceResponse

app = Flask(__name__)

KNOWN_SPAM_LIST = ["+18005550199", "+919876543210"]

@app.route("/voice-incoming", methods=['POST'])
def handle_incoming_call():
    """Triggered instantly when an incoming call starts ringing."""
    caller_number = request.form.get('From')
    response = VoiceResponse()

    print(f"📞 Incoming Call Connecting: {caller_number}")

    # Check caller against database during connection handshake
    if caller_number in KNOWN_SPAM_LIST:
        print(f"🚨 CRITICAL: Intercepted Scam Call from {caller_number}")
        # Reject the call before it rings through to the user
        response.reject(reason='busy')
    else:
        print("✅ Safe caller. Connecting call...")
        response.say("Connecting your call. Please hold.")

    return str(response)

if __name__ == "__main__":
    app.run(port=5000, debug=True)
