# ============================================================
# blood_report.py — Blood Report Analyzer (Image + Manual)
# ============================================================

import streamlit as st
from groq import Groq
from PIL import Image
import os
from dotenv import load_dotenv
load_dotenv(r"C:\AI_Health\.env")

# ── SETUP ──
groq_client = Groq(api_key=os.getenv("GROQ_API_KEY"))

# ── ANALYZE IMAGE WITH GROQ (Gemini removed) ──
def analyze_blood_image(image, age, symptoms=""):
    try:
        # Convert image to base64 for Groq vision
        import base64, io
        buf = io.BytesIO()
        image.save(buf, format="PNG")
        b64 = base64.b64encode(buf.getvalue()).decode("utf-8")

        prompt = f"""You are an expert hematologist. ALWAYS RESPOND IN ENGLISH.
Analyze this blood test report image.

Patient Age: {age}
{f"Symptoms: {symptoms}" if symptoms else ""}

1. 🔍 READ ALL VALUES: List every test value visible. Format: Test Name: Value (Normal/Abnormal)
2. ⚠️ ABNORMAL VALUES: Which values are outside normal range? High or Low?
3. 🦠 POSSIBLE CONDITIONS: List possible diseases with High/Medium/Low likelihood.
4. 🚨 CRITICAL VALUES: Any dangerously abnormal values needing immediate attention?
5. 👨‍⚕️ RECOMMENDED SPECIALIST: Which doctor to consult? How urgent?
6. 💊 NEXT STEPS: Treatment and lifestyle recommendations.

Note: AI analysis for reference only. Always consult a qualified doctor."""

        response = groq_client.chat.completions.create(
            model="meta-llama/llama-4-scout-17b-16e-instruct",
            messages=[{
                "role": "user",
                "content": [
                    {"type": "image_url", "image_url": {"url": f"data:image/png;base64,{b64}"}},
                    {"type": "text", "text": prompt}
                ]
            }],
            max_tokens=1000, temperature=0.7
        )
        return response.choices[0].message.content, True
    except Exception as e:
        return f"⚠️ Image analysis failed: {e}\n\nPlease use the Manual Entry tab instead.", False

# ── ANALYZE MANUAL VALUES WITH GROQ ──
def analyze_blood_manual(values, age, symptoms=""):
    try:
        test_lines = "\n".join([f"- {k}: {v}" for k, v in values.items() if v and v.strip()])
        prompt = f"""You are an expert hematologist. ALWAYS RESPOND IN ENGLISH. 
Analyze this blood report:

Patient Age: {age}
{f"Symptoms: {symptoms}" if symptoms else ""}

Blood Test Results:
{test_lines}

1. 🔍 FINDINGS:
Which values are abnormal (high/low)? What do they indicate?

2. 🦠 POSSIBLE CONDITIONS:
List possible diseases. Rate each High/Medium/Low likelihood.

3. ⚠️ CRITICAL VALUES:
Any dangerously abnormal values?

4. 👨‍⚕️ RECOMMENDED SPECIALIST:
Which doctor? How urgent?

5. 💊 TREATMENT & NEXT STEPS:
Recommendations for treatment and lifestyle.

Note: AI analysis for reference only."""

        response = groq_client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[{"role": "user", "content": prompt}],
            max_tokens=1000, temperature=0.7
        )
        return response.choices[0].message.content, True
    except Exception as e:
        return f"⚠ Error: {e}", False

