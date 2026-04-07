import streamlit as st
import pandas as pd
from datetime import datetime

def show_water_tracker_section():
    st.markdown("<div class='section-header'>💧 Hydration Flow</div>", unsafe_allow_html=True)
    
    if "water_intake" not in st.session_state:
        st.session_state.water_intake = 0
    if "water_goal" not in st.session_state:
        st.session_state.water_goal = 2000 # Default 2L in ml
    
    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.markdown("<div class='glass-card'>", unsafe_allow_html=True)
        st.markdown(f"### Daily Goal: {st.session_state.water_goal}ml", unsafe_allow_html=True)
        new_goal = st.number_input("Set New Goal (ml)", min_value=1000, max_value=8000, step=250, value=st.session_state.water_goal)
        if new_goal != st.session_state.water_goal:
            st.session_state.water_goal = new_goal
        
        st.markdown("---")
        st.markdown("### Log Water Intake", unsafe_allow_html=True)
        
        btn_col1, btn_col2, btn_col3 = st.columns(3)
        with btn_col1:
            if st.button("+100ml", key="add_100"):
                st.session_state.water_intake += 100
        with btn_col2:
            if st.button("+250ml", key="add_250"):
                st.session_state.water_intake += 250
        with btn_col3:
            if st.button("+500ml", key="add_500"):
                st.session_state.water_intake += 500
        
        if st.button("Reset Daily Progress", key="reset_water"):
            st.session_state.water_intake = 0
            
        st.markdown("</div>", unsafe_allow_html=True)

    with col2:
        progress = min(st.session_state.water_intake / st.session_state.water_goal, 1.0)
        percentage = int(progress * 100)
        
        st.markdown(f"""
        <div class='glass-card' style='height: 400px; display: flex; flex-direction: column; justify-content: flex-end; align-items: center; position: relative;'>
            <div style='position: absolute; top: 20px; font-size: 2rem; font-weight: 800; color: var(--p-cyan); z-index: 10;'>{percentage}%</div>
            <div style='position: absolute; top: 60px; font-size: 1rem; color: var(--text-mute); z-index: 10;'>{st.session_state.water_intake} / {st.session_state.water_goal} ml</div>
            
            <!-- WAVE ANIMATION -->
            <div style='position: absolute; bottom: 0; left: 0; width: 100%; height: {percentage}%; background: linear-gradient(0deg, #00f2fe 0%, #4facfe 100%); border-radius: 0 0 16px 16px; opacity: 0.6; transition: height 0.5s ease-out; box-shadow: 0 0 20px rgba(0,242,254,0.3);'>
            </div>
            
            <div style='margin-bottom: 20px; font-size: 4rem; z-index: 10;'>{'💧' if percentage < 100 else '🌟'}</div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("---")
    st.markdown("### Hydration Tips", unsafe_allow_html=True)
    st.write("• Proper hydration improves energy, mood, and concentration.\n"
             "• Drink a glass of water right after waking up to jumpstart your metabolism.\n"
             "• Don't wait until you're thirsty to drink water.")
