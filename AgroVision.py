import re
import time
import speech_recognition as sr
from plyer import notification  # Requires: pip install plyer

SCAM_TRIGGERS = {
    "one time password": 40, "otp": 35, "bank account suspended": 35,
    "verify your identity": 25, "cvv": 35, "gift card": 40,
    "police warrant": 35, "lottery prize": 30, "wire transfer": 30
}

def send_alert(risk_score, triggers):
    """Triggers an OS-level desktop notification popup."""
    notification.notify(
        title="🚨 SCAM CALL DETECTED!",
        message=f"Threat Level: {risk_score}%\nTriggers: {', '.join(triggers)}\nDo NOT share sensitive details!",
        app_name="Scam Shield Guard",
        timeout=10
    )

def monitor_and_notify():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print("=== Monitoring Call Audio for Threats ===")
        recognizer.adjust_for_ambient_noise(source, duration=1)

        while True:
            try:
                audio = recognizer.listen(source, phrase_time_limit=4)
                transcript = recognizer.recognize_google(audio).lower()
                print(f"User heard: {transcript}")

                matched = [word for word in SCAM_TRIGGERS if re.search(r'\b' + re.escape(word) + r'\b', transcript)]
                score = min(sum(SCAM_TRIGGERS[w] for w in matched), 100)

                if score >= 40:
                    send_alert(score, matched)

            except (sr.UnknownValueError, sr.RequestError):
                pass

if __name__ == "__main__":
    monitor_and_notify()
