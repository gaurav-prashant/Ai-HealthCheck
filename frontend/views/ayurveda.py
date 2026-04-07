# ============================================================
# ayurveda.py — Ayurveda & Home Remedies
# ============================================================

import streamlit as st
from backend.services.ai_functions import client  # reuse Groq client

COMMON_AILMENTS = [
    "Common Cold", "Cough", "Fever", "Headache", "Sore Throat",
    "Stomach Pain", "Acidity / Heartburn", "Constipation", "Diarrhea",
    "Skin Rash", "Dandruff", "Hair Fall", "Joint Pain", "Back Pain",
    "Insomnia / Poor Sleep", "Stress / Anxiety", "Weakness / Fatigue",
    "Toothache", "Eye Strain", "High Blood Pressure"
]

def get_ayurveda_remedy(symptom: str) -> dict:
    """Uses Groq AI to return Ayurvedic & home remedies for a symptom."""
    try:
        prompt = f"""You are an expert in Ayurveda and traditional home remedies. 
ALWAYS RESPOND IN ENGLISH.
For the condition/symptom: "{symptom}"

Provide a comprehensive response in this EXACT format (use these exact section headers):

🌿 **AYURVEDIC HERBS:**
- List 3-4 specific Ayurvedic herbs with how to use them

🏠 **HOME REMEDIES:**
- List 4-5 practical home remedies with simple instructions

🥗 **DIET RECOMMENDATIONS:**
- List 3-4 foods to eat and 2-3 foods to avoid

🧘 **LIFESTYLE TIPS:**
- List 3 lifestyle/yoga/breathing tips

⚠️ **WHEN TO SEE A DOCTOR:**
- Mention 2-3 warning signs that need medical attention

Keep each point concise and practical. Use simple language."""

        response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[{"role": "user", "content": prompt}],
            max_tokens=700,
            temperature=0.5
        )
        return {"success": True, "remedy": response.choices[0].message.content}
    except Exception as e:
        return {"success": False, "error": str(e)}


