# ============================================================
# report_scanner.py — Actual Image Scanner using Groq Llama 3.2 Vision
# ============================================================

import streamlit as st
import os
import base64
import io
from PIL import Image
from dotenv import load_dotenv
from groq import Groq
load_dotenv(r"C:\AI_Health\.env")

# ---------- GROQ SETUP ----------
groq_client = Groq(api_key=os.getenv("GROQ_API_KEY"))

# ---------- ANALYZE IMAGE (Using Groq Vision) ----------
def encode_image(image):
    buffered = io.BytesIO()
    image.save(buffered, format="PNG")
    return base64.b64encode(buffered.getvalue()).decode('utf-8')

def analyze_image(image, report_type, body_part, symptoms=""):
    try:
        base64_image = encode_image(image)
        
        prompt = f"""You are an expert medical AI specializing in radiology and lab report analysis. 
ALWAYS RESPOND IN ENGLISH, regardless of any non-English text in the report or user input.
Carefully analyze this {report_type} image of {body_part}.
{f"Patient symptoms: {symptoms}" if symptoms else ""}

Provide detailed analysis in these EXACT sections:

1. 🔍 FINDINGS:
What do you see in this {report_type}? Describe all visible features, abnormalities, and observations based on the image provided.

2. 🦠 POSSIBLE CONDITIONS:
List possible medical conditions based on what you see. Rate each as High/Medium/Low likelihood.

3. 👨‍⚕️ RECOMMENDED SPECIALIST:
Which doctor should be consulted? How urgent? (Emergency/Urgent/Soon/Routine)

4. ⚠️ CRITICAL OBSERVATIONS:
Any findings that need immediate attention?

5. 💡 NEXT STEPS:
What should the patient do next?

Be specific and accurate. Provide medical reasoning. 
Note: This is AI analysis for reference only — always consult a qualified doctor."""

        response = groq_client.chat.completions.create(
            model="llama-3.2-11b-vision-preview",
            messages=[
                {
                    "role": "user",
                    "content": [
                        {"type": "text", "text": prompt},
                        {
                            "type": "image_url",
                            "image_url": {
                                "url": f"data:image/png;base64,{base64_image}",
                            },
                        },
                    ],
                }
            ],
            max_tokens=1024,
            temperature=0.1 # Lower temperature for better factual consistency in reports
        )
        return response.choices[0].message.content, True

    except Exception as e:
        # Fallback to text analysis
        return analyze_text_fallback(report_type, body_part, symptoms, str(e)), False

# ---------- FALLBACK TEXT ANALYSIS ----------
def analyze_text_fallback(report_type, body_part, symptoms, error=""):
    try:
        prompt = f"""You are a medical AI. ALWAYS RESPOND IN ENGLISH.
A patient has a {report_type} of {body_part}.
{f"Symptoms: {symptoms}" if symptoms else ""}

Provide general medical guidance:

1. 🔍 FINDINGS:
Common findings in {report_type} of {body_part}

2. 🦠 POSSIBLE CONDITIONS:
Conditions typically detected by {report_type} of {body_part}
{f"Related to symptoms: {symptoms}" if symptoms else ""}

3. 👨‍⚕️ RECOMMENDED SPECIALIST:
Which doctor to consult for {report_type} analysis?

4. ⚠️ WARNING SIGNS:
Signs that need immediate attention

5. 💡 NEXT STEPS:
What patient should do next

Note: Image could not be analyzed directly. This is general guidance only."""

        response = groq_client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[{"role": "user", "content": prompt}],
            max_tokens=800,
            temperature=0.7
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"⚠ Analysis failed: {e}\n\nPlease describe your symptoms for manual analysis."

