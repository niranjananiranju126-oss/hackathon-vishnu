import re
import time
import speech_recognition as sr

# Weighted keyword dictionary mapping high-risk scam triggers to threat scores
SCAM_TRIGGERS = {
    "one time password": 40,
    "otp": 35,
    "bank account suspended": 35,
    "verify your identity": 25,
    "cvv": 35,
    "gift card": 40,
    "police warrant": 35,
    "lottery prize": 30,
    "wire transfer": 30,
    "urgent action required": 25,
    "department of revenue": 25,
    "credit card number": 35,
    "blocked": 15,
}

def calculate_scam_score(transcript: str):
    """Calculates cumulative risk score and returns detected trigger phrases."""
    text_lower = transcript.lower()
    total_score = 0
    matched_phrases = []

    for phrase, weight in SCAM_TRIGGERS.items():
        # Match whole words/phrases to prevent false positives
        if re.search(r'\b' + re.escape(phrase) + r'\b', text_lower):
            total_score += weight
            matched_phrases.append(phrase)

    # Cap threat score at 100%
    return min(total_score, 100), matched_phrases

def monitor_call_audio():
    recognizer = sr.Recognizer()
    recognizer.energy_threshold = 300  # Adjusts microphone sensitivity
    
    # Initialize Microphone Stream
    with sr.Microphone() as source:
        print("=== [SCAM SHIELD] Call Monitoring Active ===")
        print("Listening for incoming audio feed...\n")
        recognizer.adjust_for_ambient_noise(source, duration=1)

        while True:
            try:
                # Capture short audio chunks (4-second windows for real-time response)
                audio_data = recognizer.listen(source, phrase_time_limit=4)
                transcript = recognizer.recognize_google(audio_data)
                
                print(f"Transcribed Audio: \"{transcript}\"")
                risk_score, triggers = calculate_scam_score(transcript)

                # Alert threshold triggering
                if risk_score >= 50:
                    print("\n" + "="*50)
                    print(f"🚨 [HIGH RISK SCAM ALERT] Score: {risk_score}%")
                    print(f"⚠️ Detected Threat Triggers: {', '.join(triggers)}")
                    print("🛑 ACTION REQUIRED: Do NOT share OTPs, passwords, or personal details!")
                    print("="*50 + "\n")
                elif risk_score > 0:
                    print(f"ℹ️ [Caution] Suspicious term detected: {triggers} (Risk: {risk_score}%)\n")

            except sr.UnknownValueError:
                # Continuous loop: ignore background silence or unintelligible speech
                pass
            except sr.RequestError as e:
                print(f"STT Service Error: {e}")
            except KeyboardInterrupt:
                print("\nMonitoring stopped.")
                break

if __name__ == "__main__":
    monitor_call_audio()
