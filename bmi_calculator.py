# ============================================================
# bmi_calculator.py — Complete BMI Calculator
# ============================================================

import streamlit as st
import pandas as pd

# ---------- BMI CALCULATE ----------
def calculate_bmi(weight, height_cm):
    height_m = height_cm / 100
    return round(weight / (height_m ** 2), 1)

# ---------- BMI CATEGORY ----------
def get_bmi_category(bmi):
    if bmi < 18.5:
        return "Underweight", "bmi-under", "💙", "#818cf8"
    elif bmi < 25:
        return "Normal Weight", "bmi-normal", "💚", "#4ade80"
    elif bmi < 30:
        return "Overweight", "bmi-over", "🧡", "#fb923c"
    else:
        return "Obese", "bmi-obese", "❤️", "#f87171"

# ---------- IDEAL WEIGHT ----------
def get_ideal_weight(height_cm):
    ideal_min = round((18.5 * (height_cm/100)**2), 1)
    ideal_max = round((24.9 * (height_cm/100)**2), 1)
    return ideal_min, ideal_max

# ---------- DIET TIPS ----------
def get_diet_tips(category):
    tips = {
        "Underweight": {
            "eat":   ["🥜 Nuts & dry fruits", "🥑 Avocado & healthy fats", "🍌 Bananas & fruits", "🥛 Milk & dairy", "🍳 Eggs & protein", "🍚 Rice & whole grains"],
            "avoid": ["❌ Skipping meals", "❌ Excessive caffeine", "❌ Empty calorie junk food"],
            "tips":  ["Eat 5-6 small meals daily", "Add protein shakes", "Do strength training", "Sleep 8 hours daily"]
        },
        "Normal Weight": {
            "eat":   ["🥗 Fresh vegetables", "🍎 Fruits daily", "🐟 Lean protein", "🌾 Whole grains", "💧 8 glasses of water", "🥦 Green vegetables"],
            "avoid": ["❌ Processed junk food", "❌ Sugary drinks", "❌ Excessive alcohol"],
            "tips":  ["Maintain current diet", "Exercise 30 mins daily", "Stay hydrated", "Regular health checkups"]
        },
        "Overweight": {
            "eat":   ["🥗 More vegetables", "🍎 Low sugar fruits", "🐟 Grilled fish & chicken", "🫘 Lentils & beans", "💧 Lots of water", "🥒 Cucumber & celery"],
            "avoid": ["❌ Fried & oily food", "❌ White bread & pasta", "❌ Sugary drinks", "❌ Fast food"],
            "tips":  ["500 calorie deficit daily", "Walk 10,000 steps daily", "Avoid late night eating", "Track your calories"]
        },
        "Obese": {
            "eat":   ["🥗 Salads & soups", "🫘 High fiber foods", "🐟 Lean proteins only", "💧 8-10 glasses of water", "🥦 Green vegetables", "🍋 Lemon water morning"],
            "avoid": ["❌ All fried foods", "❌ Sugar & sweets", "❌ Processed foods", "❌ Alcohol & sodas", "❌ White rice & bread"],
            "tips":  ["Consult a nutritionist", "Start with light walking", "Track food intake daily", "See a doctor immediately"]
        }
    }
    return tips.get(category, tips["Normal Weight"])

