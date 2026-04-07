import streamlit as st
from backend.services.ai_functions import ai_chatbot

def show_mental_health_section():
    st.markdown("<div class='section-header'>🧘 Mental Health Oracle</div>", unsafe_allow_html=True)
    
    col1, col2 = st.columns([1, 1.2])
    
    with col1:
        st.markdown("<div class='glass-card'>", unsafe_allow_html=True)
        st.markdown("### How are you feeling today?", unsafe_allow_html=True)
        
        moods = {
            "😊 Happy": "Life is good! Keep that positive energy flowing.",
            "😔 Sad": "It's okay to feel down sometimes. Talking about it helps.",
            "😫 Stressed": "High pressure? Let's take a moment to breathe.",
            "😰 Anxious": "Take it one step at a time. The Oracle is here to listen.",
            "😡 Angry": "Let it out constructively. Peace starts within.",
            "😴 Tired": "Your body needs rest. Give yourself permission to recharge."
        }
        
        selected_mood = st.selectbox("Select Your Mood", list(moods.keys()))
        if selected_mood:
            st.info(moods[selected_mood])
        
        st.markdown("---")
        st.markdown("### Guided AI Journaling", unsafe_allow_html=True)
        st.write("Write down whatever is on your mind. The Oracle will provide empathetic guidance.")
        
        user_input = st.text_area("Your Thoughts...", height=150, placeholder="Today I felt...")
        
        if st.button("Consult the Oracle", use_container_width=True):
            if user_input:
                with st.spinner("Oracle is reflecting..."):
                    prompt = f"The user is feeling {selected_mood}. They wrote: '{user_input}'. Provide a short, empathetic, and helpful response with a mental health focus."
                    response = ai_chatbot(prompt)
                    st.session_state.mental_health_response = response
            else:
                st.warning("Please share your thoughts first.")
        st.markdown("</div>", unsafe_allow_html=True)

    with col2:
        if "mental_health_response" in st.session_state:
            st.markdown("<div class='section-title'>✨ Oracle's Guidance</div>", unsafe_allow_html=True)
            st.markdown(f"""
            <div class='glass-card' style='background: rgba(0, 242, 254, 0.05); text-align: left;'>
                {st.session_state.mental_health_response}
            </div>
            """, unsafe_allow_html=True)
        
        st.markdown("<div class='section-title'>🌿 Quick Zen Exercises</div>", unsafe_allow_html=True)
        ex_col1, ex_col2 = st.columns(2)
        
        with ex_col1:
            if st.button("🫁 4-7-8 Breathing", use_container_width=True):
                st.info("Inhale for 4s, Hold for 7s, Exhale for 8s. Repeat 4 times.")
            if st.button("🎵 Calming Sounds", use_container_width=True):
                st.info("Imagine the sound of gentle rain or ocean waves.")
        
        with ex_col2:
            if st.button("🧘 5-Minute Meditate", use_container_width=True):
                st.info("Close your eyes. Focus on your breath. Let thoughts pass like clouds.")
            if st.button("🚶 Mindful Walk", use_container_width=True):
                st.info("Take a short walk. Notice 5 things you can see, 4 you can touch, 3 you can hear.")

    # CSS for matching theme
    st.markdown("""
    <style>
    .stTextArea textarea {
        background: rgba(255, 255, 255, 0.05) !important;
        color: white !important;
        border: 1px solid rgba(255, 255, 255, 0.1) !important;
    }
    </style>
    """, unsafe_allow_html=True)