# ── RENDER RESULT ──
def render_result(result):
    sections = result.split("\n\n")
    for section in sections:
        if section.strip():
            lines = section.strip().split("\n")
            if lines:
                title = lines[0].strip()
                body  = "\n".join(lines[1:]).strip()
                if "FINDINGS" in title.upper() or "READ" in title.upper() or "VALUES" in title.upper():
                    bg="rgba(99,102,241,0.1)"; border="rgba(99,102,241,0.25)"; tc="#818cf8"
                elif "CONDITIONS" in title.upper() or "DISEASE" in title.upper():
                    bg="rgba(239,68,68,0.1)"; border="rgba(239,68,68,0.25)"; tc="#f87171"
                elif "CRITICAL" in title.upper() or "ABNORMAL" in title.upper():
                    bg="rgba(245,158,11,0.12)"; border="rgba(245,158,11,0.3)"; tc="#fbbf24"
                elif "SPECIALIST" in title.upper() or "DOCTOR" in title.upper():
                    bg="rgba(16,185,129,0.1)"; border="rgba(16,185,129,0.25)"; tc="#6ee7b7"
                else:
                    bg="rgba(124,58,237,0.1)"; border="rgba(124,58,237,0.25)"; tc="#c4b5fd"

                st.markdown(f"""
                <div style='background:{bg};border:1px solid {border};
                     padding:14px 16px;border-radius:14px;margin-bottom:12px;'>
                    <div style='color:{tc};font-weight:700;font-size:0.92rem;margin-bottom:8px;'>{title}</div>
                    <div style='color:#d4d0f0;font-size:0.86rem;line-height:1.7;'>{body.replace(chr(10),"<br>")}</div>
                </div>
                """, unsafe_allow_html=True)

