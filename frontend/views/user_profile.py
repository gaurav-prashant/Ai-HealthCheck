# ============================================================
# user_profile.py — User Health Profile Page
# ============================================================

import streamlit as st
from backend.services.auth import supabase

BLOOD_GROUPS = ["A+", "A-", "B+", "B-", "AB+", "AB-", "O+", "O-", "Unknown"]
GENDERS = ["Male", "Female", "Other", "Prefer not to say"]

# ---------- SUPABASE HELPERS ----------
def get_profile(email: str) -> dict:
    """Load the user's health profile from Supabase profiles table."""
    if not supabase:
        return {}
    try:
        res = supabase.table("profiles").select("*").eq("email", email).single().execute()
        return res.data or {}
    except Exception:
        return {}

def save_profile(email: str, data: dict) -> tuple[bool, str]:
    """Upsert (update or insert) profile data in Supabase."""
    if not supabase:
        return False, "Supabase not connected."
    try:
        # Get the user's UUID from auth session
        session = supabase.auth.get_session()
        if not session or not session.user:
            return False, "Not logged in."
        uid = session.user.id
        payload = {"id": uid, "email": email, **data}
        supabase.table("profiles").upsert(payload).execute()
        return True, "Profile saved successfully!"
    except Exception as e:
        return False, f"Error saving profile: {str(e)}"

