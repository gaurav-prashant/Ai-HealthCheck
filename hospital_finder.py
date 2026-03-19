# ============================================================
# hospital_finder.py — Nearby Hospital Finder
# ============================================================

import streamlit as st

def show_hospital_finder():
    st.markdown("<div class='section-header'>🏥 Nearby Hospital Finder</div>", unsafe_allow_html=True)

    col1, col2 = st.columns([1, 2])

    with col1:
        st.markdown("<div class='glass-box'>", unsafe_allow_html=True)
        st.markdown("<div class='section-title'>🔍 Search Filters</div>", unsafe_allow_html=True)

        specialty = st.selectbox("🏨 Specialty", [
            "All Hospitals", "General Hospital", "Emergency / Trauma",
            "Heart / Cardiology", "Eye Hospital", "Children Hospital",
            "Orthopedic", "Mental Health", "Dental Clinic",
            "Maternity / Gynecology", "Skin / Dermatology",
        ])

        st.markdown("</div>", unsafe_allow_html=True)

        # Emergency numbers
        st.markdown("""
        <div class='glass-box'>
            <div class='section-title'>🚨 Emergency Numbers</div>
            <div style='font-size:0.9rem; line-height:2.4;'>
                <div style='display:flex; justify-content:space-between; padding:8px 12px;
                     background:rgba(239,68,68,0.1); border-radius:10px; margin-bottom:6px;
                     border:1px solid rgba(239,68,68,0.2);'>
                    <span style='color:#d4d0f0;'>🚑 Ambulance</span>
                    <b style='color:#f87171; font-size:1.1rem;'>102</b>
                </div>
                <div style='display:flex; justify-content:space-between; padding:8px 12px;
                     background:rgba(239,68,68,0.1); border-radius:10px; margin-bottom:6px;
                     border:1px solid rgba(239,68,68,0.2);'>
                    <span style='color:#d4d0f0;'>🚒 Fire</span>
                    <b style='color:#f87171; font-size:1.1rem;'>101</b>
                </div>
                <div style='display:flex; justify-content:space-between; padding:8px 12px;
                     background:rgba(239,68,68,0.1); border-radius:10px; margin-bottom:6px;
                     border:1px solid rgba(239,68,68,0.2);'>
                    <span style='color:#d4d0f0;'>👮 Police</span>
                    <b style='color:#f87171; font-size:1.1rem;'>100</b>
                </div>
                <div style='display:flex; justify-content:space-between; padding:8px 12px;
                     background:rgba(239,68,68,0.1); border-radius:10px;
                     border:1px solid rgba(239,68,68,0.2);'>
                    <span style='color:#d4d0f0;'>🏥 Emergency</span>
                    <b style='color:#f87171; font-size:1.1rem;'>112</b>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)

    with col2:
        q             = specialty if specialty != "All Hospitals" else "hospital"
        url_nearby    = f"https://www.google.com/maps/search/{q.replace(' ', '+')}+near+me"
        url_emergency = "https://www.google.com/maps/search/emergency+hospital+24+hours+near+me"
        url_general   = "https://www.google.com/maps/search/hospital+near+me"

        st.markdown("<div class='section-title'>🗺️ Find Hospitals</div>", unsafe_allow_html=True)

        st.link_button(f"📍 Find Nearby Hospitals — {specialty}", url_nearby,    use_container_width=True)
        st.link_button("🚨 Find Emergency Hospital (24/7)",        url_emergency, use_container_width=True)
        st.link_button("🗺️ All Hospitals on Google Maps",          url_general,   use_container_width=True)

        st.markdown("<br>", unsafe_allow_html=True)

        st.markdown("<div class='section-title'>🗺️ Hospital Map</div>", unsafe_allow_html=True)
        map_query = q.replace(" ", "+") + "+hospital"
        embed_url = f"https://maps.google.com/maps?q={map_query}&output=embed&z=13"
        st.markdown(f"""
        <iframe src="{embed_url}" width="100%" height="400"
            style="border:none; border-radius:16px; border:1px solid rgba(124,58,237,0.3);"
            allowfullscreen="" loading="lazy">
        </iframe>
        <div style='text-align:center; color:#7c74a8; font-size:0.78rem; margin-top:8px;'>
            📍 Click the map to interact · Use buttons above to search near your location
        </div>
        """, unsafe_allow_html=True)

    # Find by City
    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown("<div class='section-header'>🏥 Find by City</div>", unsafe_allow_html=True)

    cities = {
        "Delhi":     "https://www.google.com/maps/search/hospital+in+Delhi",
        "Mumbai":    "https://www.google.com/maps/search/hospital+in+Mumbai",
        "Bangalore": "https://www.google.com/maps/search/hospital+in+Bangalore",
        "Hyderabad": "https://www.google.com/maps/search/hospital+in+Hyderabad",
        "Chennai":   "https://www.google.com/maps/search/hospital+in+Chennai",
        "Kolkata":   "https://www.google.com/maps/search/hospital+in+Kolkata",
        "Pune":      "https://www.google.com/maps/search/hospital+in+Pune",
        "Meerut":    "https://www.google.com/maps/search/hospital+in+Meerut",
        "Lucknow":   "https://www.google.com/maps/search/hospital+in+Lucknow",
        "Jaipur":    "https://www.google.com/maps/search/hospital+in+Jaipur",
        "Ahmedabad": "https://www.google.com/maps/search/hospital+in+Ahmedabad",
        "Noida":     "https://www.google.com/maps/search/hospital+in+Noida",
    }

    city_cols = st.columns(4)
    for i, (city, url) in enumerate(cities.items()):
        with city_cols[i % 4]:
            st.link_button(f"🏥 {city}", url, use_container_width=True)

    # Bottom tips
    st.markdown("""
    <div style='display:flex; gap:12px; margin-top:16px; flex-wrap:wrap;'>
        <div style='flex:1; min-width:180px; background:rgba(239,68,68,0.08);
             border:1px solid rgba(239,68,68,0.2); padding:12px 14px;
             border-radius:12px; font-size:0.82rem; color:#fca5a5;'>
            🚨 <b>Emergency?</b> Call <b>112</b> or <b>102</b> immediately
        </div>
        <div style='flex:1; min-width:180px; background:rgba(16,185,129,0.07);
             border:1px solid rgba(16,185,129,0.2); padding:12px 14px;
             border-radius:12px; font-size:0.82rem; color:#6ee7b7;'>
            💡 All buttons open <b>Google Maps</b> in new tab
        </div>
        <div style='flex:1; min-width:180px; background:rgba(124,58,237,0.07);
             border:1px solid rgba(124,58,237,0.2); padding:12px 14px;
             border-radius:12px; font-size:0.82rem; color:#c4b5fd;'>
            📍 Google Maps will detect your <b>current location</b>
        </div>
    </div>
    """, unsafe_allow_html=True)