# ---------- SHOW REPORT SCANNER ----------
def show_report_scanner():
    st.markdown("""
        <div class="section-header">
            <img src="https://img.icons8.com/fluency/96/mri-scan.png" width="50" style="margin-bottom: 10px;">
            <br>
            🔬 Medical Report Scanner
        </div>
    """, unsafe_allow_html=True)

    # Info banner
    st.markdown("""
    <div style='background:rgba(16,185,129,0.1); border:1px solid rgba(16,185,129,0.25);
         padding:12px 16px; border-radius:14px; margin-bottom:18px;
         font-size:0.87rem; color:#6ee7b7; line-height:1.8;'>
        🤖 <b>Powered by Groq Llama 3.2 Vision</b> — Professional medical AI analysis!<br>
        📸 Upload X-Ray, CT Scan, Blood Report, MRI or any medical report image<br>
        🔍 AI will <b>actually read and analyze</b> your medical image in real-time
    </div>
    """, unsafe_allow_html=True)

    col1, col2 = st.columns(2)

    with col1:
        st.markdown("<div class='glass-box'>", unsafe_allow_html=True)
        st.markdown("<div class='section-title'>📤 Upload Medical Report</div>", unsafe_allow_html=True)

        report_type = st.selectbox("🏥 Report Type", [
            "X-Ray", "CT Scan", "MRI Scan", "Blood Report","Ultrasound",
             "ECG Report", "Prescription",
            "Other Medical Report"
        ])

        body_part = st.selectbox("🫀 Body Part", [
            "Chest / Lungs", "Brain / Head", "Abdomen / Stomach",
            "Heart", "Spine / Back", "Knee / Joints",
            "Hand / Arm", "Leg / Foot", "Full Body", "Other"
        ])

        symptoms = st.text_area(
            "📝 Your Symptoms (optional but helps!)",
            placeholder="e.g. chest pain, cough, fever, shortness of breath...",
            height=90
        )

        uploaded_file = st.file_uploader(
            "📎 Upload Report Image",
            type=["jpg", "jpeg", "png", "webp"],
            help="Upload X-Ray, CT Scan, MRI, Ultrasound or any medical image"
        )

        if uploaded_file:
            image = Image.open(uploaded_file)
            st.image(image, caption=f"📋 {report_type} — {body_part}", use_column_width=True)

            if st.button("🔬 Analyze with AI", use_container_width=True):
                with st.spinner("🤖 Groq Llama 3.2 is analyzing your image... Please wait..."):
                    result, used_image = analyze_image(image, report_type, body_part, symptoms)
                st.session_state.report_result  = result
                st.session_state.report_type    = report_type
                st.session_state.report_body    = body_part
                st.session_state.report_img_used = used_image
                st.rerun()
        else:
            st.markdown("""
            <div style='text-align:center; padding:40px 20px;
                 border:2px dashed rgba(124,58,237,0.3); border-radius:16px;
                 background:rgba(124,58,237,0.04); margin-top:10px;'>
                <div style='font-size:3rem; margin-bottom:12px;'>📎</div>
                <p style='color:#7c74a8; font-size:0.9rem; font-weight:500;'>
                    Upload your medical report image<br>
                    <span style='font-size:0.8rem; opacity:0.7;'>JPG, PNG, WEBP supported</span>
                </p>
            </div>
            """, unsafe_allow_html=True)

        st.markdown("""
        <div style='margin-top:12px; padding:10px 14px;
             background:rgba(16,185,129,0.07); border:1px solid rgba(16,185,129,0.15);
             border-radius:11px; font-size:0.8rem; color:#6ee7b7;'>
            ✅ X-Ray · CT Scan · MRI · Ultrasound · Blood Report · ECG
        </div>
        """, unsafe_allow_html=True)

        st.markdown("</div>", unsafe_allow_html=True)

        st.markdown("""
        <div style='padding:10px 14px; background:rgba(245,158,11,0.08);
             border:1px solid rgba(245,158,11,0.2); border-radius:11px;
             font-size:0.78rem; color:#fbbf24; margin-top:6px;'>
            ⚠️ AI analysis is for reference only. Always consult a qualified doctor.
        </div>
        """, unsafe_allow_html=True)

    with col2:
        st.markdown("<div class='glass-box'>", unsafe_allow_html=True)
        st.markdown("<div class='section-title'>📋 AI Analysis Result</div>", unsafe_allow_html=True)

        if "report_result" in st.session_state and st.session_state.report_result:
            result      = st.session_state.report_result
            report_name = st.session_state.get("report_type", "Report")
            body_name   = st.session_state.get("report_body", "")
            img_used    = st.session_state.get("report_img_used", False)

            # Badges
            st.markdown(f"""
            <div style='margin-bottom:14px; display:flex; gap:8px; flex-wrap:wrap;'>
                <span style='background:rgba(124,58,237,0.2); color:#c4b5fd;
                     padding:5px 14px; border-radius:20px; font-size:0.8rem; font-weight:700;
                     border:1px solid rgba(124,58,237,0.3);'>🔬 {report_name}</span>
                <span style='background:rgba(16,185,129,0.12); color:#6ee7b7;
                     padding:5px 14px; border-radius:20px; font-size:0.8rem; font-weight:600;
                     border:1px solid rgba(16,185,129,0.25);'>📍 {body_name}</span>
                <span style='background:{"rgba(16,185,129,0.12)" if img_used else "rgba(245,158,11,0.1)"};
                     color:{"#34d399" if img_used else "#fbbf24"};
                     padding:5px 14px; border-radius:20px; font-size:0.8rem; font-weight:600;
                     border:1px solid {"rgba(16,185,129,0.25)" if img_used else "rgba(245,158,11,0.25)"};'>
                     {"🖼️ Image Analyzed" if img_used else "📝 Text Analysis"}</span>
            </div>
            """, unsafe_allow_html=True)

            # Parse and display sections
            sections = result.split("\n\n")
            for section in sections:
                if section.strip():
                    lines = section.strip().split("\n")
                    if lines:
                        title = lines[0].strip()
                        body  = "\n".join(lines[1:]).strip()

                        if "FINDINGS" in title.upper():
                            bg = "rgba(99,102,241,0.1)"; border = "rgba(99,102,241,0.25)"; tc = "#818cf8"
                        elif "CONDITIONS" in title.upper():
                            bg = "rgba(239,68,68,0.1)"; border = "rgba(239,68,68,0.25)"; tc = "#f87171"
                        elif "SPECIALIST" in title.upper() or "RECOMMENDED" in title.upper():
                            bg = "rgba(16,185,129,0.1)"; border = "rgba(16,185,129,0.25)"; tc = "#6ee7b7"
                        elif "CRITICAL" in title.upper() or "WARNING" in title.upper():
                            bg = "rgba(245,158,11,0.1)"; border = "rgba(245,158,11,0.25)"; tc = "#fbbf24"
                        elif "STEPS" in title.upper() or "NEXT" in title.upper():
                            bg = "rgba(124,58,237,0.1)"; border = "rgba(124,58,237,0.25)"; tc = "#c4b5fd"
                        else:
                            bg = "rgba(255,255,255,0.04)"; border = "rgba(255,255,255,0.08)"; tc = "#f0edff"

                        body_html = body.replace("\n", "<br>")
                        st.markdown(f"""
                        <div style='background:{bg}; border:1px solid {border};
                             padding:14px 16px; border-radius:14px; margin-bottom:12px;'>
                            <div style='color:{tc}; font-weight:700; font-size:0.92rem;
                                 margin-bottom:8px;'>{title}</div>
                            <div style='color:#d4d0f0; font-size:0.86rem; line-height:1.7;'>{body_html}</div>
                        </div>
                        """, unsafe_allow_html=True)

            # Download
            st.download_button(
                "📄 Download Analysis",
                data=result,
                file_name=f"{report_name}_groq_analysis.txt",
                mime="text/plain"
            )

            if st.button("🗑 Clear & Analyze New"):
                st.session_state.report_result = ""
                st.rerun()

        else:
            st.markdown("""
            <div style='text-align:center; padding:80px 20px;'>
                <div style='font-size:5rem; margin-bottom:20px;'>🔬</div>
                <p style='font-size:1.1rem; font-weight:600; color:#6b7280;'>No analysis yet</p>
                <p style='font-size:0.85rem; color:#4b5563;'>
                    Upload a medical image<br>and click Analyze with Groq AI
                </p>
            </div>
            """, unsafe_allow_html=True)

        st.markdown("</div>", unsafe_allow_html=True)