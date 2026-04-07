# ============================================================
# medical_store.py — Nearby Medical Store & Pharmacy Finder
# ============================================================

import streamlit as st
import streamlit.components.v1 as components

def show_medical_store():
    st.markdown("""
        <div class="section-header">
            <img src="https://img.icons8.com/fluency/96/pill.png" width="50" style="margin-bottom: 10px;">
            <br>
            💊 Medical Store & Pharmacy Finder
        </div>
    """, unsafe_allow_html=True)

    st.markdown("""
    <div style='background:rgba(16,185,129,0.08); border:1px solid rgba(16,185,129,0.2);
         padding:12px 16px; border-radius:14px; margin-bottom:18px;
         font-size:0.87rem; color:#d4d0f0; line-height:1.8;'>
        💊 Find <b style='color:#6ee7b7;'>medical stores & pharmacies</b> near you<br>
        🗺️ Click any store to get <b style='color:#fbbf24;'>Google Maps directions</b><br>
        🚨 Use <b style='color:#f87171;'>24/7 Pharmacy</b> button for night emergencies
    </div>
    """, unsafe_allow_html=True)

    col1, col2 = st.columns([1, 2])

    with col1:
        st.markdown("<div class='glass-box'>", unsafe_allow_html=True)
        st.markdown("<div class='section-title'>🔍 Search Filters</div>", unsafe_allow_html=True)

        store_type = st.selectbox("🏪 Store Type", [
            "All Medical Stores",
            "Pharmacy / Chemist",
            "24/7 Emergency Pharmacy",
            "Ayurvedic / Herbal Store",
            "Surgical Equipment",
            "Baby & Child Medical",
            "Homeopathic Store",
            "Optical Store",
            "Dental Supplies",
            "Health & Wellness Store",
        ])

        open_now   = st.checkbox("✅ Open Now Only")
        night_24hr = st.checkbox("🌙 24/7 Night Pharmacy")

        st.markdown("</div>", unsafe_allow_html=True)

        # Quick search by medicine
        st.markdown("<div class='glass-box'>", unsafe_allow_html=True)
        st.markdown("<div class='section-title'>💊 Search by Medicine</div>", unsafe_allow_html=True)
        medicine = st.text_input("🔍 Medicine Name", placeholder="e.g. Paracetamol, Aspirin...")
        if medicine:
            med_url = f"https://www.google.com/maps/search/pharmacy+{medicine.replace(' ', '+')}+near+me"
            st.markdown(f"""
            <a href="{med_url}" target="_blank" style="display:block;text-align:center;
               padding:10px; background:linear-gradient(135deg,#064e3b,#059669);
               color:white; border-radius:12px; font-weight:700; text-decoration:none;
               font-size:0.88rem; margin-top:8px;">
                🔍 Find Store with {medicine}
            </a>
            """, unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)

        # Emergency numbers
        st.markdown("""
        <div class='glass-box'>
            <div class='section-title'>🚨 Emergency Numbers</div>
            <div style='font-size:0.88rem; line-height:2.4;'>
                <div style='display:flex; justify-content:space-between; padding:8px 12px;
                     background:rgba(239,68,68,0.1); border-radius:10px; margin-bottom:6px;
                     border:1px solid rgba(239,68,68,0.2);'>
                    <span style='color:#d4d0f0;'>🚑 Ambulance</span>
                    <b style='color:#f87171; font-size:1.1rem;'>102</b>
                </div>
                <div style='display:flex; justify-content:space-between; padding:8px 12px;
                     background:rgba(239,68,68,0.1); border-radius:10px; margin-bottom:6px;
                     border:1px solid rgba(239,68,68,0.2);'>
                    <span style='color:#d4d0f0;'>🏥 Emergency</span>
                    <b style='color:#f87171; font-size:1.1rem;'>112</b>
                </div>
                <div style='display:flex; justify-content:space-between; padding:8px 12px;
                     background:rgba(16,185,129,0.1); border-radius:10px;
                     border:1px solid rgba(16,185,129,0.2);'>
                    <span style='color:#d4d0f0;'>💊 Poison Control</span>
                    <b style='color:#6ee7b7; font-size:1.1rem;'>1800-116-117</b>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)

    with col2:
        # Build search query
        q = store_type if store_type != "All Medical Stores" else "medical store pharmacy chemist"
        if night_24hr:
            q += " 24 hours open"
        if open_now:
            q += " open now"

        # Google Maps URLs
        url_nearby = f"https://www.google.com/maps/search/{q.replace(' ', '+')}+near+me"
        url_24hr   = "https://www.google.com/maps/search/24+hour+pharmacy+chemist+open+now+near+me"
        url_all    = "https://www.google.com/maps/search/medical+store+pharmacy+near+me"

        st.markdown("<div class='glass-box'>", unsafe_allow_html=True)
        st.markdown("<div class='section-title'>🗺️ Find Medical Stores</div>", unsafe_allow_html=True)

        st.markdown(f"""
        <div style='display:flex; flex-direction:column; gap:10px; margin-bottom:16px;'>
            <a href="{url_nearby}" target="_blank" style="
                display:block; text-align:center; padding:15px 20px;
                background:linear-gradient(135deg,#064e3b,#065f46,#059669);
                color:white; border-radius:14px; font-weight:700;
                font-size:0.95rem; text-decoration:none;
                border:2px solid rgba(16,185,129,0.3);
                box-shadow:0 4px 20px rgba(5,150,105,0.4);">
                💊 Find — {store_type}
            </a>
            <a href="{url_24hr}" target="_blank" style="
                display:block; text-align:center; padding:15px 20px;
                background:linear-gradient(135deg,#1e1b4b,#3730a3,#4f46e5);
                color:white; border-radius:14px; font-weight:700;
                font-size:0.95rem; text-decoration:none;
                border:2px solid rgba(99,102,241,0.3);
                box-shadow:0 4px 20px rgba(79,70,229,0.4);">
                🌙 Find 24/7 Night Pharmacy
            </a>
            <a href="{url_all}" target="_blank" style="
                display:block; text-align:center; padding:13px 20px;
                background:rgba(245,158,11,0.12);
                color:#fbbf24; border-radius:14px; font-weight:700;
                font-size:0.9rem; text-decoration:none;
                border:1px solid rgba(245,158,11,0.3);">
                🗺️ All Medical Stores on Google Maps
            </a>
        </div>
        """, unsafe_allow_html=True)

        # Embedded map
        st.markdown("<div class='section-title'>🗺️ Store Map</div>", unsafe_allow_html=True)
        map_q   = "medical+store+pharmacy+chemist"
        map_url = f"https://maps.google.com/maps?q={map_q}&output=embed&z=14"
        st.markdown(f"""
        <iframe src="{map_url}" width="100%" height="380"
            style="border:none; border-radius:16px; border:1px solid rgba(16,185,129,0.3);"
            allowfullscreen="" loading="lazy"></iframe>
        <div style='text-align:center; color:#7c74a8; font-size:0.78rem; margin-top:6px;'>
            📍 Click the map to interact · Use buttons above to search near your location
        </div>
        """, unsafe_allow_html=True)

        st.markdown("</div>", unsafe_allow_html=True)

    # ── POPULAR ONLINE MEDICINE STORES ──
    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown("<div class='section-header'>🛒 Order Medicine Online</div>", unsafe_allow_html=True)

    online_stores = {
        "PharmEasy":      ("https://pharmeasy.in",              "🟢", "Fast delivery · Discount 20%"),
        "1mg (Tata)":     ("https://www.1mg.com",               "🔵", "Lab tests + Medicine"),
        "Netmeds":        ("https://www.netmeds.com",           "🟣", "Reliance · Trusted"),
        "Apollo 24|7":    ("https://www.apollo247.com",         "🔴", "Apollo hospital chain"),
        "MedPlus":        ("https://www.medplusmart.com",       "🟠", "Pan India delivery"),
        "Flipkart Health":("https://www.flipkart.com/health",   "🟡", "Flipkart pharmacy"),
    }

    store_cols = st.columns(3)
    for i, (name, (url, dot, desc)) in enumerate(online_stores.items()):
        with store_cols[i % 3]:
            st.markdown(f"""
            <a href="{url}" target="_blank" style="
                display:block; padding:14px 16px; margin-bottom:10px;
                background:rgba(255,255,255,0.04); border:1px solid rgba(255,255,255,0.08);
                border-radius:14px; text-decoration:none;
                transition:all 0.2s; cursor:pointer;">
                <div style='display:flex; align-items:center; gap:10px; margin-bottom:4px;'>
                    <span style='font-size:1.2rem;'>{dot}</span>
                    <span style='color:#f0edff; font-weight:700; font-size:0.92rem;'>{name}</span>
                </div>
                <div style='color:rgba(255,255,255,0.35); font-size:0.75rem; padding-left:30px;'>{desc}</div>
            </a>
            """, unsafe_allow_html=True)

    # ── FIND BY CITY ──
    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown("<div class='section-header'>🏙️ Find by City</div>", unsafe_allow_html=True)

    cities = {
        "Delhi":     "https://www.google.com/maps/search/medical+store+pharmacy+in+Delhi",
        "Mumbai":    "https://www.google.com/maps/search/medical+store+pharmacy+in+Mumbai",
        "Meerut":    "https://www.google.com/maps/search/medical+store+pharmacy+in+Meerut",
        "Lucknow":   "https://www.google.com/maps/search/medical+store+pharmacy+in+Lucknow",
        "Noida":     "https://www.google.com/maps/search/medical+store+pharmacy+in+Noida",
        "Bangalore": "https://www.google.com/maps/search/medical+store+pharmacy+in+Bangalore",
        "Hyderabad": "https://www.google.com/maps/search/medical+store+pharmacy+in+Hyderabad",
        "Chennai":   "https://www.google.com/maps/search/medical+store+pharmacy+in+Chennai",
        "Kolkata":   "https://www.google.com/maps/search/medical+store+pharmacy+in+Kolkata",
        "Pune":      "https://www.google.com/maps/search/medical+store+pharmacy+in+Pune",
        "Jaipur":    "https://www.google.com/maps/search/medical+store+pharmacy+in+Jaipur",
        "Ahmedabad": "https://www.google.com/maps/search/medical+store+pharmacy+in+Ahmedabad",
    }

    city_cols = st.columns(4)
    for i, (city, url) in enumerate(cities.items()):
        with city_cols[i % 4]:
            st.markdown(f"""
            <a href="{url}" target="_blank" style="
                display:block; text-align:center; padding:10px 8px;
                background:rgba(16,185,129,0.08);
                color:#6ee7b7; border-radius:12px; font-weight:600;
                font-size:0.85rem; text-decoration:none; margin-bottom:8px;
                border:1px solid rgba(16,185,129,0.2);">
                💊 {city}
            </a>
            """, unsafe_allow_html=True)

    # Tips
    st.markdown("""
    <div style='display:flex; gap:12px; margin-top:16px; flex-wrap:wrap;'>
        <div style='flex:1; min-width:180px; background:rgba(16,185,129,0.07);
             border:1px solid rgba(16,185,129,0.2); padding:12px 14px;
             border-radius:12px; font-size:0.82rem; color:#6ee7b7;'>
            💡 All buttons open <b>Google Maps</b> in new tab
        </div>
        <div style='flex:1; min-width:180px; background:rgba(124,58,237,0.07);
             border:1px solid rgba(124,58,237,0.2); padding:12px 14px;
             border-radius:12px; font-size:0.82rem; color:#c4b5fd;'>
            🌙 Use 24/7 button for <b>night emergencies</b>
        </div>
        <div style='flex:1; min-width:180px; background:rgba(245,158,11,0.07);
             border:1px solid rgba(245,158,11,0.2); padding:12px 14px;
             border-radius:12px; font-size:0.82rem; color:#fbbf24;'>
            🛒 Order online for <b>home delivery</b>
        </div>
    </div>
    """, unsafe_allow_html=True)