# ---------- PROFILE PAGE UI ----------
def show_profile_page(username: str, name: str):
    """Render the full User Profile page."""

    # Load existing profile
    profile = get_profile(username)

    st.markdown("""
    <div style='background: linear-gradient(135deg, rgba(0,242,254,0.08), rgba(79,172,254,0.05));
                border: 1px solid rgba(0,242,254,0.15); border-radius: 20px;
                padding: 28px; margin-bottom: 28px;'>
        <div style='font-size:2rem; font-weight:900; background: linear-gradient(90deg, #00f2fe, #4facfe);
                    -webkit-background-clip: text; -webkit-text-fill-color: transparent;'>
            👤 Health Profile
        </div>
        <div style='color:#94a3b8; font-size:0.9rem; margin-top:4px;'>
            Your personal health card — used to personalize AI advice
        </div>
    </div>
    """, unsafe_allow_html=True)

    # ── IDENTITY SECTION ──
    st.markdown("### 🪪 Identity")
    id_col1, id_col2, id_col3 = st.columns(3)
    with id_col1:
        st.text_input("👤 Full Name", value=name, disabled=True, help="To change name, contact support")
    with id_col2:
        age = st.number_input("🎂 Age", min_value=1, max_value=120,
                              value=int(profile.get("age") or 25), step=1)
    with id_col3:
        gender = st.selectbox("⚧ Gender", GENDERS,
                              index=GENDERS.index(profile.get("gender", "Male"))
                              if profile.get("gender") in GENDERS else 0)

    st.markdown("<br>", unsafe_allow_html=True)

    # ── HEALTH INFO SECTION ──
    st.markdown("### 🏥 Health Information")
    h1, h2, h3 = st.columns(3)
    with h1:
        blood_group = st.selectbox("🩸 Blood Group", BLOOD_GROUPS,
                                   index=BLOOD_GROUPS.index(profile.get("blood_group", "Unknown"))
                                   if profile.get("blood_group") in BLOOD_GROUPS else 8)
    with h2:
        weight_kg = st.number_input("⚖️ Weight (kg)", min_value=10.0, max_value=300.0,
                                    value=float(profile.get("weight_kg") or 70.0), step=0.5)
    with h3:
        height_cm = st.number_input("📏 Height (cm)", min_value=50.0, max_value=250.0,
                                    value=float(profile.get("height_cm") or 170.0), step=0.5)

    # Calculate and show BMI preview
    if height_cm > 0:
        bmi_val = round(weight_kg / ((height_cm / 100) ** 2), 1)
        bmi_cat = (
            "Underweight 🔵" if bmi_val < 18.5 else
            "Normal ✅"      if bmi_val < 25 else
            "Overweight 🟡"  if bmi_val < 30 else
            "Obese 🔴"
        )
        st.markdown(f"""
        <div style='background:rgba(0,242,254,0.04); border:1px solid rgba(0,242,254,0.1);
                    border-radius:10px; padding:12px; margin:10px 0; display:inline-block;'>
            📊 <b>BMI:</b> {bmi_val} — <span style='color:#00f2fe;'>{bmi_cat}</span>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)
    a1, a2 = st.columns(2)
    with a1:
        allergies = st.text_area("⚠️ Known Allergies",
                                 value=profile.get("allergies") or "",
                                 placeholder="e.g. Penicillin, Peanuts, Dust...",
                                 height=100)
    with a2:
        medical_conditions = st.text_area("🩺 Existing Medical Conditions",
                                          value=profile.get("medical_conditions") or "",
                                          placeholder="e.g. Diabetes Type 2, Hypertension...",
                                          height=100)

    st.markdown("<br>", unsafe_allow_html=True)

    # ── EMERGENCY SECTION ──
    st.markdown("### 🆘 Emergency Contact")
    e1, e2 = st.columns(2)
    with e1:
        emergency_name = st.text_input("👥 Contact Name",
                                       value=profile.get("emergency_name") or "",
                                       placeholder="e.g. Rahul Sharma")
    with e2:
        emergency_phone = st.text_input("📞 Contact Phone",
                                        value=profile.get("emergency_contact") or "",
                                        placeholder="e.g. +91 98765 43210")

    st.markdown("<br>", unsafe_allow_html=True)

    # ── SAVE BUTTON ──
    if st.button("💾 SAVE PROFILE", use_container_width=True, type="primary"):
        data = {
            "age": age,
            "gender": gender,
            "blood_group": blood_group,
            "weight_kg": weight_kg,
            "height_cm": height_cm,
            "allergies": allergies,
            "medical_conditions": medical_conditions,
            "emergency_name": emergency_name,
            "emergency_contact": emergency_phone,
            "name": name,
            "username": username,
        }
        ok, msg = save_profile(username, data)
        if ok:
            st.success(f"✅ {msg}")
            st.balloons()
        else:
            st.error(f"❌ {msg}")

    # ── PROFILE CARD PREVIEW ──
    if profile:
        st.markdown("<br>", unsafe_allow_html=True)
        st.markdown("### 🪪 Your Health Card")
        st.markdown(f"""
        <div style='background:rgba(255,255,255,0.03); border:1px solid rgba(0,242,254,0.2);
                    border-radius:16px; padding:24px;'>
            <div style='display:flex; justify-content:space-between; align-items:center; margin-bottom:16px;'>
                <div>
                    <div style='font-size:1.4rem; font-weight:800; color:#00f2fe;'>{name}</div>
                    <div style='color:#94a3b8; font-size:0.85rem;'>{username}</div>
                </div>
                <div style='background:rgba(0,242,254,0.1); border:1px solid rgba(0,242,254,0.3);
                            border-radius:8px; padding:8px 16px; text-align:center;'>
                    <div style='font-size:0.7rem; color:#94a3b8;'>BLOOD</div>
                    <div style='font-size:1.2rem; font-weight:800; color:#ff4b4b;'>
                        {profile.get("blood_group", "??")}
                    </div>
                </div>
            </div>
            <div style='display:grid; grid-template-columns:1fr 1fr 1fr; gap:12px;'>
                <div><div style='font-size:0.7rem;color:#94a3b8;'>AGE</div>
                    <div style='font-weight:600;'>{profile.get("age", "N/A")} yrs</div></div>
                <div><div style='font-size:0.7rem;color:#94a3b8;'>GENDER</div>
                    <div style='font-weight:600;'>{profile.get("gender", "N/A")}</div></div>
                <div><div style='font-size:0.7rem;color:#94a3b8;'>BMI</div>
                    <div style='font-weight:600;'>{round(float(profile.get("weight_kg") or 70) / ((float(profile.get("height_cm") or 170) / 100)**2), 1)}</div></div>
            </div>
            {'<div style="margin-top:12px;"><div style="font-size:0.7rem;color:#94a3b8;">ALLERGIES</div><div style="font-weight:600;color:#fbbf24;">' + profile.get("allergies","None") + '</div></div>' if profile.get("allergies") else ''}
            {'<div style="margin-top:8px;"><div style="font-size:0.7rem;color:#94a3b8;">CONDITIONS</div><div style="font-weight:600;color:#f87171;">' + profile.get("medical_conditions","None") + '</div></div>' if profile.get("medical_conditions") else ''}
            {'<div style="margin-top:8px;"><div style="font-size:0.7rem;color:#94a3b8;">EMERGENCY CONTACT</div><div style="font-weight:600;">' + profile.get("emergency_contact","Not set") + '</div></div>' if profile.get("emergency_contact") else ''}
        </div>
        """, unsafe_allow_html=True)
