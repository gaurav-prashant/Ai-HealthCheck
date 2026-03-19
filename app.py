# ============================================================
# app.py — AI Health Checker (Complete Fixed Version)
# ============================================================

from dotenv import load_dotenv
load_dotenv()

import streamlit as st
import pickle, numpy as np, pandas as pd, io
from datetime import datetime
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet

from auth import save_user, verify_user, get_user_name
from ai_functions import ai_chatbot, get_ai_doctor, voice_input
from appointments import show_appointment_section
from styles import get_css
from diet_plan import show_diet_plan_section
from bmi_calculator import show_bmi_section
from report_scanner import show_report_scanner
from eye_test import show_eye_test
from hospital_finder import show_hospital_finder
from blood_report import show_blood_report
from medical_store import show_medical_store
from skin_disease import show_skin_disease
from medicine_reminder import show_medicine_reminder

# ── PAGE CONFIG ──
st.set_page_config(
    page_title="AI Health Checker",
    layout="wide",
    page_icon="🏥",
    initial_sidebar_state="collapsed",
    menu_items={}
)
st.markdown(get_css(), unsafe_allow_html=True)

# ── SESSION STATE ──
for k, v in {
    "logged_in": False, "username": "", "chat": [], "result": [], "doctor": "",
    "diet_plan": "", "active_page": "dashboard", "history": [], "bmi_result": None,
    "report_result": "", "eye_test_started": False, "urine_result": "",
    "stool_result": "", "blood_result": "", "skin_result": ""
}.items():
    if k not in st.session_state:
        st.session_state[k] = v

# ── MODEL LOADER ──
@st.cache_resource
def load_model():
    try:
        return pickle.load(open("model.pkl", "rb"))
    except:
        return {"model": None, "accuracy": 0.0}

# ── HELPERS ──
def get_medical_advice(d):
    a = {
        "Flu":            (["Paracetamol", "Cough Syrup"], ["Rest", "Drink fluids"]),
        "Common Cold":    (["Cetirizine"],                 ["Stay warm"]),
        "COVID-19":       (["Paracetamol", "Vitamin C"],   ["Isolation", "Mask"]),
        "Migraine":       (["Ibuprofen"],                  ["Sleep", "Avoid stress"]),
        "Food Poisoning": (["ORS", "Antacid"],             ["Drink water"]),
        "Heart Problem":  (["Aspirin"],                    ["Rest", "See cardiologist"])
    }
    return a.get(d, (["Consult Doctor"], ["Checkup"]))


def generate_pdf(result, doctor, pname, page, ref, pdate, acc):
    buf = io.BytesIO()
    doc = SimpleDocTemplate(buf)
    sty = getSampleStyleSheet()
    c = []
    c.append(Paragraph("AI Multispeciality Hospital", sty["Title"]))
    c.append(Paragraph("Medical Diagnosis Report",    sty["Heading1"]))
    c.append(Spacer(1, 10))
    c.append(Paragraph(f"Patient: {pname} | Age: {page} | Referred By: {ref} | Date: {pdate}", sty["Normal"]))
    c.append(Paragraph(f"Model Accuracy: {acc*100:.2f}%", sty["Normal"]))
    c.append(Spacer(1, 15))
    c.append(Paragraph("Prediction Results:", sty["Heading2"]))
    for d, p in result:
        c.append(Paragraph(f"{d} — {p:.2f}%", sty["Normal"]))
    c.append(Spacer(1, 10))
    c.append(Paragraph(f"Doctor Suggested: {doctor}", sty["Heading3"]))
    c.append(Spacer(1, 30))
    c.append(Paragraph("__________________________", sty["Normal"]))
    c.append(Paragraph("Authorized Doctor Signature", sty["Normal"]))
    doc.build(c)
    buf.seek(0)
    return buf

