# ============================================================
# ai_functions.py — AI Functions using Groq (Fast!)
# ============================================================

import os
import streamlit as st
import speech_recognition as sr
from groq import Groq
from dotenv import load_dotenv
load_dotenv()


# ---------- GROQ SETUP ----------
client = Groq(api_key=os.getenv("GROQ_API_KEY"))

# ---------- AI CHATBOT ----------
def ai_chatbot(user_input, language="Bilingual"):
    """
    Expert medical AI assistant. Always returns a bilingual response 
    wrapped in [EN]...[/EN] and [HI]...[/HI] tags for UI parsing.
    """
    try:
        response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[
                {
                    "role": "system",
                    "content": (
                        "You are an expert medical AI assistant. Always provide the information in both **English and Hindi**."
                        "\n\nEach response must be wrapped in language tags for parsing. Use this EXACT format:\n\n"
                        "[EN]\n"
                        "🩺 **Problem:** ...\n"
                        "💊 **Solutions:** ...\n"
                        "🛡 **Precautions:** ...\n"
                        "⚠ **When to See a Doctor:** ...\n"
                        "[/EN]\n\n"
                        "[HI]\n"
                        "🩺 **समस्या:** ...\n"
                        "💊 **उपचार:** ...\n"
                        "🛡 **सावधानियां:** ...\n"
                        "⚠ **डॉक्टर से कब मिलें:** ...\n"
                        "[/HI]\n\n"
                        "Keep your response concise, friendly, and easy to understand. "
                        "Do NOT add generic disclaimers. Do NOT give vague advice."
                    )
                },
                {
                    "role": "user",
                    "content": user_input
                }
            ],
            max_tokens=1000,
            temperature=0.6
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"⚠ Error: {e}"

# ---------- AUDIO TRANSCRIPTION (Groq Whisper) ----------
def transcribe_audio(audio_file):
    """Transcribes audio using Groq Whisper. Accepts st.audio_input UploadedFile."""
    import io
    try:
        # Get raw bytes from UploadedFile object
        if hasattr(audio_file, 'getvalue'):
            audio_bytes = audio_file.getvalue()
        elif hasattr(audio_file, 'read'):
            audio_bytes = audio_file.read()
        else:
            audio_bytes = bytes(audio_file)

        if not audio_bytes or len(audio_bytes) < 100:
            return "⚠ No audio detected. Please speak clearly and try again."

        audio_io = io.BytesIO(audio_bytes)
        audio_io.name = "recording.wav"

        # Use translations to automatically convert any spoken language (like Urdu) to English text
        translation = client.audio.translations.create(
            file=audio_io,
            model="whisper-large-v3",
            response_format="text"
        )
        result = translation if isinstance(translation, str) else translation.text
        return result.strip() if result else "⚠ Could not understand audio. Please try again."
    except Exception as e:
        return f"⚠ Error: {str(e)}"

# ---------- AI DOCTOR SUGGESTER ----------
def get_ai_doctor(disease):
    try:
        response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[
                {
                    "role": "user",
                    "content": f"Which doctor specialist treats {disease}? Reply with only the specialist name in English, nothing else. One word or two words only."
                }
            ],
            max_tokens=20,
            temperature=0.3
        )
        return response.choices[0].message.content.strip()
    except:
        return "General Physician"

# ---------- NUTRITION ESTIMATOR ----------
def get_nutrition_info(food_item: str, quantity: str = "100g") -> dict:
    """
    Returns estimated nutrition for a food item as a dict:
    {calories, protein_g, carbs_g, fat_g, fiber_g, sugar_g}
    """
    try:
        prompt = (
            f"Give estimated nutritional values for {quantity} of '{food_item}'. "
            "Respond ONLY with a valid JSON object in English, no text before or after. "
            "Use these exact keys: calories (kcal), protein_g, carbs_g, fat_g, fiber_g, sugar_g. "
            "All values must be numbers (floats). Example: "
            '{"calories": 52, "protein_g": 0.3, "carbs_g": 14, "fat_g": 0.2, "fiber_g": 2.4, "sugar_g": 10.4}'
        )
        response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[{"role": "user", "content": prompt}],
            max_tokens=150,
            temperature=0.2
        )
        import json
        raw = response.choices[0].message.content.strip()
        # Extract JSON if wrapped in markdown
        if "```" in raw:
            raw = raw.split("```")[1].replace("json", "").strip()
        return json.loads(raw)
    except Exception as e:
        return {"error": str(e)}

# ---------- VOICE INPUT ----------
def voice_input():
    r = sr.Recognizer()
    try:
        with sr.Microphone() as source:
            st.info("🎤 Listening... Speak now!")
            r.adjust_for_ambient_noise(source, duration=0.5)
            audio = r.listen(source, timeout=5)
        text = r.recognize_google(audio, language='en-US')
        return text
    except sr.WaitTimeoutError:
        return ""
    except sr.UnknownValueError:
        return ""
    except Exception:
        return ""