import os
import sys
import threading
import time

# =========================================================
# IMPORTANT
# pyaudiowpatch provides the PyAudio-compatible interface.
# SpeechRecognition normally looks specifically for "pyaudio",
# so we redirect it to pyaudiowpatch before importing it.
# =========================================================

import pyaudiowpatch as pyaudio

sys.modules["pyaudio"] = pyaudio

import speech_recognition as sr
import pyttsx3

from anthropic import Anthropic
from dotenv import load_dotenv

from visual import JarvisVisual


# =========================================================
# SETUP
# =========================================================

load_dotenv()

api_key = os.environ.get("ANTHROPIC_API_KEY")

if not api_key:
    print("ERROR: ANTHROPIC_API_KEY not found in .env")
    sys.exit(1)

client = Anthropic(
    api_key=api_key
)


# =========================================================
# VOICE
# =========================================================

recognizer = sr.Recognizer()

mic = sr.Microphone()

engine = pyttsx3.init()

engine.setProperty(
    "rate",
    175
)


# =========================================================
# CONVERSATION
# =========================================================

conversation_history = []

WAKE_WORD = "jarvis"


# =========================================================
# VISUAL
# =========================================================

jarvis = JarvisVisual()

jarvis.show(
    "SYSTEM READY"
)


# =========================================================
# ASSISTANT STATE
# =========================================================

assistant_busy = False


# =========================================================
# SPEAK
# =========================================================

def speak(text):

    global assistant_busy

    jarvis.set_status(
        "SPEAKING..."
    )

    print()
    print("JARVIS:", text)
    print()

    engine.say(text)

    engine.runAndWait()

    jarvis.set_status(
        "SYSTEM READY"
    )


# =========================================================
# LISTEN
# =========================================================

def listen():

    jarvis.set_status(
        "LISTENING..."
    )

    print("Listening...")

    try:

        with mic as source:

            recognizer.adjust_for_ambient_noise(
                source,
                duration=0.5
            )

            audio = recognizer.listen(
                source
            )

    except Exception as e:

        print(
            "Microphone error:",
            e
        )

        jarvis.set_status(
            "MICROPHONE ERROR"
        )

        time.sleep(1)

        jarvis.set_status(
            "SYSTEM READY"
        )

        return ""

    try:

        text = recognizer.recognize_google(
            audio
        )

        print(
            "You:",
            text
        )

        return text.lower()

    except sr.UnknownValueError:

        return ""

    except sr.RequestError:

        speak(
            "My speech recognition service is unavailable."
        )

        return ""


# =========================================================
# ASK CLAUDE
# =========================================================

def ask_claude(user_text):

    global conversation_history

    jarvis.set_status(
        "THINKING..."
    )

    conversation_history.append({
        "role": "user",
        "content": user_text
    })

    try:

        response = client.messages.create(

            model="claude-sonnet-4-6",

            max_tokens=300,

            system=(
                "You are JARVIS, a futuristic personal AI assistant. "
                "Be helpful, intelligent and concise. "
                "Your responses will be spoken aloud, "
                "so avoid unnecessarily long answers."
            ),

            messages=conversation_history
        )

        reply = response.content[0].text

        conversation_history.append({
            "role": "assistant",
            "content": reply
        })

        # Keep conversation manageable

        if len(conversation_history) > 10:

            del conversation_history[:2]

        return reply

    except Exception as e:

        print(
            "Claude error:",
            e
        )

        return (
            "I encountered an error while "
            "processing your request."
        )


# =========================================================
# ASSISTANT WORKER
# =========================================================

def assistant_loop():

    global assistant_busy

    speak(
        "Jarvis online. "
        "Say my name to get my attention."
    )

    while jarvis.running:

        if assistant_busy:

            time.sleep(0.1)

            continue

        heard = listen()

        if not heard:

            continue

        # -------------------------------------------------
        # SHUTDOWN
        # -------------------------------------------------

        if (
            "goodbye" in heard
            or "shut down" in heard
        ):

            speak(
                "Goodbye."
            )

            jarvis.running = False

            break

        # -------------------------------------------------
        # WAKE WORD
        # -------------------------------------------------

        if WAKE_WORD in heard:

            command = heard.replace(
                WAKE_WORD,
                ""
            ).strip(
                " ,."
            )

            # ---------------------------------------------
            # Just "Jarvis"
            # ---------------------------------------------

            if not command:

                speak(
                    "Yes?"
                )

                continue

            # ---------------------------------------------
            # Ask Claude
            # ---------------------------------------------

            reply = ask_claude(
                command
            )

            speak(
                reply
            )


# =========================================================
# START ASSISTANT THREAD
# =========================================================

assistant_thread = threading.Thread(
    target=assistant_loop,
    daemon=True
)

assistant_thread.start()


# =========================================================
# MAIN VISUAL LOOP
# =========================================================

try:

    while jarvis.running:

        jarvis.update()

        time.sleep(
            0.005
        )


finally:

    jarvis.close()