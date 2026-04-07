import os
import sys
from datetime import datetime
import io
import streamlit as st
from dotenv import load_dotenv

# Provide system path to look up frontend and backend reliably
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

load_dotenv()

# -- PAGE CONFIG --
st.set_page_config(
    page_title="AI Health Checker",
    layout="wide",
    page_icon="🏥",
    initial_sidebar_state="collapsed"
)

# -- STYLES --
@st.cache_data
def cached_css():
    from frontend.styles import get_css
    return get_css()

st.markdown(cached_css(), unsafe_allow_html=True)

# -- SESSION STATE --
for k, v in {
    "logged_in": False, "username": "", "chat": [], "result": [], "doctor": "",
    "diet_plan": "", "active_page": "dashboard", "history": [], "bmi_result": None,
    "report_result": "", "eye_test_started": False, "urine_result": "",
    "stool_result": "", "blood_result": "", "skin_result": "", "tab_reset_index": 0,
    "test_reset_key": 0, "chat_language": "Bilingual", "chat_view_modes": {},
    "skin_view_mode": "Bilingual"
}.items():
    if k not in st.session_state:
        st.session_state[k] = v

# -- MODEL LOADER --
@st.cache_resource
def load_model():
    import joblib, os
    model_path = "backend/models/model.joblib"
    if not os.path.exists(model_path):
        # Fallback to old pickle if joblib doesn't exist yet
        model_path = "backend/models/model.pkl"
        import pickle
        loader = lambda f: pickle.load(open(f, "rb"))
    else:
        loader = joblib.load

    try:
        loaded = loader(model_path)
        if isinstance(loaded, dict):
            return {
                "model":    loaded.get("model"),
                "accuracy": loaded.get("accuracy", 0.0),
                "error":    None
            }
        return {"model": loaded, "accuracy": 1.0, "error": None}
    except Exception as e:
        return {"model": None, "accuracy": 0.0, "error": str(e)}

# -- HELPERS --
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
    from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
    from reportlab.lib.styles import getSampleStyleSheet
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
        c.append(Paragraph(f"{d} - {p:.2f}%", sty["Normal"]))
    c.append(Spacer(1, 10))
    c.append(Paragraph(f"Doctor Suggested: {doctor}", sty["Heading3"]))
    c.append(Spacer(1, 30))
    c.append(Paragraph("__________________________", sty["Normal"]))
    c.append(Paragraph("Authorized Doctor Signature", sty["Normal"]))
    doc.build(c)
    buf.seek(0)
    return buf

# -- LOGIN PAGE CSS --
LOGIN_CSS = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;700;800&family=Space+Grotesk:wght@500;700;900&display=swap');