# ---------- SHOW BMI SECTION ----------
def show_bmi_section():
    st.markdown("<div class='section-header'>💪 BMI Calculator</div>", unsafe_allow_html=True)

    col1, col2 = st.columns(2)

    with col1:
        st.markdown("<div class='glass-box'>", unsafe_allow_html=True)
        st.markdown("<div class='section-title'>📏 Enter Your Details</div>", unsafe_allow_html=True)

        st.text_input("👤 Your Name", key="bmi_name_input")
        st.number_input("🎂 Age", 1, 120, 25, key="bmi_age_input")
        gender    = st.selectbox("⚧ Gender", ["Male", "Female"])
        height_cm = st.number_input("📏 Height (cm)", 50, 250, 170, key="bmi_height_input")
        weight_kg = st.number_input("⚖️ Weight (kg)", 10, 300, 70, key="bmi_weight_input")

        # Show in feet/inches
        feet   = int(height_cm / 30.48)
        inches = int((height_cm % 30.48) / 2.54)
        st.markdown(f"<div style='color:#a89ec9; font-size:0.82rem; margin-top:-10px; margin-bottom:10px;'>= {feet} ft {inches} in</div>", unsafe_allow_html=True)

        if st.button("💪 Calculate BMI", use_container_width=True):
            bmi = calculate_bmi(weight_kg, height_cm)
            category, css_class, icon, color = get_bmi_category(bmi)
            ideal_min, ideal_max = get_ideal_weight(height_cm)
            st.session_state.bmi_result   = bmi
            st.session_state.bmi_category = category
            st.session_state.bmi_css      = css_class
            st.session_state.bmi_icon     = icon
            st.session_state.bmi_color    = color
            st.session_state.ideal_min    = ideal_min
            st.session_state.ideal_max    = ideal_max
            st.session_state.bmi_weight   = weight_kg
            st.rerun()

        st.markdown("</div>", unsafe_allow_html=True)

        # BMI Scale
        st.markdown("<div class='glass-box'>", unsafe_allow_html=True)
        st.markdown("<div class='section-title'>📊 BMI Scale</div>", unsafe_allow_html=True)
        st.markdown("""
        <div style='font-size:0.88rem; line-height:1.6;'>
            <div style='display:flex; justify-content:space-between; padding:10px 14px;
                 background:rgba(129,140,248,0.1); border-radius:10px; margin-bottom:7px;
                 border-left:3px solid #818cf8;'>
                <span>💙 Underweight</span>
                <span style='color:#818cf8; font-weight:700;'>Below 18.5</span>
            </div>
            <div style='display:flex; justify-content:space-between; padding:10px 14px;
                 background:rgba(74,222,128,0.1); border-radius:10px; margin-bottom:7px;
                 border-left:3px solid #4ade80;'>
                <span>💚 Normal Weight</span>
                <span style='color:#4ade80; font-weight:700;'>18.5 – 24.9</span>
            </div>
            <div style='display:flex; justify-content:space-between; padding:10px 14px;
                 background:rgba(251,146,60,0.1); border-radius:10px; margin-bottom:7px;
                 border-left:3px solid #fb923c;'>
                <span>🧡 Overweight</span>
                <span style='color:#fb923c; font-weight:700;'>25.0 – 29.9</span>
            </div>
            <div style='display:flex; justify-content:space-between; padding:10px 14px;
                 background:rgba(248,113,113,0.1); border-radius:10px;
                 border-left:3px solid #f87171;'>
                <span>❤️ Obese</span>
                <span style='color:#f87171; font-weight:700;'>30.0 and above</span>
            </div>
        </div>
        """, unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)

    with col2:
        st.markdown("<div class='glass-box'>", unsafe_allow_html=True)
        st.markdown("<div class='section-title'>📊 Your BMI Result</div>", unsafe_allow_html=True)

        if "bmi_result" in st.session_state and st.session_state.bmi_result:
            bmi       = st.session_state.bmi_result
            category  = st.session_state.bmi_category
            css       = st.session_state.bmi_css
            icon      = st.session_state.bmi_icon
            ideal_min = st.session_state.ideal_min
            ideal_max = st.session_state.ideal_max
            weight    = st.session_state.bmi_weight

            # Big BMI Score
            st.markdown(f"""
            <div class='bmi-result {css}'>
                <div style='font-size:4.5rem; font-weight:900; letter-spacing:-2px;'>{bmi}</div>
                <div style='font-size:1.4rem; margin-top:8px; font-weight:700;'>{icon} {category}</div>
                <div style='font-size:0.82rem; opacity:0.6; margin-top:5px;'>Body Mass Index</div>
            </div>
            """, unsafe_allow_html=True)

            # Ideal Weight
            weight_diff = round(weight - ideal_max, 1)
            if category == "Normal Weight":
                weight_msg   = "✅ You are at your ideal weight! Keep it up!"
                weight_color = "#4ade80"
            elif category == "Underweight":
                weight_msg   = f"⬆️ Gain {abs(weight_diff)} kg to reach ideal weight"
                weight_color = "#818cf8"
            else:
                weight_msg   = f"⬇️ Lose {abs(weight_diff)} kg to reach ideal weight"
                weight_color = "#fb923c"

            st.markdown(f"""
            <div style='background:rgba(255,255,255,0.04); border:1px solid rgba(255,255,255,0.08);
                 padding:18px; border-radius:14px; margin-top:16px; text-align:center;'>
                <div style='color:#a89ec9; font-size:0.82rem; margin-bottom:6px;'>🎯 Ideal Weight Range</div>
                <div style='color:white; font-size:1.5rem; font-weight:800;'>{ideal_min} – {ideal_max} kg</div>
                <div style='color:{weight_color}; font-size:0.9rem; margin-top:10px; font-weight:600;'>{weight_msg}</div>
            </div>
            """, unsafe_allow_html=True)

            # Bar Chart
            st.markdown("<br>**📈 BMI Comparison:**", unsafe_allow_html=True)
            chart_data = pd.DataFrame({
                "Category": ["Underweight\n(17)", "Normal\n(22)", "Overweight\n(27)", "Obese\n(35)", f"Your BMI\n({bmi})"],
                "BMI":      [17, 22, 27, 35, bmi]
            })
            st.bar_chart(chart_data.set_index("Category"))

        else:
            st.markdown("""
            <div style='text-align:center; padding:80px 20px; color:#475569;'>
                <div style='font-size:5rem; margin-bottom:20px;'>💪</div>
                <p style='font-size:1.1rem; font-weight:600; color:#6b7280;'>No result yet</p>
                <p style='font-size:0.85rem;'>Enter your details and click Calculate BMI</p>
            </div>
            """, unsafe_allow_html=True)

        st.markdown("</div>", unsafe_allow_html=True)

    # Diet Tips Section
    if "bmi_result" in st.session_state and st.session_state.bmi_result:
        category  = st.session_state.bmi_category
        tips_data = get_diet_tips(category)

        st.markdown("<br>", unsafe_allow_html=True)
        st.markdown(f"<div class='section-header'>🥗 Diet Tips for {category}</div>", unsafe_allow_html=True)

        t1, t2, t3 = st.columns(3)

        with t1:
            st.markdown("<div class='glass-box'>", unsafe_allow_html=True)
            st.markdown("<div class='section-title'>✅ Foods to Eat</div>", unsafe_allow_html=True)
            for food in tips_data["eat"]:
                st.markdown(f"""
                <div style='background:rgba(74,222,128,0.07); border:1px solid rgba(74,222,128,0.15);
                     padding:9px 13px; border-radius:10px; margin-bottom:7px;
                     color:#86efac; font-size:0.88rem;'>{food}</div>
                """, unsafe_allow_html=True)
            st.markdown("</div>", unsafe_allow_html=True)

        with t2:
            st.markdown("<div class='glass-box'>", unsafe_allow_html=True)
            st.markdown("<div class='section-title'>❌ Foods to Avoid</div>", unsafe_allow_html=True)
            for food in tips_data["avoid"]:
                st.markdown(f"""
                <div style='background:rgba(248,113,113,0.07); border:1px solid rgba(248,113,113,0.15);
                     padding:9px 13px; border-radius:10px; margin-bottom:7px;
                     color:#fca5a5; font-size:0.88rem;'>{food}</div>
                """, unsafe_allow_html=True)
            st.markdown("</div>", unsafe_allow_html=True)

        with t3:
            st.markdown("<div class='glass-box'>", unsafe_allow_html=True)
            st.markdown("<div class='section-title'>💡 Health Tips</div>", unsafe_allow_html=True)
            for tip in tips_data["tips"]:
                st.markdown(f"""
                <div style='background:rgba(167,139,250,0.07); border:1px solid rgba(167,139,250,0.15);
                     padding:9px 13px; border-radius:10px; margin-bottom:7px;
                     color:#c4b5fd; font-size:0.88rem;'>💡 {tip}</div>
                """, unsafe_allow_html=True)
            st.markdown("</div>", unsafe_allow_html=True)
