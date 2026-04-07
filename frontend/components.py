import streamlit as st

def health_meter(score, trend="Optimal"):
    """Renders a gauge for health score exactly like mockup."""
    st.markdown(f"""
    <div class="gauge-container">
        <div class="gauge-val">{score}</div>
        <div class="gauge-lab">Health Score: <b>{trend}</b></div>
        <div style="font-size: 0.65rem; color: #94a3b8; margin-top: 4px;">Daily Insight: Focus on hydration.</div>
        <div style="margin-top: 15px; position: relative; height: 40px;">
           <svg viewBox="0 0 100 50" style="width: 120px; margin: 0 auto; display: block;">
              <path d="M 10 50 A 40 40 0 0 1 90 50" fill="transparent" stroke="#f1f5f9" stroke-width="12" />
              <path d="M 10 50 A 40 40 0 0 1 90 50" fill="transparent" stroke="#10b981" stroke-width="12" stroke-dasharray="125.6" stroke-dashoffset="{125.6 * (1 - score/100)}" />
           </svg>
        </div>
    </div>
    """, unsafe_allow_html=True)

def medicine_reminder_widget():
    """Renders medicine reminders exactly like mockup."""
    st.markdown("""
    <div class="med-row">
        <div style="font-size: 1.2rem;">💊</div>
        <div class="med-info">
            <div class="med-time">10:00 - 3:00 PM</div>
            <div class="med-details">Dosage: 200 mg</div>
        </div>
        <div class="med-check active">✓</div>
    </div>
    <div class="med-row">
        <div style="font-size: 1.2rem;">💊</div>
        <div class="med-info">
            <div class="med-time">10 AM - 1:30 PM</div>
            <div class="med-details">Dosage: 200 mg</div>
        </div>
        <div class="med-check"></div>
    </div>
    """, unsafe_allow_html=True)

def report_scanner_widget():
    """Renders report scanner exactly like mockup."""
    scans = [
        {"n": "CT", "i": "🌀"}, {"n": "X-Ray", "i": "🦴"},
        {"n": "MRI", "i": "🧠"}, {"n": "Blood Reports", "i": "🩸"}
    ]
    cols = st.columns(2)
    for idx, s in enumerate(scans):
        with cols[idx % 2]:
            st.markdown(f"""
            <div class="btn-tile">
                <div style="font-size: 1.2rem; margin-bottom: 4px;">{s['i']}</div>
                <div style="font-size: 0.75rem; font-weight: 600;">{s['n']}</div>
            </div>
            <div class="btn-upload">Upload</div>
            """, unsafe_allow_html=True)
            st.markdown("<div style='margin-bottom: 12px;'></div>", unsafe_allow_html=True)

def bmi_calculator_widget():
    """Renders BMI exactly like mockup."""
    c1, c2 = st.columns(2)
    with c1: st.text_input("Height", value="175 cm", label_visibility="collapsed", key="bmi_h_m")
    with c2: st.text_input("Weight", value="70 kg", label_visibility="collapsed", key="bmi_w_m")
    st.markdown("""
    <div class="gauge-container" style="padding-top: 0;">
        <svg viewBox="0 0 100 50" style="width: 140px; margin: 0 auto; display: block;">
            <path d="M 10 50 A 40 40 0 0 1 90 50" fill="transparent" stroke="url(#bmi-grad)" stroke-width="15" />
            <defs>
                <linearGradient id="bmi-grad">
                    <stop offset="0%" stop-color="#10b981" />
                    <stop offset="50%" stop-color="#f59e0b" />
                    <stop offset="100%" stop-color="#ef4444" />
                </linearGradient>
            </defs>
            <line x1="50" y1="50" x2="50" y2="15" stroke="#1e293b" stroke-width="3" stroke-linecap="round" transform="rotate(-40 50 50)" />
        </svg>
    </div>
    """, unsafe_allow_html=True)

def snellen_chart_widget():
    """Renders a full Snellen chart."""
    st.markdown("""
    <div style="text-align: center; font-family: 'Courier New', monospace; line-height: 1.1; letter-spacing: 2px;">
        <div style="font-size: 2.2rem; font-weight: 900;">E</div>
        <div style="font-size: 1.4rem; font-weight: 800;">F P</div>
        <div style="font-size: 1rem; font-weight: 700;">T O Z</div>
        <div style="font-size: 0.8rem; font-weight: 600;">L P E D</div>
        <div style="font-size: 0.65rem; font-weight: 500;">P E C F D</div>
        <div style="font-size: 0.55rem; font-weight: 500;">E D F C Z P</div>
        <div style="font-size: 0.45rem; font-weight: 400;">F E L O P Z D</div>
    </div>
    """, unsafe_allow_html=True)

def ayurvedic_remedies_widget():
    """Renders ayurvedic list exactly like mockup."""
    remedies = [
        {"name": "Natural Remedies", "desc": "Natural remedies help relieve pain, inflammation, and other natural factors."},
        {"name": "Natural Remedies", "desc": "Natural remedies restores natural, and body, symptom, and inflammation and elements."}
    ]
    for r in remedies:
        st.markdown(f"""
        <div class="med-row" style="background: white; border-color: #f1f5f9;">
            <div style="width: 50px; height: 50px; background: #f0fdf4; border-radius: 8px; flex-shrink: 0; display:flex; align-items:center; justify-content:center; font-size: 1.5rem;">🌿</div>
            <div class="med-info">
                <div class="med-name" style="color: #166534;">{r['name']}</div>
                <div class="med-details">{r['desc']}</div>
            </div>
        </div>
        """, unsafe_allow_html=True)