# ── LOGIN PAGE CSS ──
LOGIN_CSS = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@300;400;500;600;700&family=Syne:wght@700;800;900&display=swap');
[data-testid="stAppViewContainer"]{
    background:radial-gradient(ellipse at 20% 50%,#0d0221 0%,#000 40%,#020818 100%)!important;
}
[data-testid="stHeader"]{background:transparent!important;}
.block-container{padding-top:0!important;}
.mesh{position:fixed;top:0;left:0;width:100%;height:100%;z-index:0;pointer-events:none;
  background:radial-gradient(ellipse 80% 60% at 10% 20%,rgba(120,40,200,.22) 0%,transparent 60%),
  radial-gradient(ellipse 60% 50% at 90% 80%,rgba(0,180,255,.12) 0%,transparent 60%);
  animation:mA 8s ease-in-out infinite alternate;}
@keyframes mA{0%{opacity:.8}100%{opacity:1}}
.grid{position:fixed;top:0;left:0;width:100%;height:100%;z-index:0;pointer-events:none;
  background-image:linear-gradient(rgba(120,40,200,.05) 1px,transparent 1px),
  linear-gradient(90deg,rgba(120,40,200,.05) 1px,transparent 1px);
  background-size:60px 60px;}
.lhero{text-align:center;padding:50px 20px 20px;position:relative;z-index:2;}
.logo-c{width:110px;height:110px;margin:0 auto 24px;position:relative;
  display:inline-flex;align-items:center;justify-content:center;}
.logo-ro{position:absolute;inset:0;border-radius:50%;
  background:conic-gradient(#7c3aed 0%,#06b6d4 25%,#ec4899 50%,#f59e0b 75%,#7c3aed 100%);
  animation:rs 4s linear infinite;}
.logo-ri{position:absolute;inset:4px;border-radius:50%;background:#000;}
.logo-e{position:relative;z-index:1;font-size:3rem;animation:lb 2.5s ease-in-out infinite;}
@keyframes rs{to{transform:rotate(360deg)}}
@keyframes lb{0%,100%{transform:translateY(0)}50%{transform:translateY(-10px)}}
.ltitle{font-family:'Syne',sans-serif!important;font-size:3.8rem;font-weight:900;
  line-height:1;letter-spacing:-2px;
  background:linear-gradient(135deg,#fff 0%,#a78bfa 25%,#38bdf8 55%,#fb923c 80%,#f472b6 100%);
  -webkit-background-clip:text;-webkit-text-fill-color:transparent;background-clip:text;
  margin-bottom:6px;background-size:200% auto;animation:ts 4s ease-in-out infinite;}
@keyframes ts{0%{background-position:0% center}50%{background-position:100% center}100%{background-position:0% center}}
.lsub{font-family:'Space Grotesk',sans-serif!important;font-size:.88rem;
  letter-spacing:4px;color:rgba(255,255,255,.25);text-transform:uppercase;margin-bottom:24px;}
.scanline{width:300px;height:1px;margin:0 auto 24px;position:relative;}
.scanline::before{content:'';position:absolute;inset:0;
  background:linear-gradient(90deg,transparent,#a78bfa,#38bdf8,#f472b6,transparent);
  animation:sp 2s ease-in-out infinite;}
@keyframes sp{0%,100%{opacity:.3;transform:scaleX(.4)}50%{opacity:1;transform:scaleX(1)}}
.lstats{display:inline-flex;gap:0;background:rgba(255,255,255,.03);
  border:1px solid rgba(255,255,255,.07);border-radius:20px;overflow:hidden;margin-bottom:36px;}
.lstat{padding:14px 22px;text-align:center;border-right:1px solid rgba(255,255,255,.06);}
.lstat:last-child{border-right:none;}
.lsn{font-family:'Syne',sans-serif;font-size:1.4rem;font-weight:900;
  background:linear-gradient(135deg,#a78bfa,#38bdf8);
  -webkit-background-clip:text;-webkit-text-fill-color:transparent;display:block;}
.lsl{font-size:.58rem;color:rgba(255,255,255,.2);text-transform:uppercase;
  letter-spacing:1.5px;margin-top:2px;display:block;}
/* ── INPUT & BUTTON FIX ── */
.stTextInput,.stTextInput>div,.stTextInput>div>div,.stTextInput>div>div>input{
  pointer-events:all!important;position:relative!important;z-index:9999!important;
  cursor:text!important;}
.stButton,.stButton>button{pointer-events:all!important;position:relative!important;
  z-index:9999!important;opacity:1!important;visibility:visible!important;
  display:flex!important;}
.stTabs,.stTabs>div{position:relative!important;z-index:9999!important;}
.mesh,.grid{pointer-events:none!important;z-index:0!important;}
</style>"""

# ── DASHBOARD CSS ──
DASH_CSS = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@300;400;500;600;700&family=Syne:wght@700;800;900&display=swap');
.wt{text-align:center;margin-bottom:24px;font-family:'Space Grotesk',sans-serif!important;
  font-size:1.05rem;color:rgba(255,255,255,.3);letter-spacing:.5px;}
.wt b{color:#a78bfa;font-family:'Syne',sans-serif;}
.nh{background:linear-gradient(135deg,rgba(124,58,237,.12),rgba(13,18,32,.9),rgba(6,182,212,.06));
  border:1px solid rgba(124,58,237,.18);border-radius:20px;padding:22px 28px;margin-bottom:20px;
  position:relative;overflow:hidden;box-shadow:0 4px 30px rgba(0,0,0,.4);}
.nh::before{content:'';position:absolute;top:0;left:0;right:0;height:1px;
  background:linear-gradient(90deg,transparent,#a78bfa,#38bdf8,#f472b6,transparent);}
.ht{font-family:'Syne',sans-serif!important;font-size:2rem;font-weight:900;
  letter-spacing:-.5px;margin:0;
  background:linear-gradient(135deg,#fff,#a78bfa,#38bdf8);
  -webkit-background-clip:text;-webkit-text-fill-color:transparent;background-clip:text;}
.hs{color:rgba(255,255,255,.25);font-size:.78rem;margin:5px 0 10px;
  letter-spacing:2px;text-transform:uppercase;font-family:'Space Grotesk',sans-serif!important;}
.hb{display:inline-block;padding:4px 13px;border-radius:20px;font-size:.73rem;font-weight:600;margin-right:7px;}
.hp{background:rgba(124,58,237,.18);color:#a78bfa;border:1px solid rgba(124,58,237,.28);}
.hc{background:rgba(6,182,212,.12);color:#67e8f9;border:1px solid rgba(6,182,212,.22);}
.dc{border-radius:18px;padding:26px 14px 18px;text-align:center;margin-bottom:4px;
  position:relative;overflow:hidden;transition:all .3s cubic-bezier(.25,.8,.25,1);
  min-height:185px;display:flex;flex-direction:column;align-items:center;
  justify-content:center;gap:9px;box-shadow:0 8px 28px rgba(0,0,0,.35);}
.dc::before{content:'';position:absolute;top:0;left:15%;right:15%;height:1px;
  background:linear-gradient(90deg,transparent,rgba(255,255,255,.15),transparent);}
.dc::after{content:'';position:absolute;inset:0;background:radial-gradient(circle at 50% 0%,rgba(255,255,255,.1) 0%,transparent 70%);opacity:0;transition:opacity .3s;}
.dc:hover{transform:translateY(-6px) scale(1.02);box-shadow:0 15px 35px rgba(124,58,237,.3);border-color:rgba(196,181,253,.4)!important;}
.dc:hover::after{opacity:1;}
.dc:hover .ci{transform:scale(1.15);transition:transform .3s ease;}
.ci{font-size:2.6rem;line-height:1;filter:drop-shadow(0 4px 10px rgba(0,0,0,.3));transition:transform .3s ease;}
.ct{font-family:'Syne',sans-serif!important;font-size:.95rem;font-weight:800;letter-spacing:.3px;}
.cd{font-size:.74rem;color:rgba(255,255,255,.35);line-height:1.5;max-width:150px;
  font-family:'Space Grotesk',sans-serif!important;}
/* Dashboard Open buttons — invisible overlay */
.card-btn .stButton>button{
  opacity:0!important;height:185px!important;min-height:185px!important;
  width:100%!important;margin-top:-189px!important;
  position:relative!important;z-index:100!important;
  background:transparent!important;border:none!important;
  box-shadow:none!important;cursor:pointer!important;}
/* All other buttons — fully visible */
.stButton>button{
  background:linear-gradient(135deg,#3b0764,#581c87,#7c3aed)!important;
  color:#f0edff!important;border:1px solid rgba(196,181,253,.2)!important;
  border-radius:12px!important;padding:10px 20px!important;font-weight:700!important;
  font-size:.87rem!important;transition:all .25s ease!important;
  box-shadow:0 4px 14px rgba(124,58,237,.3)!important;
  height:auto!important;opacity:1!important;visibility:visible!important;
  margin-top:0!important;display:flex!important;}
.stButton>button:hover{transform:translateY(-2px)!important;
  box-shadow:0 8px 24px rgba(124,58,237,.5)!important;filter:brightness(1.1)!important;}
.stDownloadButton>button{
  background:linear-gradient(135deg,#78350f,#d97706)!important;
  color:#fef3c7!important;border-radius:12px!important;font-weight:700!important;}
.bmi-result{text-align:center;padding:28px;border-radius:18px;margin-top:14px;font-size:2rem;font-weight:900;}
.bmi-normal{background:rgba(5,150,105,.12);border:1px solid rgba(5,150,105,.3);color:#34d399;}
.bmi-under{background:rgba(99,102,241,.12);border:1px solid rgba(99,102,241,.3);color:#818cf8;}
.bmi-over{background:rgba(249,115,22,.12);border:1px solid rgba(249,115,22,.3);color:#fb923c;}
.bmi-obese{background:rgba(239,68,68,.12);border:1px solid rgba(239,68,68,.3);color:#f87171;}
</style>"""

# ══════════════════════════════════════════
# LOGIN PAGE
# ══════════════════════════════════════════
if not st.session_state.logged_in:
    st.markdown(LOGIN_CSS, unsafe_allow_html=True)
    st.markdown("""
    <div class="mesh"></div>
    <div class="grid"></div>
    <div class="lhero">
        <div class="logo-c">
            <div class="logo-ro"></div>
            <div class="logo-ri"></div>
            <div class="logo-e">🏥</div>
        </div>
        <div class="ltitle">AI HEALTH</div>
        <div class="ltitle" style="font-size:2.4rem;letter-spacing:2px;margin-top:-8px;">CHECKER</div>
        <div class="lsub">Next Gen &nbsp;·&nbsp; AI Powered &nbsp;·&nbsp; Smart Diagnosis</div>
        <div class="scanline"></div>
        <div class="lstats">
            <div class="lstat"><span class="lsn">14+</span><span class="lsl">Features</span></div>
            <div class="lstat"><span class="lsn">56+</span><span class="lsl">Doctors</span></div>
            <div class="lstat"><span class="lsn">100%</span><span class="lsl">AI Power</span></div>
            <div class="lstat"><span class="lsn">FREE</span><span class="lsl">Forever</span></div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    _, cc, _ = st.columns([1, 2, 1])
    with cc:
        t1, t2 = st.tabs(["🔐 Login", "📝 Register"])

        with t1:
            st.markdown("""
            <div style='text-align:center;margin-bottom:16px;'>
                <div style='font-family:Syne,sans-serif;font-size:1.2rem;font-weight:800;
                     letter-spacing:2px;color:white;'>SYSTEM ACCESS</div>
                <div style='color:rgba(255,255,255,.25);font-size:.75rem;letter-spacing:2px;
                     text-transform:uppercase;margin-top:4px;'>Enter credentials to continue</div>
            </div>
            """, unsafe_allow_html=True)
            lu = st.text_input("📧 Email", key="login_user", placeholder="Enter email")
            lp = st.text_input("🔒 Password", type="password", key="login_pass", placeholder="Enter password")
            if st.button("⚡ LOGIN", use_container_width=True):
                if lu and lp:
                    if verify_user(lu, lp):
                        st.session_state.logged_in   = True
                        st.session_state.username    = lu
                        st.session_state.active_page = "dashboard"
                        st.success(f"✅ Welcome, {get_user_name(lu)}!")
                        st.rerun()
                    else:
                        st.error("⛔ Wrong username or password!")
                else:
                    st.warning("⚠ Please enter credentials!")

        with t2:
            st.markdown("""
            <div style='text-align:center;margin-bottom:16px;'>
                <div style='font-family:Syne,sans-serif;font-size:1.2rem;font-weight:800;
                     letter-spacing:2px;color:white;'>CREATE PROFILE</div>
                <div style='color:rgba(255,255,255,.25);font-size:.75rem;letter-spacing:2px;
                     text-transform:uppercase;margin-top:4px;'>Join the health platform</div>
            </div>
            """, unsafe_allow_html=True)
            rn  = st.text_input("👤 Full Name",        key="reg_name",  placeholder="Your full name")
            re  = st.text_input("📧 Email",            key="reg_email", placeholder="your@email.com")
            ru  = st.text_input("🆔 Username",         key="reg_user",  placeholder="Choose username")
            rp  = st.text_input("🔒 Password",         type="password", key="reg_pass",  placeholder="Min 6 characters")
            rp2 = st.text_input("🔒 Confirm Password", type="password", key="reg_pass2", placeholder="Repeat password")
            if st.button("🚀 CREATE ACCOUNT", use_container_width=True):
                if rn and re and ru and rp and rp2:
                    if rp != rp2:
                        st.error("❌ Passwords do not match!")
                    elif len(rp) < 6:
                        st.warning("⚠ Min 6 characters!")
                    else:
                        if save_user(ru, rp, re, rn):
                            st.success("✅ Account created! Please login.")
                            st.balloons()
                else:
                    st.warning("⚠ Please fill all fields!")

# ══════════════════════════════════════════
# MAIN APP
# ══════════════════════════════════════════
else:
    # Load model only after login (faster login page)
    data     = load_model()
    model    = data["model"]
    accuracy = data["accuracy"]
    ufn      = get_user_name(st.session_state.username)

    st.markdown(DASH_CSS, unsafe_allow_html=True)

    # ── HEADER ──
    h1, h2 = st.columns([9, 1])
    with h1:
        st.markdown(f"""
        <div class='nh'>
            <div class='ht'>🏥 AI Health Checker</div>
            <div class='hs'>Smart Diagnosis · AI Chatbot · Specialist Appointments</div>
            <span class='hb hp'>🎯 Accuracy: {accuracy*100:.1f}%</span>
            <span class='hb hc'>👤 {ufn} (@{st.session_state.username})</span>
        </div>
        """, unsafe_allow_html=True)
    with h2:
        st.markdown("<br><br>", unsafe_allow_html=True)
        if st.button("🚪 Logout"):
            for k, v in {
                "logged_in": False, "username": "", "chat": [], "result": [], "doctor": "",
                "diet_plan": "", "history": [], "bmi_result": None, "report_result": "",
                "urine_result": "", "stool_result": "", "blood_result": "", "skin_result": ""
            }.items():
                st.session_state[k] = v
            st.session_state.active_page = "dashboard"
            st.rerun()

    # ══════════════════════════════════════════
    # DASHBOARD
    # ══════════════════════════════════════════
    if st.session_state.active_page == "dashboard":
        st.markdown(f"<div class='wt'>👋 Hello <b>{ufn}</b>! What would you like to do today?</div>", unsafe_allow_html=True)

        cards = [
            ("prediction", "🧠", "Health Prediction",   "Check symptoms & get AI diagnosis",   "rgba(99,102,241,.12)",  "rgba(99,102,241,.35)",  "#818cf8"),
            ("chatbot",    "🤖", "AI Doctor Chatbot",   "Ask health questions to AI doctor",   "rgba(168,85,247,.12)",  "rgba(168,85,247,.35)",  "#d8b4fe"),
            ("appointment","📅", "Doctor Appointment",  "Book specialist appointments",         "rgba(20,184,166,.12)",  "rgba(20,184,166,.35)",  "#5eead4"),
            ("diet",       "🥗", "AI Diet Plan",        "Personalized meal & diet plan",        "rgba(249,115,22,.12)",  "rgba(249,115,22,.35)",  "#fdba74"),
            ("history",    "📊", "Patient History",     "View past health predictions",         "rgba(236,72,153,.12)",  "rgba(236,72,153,.35)",  "#f9a8d4"),
            ("bmi",        "💪", "BMI Calculator",      "Calculate Body Mass Index",            "rgba(234,179,8,.12)",   "rgba(234,179,8,.35)",   "#fde047"),
            ("scanner",    "🔬", "Report Scanner",      "Analyze X-Ray & CT Scan with AI",     "rgba(14,165,233,.12)",  "rgba(14,165,233,.35)",  "#7dd3fc"),
            ("eyetest",    "👁️", "Eye Test",            "Check your eyesight with voice",       "rgba(139,92,246,.12)",  "rgba(139,92,246,.35)",  "#c4b5fd"),
            ("hospital",   "🗺️", "Hospital Finder",     "Find nearby hospitals",                "rgba(239,68,68,.12)",   "rgba(239,68,68,.35)",   "#fca5a5"),
            ("blood",      "🩸", "Blood Report",        "Analyze blood test & find diseases",   "rgba(220,38,38,.12)",   "rgba(220,38,38,.35)",   "#fca5a5"),
            ("medstore",   "💊", "Medical Store",       "Find nearby pharmacy & medicine",      "rgba(16,185,129,.12)",  "rgba(16,185,129,.35)",  "#6ee7b7"),
            ("skin",       "🔬", "Skin Disease",        "Detect skin disease from photo",       "rgba(251,146,60,.12)",  "rgba(251,146,60,.35)",  "#fdba74"),
            ("reminder",   "💊", "Medicine Reminder",   "Set medicine alarms & alerts",         "rgba(236,72,153,.12)",  "rgba(236,72,153,.35)",  "#f9a8d4"),
        ]

        for row_start in range(0, len(cards), 3):
            row  = cards[row_start:row_start + 3]
            cols = st.columns(3)
            for i, (pg, ic, ti, de, cbg, bd, tc) in enumerate(row):
                with cols[i]:
                    st.markdown(f"""
                    <div class="dc" style="background:{cbg};border:1px solid {bd};">
                        <div class="ci">{ic}</div>
                        <div class="ct" style="color:{tc};">{ti}</div>
                        <div class="cd">{de}</div>
                    </div>
                    """, unsafe_allow_html=True)
                    with st.container():
                        st.markdown("<div class='card-btn'>", unsafe_allow_html=True)
                        if st.button("Open", key=f"btn_{pg}", use_container_width=True):
                            st.session_state.active_page = pg
                            st.rerun()
                        st.markdown("</div>", unsafe_allow_html=True)
            st.markdown("<br>", unsafe_allow_html=True)

    # ── HEALTH PREDICTION ──
    elif st.session_state.active_page == "prediction":
        if st.button("⬅ Back to Dashboard"):
            st.session_state.active_page = "dashboard"
            st.rerun()

        st.markdown("<div class='section-header'>🧠 Health Prediction</div>", unsafe_allow_html=True)

        # ✅ FIX 1: Properly unpack columns so 'with' works correctly
        c1, c2, c3, c4 = st.columns(4)
        with c1:
            pa = st.number_input("🎂 Age", 1, 120)

        r1, r2 = st.columns(2)
        with r1:
            st.markdown("<div class='section-title'>✅ Select Your Symptoms</div>", unsafe_allow_html=True)
            syms = [
                "Fever", "Cough", "Headache", "Fatigue", "Vomiting", "Cold",
                "Body Pain", "Sore Throat", "Breathlessness", "Chest Pain",
                "Dizziness", "Diarrhea", "Nausea", "Loss of Smell", "Loss of Taste",
                "Runny Nose", "Sneezing", "Joint Pain", "Muscle Pain", "Back Pain",
                "Skin Rash", "Itching", "Swelling", "Weight Loss", "Night Sweats",
                "Chills", "Sweating", "Weakness", "Loss of Appetite", "Stomach Pain",
                "Bloating", "Constipation", "Burning Urination", "Frequent Urination",
                "Eye Redness", "Ear Pain", "Neck Stiffness", "Confusion",
                "High Blood Pressure", "Palpitations", "Anxiety"
            ]
            ca, cb = st.columns(2)
            inp = []
            for i, s in enumerate(syms):
                if i % 2 == 0:
                    with ca:
                        inp.append(st.checkbox(s))
                else:
                    with cb:
                        inp.append(st.checkbox(s))

            st.markdown("<br>", unsafe_allow_html=True)
            if st.button("🔍 Check My Health", use_container_width=True):
                if model:
                    with st.spinner("🧠 Analyzing..."):
                        idata = np.array([list(map(int, inp))])
                        pred  = model.predict(idata)[0]
                        prob  = model.predict_proba(idata)[0]
                        res   = sorted(zip(model.classes_, prob * 100), key=lambda x: x[1], reverse=True)[:3]
                        doc   = get_ai_doctor(pred)
                    st.session_state.result = res
                    st.session_state.doctor = doc
                    # ✅ FIX 3: Added 'date' key so history page doesn't crash
                    st.session_state.history.append({
                        "date":        datetime.now().strftime("%Y-%m-%d"),
                        "disease":     res[0][0],
                        "probability": f"{res[0][1]:.1f}%",
                        "doctor":      doc
                    })
                    st.rerun()
                else:
                    st.error("❌ Model not loaded. Please ensure model.pkl exists.")

        with r2:
            st.markdown("<div class='section-title'>📊 Prediction Result</div>", unsafe_allow_html=True)
            if st.session_state.result:
                for d, p in st.session_state.result:
                    st.markdown(f"<div class='result-card'>🦠 {d} <span class='badge'>{p:.1f}%</span></div>", unsafe_allow_html=True)
                    meds, prec = get_medical_advice(d)
                    st.markdown(f"<div class='doctor-box'>💊 <b>Medicines:</b> {', '.join(meds)}</div>", unsafe_allow_html=True)
                    st.markdown(f"<div class='doctor-box'>🛡 <b>Precautions:</b> {', '.join(prec)}</div>", unsafe_allow_html=True)
                st.markdown(f"<div class='doctor-box'>👨‍⚕️ <b>Recommended:</b> {st.session_state.doctor}</div>", unsafe_allow_html=True)
                st.bar_chart(pd.DataFrame(st.session_state.result, columns=["Disease", "Probability"]).set_index("Disease"))

                # ✅ FIX 2: Pass all required arguments to generate_pdf
                pdf = generate_pdf(
                    st.session_state.result,
                    st.session_state.doctor,
                    ufn,                                        # patient name
                    pa,                                         # age
                    "Self",                                     # referred by
                    datetime.now().strftime("%Y-%m-%d"),        # date
                    accuracy                                    # model accuracy
                )
                st.download_button("📄 Download PDF Report", pdf, "health_report.pdf")
            else:
                st.markdown("""<div style='text-align:center;padding:40px;color:#475569;'>
                    <div style='font-size:3rem;'>🩺</div>
                    <p>Select symptoms and click Check My Health</p>
                </div>""", unsafe_allow_html=True)

    # ── AI CHATBOT ──
    elif st.session_state.active_page == "chatbot":
        if st.button("⬅ Back to Dashboard"):
            st.session_state.active_page = "dashboard"
            st.rerun()
        st.markdown("<div class='section-header'>🤖 AI Doctor Chatbot</div>", unsafe_allow_html=True)
        r1, r2 = st.columns(2)
        with r1:
            st.markdown("<div class='section-title'>💬 Ask the AI Doctor</div>", unsafe_allow_html=True)
            st.text_input("👤 Your Name", value=ufn)
            msg = st.text_input("💬 Type your health question")
            c1, c2 = st.columns(2)
            with c1:
                if st.button("📨 Send", use_container_width=True):
                    if msg:
                        with st.spinner("🤖 Thinking..."):
                            reply = ai_chatbot(msg)
                        st.session_state.chat.extend([("You", msg), ("AI", reply)])
                        st.rerun()
            with c2:
                if st.button("🎤 Speak", use_container_width=True):
                    spoken = voice_input()
                    if spoken:
                        with st.spinner("🤖 Thinking..."):
                            reply = ai_chatbot(spoken)
                        st.session_state.chat.extend([("You", spoken), ("AI", reply)])
                        st.rerun()
        with r2:
            st.markdown("<div class='section-title'>📜 Chat History</div>", unsafe_allow_html=True)
            if st.button("🗑 Clear Chat"):
                st.session_state.chat = []
            for s, m in st.session_state.chat:
                cls = "user-bubble" if s == "You" else "ai-bubble"
                ico = "🧑" if s == "You" else "🤖"
                st.markdown(f"<div class='{cls}'>{ico} {m}</div>", unsafe_allow_html=True)

    # ── DOCTOR APPOINTMENT ──
    elif st.session_state.active_page == "appointment":
        if st.button("⬅ Back to Dashboard"):
            st.session_state.active_page = "dashboard"
            st.rerun()
        show_appointment_section(st.session_state.username, ufn)

    # ── DIET PLAN ──
    elif st.session_state.active_page == "diet":
        if st.button("⬅ Back to Dashboard"):
            st.session_state.active_page = "dashboard"
            st.rerun()
        show_diet_plan_section()

    # ── PATIENT HISTORY ──
    elif st.session_state.active_page == "history":
        if st.button("⬅ Back to Dashboard"):
            st.session_state.active_page = "dashboard"
            st.rerun()
        st.markdown("<div class='section-header'>📊 Patient History</div>", unsafe_allow_html=True)
        if st.session_state.history:
            for h in reversed(st.session_state.history):
                st.markdown(f"""<div class='appt-card'>
                    📅 <b>Date:</b> {h.get('date', 'N/A')}<br>
                    🦠 <b>Disease:</b> {h.get('disease', 'N/A')}<br>
                    📊 <b>Probability:</b> {h.get('probability', 'N/A')}<br>
                    👨‍⚕️ <b>Doctor:</b> {h.get('doctor', 'N/A')}
                </div>""", unsafe_allow_html=True)
            if st.button("🗑 Clear History"):
                st.session_state.history = []
                st.rerun()
        else:
            st.markdown("""<div style='text-align:center;padding:40px;color:#475569;'>
                <div style='font-size:3rem;'>📊</div><p>No history yet</p></div>""", unsafe_allow_html=True)

    # ── BMI ──
    elif st.session_state.active_page == "bmi":
        if st.button("⬅ Back to Dashboard"):
            st.session_state.active_page = "dashboard"
            st.rerun()
        show_bmi_section()

    # ── REPORT SCANNER ──
    elif st.session_state.active_page == "scanner":
        if st.button("⬅ Back to Dashboard"):
            st.session_state.active_page = "dashboard"
            st.rerun()
        show_report_scanner()

    # ── EYE TEST ──
    elif st.session_state.active_page == "eyetest":
        if st.button("⬅ Back to Dashboard"):
            st.session_state.active_page = "dashboard"
            st.rerun()
        show_eye_test()

    # ── HOSPITAL FINDER ──
    elif st.session_state.active_page == "hospital":
        if st.button("⬅ Back to Dashboard"):
            st.session_state.active_page = "dashboard"
            st.rerun()
        show_hospital_finder()

    # ── BLOOD REPORT ──
    elif st.session_state.active_page == "blood":
        if st.button("⬅ Back to Dashboard"):
            st.session_state.active_page = "dashboard"
            st.rerun()
        show_blood_report()

    # ── MEDICAL STORE ──
    elif st.session_state.active_page == "medstore":
        if st.button("⬅ Back to Dashboard"):
            st.session_state.active_page = "dashboard"
            st.rerun()
        show_medical_store()

    # ── SKIN DISEASE DETECTOR ──
    elif st.session_state.active_page == "skin":
        if st.button("⬅ Back to Dashboard"):
            st.session_state.active_page = "dashboard"
            st.rerun()
        show_skin_disease()

    # ── MEDICINE REMINDER ──
    elif st.session_state.active_page == "reminder":
        if st.button("⬅ Back to Dashboard"):
            st.session_state.active_page = "dashboard"
            st.rerun()
        show_medicine_reminder()