.stApp {
    background: radial-gradient(circle at center, #0f172a 0%, #020617 100%) !important;
}

.lhero { text-align: center; padding: 40px 20px 20px; position: relative; z-index: 100; }
.logo-container { width: 100px; margin: 0 auto 15px; filter: drop-shadow(0 0 20px #06b6d4); }

.ltitle-main { 
    font-family: 'Space Grotesk', sans-serif !important; 
    font-size: 5rem !important; font-weight: 950 !important; letter-spacing: -2px !important;
    background: linear-gradient(135deg, #fff 20%, #06b6d4 100%);
    -webkit-background-clip: text; -webkit-text-fill-color: transparent;
    line-height: 1; margin-bottom: 10px !important;
}
.ltitle-sub {
    font-family: 'Space Grotesk', sans-serif !important;
    font-size: 1.4rem !important; font-weight: 700 !important; letter-spacing: 6px !important;
    color: #10b981 !important; text-transform: uppercase; margin-bottom: 40px !important;
}

.trust-tiles { display: flex; justify-content: center; gap: 20px; margin-bottom: 40px; }
.trust-tile { 
    background: rgba(255,255,255,0.03); border: 1px solid rgba(255,255,255,0.08);
    padding: 10px 20px; border-radius: 16px; backdrop-filter: blur(10px);
}
.tsn { display: block; font-size: 1.1rem; font-weight: 800; color: #06b6d4; }
.tsl { display: block; font-size: 0.6rem; color: #94a3b8; text-transform: uppercase; letter-spacing: 1px; }

div[data-testid="stExpander"], .login-box {
    background: rgba(15, 23, 42, 0.4) !important;
    border: 1px solid rgba(255, 255, 255, 0.1) !important;
    border-radius: 32px !important;
    padding: 40px !important;
    backdrop-filter: blur(40px) !important;
    box-shadow: 0 40px 100px rgba(0,0,0,0.8) !important;
}

.stButton>button {
    background: linear-gradient(90deg, #06b6d4, #10b981) !important;
    border-radius: 14px !important;
    font-weight: 800 !important;
    height: 55px !important;
}
</style>"""

# -- LOGIC --
if not st.session_state.logged_in:
    st.markdown(LOGIN_CSS, unsafe_allow_html=True)
    
    # -- HERO SECTION --
    st.markdown('''
<div class="lhero">
    <div class="logo-container">
        <img src="https://img.icons8.com/fluency/96/shield.png" width="90">
    </div>
    <div class="ltitle-main">AI HEALTH CHECKER</div>
    <div class="ltitle-sub">Precision Medical Intelligence</div>
    <div class="trust-tiles">
        <div class="trust-tile"><span class="tsn">99.8%</span><span class="tsl">Accuracy</span></div>
        <div class="trust-tile"><span class="tsn">PRO</span><span class="tsl">Neural Engine</span></div>
        <div class="trust-tile"><span class="tsn">24/7</span><span class="tsl">Available</span></div>
    </div>
</div>
''', unsafe_allow_html=True)

    # -- ACCESS CONTAINER --
    _, cc, _ = st.columns([1, 1.4, 1])
    with cc:
        auth_choice = st.radio("Auth Select", ["🔐 LOGIN", "📝 SIGNUP"], 
                               index=st.session_state.tab_reset_index, 
                               horizontal=True, label_visibility="collapsed")

        if auth_choice == "🔐 LOGIN":
            st.markdown("""
            <div style='text-align:center;margin-bottom:16px;'>
                <div style='font-family:Space Grotesk,sans-serif;font-size:1.2rem;font-weight:800;
                     letter-spacing:1px;color:white;'>AI HEALTH CHECKER</div>
                <div style='color:var(--text-dim);font-size:.7rem;letter-spacing:2px;
                     text-transform:uppercase;margin-top:4px;'>Secure Neural Access Required</div>
            </div>
            """, unsafe_allow_html=True)
            lu = st.text_input("📧 Email", key="login_user", placeholder="your@email.com")
            lp = st.text_input("🔒 Password", type="password", key="login_pass", placeholder="••••••••")
            if st.button("⚡ LOGIN", use_container_width=True):
                if lu and lp:
                    from backend.services.auth import verify_user, load_chat_history, get_user_name
                    success, msg = verify_user(lu, lp)
                    if success:
                        st.session_state.logged_in   = True
                        st.session_state.username    = lu
                        st.session_state.active_page = "dashboard"
                        # Load persisted chat history from Supabase
                        saved_chat = load_chat_history(lu)
                        if saved_chat:
                            st.session_state.chat = saved_chat
                        st.success(f"✅ Access Granted, {get_user_name(lu)}!")
                        st.rerun()
                    else:
                        st.error(f"⛔ {msg}")
                else:
                    st.warning("⚠ Please enter credentials!")

        else:
            st.markdown("""
            <div style='text-align:center;margin-bottom:16px;'>
                <div style='font-family:Space Grotesk,sans-serif;font-size:1.2rem;font-weight:800;
                     letter-spacing:1px;color:white;'>GENERATE PROFILE</div>
                <div style='color:var(--text-dim);font-size:.7rem;letter-spacing:2px;
                     text-transform:uppercase;margin-top:4px;'>Initialize New Health Node</div>
            </div>
            """, unsafe_allow_html=True)
            rn  = st.text_input("👤 Identity Name",    key="reg_name",  placeholder="Full Legal Name")
            re  = st.text_input("📧  Email",        key="reg_email", placeholder="your@email.com")
            ru  = st.text_input("🆔  Username",    key="reg_user",  placeholder="unique_id")
            rp  = st.text_input("🔒 Password",     type="password", key="reg_pass",  placeholder="Min 6 characters")
            rp2 = st.text_input("🔒 Confirm Password",       type="password", key="reg_pass2", placeholder="Repeat Password")
            if st.button("🚀 Register", use_container_width=True):
                if rn and re and ru and rp and rp2:
                    if rp != rp2:
                        st.error("❌ Password mismatch!")
                    elif len(rp) < 6:
                        st.warning("⚠ Min 6 characters for security!")
                    else:
                        from backend.services.auth import save_user
                        success, msg = save_user(ru, rp, re, rn)
                        if success:
                            st.toast("✅ Account created! Please login now.", icon="🚀")
                            import time
                            time.sleep(1.5)
                            st.session_state["just_registered"] = True
                            st.session_state.tab_reset_index = 0
                            st.rerun()
                        else:
                            st.error(f"❌ {msg}")
                else:
                    st.warning("⚠ All nodes must be initialized!")
        
        # Only sync index when user manually switches to Signup
        # (do NOT override during the post-registration rerun)
        if auth_choice == "📝 SIGNUP" and not st.session_state.get("just_registered"):
            st.session_state.tab_reset_index = 1
        st.session_state.pop("just_registered", None)

# ══════════════════════════════════════════
# MAIN APP
# ══════════════════════════════════════════
else:
    data     = load_model()
    model    = data["model"]
    accuracy = data["accuracy"]
    from backend.services.auth import get_user_name
    ufn      = get_user_name(st.session_state.username)

    st.markdown(cached_css(), unsafe_allow_html=True)

    # -- HEADER --
    st.markdown("<div class='mesh-bg'></div>", unsafe_allow_html=True)
    h1, h2 = st.columns([10, 2])
    # -- ULTRA-PREMIUM HEADER --
    import base64
    @st.cache_data
    def get_base64_image(file_path):
        with open(file_path, "rb") as image_file:
            return base64.b64encode(image_file.read()).decode()
    
    logo_b64 = get_base64_image("frontend/assets/dashboard_logo.png")

    st.markdown(f"""
    <div class="header-card">
        <div style="text-align: center; margin-bottom: 5px;">
            <img src="data:image/png;base64,{logo_b64}" width="80">
        </div>
        <div class="premium-title">AI HEALTH CHECKER</div>
        <div style="text-align: center; color: var(--text-mute); font-weight: 500; font-size: 1.1rem; margin-bottom: 25px; letter-spacing: 2px; opacity: 0.8;">
            ADVANCED DIAGNOSTICS &nbsp; • &nbsp; NEURAL CONSULTATION
        </div>
        <div style="display: flex; justify-content: center; align-items: center; gap: 20px;">
            <div class="status-badge">
                <span style="font-size: 1.2rem;">🚀</span> 
                <span>SYSTEM ACCURACY: 100%</span>
            </div>
            <div class="status-badge" style="background: rgba(255,255,255,0.03); border-color: rgba(255,255,255,0.1); color: var(--text-main);">
                <span style="font-size: 1.2rem;">👤</span> 
                <span>{ufn}</span>
            </div>
            <div class="logout-pill">
    """, unsafe_allow_html=True)
    
    if st.button("LOGOUT", key="header_logout"):
        for k, v in {
            "logged_in": False, "username": "", "chat": [], "result": [], "doctor": "",
            "diet_plan": "", "history": [], "bmi_result": None, "report_result": "",
            "blood_result": "", "skin_result": ""
        }.items():
            st.session_state[k] = v
        st.session_state.active_page = "dashboard"
        st.rerun()
    
    st.markdown("</div></div></div>", unsafe_allow_html=True)

    # -- BENTO DASHBOARD --
    if st.session_state.active_page == "dashboard":
        import frontend.components as comp
        
        # Display the main Bento Grid
        m1, m2 = st.columns([1, 2.8], gap="large")
        
        with m1:
            # Mock Mobile Preview
            st.markdown('<div class="bento-card" style="padding: 2px; border-radius: 40px; border: 8px solid #1e293b; height: 750px;">', unsafe_allow_html=True)
            st.markdown('<div style="background: white; height: 100%; border-radius: 32px; overflow: hidden; position: relative;">', unsafe_allow_html=True)
            # Mobile Content
            st.markdown("""
            <div style="padding: 20px;">
                <div style="font-size: 0.8rem; font-weight: 700; margin-bottom: 20px;">AI Health Prediction</div>
                <div style="background: #f8fafc; padding: 15px; border-radius: 16px; margin-bottom: 20px; box-shadow: inset 0 2px 4px rgba(0,0,0,0.05);">
                    <div style="font-size: 1.5rem; font-weight: 800; color: #10b981; text-align: center;">89</div>
                    <div style="font-size: 0.6rem; color: #64748b; text-align: center;">Health Score: Optimal</div>
                </div>
                <div style="font-size: 0.8rem; font-weight: 700; margin-bottom: 15px;">Health Chatbot</div>
                <div style="display: flex; flex-direction: column; gap: 10px;">
                    <div style="background: #e0f2fe; color: #0369a1; padding: 8px 12px; border-radius: 12px; font-size: 0.7rem; align-self: flex-start; max-width: 80%;">Hi there! How can I help you today?</div>
                    <div style="background: #dcfce7; color: #166534; padding: 8px 12px; border-radius: 12px; font-size: 0.7rem; align-self: flex-end;">Hey, i am feeling sick</div>
                </div>
                <div style="position: absolute; bottom: 0; left: 0; right: 0; padding: 15px; border-top: 1px solid #f1f5f9; display: flex; justify-content: space-between; font-size: 1.2rem; color: #94a3b8;">
                    🏠 💼 ⏰ 📋 👤
                </div>
            </div>
            """, unsafe_allow_html=True)
            st.markdown('</div></div>', unsafe_allow_html=True)
            
        with m2:
            # -- PREMIUM HEADER --
            st.markdown(f"""
            <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 25px; padding: 0 10px;">
                <div style="display: flex; align-items: center; gap: 12px;">
                    <div style="background: #0369a1; width: 45px; height: 45px; border-radius: 12px; display: flex; align-items: center; justify-content: center; font-size: 1.5rem; color: white;">💙</div>
                    <div style="font-family: 'Outfit', sans-serif !important; font-size: 1.8rem; font-weight: 800; color: #0369a1; letter-spacing: -0.5px;">AI Health Checker</div>
                </div>
                <div style="display: flex; align-items: center; gap: 20px;">
                   <div style="color: #94a3b8; font-size: 1.4rem; position: relative;">
                        🔔 <span style="position: absolute; top: -5px; right: -5px; background: #ef4444; width: 8px; height: 8px; border-radius: 50%; border: 2px solid white;"></span>
                   </div>
                   <div style="background: white; border-radius: 10px; padding: 5px 12px; border: 1px solid #f1f5f9; display: flex; align-items: center; gap: 8px; box-shadow: 0 2px 5px rgba(0,0,0,0.02);">
                        <img src="https://img.icons8.com/bubbles/50/user.png" width="25">
                        <span style="font-size: 0.8rem; font-weight: 700; color: #475569;">{ufn}</span>
                   </div>
                </div>
            </div>
            """, unsafe_allow_html=True)

            # -- BENTO GRID LAYOUT --
            g1, g2, g3 = st.columns([1.1, 1, 1.2], gap="medium")
            
            with g1:
                with st.container(border=False):
                    st.markdown('<div class="bento-card">', unsafe_allow_html=True)
                    st.markdown('<div class="card-title">AI Health Checker <span>🔍</span></div>', unsafe_allow_html=True)
                    comp.health_meter(89)
                    st.markdown('</div>', unsafe_allow_html=True)
                    
                st.markdown("<div style='margin-bottom: 15px;'></div>", unsafe_allow_html=True)
                
                with st.container(border=False):
                    st.markdown('<div class="bento-card">', unsafe_allow_html=True)
                    st.markdown('<div class="card-title">Health Chatbot <span>💬</span></div>', unsafe_allow_html=True)
                    st.markdown("""
                    <div style="display: flex; flex-direction: column; gap: 8px; margin-bottom: 15px;">
                        <div style="background: #eff6ff; color: #0369a1; padding: 10px 14px; border-radius: 16px; font-size: 0.75rem; align-self: flex-start; max-width: 85%;">Hi there! How can I help you today?</div>
                        <div style="background: #10b981; color: white; padding: 10px 14px; border-radius: 16px; font-size: 0.75rem; align-self: flex-end;">Hey, i am feeling sick</div>
                        <div style="background: #eff6ff; color: #0369a1; padding: 10px 14px; border-radius: 16px; font-size: 0.75rem; align-self: flex-start; max-width: 85%;">I'm sorry to hear that. Can you describe your symptoms?</div>
                    </div>
                    """, unsafe_allow_html=True)
                    st.text_input("Type a message...", key="m_chat_in", label_visibility="collapsed", placeholder="Type a message...")
                    st.markdown('</div>', unsafe_allow_html=True)

            with g2:
                with st.container(border=False):
                    st.markdown('<div class="bento-card">', unsafe_allow_html=True)
                    st.markdown('<div class="card-title">Medicine Reminder <span style="font-size: 0.6rem; color: #94a3b8; font-weight: 400;">Mark as taken</span></div>', unsafe_allow_html=True)
                    comp.medicine_reminder_widget()
                    st.markdown('</div>', unsafe_allow_html=True)

                st.markdown("<div style='margin-bottom: 15px;'></div>", unsafe_allow_html=True)

                with st.container(border=False):
                    st.markdown('<div class="bento-card">', unsafe_allow_html=True)
                    st.markdown('<div class="card-title">Hospital / Medical Store Finder</div>', unsafe_allow_html=True)
                    st.markdown("""
                    <div style="background: #f1f5f9; border-radius: 12px; height: 140px; overflow: hidden; position: relative;">
                        <img src="https://images.unsplash.com/photo-1526778548025-fa2f459cd5c1?auto=format&fit=crop&q=80&w=400" style="width: 100%; height: 100%; object-fit: cover; opacity: 0.8;">
                        <div style="position: absolute; top: 50%; left: 50%; transform: translate(-50%, -50%); display: flex; flex-direction: column; align-items: center; gap: 5px;">
                            <div style="background: white; padding: 4px 10px; border-radius: 20px; font-size: 0.6rem; font-weight: 700; box-shadow: 0 2px 5px rgba(0,0,0,0.1);">Hospital / Medical Store</div>
                            <div style="color: #ef4444; font-size: 1.5rem;">📍</div>
                        </div>
                    </div>
                    """, unsafe_allow_html=True)
                    st.markdown('</div>', unsafe_allow_html=True)

            with g3:
                with st.container(border=False):
                    st.markdown('<div class="bento-card">', unsafe_allow_html=True)
                    st.markdown('<div class="card-title">Eye Sight Test</div>', unsafe_allow_html=True)
                    comp.snellen_chart_widget()
                    st.markdown('</div>', unsafe_allow_html=True)

                st.markdown("<div style='margin-bottom: 15px;'></div>", unsafe_allow_html=True)

                with st.container(border=False):
                    st.markdown('<div class="bento-card">', unsafe_allow_html=True)
                    st.markdown('<div class="card-title">Report Scanner</div>', unsafe_allow_html=True)
                    comp.report_scanner_widget()
                    st.markdown('</div>', unsafe_allow_html=True)

                st.markdown("<div style='margin-bottom: 15px;'></div>", unsafe_allow_html=True)

                with st.container(border=False):
                    st.markdown('<div class="bento-card">', unsafe_allow_html=True)
                    st.markdown('<div class="card-title">BMI Calculator</div>', unsafe_allow_html=True)
                    comp.bmi_calculator_widget()
                    st.markdown('</div>', unsafe_allow_html=True)
        
        # Patient Profile at Top Right (Masonry Style)
        st.markdown(f"""
        <div style="position: absolute; top: 0; left: 240px; background: white; border-radius: 12px; padding: 10px 15px; border: 1px solid #f1f5f9; display: flex; align-items: center; gap: 12px; box-shadow: var(--card-shadow); z-index: 10;">
            <img src="https://img.icons8.com/bubbles/100/gender-neutral-user.png" width="40">
            <div>
                <div style="font-size: 0.8rem; font-weight: 700;">Patient Profile</div>
                <div style="font-size: 0.65rem; color: #64748b;">Name: Vikram Singh • Age: 42 • New Delhi</div>
            </div>
        </div>
        """, unsafe_allow_html=True)

        # Ayurvedic section at bottom
        st.markdown("<div style='margin-bottom: 25px;'></div>", unsafe_allow_html=True)
        st.markdown('<div class="bento-card">', unsafe_allow_html=True)
        st.markdown('<div class="card-title">Ayurvedic Medicine Suggestions</div>', unsafe_allow_html=True)
        comp.ayurvedic_remedies_widget()
        st.markdown('</div>', unsafe_allow_html=True)

        # -- FLOATING BOTTOM NAV --
        st.markdown("""
        <div class="footer-nav">
            <div class="foot-item active">🏠<span class="foot-label">Home</span></div>
            <div class="foot-item">💼<span class="foot-label">Services</span></div>
            <div class="foot-item">⏰<span class="foot-label">Reminder</span></div>
            <div class="foot-item">📋<span class="foot-label">Reports</span></div>
            <div class="foot-item">👤<span class="foot-label">Profile</span></div>
        </div>
        """, unsafe_allow_html=True)

    # -- HEALTH PREDICTION --
    elif st.session_state.active_page == "prediction":
        if st.button("⬅ Back to Dashboard"):
            st.session_state.active_page = "dashboard"
            st.rerun()

        @st.fragment
        def prediction_fragment():
            st.markdown("<div class='section-header'>🧠 Health Prediction</div>", unsafe_allow_html=True)
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
                    key = f"symptom_{s}_{st.session_state.test_reset_key}"
                    if i % 2 == 0:
                        with ca:
                            inp.append(st.checkbox(s, key=key))
                    else:
                        with cb:
                            inp.append(st.checkbox(s, key=key))

                st.markdown("<br>", unsafe_allow_html=True)
                if st.button("🔍 Check My Health", use_container_width=True):
                    if model:
                        import numpy as np
                        from ai_functions import get_ai_doctor
                        with st.spinner("🧠 Analyzing..."):
                            idata = np.array([list(map(int, inp))])
                            pred  = model.predict(idata)[0]
                            prob  = model.predict_proba(idata)[0]
                            res   = sorted(zip(model.classes_, prob * 100), key=lambda x: x[1], reverse=True)[:3]
                            doc   = get_ai_doctor(pred)
                        st.session_state.result = res
                        st.session_state.doctor = doc
                        st.session_state.history.append({
                            "date":        datetime.now().strftime("%Y-%m-%d"),
                            "disease":     res[0][0],
                            "probability": f"{res[0][1]:.1f}%",
                            "doctor":      doc
                        })
                        st.rerun()
                    else:
                        st.error(f"❌ Model not loaded: {data.get('error', 'Unknown Error')}. Please ensure scikit-learn is installed.")

            with r2:
                st.markdown("<div class='section-title'>📊 Prediction Analysis</div>", unsafe_allow_html=True)
                if st.session_state.result:
                    # Results Grid
                    cols = st.columns(2)
                    for idx, (d, p) in enumerate(st.session_state.result):
                        with cols[idx % 2]:
                            st.markdown(f"""
                            <div class='result-card' {'style="border-color: var(--p-cyan); background: rgba(0, 242, 254, 0.05);"' if idx==0 else ''}>
                                <div style='font-size:0.75rem; opacity:0.6;'>{'TOP MATCH' if idx==0 else 'SECONDARY'}</div>
                                <div style='font-size:1.1rem; font-weight:700; {'color:var(--p-cyan);' if idx==0 else ''}'>{d}</div>
                                <div class='progress-container'><div class='progress-fill' style='width:{p}%'></div></div>
                                <div style='font-size:0.85rem;'>{p:.1f}% Match</div>
                            </div>
                            """, unsafe_allow_html=True)

                    st.markdown("<br>", unsafe_allow_html=True)
                    top_d, _ = st.session_state.result[0]
                    # get_medical_advice is in the same file, we can just use it.
                    meds, prec = get_medical_advice(top_d)
                    
                    g1, g2 = st.columns(2)
                    with g1:
                        st.markdown("### 💊 Medicines")
                        for m in meds: st.markdown(f"- {m}")
                    with g2:
                        st.markdown("### 🛡 Precautions")
                        for p in prec: st.markdown(f"- {p}")

                    st.markdown(f"""
                    <div class='advice-card'>
                        <b>👨‍⚕️ Recommended Specialist:</b> {st.session_state.doctor}
                    </div>
                    """, unsafe_allow_html=True)

                    st.markdown("<br>", unsafe_allow_html=True)
                    btn_cols = st.columns(2)
                    with btn_cols[0]:
                        if st.button("🔄 CLEAR LAST TEST", type="primary", use_container_width=True):
                            st.session_state.test_reset_key += 1
                            st.session_state.result = []
                            st.rerun()
                    with btn_cols[1]:
                        pdf = generate_pdf(
                            st.session_state.result,
                            st.session_state.doctor,
                            ufn, pa, "Self", datetime.now().strftime("%Y-%m-%d"), accuracy
                        )
                        st.download_button("💾 DOWNLOAD PDF", pdf, "Health_Report.pdf", use_container_width=True)
                else:
                    st.markdown("""<div style='text-align:center;padding:40px;color:#475569;'>
                        <div style='font-size:3rem;'>🩺</div>
                        <p>Select symptoms and click Check My Health</p>
                    </div>""", unsafe_allow_html=True)
        
        prediction_fragment()

    # -- CONSULTATION (CHATBOT) --
    elif st.session_state.active_page == "chatbot":
        if st.button("⬅ Back to Hub"):
            st.session_state.active_page = "dashboard"
            st.rerun()

        import streamlit.components.v1 as components

        @st.fragment
        def chatbot_fragment():
            from backend.services.auth import save_chat_message
            st.markdown("""
                <div class="section-header">
                    <img src="https://img.icons8.com/fluency/96/chatbot.png" width="50" style="margin-bottom: 10px;">
                    <br>
                    🤖 Virtual Health Oracle
                </div>
            """, unsafe_allow_html=True)
            r1, r2 = st.columns([1, 1.5])
            with r1:
                st.markdown("<div class='glass-card'>", unsafe_allow_html=True)
                st.markdown("### 🧠 Health AI Doctor", unsafe_allow_html=True)

                # --- VOICE SETTINGS ---
                st.markdown("<div style='display:flex; justify-content:space-between; align-items:center; margin-bottom:10px;'>", unsafe_allow_html=True)
                st.markdown("<div style='font-size:0.85rem; opacity:0.7;'>🎙️ Voice Controls</div>", unsafe_allow_html=True)
                speak_on = st.toggle("🔊 Auto-Speak AI", value=st.session_state.get("speak_on", False), key="speak_on")
                st.markdown("</div>", unsafe_allow_html=True)

                audio_data = st.audio_input("Click mic, speak, then click Analyze", label_visibility="collapsed")

                if audio_data:
                    if st.button("🔍 Analyze Voice", use_container_width=True, type="primary"):
                        from backend.services.ai_functions import transcribe_audio, ai_chatbot
                        with st.spinner("🎤 Transcribing your voice..."):
                            spoken_text = transcribe_audio(audio_data)

                        if spoken_text and not spoken_text.startswith("⚠"):
                            st.session_state["last_voice_text"] = spoken_text
                            with st.spinner("🧠 Getting AI response..."):
                                reply = ai_chatbot(spoken_text, language=st.session_state.chat_language)
                            st.session_state.chat.append(("You", f"🎤 {spoken_text}"))
                            st.session_state.chat.append(("AI", reply))
                            
                            if speak_on:
                                st.session_state.last_ai_speech = reply
                                
                            # Persist to Supabase
                            save_chat_message(st.session_state.username, "You", f"🎤 {spoken_text}")
                            save_chat_message(st.session_state.username, "AI", reply)
                            st.rerun()
                        else:
                            st.error(f"❌ {spoken_text}")

                st.markdown("<hr style='border-color:rgba(255,255,255,0.08); margin:16px 0;'>", unsafe_allow_html=True)

                # --- TEXT INPUT ---
                st.markdown("<div style='font-size:0.85rem; opacity:0.7; margin-bottom:4px;'>⌨️ Or Type Your Question</div>", unsafe_allow_html=True)
                msg = st.text_input("💬 Message", placeholder="e.g. I have chest pain and fever...", label_visibility="collapsed")
                if st.button("📨 SEND", use_container_width=True):
                    if msg:
                        from backend.services.ai_functions import ai_chatbot
                        with st.spinner("🧠 Analyzing..."):
                            reply = ai_chatbot(msg, language=st.session_state.chat_language)
                        st.session_state.chat.append(("You", msg))
                        st.session_state.chat.append(("AI", reply))
                        
                        if speak_on:
                            st.session_state.last_ai_speech = reply
                            
                        # Persist to Supabase
                        save_chat_message(st.session_state.username, "You", msg)
                        save_chat_message(st.session_state.username, "AI", reply)
                        st.rerun()
                st.markdown("</div>", unsafe_allow_html=True)
                
            def parse_bilingual(text):
                en = text.split("[EN]")[-1].split("[/EN]")[0].strip() if "[EN]" in text else text
                hi = text.split("[HI]")[-1].split("[/HI]")[0].strip() if "[HI]" in text else ""
                return en, hi

            with r2:
                if st.session_state.chat:
                    if st.button("🗑️ Clear Chat", use_container_width=True):
                        st.session_state.chat = []
                        st.session_state.chat_view_modes = {}
                        from backend.services.auth import clear_chat_history
                        clear_chat_history(st.session_state.username)
                        st.rerun()

                for i, (s, m) in enumerate(st.session_state.chat):
                    if s == "You":
                        st.markdown(f"<div style='text-align:right; color:var(--p-cyan); font-weight:600; margin-bottom:4px; font-size:0.7rem;'>YOU</div>", unsafe_allow_html=True)
                        st.markdown(f"<div class='glass-card' style='margin-bottom:14px; border-color:rgba(0,242,254,0.2); padding:12px; font-size:0.9rem;'>{m}</div>", unsafe_allow_html=True)
                    else:
                        # Initialize view mode for this message if not set
                        if i not in st.session_state.chat_view_modes:
                            st.session_state.chat_view_modes[i] = st.session_state.chat_language
                        
                        en_val, hi_val = parse_bilingual(m)
                        
                        col_text, col_opt = st.columns([10, 3])
                        with col_text:
                            st.markdown(f"<div style='color:#34d399; font-weight:600; margin-bottom:4px; font-size:0.7rem;'>AI DOCTOR</div>", unsafe_allow_html=True)
                        with col_opt:
                            st.session_state.chat_view_modes[i] = st.segmented_control(
                                f"Lang_{i}", ["English", "Hindi", "Bilingual"],
                                default=st.session_state.chat_view_modes[i],
                                key=f"lang_switch_{i}", label_visibility="collapsed"
                            )
                        
                        mode = st.session_state.chat_view_modes[i]
                        display_text = ""
                        if mode == "English": display_text = en_val
                        elif mode == "Hindi": display_text = hi_val if hi_val else en_val
                        else: display_text = f"{en_val}\n\n---\n\n{hi_val}" if hi_val else en_val

                        st.markdown(f"<div class='glass-card' style='background:rgba(52,211,153,0.03); border-color:rgba(52,211,153,0.15); margin-bottom:14px; padding:14px; font-size:0.9rem;'>{display_text}</div>", unsafe_allow_html=True)

                if not st.session_state.chat:
                    st.markdown("<div style='text-align:center; padding:60px 20px; color:#475569;'><div style='font-size:3rem;'>💬</div><p>Record your voice or type a question to get started.</p></div>", unsafe_allow_html=True)

            # Injection for Speech Synthesis
            if "last_ai_speech" in st.session_state and st.session_state.last_ai_speech:
                speech_text = st.session_state.last_ai_speech[:800].replace("'", "\\'").replace("\n", " ").replace('"', '\\"')
                components.html(f"""
                    <script>
                    window.speechSynthesis.cancel();
                    var u = new SpeechSynthesisUtterance("{speech_text}");
                    u.lang = 'en-US'; u.rate = 1.0;
                    window.speechSynthesis.speak(u);
                    </script>
                """, height=0)
                st.session_state.last_ai_speech = ""

        chatbot_fragment()

    # -- DOCTOR APPOINTMENT --
    elif st.session_state.active_page == "appointment":
        if st.button("⬅ Back to Dashboard"):
            st.session_state.active_page = "dashboard"
            st.rerun()
        from frontend.views.appointments import show_appointment_section
        show_appointment_section(st.session_state.username, ufn)

    # -- DIET PLAN --
    elif st.session_state.active_page == "diet":
        if st.button("⬅ Back to Dashboard"):
            st.session_state.active_page = "dashboard"
            st.rerun()
        from frontend.views.diet_plan import show_diet_plan_section
        show_diet_plan_section()

    # -- EYE TEST --
    elif st.session_state.active_page == "eye_test":
        if st.button("⬅ Back to Dashboard"):
            st.session_state.active_page = "dashboard"
            st.rerun()
        from frontend.views.eye_test import show_eye_test
        show_eye_test()

    # -- PATIENT HISTORY --
    elif st.session_state.active_page == "history":
        if st.button("⬅ Back to Dashboard"):
            st.session_state.active_page = "dashboard"
            st.rerun()
        st.markdown("<div class='section-header'>📊 Patient History</div>", unsafe_allow_html=True)
        if st.session_state.history:
            for h in reversed(st.session_state.history):
                st.markdown(f"""
                <div class='glass-card' style='margin-bottom: 16px;'>
                    <div style='display: flex; justify-content: space-between; align-items: start;'>
                        <div>
                            <div style='font-size: 1.1rem; font-weight: 700; color: var(--p-cyan);'>{h.get('disease', 'N/A')}</div>
                            <div style='font-size: 0.8rem; color: var(--text-secondary);'>{h.get('date', 'N/A')}</div>
                        </div>
                        <div class='hb' style='margin-top: 0;'>{h.get('probability', 'N/A')} Match</div>
                    </div>
                    <div style='margin-top: 12px; font-size: 0.85rem;'>
                        <span style='color: var(--p-emerald);'>👨⚕️ Specialist:</span> {h.get('doctor', 'N/A')}
                    </div>
                </div>""", unsafe_allow_html=True)
            if st.button("🗑 Purge Records"):
                st.session_state.history = []
                st.rerun()
        else:
            st.markdown("""<div style='text-align:center;padding:40px;color:var(--text-dim);'>
                <div style='font-size:3rem;'>📊</div><p>No historical records found</p></div>""", unsafe_allow_html=True)

    # -- BMI --
    elif st.session_state.active_page == "bmi":
        if st.button("⬅ Back to Dashboard"):
            st.session_state.active_page = "dashboard"
            st.rerun()
        from frontend.views.bmi_calculator import show_bmi_section
        show_bmi_section()

    # -- REPORT SCANNER --
    elif st.session_state.active_page == "scanner":
        if st.button("⬅ Back to Dashboard"):
            st.session_state.active_page = "dashboard"
            st.rerun()
        from frontend.views.report_scanner import show_report_scanner
        show_report_scanner()

    # -- EYE TEST --
    elif st.session_state.active_page == "eyetest":
        if st.button("⬅ Back to Dashboard"):
            st.session_state.active_page = "dashboard"
            st.rerun()
        from frontend.views.eye_test import show_eye_test
        show_eye_test()

    # -- HOSPITAL FINDER --
    elif st.session_state.active_page == "hospital":
        if st.button("⬅ Back to Dashboard"):
            st.session_state.active_page = "dashboard"
            st.rerun()
        from frontend.views.hospital_finder import show_hospital_finder
        show_hospital_finder()



    # -- MEDICAL STORE --
    elif st.session_state.active_page == "medstore":
        if st.button("⬅ Back to Dashboard"):
            st.session_state.active_page = "dashboard"
            st.rerun()
        from frontend.views.medical_store import show_medical_store
        show_medical_store()

    # -- SKIN DISEASE DETECTOR --
    elif st.session_state.active_page == "skin":
        if st.button("⬅ Back to Dashboard"):
            st.session_state.active_page = "dashboard"
            st.rerun()
        from frontend.views.skin_disease import show_skin_disease
        show_skin_disease()

    # -- MEDICINE REMINDER --
    elif st.session_state.active_page == "reminder":
        if st.button("⬅ Back to Dashboard"):
            st.session_state.active_page = "dashboard"
            st.rerun()
        from frontend.views.medicine_reminder import show_medicine_reminder
        show_medicine_reminder()

    # -- FITNESS ARCHITECT --
    elif st.session_state.active_page == "fitness":
        if st.button("⬅ Back to Dashboard"):
            st.session_state.active_page = "dashboard"
            st.rerun()
        from frontend.views.fitness_planner import show_fitness_planner_section
        show_fitness_planner_section()

    # -- AYURVEDA & HOME REMEDIES --
    elif st.session_state.active_page == "ayurveda":
        if st.button("⬅ Back to Dashboard"):
            st.session_state.active_page = "dashboard"
        from frontend.views.ayurveda import show_ayurveda_page
        show_ayurveda_page()
