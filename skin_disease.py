# ============================================================
# skin_disease.py — Skin Disease Detector using Gemini Vision
# ============================================================

import streamlit as st
import google.generativeai as genai
from PIL import Image
import os, re
from dotenv import load_dotenv
load_dotenv(r"C:\AI_Health\.env")

genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

# ---------- CLEAN RESULT TEXT ----------
def clean_result(text):
    if not isinstance(text, str):
        text = str(text)
    text = text.strip("()'\"")
    text = text.replace("\\n", "\n")
    text = re.sub(r'#{1,3} ', '', text)
    text = text.replace("**", "")
    text = re.sub(r'\n{3,}', '\n\n', text)
    return text.strip()

# ---------- ANALYZE SKIN IMAGE ----------
def analyze_skin(image, body_part, symptoms=""):
    try:
        model  = genai.GenerativeModel("gemini-1.5-flash")
        prompt = f"""You are an expert dermatologist AI. Carefully analyze this skin image.

Body Part: {body_part}
{f"Patient Symptoms: {symptoms}" if symptoms else ""}

Provide a detailed dermatological analysis:

1. VISUAL FINDINGS:
Describe exactly what you see — color, texture, shape, size, pattern.

2. POSSIBLE CONDITIONS:
List possible skin diseases with High/Medium/Low likelihood.
Consider: Acne, Eczema, Psoriasis, Ringworm, Fungal infection, Vitiligo,
Rosacea, Hives, Dermatitis, Melanoma, Warts, Herpes, Scabies, Heat Rash.

3. WARNING SIGNS:
Any signs of serious conditions like skin cancer? What needs immediate attention?

4. RECOMMENDED SPECIALIST:
Which doctor to consult? How urgent? (Emergency/Urgent/Soon/Routine)

5. TREATMENT AND CARE:
Possible treatments, home remedies, and skincare advice.

6. TESTS RECOMMENDED:
Any skin tests or biopsies recommended?

Note: AI analysis for reference only. Always consult a qualified dermatologist."""

        response = model.generate_content([prompt, image])
        return response.text, True

    except Exception as e:
        # Fallback to Groq
        from groq import Groq
        try:
            client = Groq(api_key=os.getenv("GROQ_API_KEY"))
            prompt2 = f"""You are a dermatologist AI. Patient has skin condition on {body_part}.
Symptoms: {symptoms}

Provide analysis:
1. VISUAL FINDINGS - common findings for skin conditions on {body_part}
2. POSSIBLE CONDITIONS - list diseases with High/Medium/Low likelihood
3. WARNING SIGNS - signs needing immediate attention
4. RECOMMENDED SPECIALIST - which doctor and urgency
5. TREATMENT AND CARE - treatments and home remedies
6. TESTS RECOMMENDED - any tests needed

Note: Image could not be analyzed directly. This is symptom-based guidance only."""

            resp = client.chat.completions.create(
                model="llama-3.3-70b-versatile",
                messages=[{"role": "user", "content": prompt2}],
                max_tokens=800, temperature=0.7
            )
            return resp.choices[0].message.content, False
        except Exception as e2:
            return f"Analysis failed: {e2}", False