def show_ayurveda_page():
    """Render the Ayurveda & Home Remedies page."""

    # ── Header ──
    st.markdown("""
    <div style='background:linear-gradient(135deg,rgba(34,197,94,0.1),rgba(16,185,129,0.05));
                border:1px solid rgba(34,197,94,0.2); border-radius:20px;
                padding:28px; margin-bottom:28px;'>
        <div style='font-size:2rem; font-weight:900;
                    background:linear-gradient(90deg,#22c55e,#10b981);
                    -webkit-background-clip:text; -webkit-text-fill-color:transparent;'>
            🌿 Ayurveda & Home Remedies
        </div>
        <div style='color:#94a3b8; font-size:0.9rem; margin-top:4px;'>
            Ancient wisdom meets AI — natural remedies for common ailments
        </div>
    </div>
    """, unsafe_allow_html=True)

    left, right = st.columns([1, 1.6])

    with left:
        st.markdown("### 🔍 Find Remedies")

        # Quick select from common ailments
        st.markdown("<div style='font-size:0.85rem; color:#94a3b8; margin-bottom:6px;'>Select an ailment:</div>",
                    unsafe_allow_html=True)
        selected_quick = st.selectbox(
            "Common ailments", ["— Choose —"] + COMMON_AILMENTS,
            label_visibility="collapsed"
        )

        # Determine final query
        query = selected_quick if selected_quick != "— Choose —" else ""

        if query:
            st.markdown(f"""
            <div style='background:rgba(34,197,94,0.06); border:1px solid rgba(34,197,94,0.2);
                        border-radius:10px; padding:10px 14px; margin:10px 0;
                        font-size:0.9rem; color:#86efac;'>
                🎯 Looking up remedies for: <b>{query}</b>
            </div>
            """, unsafe_allow_html=True)

        if st.button("🌿 GET REMEDIES", use_container_width=True, type="primary",
                     disabled=not bool(query)):
            if query:
                with st.spinner("🧠 Consulting Ayurvedic wisdom..."):
                    result = get_ayurveda_remedy(query)
                st.session_state["ayur_result"] = result
                st.session_state["ayur_query"] = query
                st.rerun()

        # ── Disclaimer ──
        st.markdown("<br>", unsafe_allow_html=True)
        st.markdown("""
        <div style='background:rgba(251,191,36,0.06); border:1px solid rgba(251,191,36,0.15);
                    border-radius:10px; padding:12px 14px; font-size:0.78rem; color:#94a3b8;'>
            ⚠️ <b>Disclaimer:</b> These are traditional home remedies for general wellness only.
            They are not a substitute for professional medical advice.
            Always consult a doctor for serious conditions.
        </div>
        """, unsafe_allow_html=True)

        # ── Quick herb cards ──
        st.markdown("<br>", unsafe_allow_html=True)
        st.markdown("### 🌱 Power Herbs")
        herbs = [
            ("🫚", "Turmeric", "Anti-inflammatory, immunity booster"),
            ("🌿", "Tulsi", "Respiratory health, stress relief"),
            ("🧄", "Ginger", "Digestion, nausea, cold & cough"),
            ("🍯", "Honey", "Antibacterial, sore throat relief"),
            ("🌰", "Ashwagandha", "Stress, energy, sleep quality"),
            ("🫙", "Triphala", "Digestion, detox, bowel health"),
        ]
        for emoji, name, desc in herbs:
            st.markdown(f"""
            <div style='display:flex; align-items:center; gap:10px; padding:8px 12px;
                        background:rgba(34,197,94,0.03); border:1px solid rgba(34,197,94,0.1);
                        border-radius:10px; margin-bottom:6px;'>
                <div style='font-size:1.4rem;'>{emoji}</div>
                <div>
                    <div style='font-weight:700; font-size:0.88rem; color:#86efac;'>{name}</div>
                    <div style='font-size:0.75rem; color:#94a3b8;'>{desc}</div>
                </div>
            </div>
            """, unsafe_allow_html=True)

    # ── RIGHT: Results ──
    with right:
        st.markdown("### 📜 Remedy Guide")

        result = st.session_state.get("ayur_result")
        query_used = st.session_state.get("ayur_query", "")

        if result:
            if result.get("success"):
                st.markdown(f"""
                <div style='background:rgba(34,197,94,0.04); border:1px solid rgba(34,197,94,0.15);
                            border-radius:14px; padding:22px; font-size:0.9rem; line-height:1.8;
                            color:#e2e8f0; white-space:pre-wrap;'>
                    <div style='font-size:0.7rem; color:#22c55e; font-weight:700;
                                letter-spacing:1.5px; margin-bottom:12px;'>
                        AYURVEDIC REMEDY FOR: {query_used.upper()}
                    </div>
                    {result['remedy']}
                </div>
                """, unsafe_allow_html=True)

                # Clear button
                st.markdown("<br>", unsafe_allow_html=True)
                if st.button("🔄 Clear & Search Again", use_container_width=True):
                    del st.session_state["ayur_result"]
                    del st.session_state["ayur_query"]
                    st.rerun()
            else:
                st.error(f"❌ Error: {result.get('error')}")
        else:
            # Placeholder state
            st.markdown("""
            <div style='text-align:center; padding:60px 20px; color:#475569;'>
                <div style='font-size:4rem; margin-bottom:16px;'>🌿</div>
                <div style='font-size:1rem; font-weight:600; color:#64748b;'>
                    Select an ailment or type a symptom
                </div>
                <div style='font-size:0.85rem; margin-top:8px;'>
                    Get Ayurvedic herbs, home remedies, diet tips & lifestyle advice
                </div>
            </div>
            """, unsafe_allow_html=True)

            # Preview cards of what you'll get
            sections = [
                ("🌿", "Ayurvedic Herbs", "Specific herbs with usage instructions"),
                ("🏠", "Home Remedies", "Easy kitchen remedies you can make today"),
                ("🥗", "Diet Tips", "What to eat and what to avoid"),
                ("🧘", "Lifestyle", "Yoga, breathing & wellness tips"),
            ]
            preview_cols = st.columns(2)
            for i, (icon, title, desc) in enumerate(sections):
                with preview_cols[i % 2]:
                    st.markdown(f"""
                    <div style='background:rgba(34,197,94,0.04); border:1px solid rgba(34,197,94,0.1);
                                border-radius:12px; padding:16px; margin-bottom:10px; text-align:center;'>
                        <div style='font-size:1.8rem;'>{icon}</div>
                        <div style='font-weight:700; font-size:0.85rem; color:#86efac; margin-top:4px;'>{title}</div>
                        <div style='font-size:0.75rem; color:#94a3b8; margin-top:2px;'>{desc}</div>
                    </div>
                    """, unsafe_allow_html=True)