# ── MAIN FUNCTION ──
def show_blood_report():
    st.markdown("""
        <div class="section-header">
            <img src="https://img.icons8.com/fluency/96/test-tube.png" width="50" style="margin-bottom: 10px;">
            <br>
            🩸 Blood Report Analyzer
        </div>
    """, unsafe_allow_html=True)

    # Patient info — gender removed
    st.markdown("<div class='patient-box'>", unsafe_allow_html=True)
    pc1, pc2 = st.columns(2)
    with pc1: age      = st.number_input("🎂 Age", 1, 120, 25)
    with pc2: symptoms = st.text_input("📝 Symptoms (optional)", placeholder="e.g. fatigue, dizziness...")
    st.markdown("</div>", unsafe_allow_html=True)

    # Two tabs
    img_tab, manual_tab = st.tabs(["📸 Upload Image (AI Reads)", "✍️ Manual Entry"])

    # ── IMAGE TAB ──
    with img_tab:
        col1, col2 = st.columns(2)

        with col1:
            st.markdown("<div class='glass-box'>", unsafe_allow_html=True)
            st.markdown("<div class='section-title'>📸 Upload Blood Report</div>", unsafe_allow_html=True)

            uploaded = st.file_uploader(
                "📎 Upload Blood Report Image",
                type=["jpg", "jpeg", "png", "webp"],
                help="Take a clear photo of your blood report"
            )

            if uploaded:
                image = Image.open(uploaded)
                st.image(image, caption="📋 Blood Report", use_column_width=True)

                if st.button("🔬 Analyze with AI", use_container_width=True):
                    with st.spinner("🤖 Groq AI is reading your blood report..."):
                        result, success = analyze_blood_image(image, age, symptoms)
                    st.session_state.blood_result   = result
                    st.session_state.blood_img_used = success
                    st.session_state.blood_method   = "image"
                    st.rerun()
            else:
                st.markdown("""
                <div style='text-align:center; padding:40px 20px;
                     border:2px dashed rgba(239,68,68,0.3); border-radius:16px;
                     background:rgba(239,68,68,0.04); margin-top:10px;'>
                    <div style='font-size:3rem; margin-bottom:12px;'>📋</div>
                    <p style='color:#7c74a8; font-size:0.9rem;'>
                        Upload your blood report photo<br>
                        <span style='font-size:0.8rem; opacity:0.7;'>Clear photo = Better results</span>
                    </p>
                </div>
                """, unsafe_allow_html=True)

            st.markdown("""
            <div style='margin-top:14px; padding:10px 14px;
                 background:rgba(245,158,11,0.08); border:1px solid rgba(245,158,11,0.2);
                 border-radius:11px; font-size:0.8rem; color:#fbbf24;'>
                💡 <b>Tips for best results:</b><br>
                • Take photo in good lighting<br>
                • Make sure all values are clearly visible<br>
                • Keep the camera steady — no blur<br>
                • Include the full report in the frame
            </div>
            """, unsafe_allow_html=True)

            st.markdown("</div>", unsafe_allow_html=True)

        with col2:
            st.markdown("<div class='glass-box'>", unsafe_allow_html=True)
            st.markdown("<div class='section-title'>🤖 AI Analysis Result</div>", unsafe_allow_html=True)

            if "blood_result" in st.session_state and st.session_state.blood_result and st.session_state.get("blood_method") == "image":
                method = "🖼️ Image Analyzed by AI" if st.session_state.get("blood_img_used") else "📝 Text Analysis"
                color  = "#34d399" if st.session_state.get("blood_img_used") else "#fbbf24"
                st.markdown(f"""
                <div style='background:rgba(124,58,237,0.1); border:1px solid rgba(124,58,237,0.25);
                     padding:8px 14px; border-radius:12px; margin-bottom:14px;
                     font-size:0.82rem; font-weight:600; color:{color};'>
                    {method}
                </div>
                """, unsafe_allow_html=True)

                render_result(st.session_state.blood_result)

                st.download_button("📄 Download Report", data=st.session_state.blood_result,
                    file_name="blood_report_analysis.txt", mime="text/plain")

                if st.button("🗑 Clear Result", key="clear_img"):
                    st.session_state.blood_result = ""
                    st.session_state.blood_method = ""
                    st.rerun()
            else:
                st.markdown("""
                <div style='text-align:center; padding:80px 20px;'>
                    <div style='font-size:5rem; margin-bottom:20px;'>🩸</div>
                    <p style='color:#6b7280;'>Upload a blood report image<br>and click Analyze</p>
                </div>
                """, unsafe_allow_html=True)
            st.markdown("</div>", unsafe_allow_html=True)

    # ── MANUAL TAB ──
    with manual_tab:
        st.markdown("""
        <div style='background:rgba(124,58,237,0.08); border:1px solid rgba(124,58,237,0.2);
             padding:10px 14px; border-radius:12px; margin-bottom:16px; font-size:0.82rem; color:#c4b5fd;'>
            ✍️ Enter values from your blood report manually. Leave empty if not tested.
        </div>
        """, unsafe_allow_html=True)

        values = {}
        t1, t2, t3, t4, t5 = st.tabs(["🩸 CBC", "🍬 Sugar", "❤️ Lipids", "🫘 Kidney & Liver", "🦋 Thyroid & Others"])

        with t1:
            c1, c2 = st.columns(2)
            with c1:
                values["Hemoglobin"]  = st.text_input("Hemoglobin (g/dL)",  placeholder="M:13.5-17.5 F:12-15.5")
                values["RBC Count"]   = st.text_input("RBC Count (M/µL)",   placeholder="M:4.5-5.9 F:4.1-5.1")
                values["WBC Count"]   = st.text_input("WBC Count (/µL)",    placeholder="4500-11000")
                values["Platelets"]   = st.text_input("Platelets (/µL)",    placeholder="150000-400000")
                values["Hematocrit"]  = st.text_input("Hematocrit (%)",     placeholder="M:41-53 F:36-46")
                values["ESR"]         = st.text_input("ESR (mm/hr)",        placeholder="M:<15 F:<20")
            with c2:
                values["MCV"]         = st.text_input("MCV (fL)",           placeholder="80-100")
                values["MCH"]         = st.text_input("MCH (pg)",           placeholder="27-33")
                values["MCHC"]        = st.text_input("MCHC (g/dL)",        placeholder="32-36")
                values["Neutrophils"] = st.text_input("Neutrophils (%)",    placeholder="40-70")
                values["Lymphocytes"] = st.text_input("Lymphocytes (%)",    placeholder="20-40")
                values["Eosinophils"] = st.text_input("Eosinophils (%)",    placeholder="1-4")

        with t2:
            c1, c2 = st.columns(2)
            with c1:
                values["Fasting Sugar"] = st.text_input("Fasting Sugar (mg/dL)", placeholder="70-100")
                values["PP Sugar"]      = st.text_input("PP Sugar (mg/dL)",      placeholder="<140")
            with c2:
                values["HbA1c"]        = st.text_input("HbA1c (%)",             placeholder="<5.7")
                values["Random Sugar"] = st.text_input("Random Sugar (mg/dL)",  placeholder="<200")

        with t3:
            c1, c2 = st.columns(2)
            with c1:
                values["Total Cholesterol"] = st.text_input("Total Cholesterol (mg/dL)", placeholder="<200")
                values["HDL"]               = st.text_input("HDL Good (mg/dL)",          placeholder="M:>40 F:>50")
            with c2:
                values["LDL"]          = st.text_input("LDL Bad (mg/dL)",       placeholder="<100")
                values["Triglycerides"] = st.text_input("Triglycerides (mg/dL)", placeholder="<150")

        with t4:
            c1, c2 = st.columns(2)
            with c1:
                values["Creatinine"] = st.text_input("Creatinine (mg/dL)",    placeholder="M:0.7-1.3 F:0.6-1.1")
                values["Urea/BUN"]   = st.text_input("Urea/BUN (mg/dL)",      placeholder="7-20")
                values["Uric Acid"]  = st.text_input("Uric Acid (mg/dL)",     placeholder="M:3.4-7 F:2.4-6")
                values["Sodium"]     = st.text_input("Sodium (mEq/L)",         placeholder="136-145")
                values["Potassium"]  = st.text_input("Potassium (mEq/L)",      placeholder="3.5-5.0")
            with c2:
                values["SGPT/ALT"]  = st.text_input("SGPT/ALT (U/L)",         placeholder="7-56")
                values["SGOT/AST"]  = st.text_input("SGOT/AST (U/L)",         placeholder="10-40")
                values["Bilirubin"] = st.text_input("Total Bilirubin (mg/dL)", placeholder="0.2-1.2")
                values["Alk Phos"]  = st.text_input("Alk Phosphatase (U/L)",  placeholder="44-147")
                values["Albumin"]   = st.text_input("Albumin (g/dL)",         placeholder="3.5-5.0")

        with t5:
            c1, c2 = st.columns(2)
            with c1:
                values["TSH"]       = st.text_input("TSH (mIU/L)",       placeholder="0.4-4.0")
                values["T3"]        = st.text_input("T3 (ng/dL)",        placeholder="80-200")
                values["T4"]        = st.text_input("T4 (µg/dL)",        placeholder="5.0-12.0")
                values["Calcium"]   = st.text_input("Calcium (mg/dL)",   placeholder="8.5-10.5")
                values["Iron"]      = st.text_input("Iron (µg/dL)",      placeholder="60-170")
            with c2:
                values["Vitamin D"]   = st.text_input("Vitamin D (ng/mL)",   placeholder="20-50")
                values["Vitamin B12"] = st.text_input("Vitamin B12 (pg/mL)", placeholder="200-900")
                values["Ferritin"]    = st.text_input("Ferritin (ng/mL)",    placeholder="M:24-336 F:11-307")
                values["CRP"]         = st.text_input("CRP (mg/L)",          placeholder="<10")

        # Remove empty
        values = {k: v for k, v in values.items() if v and v.strip()}

        if st.button("🩸 Analyze Blood Report", use_container_width=True):
            if not values:
                st.warning("⚠ Please enter at least one blood test value!")
            else:
                with st.spinner("🤖 Analyzing your blood report..."):
                    result, success = analyze_blood_manual(values, age, symptoms)
                st.session_state.blood_result   = result
                st.session_state.blood_values   = values
                st.session_state.blood_method   = "manual"
                st.session_state.blood_img_used = False
                st.rerun()

        # Show manual results
        if "blood_result" in st.session_state and st.session_state.blood_result and st.session_state.get("blood_method") == "manual":
            st.markdown("<br>", unsafe_allow_html=True)
            st.markdown("<div class='section-header'>📊 AI Blood Report Analysis</div>", unsafe_allow_html=True)

            vals = st.session_state.get("blood_values", {})
            if vals:
                st.markdown("<div class='glass-box'>", unsafe_allow_html=True)
                st.markdown("<div class='section-title'>📋 Entered Values</div>", unsafe_allow_html=True)
                vcols = st.columns(4)
                for i, (k, v) in enumerate(vals.items()):
                    with vcols[i % 4]:
                        st.markdown(f"""
                        <div style='background:rgba(255,255,255,0.03);padding:7px 10px;
                             border-radius:9px;margin-bottom:6px;font-size:0.78rem;'>
                            <div style='color:#a89ec9;'>{k}</div>
                            <div style='color:#c4b5fd;font-weight:700;'>{v}</div>
                        </div>
                        """, unsafe_allow_html=True)
                st.markdown("</div>", unsafe_allow_html=True)

            rc1, rc2 = st.columns(2)
            result   = st.session_state.blood_result
            sections = [s for s in result.split("\n\n") if s.strip()]
            mid      = len(sections) // 2

            with rc1:
                for section in sections[:mid]:
                    lines = section.strip().split("\n")
                    title = lines[0].strip()
                    body  = "\n".join(lines[1:]).strip()
                    if "FINDINGS" in title.upper():
                        bg="rgba(99,102,241,0.1)"; border="rgba(99,102,241,0.25)"; tc="#818cf8"
                    else:
                        bg="rgba(239,68,68,0.1)"; border="rgba(239,68,68,0.25)"; tc="#f87171"
                    st.markdown(f"""
                    <div style='background:{bg};border:1px solid {border};
                         padding:14px 16px;border-radius:14px;margin-bottom:12px;'>
                        <div style='color:{tc};font-weight:700;font-size:0.92rem;margin-bottom:8px;'>{title}</div>
                        <div style='color:#d4d0f0;font-size:0.86rem;line-height:1.7;'>{body.replace(chr(10),"<br>")}</div>
                    </div>
                    """, unsafe_allow_html=True)

            with rc2:
                for section in sections[mid:]:
                    lines = section.strip().split("\n")
                    title = lines[0].strip()
                    body  = "\n".join(lines[1:]).strip()
                    if "CRITICAL" in title.upper():
                        bg="rgba(245,158,11,0.1)"; border="rgba(245,158,11,0.25)"; tc="#fbbf24"
                    elif "SPECIALIST" in title.upper():
                        bg="rgba(16,185,129,0.1)"; border="rgba(16,185,129,0.25)"; tc="#6ee7b7"
                    else:
                        bg="rgba(124,58,237,0.1)"; border="rgba(124,58,237,0.25)"; tc="#c4b5fd"
                    st.markdown(f"""
                    <div style='background:{bg};border:1px solid {border};
                         padding:14px 16px;border-radius:14px;margin-bottom:12px;'>
                        <div style='color:{tc};font-weight:700;font-size:0.92rem;margin-bottom:8px;'>{title}</div>
                        <div style='color:#d4d0f0;font-size:0.86rem;line-height:1.7;'>{body.replace(chr(10),"<br>")}</div>
                    </div>
                    """, unsafe_allow_html=True)

            d1, d2 = st.columns(2)
            with d1:
                st.download_button("📄 Download Report", data=result,
                    file_name="blood_report_analysis.txt", mime="text/plain", use_container_width=True)
            with d2:
                if st.button("🗑 Clear & Analyze Again", use_container_width=True):
                    st.session_state.blood_result = ""
                    st.session_state.blood_method = ""
                    st.rerun()

    st.markdown("""
    <div style='padding:10px 14px; background:rgba(245,158,11,0.08);
         border:1px solid rgba(245,158,11,0.2); border-radius:12px;
         font-size:0.78rem; color:#fbbf24; margin-top:12px;'>
        ⚠️ AI analysis is for reference only. Always consult a qualified doctor for proper diagnosis.
    </div>
    """, unsafe_allow_html=True)