# ---------- SHOW SKIN DISEASE DETECTOR ----------
def show_skin_disease():
    st.markdown("<div class='section-header'>🔬 Skin Disease Detector</div>", unsafe_allow_html=True)

    st.markdown("""
    <div style='background:rgba(251,146,60,0.08); border:1px solid rgba(251,146,60,0.25);
         padding:12px 16px; border-radius:14px; margin-bottom:18px;
         font-size:0.87rem; color:#d4d0f0; line-height:1.9;'>
        📸 <b style='color:#fb923c;'>Upload a clear photo</b> of your skin condition<br>
        🤖 <b style='color:#6ee7b7;'>Gemini 1.5 Flash</b> will analyze and detect possible skin diseases<br>
        🔍 Works for: <b style='color:#fbbf24;'>Acne, Eczema, Psoriasis, Fungal infections, Rashes</b> and more
    </div>
    """, unsafe_allow_html=True)

    col1, col2 = st.columns(2)

    with col1:
        st.markdown("<div class='glass-box'>", unsafe_allow_html=True)
        st.markdown("<div class='section-title'>📸 Upload Skin Photo</div>", unsafe_allow_html=True)

        symptoms = st.text_area(
            "📝 Describe your symptoms",
            placeholder="e.g. itching, burning, redness since 3 days, spreading rash...",
            height=90
        )

        duration = st.selectbox("📅 How long do you have this?", [
            "Just appeared today", "2-3 days", "1 week",
            "2-4 weeks", "1-3 months", "More than 3 months", "Years (Chronic)"
        ])

        uploaded = st.file_uploader(
            "📎 Upload Skin Photo",
            type=["jpg", "jpeg", "png", "webp"],
            help="Clear, well-lit photo of affected skin area"
        )

        if uploaded:
            image = Image.open(uploaded)
            st.image(image, caption="📸 Skin Photo", use_column_width=True)

            if st.button("🔬 Analyze Skin Condition", use_container_width=True):
                full_symptoms = f"{symptoms}. Duration: {duration}" if symptoms else f"Duration: {duration}"
                with st.spinner("🤖 Gemini AI is analyzing your skin..."):
                    result_text, img_used = analyze_skin(image, "Skin", full_symptoms)

                st.session_state.skin_result   = clean_result(result_text)
                st.session_state.skin_part     = "Skin"
                st.session_state.skin_img_used = img_used
                st.rerun()
        else:
            st.markdown("""
            <div style='text-align:center; padding:40px 20px;
                 border:2px dashed rgba(251,146,60,0.3); border-radius:16px;
                 background:rgba(251,146,60,0.04); margin-top:10px;'>
                <div style='font-size:3rem; margin-bottom:12px;'>📸</div>
                <p style='color:#7c74a8; font-size:0.9rem;'>
                    Upload a clear photo of your skin<br>
                    <span style='font-size:0.8rem; opacity:0.7;'>Good lighting = Better results</span>
                </p>
            </div>
            """, unsafe_allow_html=True)

        st.markdown("""
        <div style='margin-top:14px; padding:12px 14px;
             background:rgba(251,146,60,0.07); border:1px solid rgba(251,146,60,0.18);
             border-radius:12px; font-size:0.82rem; color:#fdba74;'>
            💡 <b>Tips:</b> Good lighting · Clear focus · Close-up · No makeup
        </div>
        """, unsafe_allow_html=True)

        st.markdown("<br>", unsafe_allow_html=True)
        st.markdown("<div class='glass-box'>", unsafe_allow_html=True)
        st.markdown("<div class='section-title'>🦠 Common Skin Conditions</div>", unsafe_allow_html=True)
        for emoji, name, desc in [
            ("🔴", "Acne",             "Pimples, blackheads"),
            ("🟤", "Eczema",           "Itchy, dry, inflamed"),
            ("⚪", "Psoriasis",        "Scaly, silvery patches"),
            ("🟡", "Ringworm",         "Circular ring pattern"),
            ("🔵", "Vitiligo",         "White patches on skin"),
            ("🟠", "Rosacea",          "Facial redness"),
            ("🔴", "Hives",            "Raised, itchy welts"),
            ("🟤", "Dermatitis",       "Skin inflammation"),
            ("⚫", "Melanoma",         "Dark irregular moles"),
            ("🟡", "Fungal Infection", "Itchy, flaky skin"),
        ]:
            st.markdown(f"""
            <div style='display:flex;align-items:center;gap:10px;padding:6px 8px;
                 background:rgba(255,255,255,0.03);border-radius:8px;margin-bottom:5px;font-size:0.82rem;'>
                <span>{emoji}</span>
                <span style='color:#f0edff;font-weight:600;'>{name}</span>
                <span style='color:#a89ec9;'>— {desc}</span>
            </div>
            """, unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)

    with col2:
        st.markdown("<div class='glass-box'>", unsafe_allow_html=True)
        st.markdown("<div class='section-title'>🤖 AI Skin Analysis Result</div>", unsafe_allow_html=True)

        if st.session_state.get("skin_result"):
            result   = st.session_state.skin_result
            part     = st.session_state.get("skin_part", "Skin")
            img_used = st.session_state.get("skin_img_used", False)

            method = "🖼️ Image Analyzed by Gemini" if img_used else "📝 Symptom-Based Analysis"
            color  = "#34d399" if img_used else "#fbbf24"

            st.markdown(f"""
            <div style='display:flex;gap:8px;margin-bottom:14px;flex-wrap:wrap;'>
                <span style='background:rgba(251,146,60,0.15);color:#fb923c;
                     padding:5px 14px;border-radius:20px;font-size:0.8rem;font-weight:700;
                     border:1px solid rgba(251,146,60,0.3);'>🔬 {part}</span>
                <span style='background:rgba(16,185,129,0.1);color:{color};
                     padding:5px 14px;border-radius:20px;font-size:0.8rem;font-weight:600;
                     border:1px solid rgba(16,185,129,0.2);'>{method}</span>
            </div>
            """, unsafe_allow_html=True)

            sections = result.split("\n\n")
            for section in sections:
                section = section.strip()
                if not section:
                    continue
                lines = section.split("\n")
                title = lines[0].strip()
                body  = "\n".join(lines[1:]).strip()

                if not title:
                    continue

                tu = title.upper()
                if any(w in tu for w in ["FINDINGS", "VISUAL"]):
                    bg = "rgba(251,146,60,0.1)";  border = "rgba(251,146,60,0.25)";  tc = "#fdba74"
                elif any(w in tu for w in ["CONDITIONS", "DISEASE", "POSSIBLE"]):
                    bg = "rgba(239,68,68,0.1)";   border = "rgba(239,68,68,0.25)";   tc = "#f87171"
                elif any(w in tu for w in ["WARNING", "DANGER", "SIGNS"]):
                    bg = "rgba(245,158,11,0.12)"; border = "rgba(245,158,11,0.3)";   tc = "#fbbf24"
                elif any(w in tu for w in ["SPECIALIST", "DOCTOR", "RECOMMENDED"]):
                    bg = "rgba(16,185,129,0.1)";  border = "rgba(16,185,129,0.25)";  tc = "#6ee7b7"
                elif any(w in tu for w in ["TREATMENT", "CARE", "REMEDY"]):
                    bg = "rgba(99,102,241,0.1)";  border = "rgba(99,102,241,0.25)";  tc = "#818cf8"
                elif any(w in tu for w in ["TEST", "BIOPSY"]):
                    bg = "rgba(124,58,237,0.1)";  border = "rgba(124,58,237,0.25)";  tc = "#c4b5fd"
                else:
                    bg = "rgba(255,255,255,0.04)"; border = "rgba(255,255,255,0.08)"; tc = "#f0edff"

                body_html = body.replace("\n", "<br>").replace("- ", "• ")
                content   = body_html if body_html.strip() else title

                st.markdown(f"""
                <div style='background:{bg};border:1px solid {border};
                     padding:14px 16px;border-radius:14px;margin-bottom:12px;'>
                    <div style='color:{tc};font-weight:700;font-size:0.92rem;margin-bottom:6px;'>{title}</div>
                    <div style='color:#d4d0f0;font-size:0.86rem;line-height:1.8;'>{content}</div>
                </div>
                """, unsafe_allow_html=True)

            d1, d2 = st.columns(2)
            with d1:
                st.download_button("📄 Download Report", data=result,
                    file_name="skin_analysis.txt", mime="text/plain", use_container_width=True)
            with d2:
                if st.button("🗑 Clear Result", use_container_width=True):
                    st.session_state.skin_result = ""
                    st.rerun()
        else:
            st.markdown("""
            <div style='text-align:center;padding:80px 20px;'>
                <div style='font-size:5rem;margin-bottom:20px;'>🔬</div>
                <p style='font-size:1rem;font-weight:600;color:#6b7280;'>No analysis yet</p>
                <p style='font-size:0.85rem;color:#4b5563;'>
                    Upload a skin photo<br>and click Analyze
                </p>
            </div>
            """, unsafe_allow_html=True)

        st.markdown("</div>", unsafe_allow_html=True)

        st.markdown("""
        <div style='padding:10px 14px;background:rgba(245,158,11,0.08);
             border:1px solid rgba(245,158,11,0.2);border-radius:12px;
             font-size:0.78rem;color:#fbbf24;margin-top:8px;'>
            ⚠️ AI skin analysis is for reference only. Always consult a qualified dermatologist.
        </div>
        """, unsafe_allow_html=True)