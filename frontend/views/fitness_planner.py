import streamlit as st
from backend.services.ai_functions import ai_chatbot

def show_fitness_planner_section():
    st.markdown("<div class='section-header'>💪 AI Fitness Architect</div>", unsafe_allow_html=True)
    
    col1, col2 = st.columns([1, 1.2])
    
    with col1:
        st.markdown("<div class='glass-card'>", unsafe_allow_html=True)
        st.markdown("### Design Your Routine", unsafe_allow_html=True)
        
        goal = st.selectbox("What is your primary goal?", [
            "Weight Loss", "Muscle Gain", "Endurance / Cardio", "Flexibility / Yoga", "General Fitness"
        ])
        
        level = st.select_slider("Select your experience level", options=["Beginner", "Intermediate", "Advanced"])
        
        days = st.slider("Days per week available", 1, 7, 3)
        
        equipment = st.multiselect("Available Equipment", ["No Equipment (Bodyweight)", "Dumbbells", "Resistance Bands", "Full Gym"])
        
        if st.button("Generate My Plan", use_container_width=True):
            with st.spinner("Architecting your routine..."):
                prompt = (f"Act as a professional fitness trainer. Generate a {days}-day weekly workout plan for a {level} level person "
                          f"whose goal is {goal}. Equipment available: {', '.join(equipment) if equipment else 'None'}. "
                          "Format it clearly with exercises and sets/reps.")
                plan = ai_chatbot(prompt)
                st.session_state.fitness_plan = plan
        st.markdown("</div>", unsafe_allow_html=True)

    with col2:
        if "fitness_plan" in st.session_state:
            st.markdown("<div class='section-title'>📋 Your Personalized Plan</div>", unsafe_allow_html=True)
            st.markdown(f"""
            <div class='glass-card' style='background: rgba(16, 185, 129, 0.05); text-align: left; overflow-y: auto; max-height: 500px;'>
                {st.session_state.fitness_plan}
            </div>
            """, unsafe_allow_html=True)
        else:
            st.markdown("""
            <div style='text-align:center;padding:40px;color:var(--text-dim);'>
                <div style='font-size:3rem;'>🏋️️</div>
                <p>Fill in your details and click Generate My Plan</p>
            </div>
            """, unsafe_allow_html=True)

    st.markdown("---")
    st.markdown("### Pro Fitness Tips", unsafe_allow_html=True)
    st.write("• Consistency is more important than intensity in the beginning.\n"
             "• Always warm up for 5-10 minutes before starting your workout.\n"
             "• Listen to your body and rest when needed to avoid injury.")
