# ============================================================
# ai_functions.py — AI Functions using Groq (Fast!)
# ============================================================

import os
import streamlit as st
import speech_recognition as sr
from groq import Groq
from dotenv import load_dotenv
load_dotenv(r"C:\AI_Health\.env")

# ---------- GROQ SETUP ----------
client = Groq(api_key=os.getenv("GROQ_API_KEY"))

# ---------- AI CHATBOT ----------
def ai_chatbot(user_input):
    try:
        response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[
                {
                    "role": "system",
                    "content": "You are a helpful medical assistant. Give short, clear and accurate health advice in 2-3 lines only."
                },
                {
                    "role": "user",
                    "content": user_input
                }
            ],
            max_tokens=300,
            temperature=0.7
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"⚠ Error: {e}"

# ---------- AI DOCTOR SUGGESTER ----------
def get_ai_doctor(disease):
    try:
        response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[
                {
                    "role": "user",
                    "content": f"Which doctor specialist treats {disease}? Reply with only the specialist name, nothing else. One word or two words only."
                }
            ],
            max_tokens=20,
            temperature=0.3
        )
        return response.choices[0].message.content.strip()
    except:
        return "General Physician"

# ---------- VOICE INPUT ----------
def voice_input():
    r = sr.Recognizer()
    try:
        with sr.Microphone() as source:
            st.info("🎤 Listening... Speak now!")
            r.adjust_for_ambient_noise(source, duration=0.5)
            audio = r.listen(source, timeout=5)
        text = r.recognize_google(audio)
        return text
    except sr.WaitTimeoutError:
        return ""
    except sr.UnknownValueError:
        return ""
    except Exception:
        return ""