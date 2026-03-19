# ============================================================
# styles.py — Ultra Premium CSS (Deep Space Theme)
# ============================================================

def get_css():
    return """
<style>
@import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@300;400;500;600;700;800;900&display=swap');

:root {
    --p1: #7c3aed;
    --p2: #8b5cf6;
    --p3: #a78bfa;
    --p4: #c4b5fd;
    --g1: #059669;
    --g2: #10b981;
    --a1: #d97706;
    --a2: #f59e0b;
    --a3: #fbbf24;
    --bg0: #020408;
    --bg1: #080c14;
    --bg2: #0d1220;
    --bg3: #121829;
    --bg4: #1a2236;
    --glass: rgba(124,58,237,0.06);
    --glass2: rgba(124,58,237,0.10);
    --border: rgba(124,58,237,0.15);
    --border2: rgba(124,58,237,0.25);
    --text: #f0edff;
    --text2: #b8b0d8;
    --text3: #7c74a8;
}

* { font-family: 'Plus Jakarta Sans', sans-serif !important; }

.stApp {
    background:
        radial-gradient(ellipse 80% 50% at 10% 0%, rgba(124,58,237,0.12) 0%, transparent 60%),
        radial-gradient(ellipse 60% 40% at 90% 100%, rgba(217,119,6,0.08) 0%, transparent 60%),
        radial-gradient(ellipse 100% 100% at 50% 50%, #080c14 0%, #020408 100%);
    color: var(--text);
    min-height: 100vh;
}

#MainMenu, footer, header { visibility: hidden; }
.block-container { padding: 1.2rem 2rem !important; max-width: 1440px !important; }

::-webkit-scrollbar { width: 4px; }
::-webkit-scrollbar-track { background: var(--bg1); }
::-webkit-scrollbar-thumb { background: linear-gradient(180deg, var(--p2), var(--a2)); border-radius: 4px; }

/* ── HEADER ── */
.header-box {
    text-align: center;
    padding: 32px 24px;
    background:
        linear-gradient(135deg, rgba(124,58,237,0.3) 0%, rgba(109,40,217,0.2) 50%, rgba(217,119,6,0.15) 100%);
    border-radius: 20px;
    margin-bottom: 24px;
    border: 1px solid rgba(124,58,237,0.25);
    position: relative;
    overflow: hidden;
    box-shadow: 0 0 60px rgba(124,58,237,0.15), inset 0 1px 0 rgba(196,181,253,0.1);
}
.header-box::before {
    content: '';
    position: absolute; top: 0; left: -200%;
    width: 500%; height: 1px;
    background: linear-gradient(90deg, transparent 0%, rgba(196,181,253,0.6) 30%, rgba(251,191,36,0.4) 50%, rgba(196,181,253,0.6) 70%, transparent 100%);
    animation: topLine 5s infinite ease-in-out;
}
@keyframes topLine { 0%,100%{left:-200%} 50%{left:0%} }
.header-box::after {
    content: '';
    position: absolute; bottom: 0; left: 0; right: 0; height: 1px;
    background: linear-gradient(90deg, transparent, rgba(124,58,237,0.5), rgba(217,119,6,0.3), rgba(124,58,237,0.5), transparent);
}

/* ── BADGES ── */
.accuracy-badge {
    background: linear-gradient(135deg, rgba(217,119,6,0.2), rgba(245,158,11,0.1));
    color: var(--a3);
    padding: 6px 16px; border-radius: 30px;
    font-size: 0.8rem; font-weight: 700;
    border: 1px solid rgba(217,119,6,0.3);
    display: inline-block; margin-top: 10px;
    letter-spacing: 0.5px;
}
.user-badge {
    background: linear-gradient(135deg, rgba(124,58,237,0.2), rgba(139,92,246,0.1));
    border: 1px solid rgba(124,58,237,0.3);
    color: var(--p4);
    padding: 6px 16px; border-radius: 30px;
    font-size: 0.8rem; font-weight: 600;
    display: inline-block; margin-top: 8px; margin-left: 8px;
    letter-spacing: 0.3px;
}

/* ── GLASS BOX ── */
.glass-box {
    background: linear-gradient(145deg, var(--glass) 0%, rgba(13,18,32,0.8) 100%);
    backdrop-filter: blur(24px);
    -webkit-backdrop-filter: blur(24px);
    padding: 22px;
    border-radius: 18px;
    border: 1px solid var(--border);
    margin-bottom: 18px;
    box-shadow: 0 4px 24px rgba(0,0,0,0.4), inset 0 1px 0 rgba(196,181,253,0.06);
    transition: transform 0.25s ease, border-color 0.25s ease, box-shadow 0.25s ease;
    position: relative;
    overflow: hidden;
}
.glass-box::before {
    content: '';
    position: absolute; top: 0; left: 0; right: 0; height: 1px;
    background: linear-gradient(90deg, transparent 0%, rgba(196,181,253,0.3) 50%, transparent 100%);
}
.glass-box:hover {
    transform: translateY(-4px);
    border-color: var(--border2);
    box-shadow: 0 12px 40px rgba(0,0,0,0.5), 0 0 20px rgba(124,58,237,0.08);
}

/* ── SECTION TITLES ── */
.section-title {
    font-size: 1rem; font-weight: 700;
    color: var(--p4);
    margin-bottom: 16px; padding-bottom: 10px;
    border-bottom: 1px solid rgba(124,58,237,0.15);
    letter-spacing: 0.2px;
}
.section-header {
    font-size: 1.4rem; font-weight: 800;
    background: linear-gradient(135deg, var(--p4) 0%, var(--a3) 100%);
    -webkit-background-clip: text; -webkit-text-fill-color: transparent;
    background-clip: text;
    margin-bottom: 18px;
    letter-spacing: -0.3px;
}

/* ── PATIENT BOX ── */
.patient-box {
    background: linear-gradient(135deg, rgba(124,58,237,0.08) 0%, rgba(217,119,6,0.04) 100%);
    border: 1px solid rgba(124,58,237,0.15);
    padding: 18px 22px; border-radius: 16px; margin-bottom: 22px;
}

/* ── RESULT CARDS ── */
.result-card {
    background: linear-gradient(135deg, rgba(124,58,237,0.1) 0%, rgba(124,58,237,0.03) 100%);
    border: 1px solid rgba(124,58,237,0.2);
    padding: 13px 16px; border-radius: 13px; margin-bottom: 10px;
    font-weight: 600; color: var(--p4);
    transition: all 0.2s ease;
    position: relative; overflow: hidden;
}
.result-card::before {
    content: '';
    position: absolute; left: 0; top: 0; bottom: 0; width: 3px;
    background: linear-gradient(180deg, var(--p2), var(--a2));
    border-radius: 3px 0 0 3px;
}
.result-card:hover { background: rgba(124,58,237,0.14); transform: translateX(4px); }

/* ── DOCTOR BOX ── */
.doctor-box {
    background: rgba(5,150,105,0.08);
    border: 1px solid rgba(5,150,105,0.18);
    padding: 9px 13px; border-radius: 11px; margin-top: 7px;
    color: #6ee7b7; font-size: 0.87rem;
}

/* ── CHAT BUBBLES ── */
.user-bubble {
    background: linear-gradient(135deg, #3b0764, #581c87, #7c3aed);
    color: #f0edff;
    padding: 11px 15px;
    border-radius: 18px 18px 4px 18px;
    margin-bottom: 9px; font-weight: 500; font-size: 0.88rem;
    max-width: 80%; margin-left: auto;
    border: 1px solid rgba(196,181,253,0.15);
}
.ai-bubble {
    background: rgba(124,58,237,0.07);
    border: 1px solid rgba(124,58,237,0.12);
    color: var(--text);
    padding: 11px 15px;
    border-radius: 18px 18px 18px 4px;
    margin-bottom: 9px; font-size: 0.88rem;
    max-width: 80%; line-height: 1.65;
}

/* ── APPOINTMENT CARDS ── */
.appt-card {
    background: linear-gradient(135deg, rgba(124,58,237,0.07) 0%, rgba(217,119,6,0.03) 100%);
    border: 1px solid rgba(124,58,237,0.14);
    padding: 15px; border-radius: 13px; margin-bottom: 11px;
    color: var(--text); line-height: 1.8; font-size: 0.88rem;
    transition: border-color 0.2s;
}
.appt-card:hover { border-color: rgba(124,58,237,0.28); }
.cancelled {
    background: rgba(239,68,68,0.06); border: 1px solid rgba(239,68,68,0.14);
    padding: 15px; border-radius: 13px; margin-bottom: 11px;
    color: #fca5a5; line-height: 1.8; font-size: 0.88rem; opacity: 0.6;
}
.body-part-card {
    background: linear-gradient(135deg, rgba(124,58,237,0.08), rgba(217,119,6,0.04));
    border: 1px solid rgba(124,58,237,0.18);
    padding: 15px; border-radius: 13px; margin-top: 11px;
    color: var(--text); line-height: 1.9; font-size: 0.88rem;
}
.doctor-info-card {
    background: rgba(5,150,105,0.07); border: 1px solid rgba(5,150,105,0.18);
    padding: 9px 13px; border-radius: 10px; margin-bottom: 6px;
    color: #6ee7b7; font-size: 0.86rem; transition: background 0.2s;
}
.doctor-info-card:hover { background: rgba(5,150,105,0.12); }

/* ── BADGES ── */
.badge {
    display: inline-block; padding: 3px 9px; border-radius: 20px;
    font-size: 0.7rem; font-weight: 700;
    background: rgba(124,58,237,0.15); color: var(--p4);
    border: 1px solid rgba(124,58,237,0.3); margin-left: 7px;
    letter-spacing: 0.3px;
}
.dept-badge {
    display: inline-block; padding: 4px 13px; border-radius: 20px;
    font-size: 0.78rem; font-weight: 600;
    background: rgba(217,119,6,0.15); color: var(--a3);
    border: 1px solid rgba(217,119,6,0.3);
}

/* ── LOGIN CONTAINER ── */
.login-container {
    max-width: 460px; margin: 30px auto;
    background: linear-gradient(145deg, rgba(124,58,237,0.1), rgba(13,18,32,0.95));
    border: 1px solid rgba(124,58,237,0.22);
    border-radius: 24px; padding: 40px;
    box-shadow: 0 20px 60px rgba(0,0,0,0.6), 0 0 40px rgba(124,58,237,0.08);
    position: relative; overflow: hidden;
}
.login-container::before {
    content: '';
    position: absolute; top: 0; left: 0; right: 0; height: 1px;
    background: linear-gradient(90deg, transparent, rgba(196,181,253,0.5), rgba(251,191,36,0.3), rgba(196,181,253,0.5), transparent);
}
.login-title {
    text-align: center; font-size: 1.8rem; font-weight: 800;
    background: linear-gradient(135deg, var(--p4), var(--a3));
    -webkit-background-clip: text; -webkit-text-fill-color: transparent; background-clip: text;
    margin-bottom: 6px;
}
.login-subtitle { text-align: center; color: var(--text3); font-size: 0.88rem; margin-bottom: 28px; }

/* ── BUTTONS ── */
.stButton > button {
    background: linear-gradient(135deg, #3b0764 0%, #581c87 40%, #7c3aed 100%) !important;
    color: #f0edff !important;
    border: 1px solid rgba(196,181,253,0.25) !important;
    border-radius: 12px !important;
    padding: 10px 20px !important;
    font-weight: 700 !important; font-size: 0.87rem !important;
    transition: all 0.25s ease !important;
    box-shadow: 0 4px 14px rgba(124,58,237,0.3) !important;
    letter-spacing: 0.2px !important;
    height: auto !important;
    width: auto !important;
    opacity: 1 !important;
    margin-top: 0 !important;
}
.stButton > button:hover {
    transform: translateY(-2px) !important;
    box-shadow: 0 8px 24px rgba(124,58,237,0.5) !important;
    filter: brightness(1.1) !important;
}
.stButton > button:active { transform: translateY(0) !important; }

/* ── DOWNLOAD BUTTON ── */
.stDownloadButton > button {
    background: linear-gradient(135deg, #78350f 0%, #b45309 50%, #d97706 100%) !important;
    color: #fef3c7 !important;
    border: 1px solid rgba(217,119,6,0.3) !important;
    border-radius: 12px !important; font-weight: 700 !important;
    box-shadow: 0 4px 14px rgba(180,83,9,0.3) !important;
}
.stDownloadButton > button:hover {
    box-shadow: 0 8px 24px rgba(180,83,9,0.5) !important;
    transform: translateY(-2px) !important;
}

/* ── INPUTS ── */
.stTextInput > div > div > input,
.stNumberInput > div > div > input {
    background: rgba(124,58,237,0.07) !important;
    border: 1px solid rgba(124,58,237,0.18) !important;
    border-radius: 11px !important; color: var(--text) !important;
    padding: 10px 14px !important; transition: all 0.2s !important;
    font-size: 0.88rem !important;
}
.stTextInput > div > div > input:focus,
.stNumberInput > div > div > input:focus {
    border-color: var(--p2) !important;
    box-shadow: 0 0 0 3px rgba(124,58,237,0.15) !important;
    background: rgba(124,58,237,0.1) !important;
}
.stSelectbox > div > div {
    background: rgba(124,58,237,0.07) !important;
    border: 1px solid rgba(124,58,237,0.18) !important;
    border-radius: 11px !important; color: var(--text) !important;
}
.stDateInput > div > div > input {
    background: rgba(124,58,237,0.07) !important;
    border: 1px solid rgba(124,58,237,0.18) !important;
    border-radius: 11px !important; color: var(--text) !important;
}
.stCheckbox > label { color: var(--text) !important; font-size: 0.87rem !important; }
.stCheckbox > label:hover { color: var(--p4) !important; }

/* ── TABS ── */
.stTabs [data-baseweb="tab-list"] {
    background: rgba(124,58,237,0.08) !important;
    border-radius: 14px !important; padding: 4px !important;
    border: 1px solid rgba(124,58,237,0.15) !important;
    gap: 4px !important;
}
.stTabs [data-baseweb="tab"] {
    border-radius: 10px !important; color: var(--text3) !important;
    font-weight: 600 !important; font-size: 0.88rem !important;
    padding: 8px 20px !important;
}
.stTabs [aria-selected="true"] {
    background: linear-gradient(135deg, #3b0764, #7c3aed) !important;
    color: #f0edff !important;
    box-shadow: 0 2px 10px rgba(124,58,237,0.3) !important;
}

/* ── DIVIDER ── */
hr {
    border: none !important; height: 1px !important;
    background: linear-gradient(90deg, transparent, rgba(124,58,237,0.3), rgba(217,119,6,0.2), rgba(124,58,237,0.3), transparent) !important;
    margin: 28px 0 !important;
}

/* ── ALERTS ── */
.stAlert { border-radius: 12px !important; }
</style>
"""