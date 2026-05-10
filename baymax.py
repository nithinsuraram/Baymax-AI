# =========================
# IMPORT REQUIRED LIBRARIES
# =========================

import google.generativeai as genai
import speech_recognition as sr
import asyncio
import edge_tts
import playsound
import os
import webbrowser
import datetime
import time
import uuid
import subprocess
import random 
awake = True
last_question = ""
loop = asyncio.new_event_loop()
asyncio.set_event_loop(loop)

genai.configure(api_key="AIzaSyAncEE3DU5Sc3WRbl74uW6r177TVziMUtM")
model = genai.GenerativeModel("gemini-1.5-flash")


# ---------------- SETTINGS ----------------
VOICE = "en-US-GuyNeural"   # Baymax-style calm voice
RATE = "+30%"            # Speed of speech


#----------intent dictionary----------------
intents = {
    "greeting": ["hi", "hello", "hey"],
    "time": ["time", "clock"],
    "date": ["date"],
    "open_youtube": ["youtube", "yt"],
    "open_chrome": ["chrome"],
    "open_google": ["google"],
    "open_notepad": ["notepad"],
    "open_calculator": ["calculator", "calc"],
    "sleep": ["sleep", "go to sleep"],
    "exit": ["exit", "quit", "stop"]
}



#-----------------intent dictionary function ----------------
def detect_intent(text):
    for intent, keywords in intents.items():
        for word in keywords:
            if word in text:
                return intent
    return "unknown"



# ---------------- SPEAK ----------------
async def speak_async(text):
    print("Baymax:", text)
    filename = f"baymax_{uuid.uuid4()}.mp3"

    communicate = edge_tts.Communicate(text, VOICE, rate=RATE)
    await communicate.save(filename)

    playsound.playsound(filename, block=True)
    os.remove(filename)

def speak(text):
    try:
        loop.run_until_complete(speak_async(text))
    except RuntimeError:
        pass




# ---------------- LISTEN ----------------
def listen():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("🎧 Listening...")
        r.adjust_for_ambient_noise(source, duration=0.4)
        try:
            audio = r.listen(source, timeout=5, phrase_time_limit=5)
            query = r.recognize_google(audio)
            print("You said:", query)
            return query.lower()
        except:
            return ""


# =================================
# BAYMAX IDENTITY RESPONSE FUNCTION
# =================================

def identity_response(command):
    command = command.lower()

    if "your name" in command:
        return "My name is Baymax."

    elif "who made you" in command or "who created you" in command:
        return "I was created by Nithin as a personal AI assistant."

    elif "what can you do" in command:
        return "I can listen to you, talk, open applications, play games, browse the internet, and assist you."

    return None


# =========================
# WAKE WORD DETECTION
# =========================
def wake_word_detected(text):
    wake_words = ["hey baymax", "baymax"]
    return any(word in text for word in wake_words)



#----------ai response function
def ai_reply(question):
    prompt = (
        "Answer briefly in 2–3 lines. "
        "Only explain in detail if I ask 'explain more'.\n\n"
        + question
    )

    response = model.generate_content(prompt)
    return response.text

# ---------- GLOBAL STATE ----------
awake = False

# ---------- INTRO ----------
speak("Hello. I am Baymax. Your personal voice assistant. How can I help you?")

THANK_RESPONSES = [
    "You are welcome.",
    "Always happy to help.",
    "It is my pleasure."
]


# =========================
# MAIN LOOP
# =========================
while True:
    query = listen()

    if len(query) < 2:
        continue

    intent = detect_intent(query)
    print("Detected Intent:", intent)

    # -------- WAKE WORD --------
    if not awake:
        if "hey baymax" in query or query.strip() == "baymax":
            awake = True
            speak("Yes. How can I help you?")
        continue

    # -------- COMMAND HANDLER --------
    if intent == "greeting":
        speak("Hello. How can I help you?")

    elif "your name" in query:
        speak("My name is Baymax.")

    elif "who made you" in query or "who created you" in query:
        speak("I was created by Nithin as a personal AI voice assistant.")

    elif "how are you" in query:
        speak("I am functioning properly. Thank you for asking.")

    elif "thank" in query:
        speak(random.choice(THANK_RESPONSES))

    elif intent == "time":
        now = datetime.datetime.now().strftime("%I:%M %p")
        speak(f"The current time is {now}")

    elif intent == "date":
        today = datetime.datetime.now().strftime("%d %B %Y")
        speak(f"Today's date is {today}")

    elif intent == "open_youtube":
        speak("Opening YouTube")
        webbrowser.open("https://www.youtube.com")

    elif intent == "open_google":
        speak("Opening Google")
        webbrowser.open("https://www.google.com")

    elif intent == "open_chrome":
        speak("Opening Google Chrome")
        subprocess.Popen(
            r"C:\Program Files\Google\Chrome\Application\chrome.exe"
        )

    elif intent == "open_notepad":
        speak("Opening Notepad")
        subprocess.Popen("notepad")

    elif intent == "open_calculator":
        speak("Opening Calculator")
        subprocess.Popen("calc")

    elif intent == "sleep":
        speak("Going to sleep. Say Hey Baymax to wake me up.")
        awake = False

    elif intent == "exit":
        speak("Shutting down. Goodbye.")
        break

    else:
        answer = ai_reply(query)
        speak(answer)

    time.sleep(0.5)
