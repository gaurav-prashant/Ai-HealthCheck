# ============================================================
# diet_plan.py — Diet Plan Generator
# ============================================================

import streamlit as st
import os
import cohere

co = cohere.Client(os.getenv("COHERE_API_KEY"))

# ---------- GENERATE DIET PLAN ----------
def generate_diet_plan(disease, body_type, age):
    try:
        prompt = f"""
You are a professional nutritionist. ALWAYS RESPOND IN ENGLISH.
Create a detailed 1-day diet plan for a patient with the following details:
- Disease/Condition: {disease}
- Diet Type: {body_type}
- Age: {age}

Format the response EXACTLY like this:

🌅 BREAKFAST:
- Item 1
- Item 2
- Item 3

☀️ LUNCH:
- Item 1
- Item 2
- Item 3

🌆 DINNER:
- Item 1
- Item 2
- Item 3

🍎 SNACKS:
- Item 1
- Item 2

🥤 DRINKS/JUICES:
- Item 1
- Item 2

❌ FOODS TO AVOID:
- Item 1
- Item 2
- Item 3

Keep it simple, healthy and suitable for the disease. Max 3-4 items per section.
"""
        response = co.chat(
            message=prompt,
            model="command-r-08-2024"
        )
        return response.text
    except Exception as e:
        return f"⚠ Error generating diet plan: {e}"

# ---------- SHOW DIET PLAN ----------
def show_diet_plan_section():
    st.markdown("""
        <div class="section-header">
            <img src="https://img.icons8.com/fluency/96/salad.png" width="50" style="margin-bottom: 10px;">
            <br>
            🥗 AI Diet Plan Generator
        </div>
    """, unsafe_allow_html=True)

    col1, col2 = st.columns(2)

    with col1:
        st.markdown("<div class='glass-box'>", unsafe_allow_html=True)
        st.markdown("<div class='section-title'>🍽️ Generate Your Diet Plan</div>", unsafe_allow_html=True)

        # Disease Input
        disease_options = [
            "Flu", "Common Cold", "COVID-19", "Migraine",
            "Food Poisoning", "Heart Problem", "Diabetes",
            "High Blood Pressure", "Obesity", "Anemia",
            "Thyroid", "Asthma", "Arthritis", "General Health"
        ]
        selected_disease = st.selectbox("🦠 Select Disease / Condition", disease_options)

        # Body Type
        body_type = st.selectbox("🥦 Diet Preference", [
            "Vegetarian",
            "Non-Vegetarian",
            "Vegan",
            "Eggetarian"
        ])

        # Age
        age = st.number_input("🎂 Your Age", min_value=1, max_value=120, value=25)

        # Extra notes
        extra = st.text_input("📝 Any extra notes (optional)", placeholder="e.g. diabetic, allergic to nuts")

        if st.button("🥗 Generate Diet Plan"):
            disease_input = f"{selected_disease}. {extra}" if extra else selected_disease
            with st.spinner("🤖 AI is creating your personalized diet plan..."):
                plan = generate_diet_plan(disease_input, body_type, age)
            st.session_state.diet_plan = plan
            st.rerun()

        st.markdown("</div>", unsafe_allow_html=True)

    with col2:
        st.markdown("<div class='glass-box'>", unsafe_allow_html=True)
        st.markdown("<div class='section-title'>📋 Your Diet Plan</div>", unsafe_allow_html=True)

        if "diet_plan" in st.session_state and st.session_state.diet_plan:
            plan = st.session_state.diet_plan

            # Split and display each section nicely
            sections = plan.split("\n\n")
            for section in sections:
                if section.strip():
                    lines = section.strip().split("\n")
                    if lines:
                        title = lines[0]
                        items = lines[1:]

                        # Choose color based on section
                        if "BREAKFAST" in title:
                            color = "rgba(251,191,36,0.1)"
                            border = "rgba(251,191,36,0.3)"
                            text_color = "#fbbf24"
                        elif "LUNCH" in title:
                            color = "rgba(34,197,94,0.1)"
                            border = "rgba(34,197,94,0.3)"
                            text_color = "#4ade80"
                        elif "DINNER" in title:
                            color = "rgba(139,92,246,0.1)"
                            border = "rgba(139,92,246,0.3)"
                            text_color = "#c4b5fd"
                        elif "SNACK" in title:
                            color = "rgba(249,115,22,0.1)"
                            border = "rgba(249,115,22,0.3)"
                            text_color = "#fb923c"
                        elif "DRINK" in title or "JUICE" in title:
                            color = "rgba(6,182,212,0.1)"
                            border = "rgba(6,182,212,0.3)"
                            text_color = "#22d3ee"
                        elif "AVOID" in title:
                            color = "rgba(239,68,68,0.1)"
                            border = "rgba(239,68,68,0.3)"
                            text_color = "#f87171"
                        else:
                            color = "rgba(255,255,255,0.05)"
                            border = "rgba(255,255,255,0.1)"
                            text_color = "#e2e8f0"

                        items_html = "".join([f"<li style='margin:4px 0;'>{item.replace('- ', '')}</li>" for item in items if item.strip()])

                        st.markdown(f"""
                        <div style='background:{color}; border:1px solid {border};
                             padding:14px 16px; border-radius:14px; margin-bottom:12px;'>
                            <div style='color:{text_color}; font-weight:700; font-size:0.95rem; margin-bottom:8px;'>{title}</div>
                            <ul style='color:#e2e8f0; margin:0; padding-left:18px; font-size:0.88rem; line-height:1.7;'>
                                {items_html}
                            </ul>
                        </div>
                        """, unsafe_allow_html=True)

            # Download button
            st.download_button(
                "📄 Download Diet Plan",
                data=plan,
                file_name="diet_plan.txt",
                mime="text/plain"
            )

            if st.button("🗑 Clear Diet Plan"):
                st.session_state.diet_plan = ""
                st.rerun()
        else:
            st.markdown("""
            <div style='text-align:center; padding:40px 20px; color:#475569;'>
                <div style='font-size:3rem; margin-bottom:15px;'>🥗</div>
                <p style='font-size:1rem; font-weight:500;'>No diet plan yet</p>
                <p style='font-size:0.85rem;'>Select your condition and click Generate</p>
            </div>
            """, unsafe_allow_html=True)

        st.markdown("</div>", unsafe_allow_html=True)
