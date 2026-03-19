# ============================================================
# appointments.py — Doctor Appointment with Rich Data
# ============================================================

import pandas as pd
import os
import streamlit as st

APPOINTMENT_FILE = "appointments.csv"
HOSPITAL_NAME = "AI Multispeciality Hospital"
HOSPITAL_ADDRESS = "123 Health Avenue, Medical District"

# ---------- RICH DOCTOR DATA ----------
DOCTOR_DATA = {

    "🦷 Teeth & Mouth": {
        "department": "Dental & Oral Surgery",
        "room": "Block A, Floor 1",
        "treatments": ["Tooth Cavity", "Braces & Alignment", "Root Canal", "Tooth Extraction", "Gum Disease", "Teeth Whitening", "Dental Implants"],
        "doctors": [
            {"name": "Dr. Rahul Sharma", "spec": "Senior Dentist", "exp": 15, "fee": 500, "rating": 4.8, "avail": "Mon, Tue, Wed, Thu, Fri"},
            {"name": "Dr. Priya Singh", "spec": "Orthodontist", "exp": 10, "fee": 700, "rating": 4.9, "avail": "Mon, Wed, Fri"},
            {"name": "Dr. Amit Verma", "spec": "Oral & Maxillofacial Surgeon", "exp": 12, "fee": 900, "rating": 4.7, "avail": "Tue, Thu, Sat"},
            {"name": "Dr. Sneha Patel", "spec": "Pediatric Dentist", "exp": 8, "fee": 450, "rating": 4.6, "avail": "Mon, Tue, Thu, Fri"},
        ]
    },

    "👁️ Eyes": {
        "department": "Ophthalmology",
        "room": "Block B, Floor 2",
        "treatments": ["Eyesight Check", "Cataract Surgery", "Glaucoma Treatment", "Dry Eyes", "Laser Eye Surgery", "Retina Treatment", "Eye Infection"],
        "doctors": [
            {"name": "Dr. Neha Gupta", "spec": "Senior Eye Specialist", "exp": 18, "fee": 600, "rating": 4.9, "avail": "Mon, Tue, Wed, Thu, Fri"},
            {"name": "Dr. Raj Patel", "spec": "Retina Specialist", "exp": 14, "fee": 1000, "rating": 4.8, "avail": "Mon, Wed, Fri"},
            {"name": "Dr. Sana Khan", "spec": "Glaucoma Expert", "exp": 11, "fee": 800, "rating": 4.7, "avail": "Tue, Thu"},
            {"name": "Dr. Vivek Mehta", "spec": "Laser Surgery Specialist", "exp": 9, "fee": 1200, "rating": 4.9, "avail": "Wed, Thu, Sat"},
        ]
    },

    "👂 Ears, Nose & Throat": {
        "department": "ENT (Otolaryngology)",
        "room": "Block A, Floor 3",
        "treatments": ["Ear Infection", "Sinus Treatment", "Tonsil Removal", "Hearing Loss", "Snoring", "Nose Polyps", "Throat Infection", "Voice Disorders"],
        "doctors": [
            {"name": "Dr. Vikram Joshi", "spec": "Senior ENT Specialist", "exp": 20, "fee": 650, "rating": 4.9, "avail": "Mon, Tue, Wed, Thu, Fri"},
            {"name": "Dr. Meera Rao", "spec": "Rhinologist (Nose Specialist)", "exp": 13, "fee": 700, "rating": 4.7, "avail": "Mon, Wed, Fri"},
            {"name": "Dr. Arjun Das", "spec": "Laryngologist (Throat Expert)", "exp": 10, "fee": 600, "rating": 4.6, "avail": "Tue, Thu, Sat"},
            {"name": "Dr. Kavya Iyer", "spec": "Audiologist (Hearing Specialist)", "exp": 7, "fee": 500, "rating": 4.8, "avail": "Mon, Tue, Thu"},
        ]
    },

    "🧠 Brain & Nerves": {
        "department": "Neurology",
        "room": "Block C, Floor 4",
        "treatments": ["Migraine", "Epilepsy", "Memory Loss", "Stroke", "Parkinson's", "Brain Tumor", "Nerve Pain", "Multiple Sclerosis"],
        "doctors": [
            {"name": "Dr. Suresh Kumar", "spec": "Senior Neurologist", "exp": 22, "fee": 1200, "rating": 5.0, "avail": "Mon, Wed, Fri"},
            {"name": "Dr. Anita Mehta", "spec": "Stroke & Brain Specialist", "exp": 16, "fee": 1100, "rating": 4.9, "avail": "Tue, Thu"},
            {"name": "Dr. Ravi Bose", "spec": "Spine & Nerve Expert", "exp": 14, "fee": 1000, "rating": 4.8, "avail": "Mon, Tue, Wed"},
            {"name": "Dr. Pooja Sharma", "spec": "Pediatric Neurologist", "exp": 11, "fee": 900, "rating": 4.7, "avail": "Thu, Fri, Sat"},
        ]
    },

    "❤️ Heart": {
        "department": "Cardiology",
        "room": "Block D, Floor 1 (Emergency Wing)",
        "treatments": ["Chest Pain", "Heart Attack", "High BP", "Heart Failure", "Arrhythmia", "Angioplasty", "Bypass Surgery", "Heart Valve Disease"],
        "doctors": [
            {"name": "Dr. Ajay Malhotra", "spec": "Senior Cardiologist", "exp": 25, "fee": 1500, "rating": 5.0, "avail": "Mon, Tue, Wed, Thu, Fri"},
            {"name": "Dr. Deepa Nair", "spec": "Cardiac Surgeon", "exp": 20, "fee": 2000, "rating": 4.9, "avail": "Mon, Wed, Fri"},
            {"name": "Dr. Rohit Shah", "spec": "Interventional Cardiologist", "exp": 17, "fee": 1800, "rating": 4.8, "avail": "Tue, Thu"},
            {"name": "Dr. Sunita Pillai", "spec": "Heart Failure Specialist", "exp": 13, "fee": 1300, "rating": 4.7, "avail": "Mon, Tue, Thu, Fri"},
        ]
    },

    "🫁 Lungs & Breathing": {
        "department": "Pulmonology",
        "room": "Block B, Floor 3",
        "treatments": ["Asthma", "COVID-19", "Tuberculosis", "Breathlessness", "Lung Infection", "COPD", "Lung Cancer Screening", "Sleep Apnea"],
        "doctors": [
            {"name": "Dr. Kavita Reddy", "spec": "Senior Pulmonologist", "exp": 19, "fee": 900, "rating": 4.9, "avail": "Mon, Tue, Wed, Thu, Fri"},
            {"name": "Dr. Sandeep Tiwari", "spec": "Chest & TB Specialist", "exp": 15, "fee": 800, "rating": 4.7, "avail": "Mon, Wed, Sat"},
            {"name": "Dr. Pooja Jain", "spec": "Asthma & Allergy Expert", "exp": 12, "fee": 750, "rating": 4.8, "avail": "Tue, Thu, Fri"},
            {"name": "Dr. Nikhil Gupta", "spec": "Sleep Medicine Specialist", "exp": 9, "fee": 700, "rating": 4.6, "avail": "Wed, Thu, Sat"},
        ]
    },

    "🦴 Bones & Joints": {
        "department": "Orthopedics",
        "room": "Block C, Floor 2",
        "treatments": ["Fracture", "Arthritis", "Back Pain", "Knee Pain", "Slip Disc", "Joint Replacement", "Sports Injury", "Scoliosis"],
        "doctors": [
            {"name": "Dr. Manoj Yadav", "spec": "Senior Orthopedic Surgeon", "exp": 21, "fee": 1100, "rating": 4.9, "avail": "Mon, Tue, Wed, Thu, Fri"},
            {"name": "Dr. Sunita Pillai", "spec": "Joint Replacement Specialist", "exp": 16, "fee": 1300, "rating": 4.8, "avail": "Mon, Wed, Fri"},
            {"name": "Dr. Kiran Desai", "spec": "Sports Medicine Expert", "exp": 13, "fee": 1000, "rating": 4.7, "avail": "Tue, Thu, Sat"},
            {"name": "Dr. Arun Tiwari", "spec": "Spine Surgeon", "exp": 18, "fee": 1500, "rating": 4.9, "avail": "Mon, Tue, Thu"},
        ]
    },

    "🍽️ Stomach & Digestion": {
        "department": "Gastroenterology",
        "room": "Block A, Floor 2",
        "treatments": ["Acidity & GERD", "IBS", "Liver Disease", "Stomach Ulcer", "Food Poisoning", "Crohn's Disease", "Colonoscopy", "Jaundice"],
        "doctors": [
            {"name": "Dr. Ashok Tripathi", "spec": "Senior Gastroenterologist", "exp": 18, "fee": 950, "rating": 4.8, "avail": "Mon, Tue, Wed, Thu, Fri"},
            {"name": "Dr. Rekha Agarwal", "spec": "Hepatologist (Liver Specialist)", "exp": 14, "fee": 1100, "rating": 4.9, "avail": "Mon, Wed, Fri"},
            {"name": "Dr. Nitin Saxena", "spec": "Endoscopy Specialist", "exp": 11, "fee": 850, "rating": 4.7, "avail": "Tue, Thu"},
            {"name": "Dr. Priti Desai", "spec": "Colorectal Surgeon", "exp": 15, "fee": 1200, "rating": 4.8, "avail": "Wed, Fri, Sat"},
        ]
    },

    "🧒 Children": {
        "department": "Pediatrics",
        "room": "Block E, Floor 1 (Kids Wing)",
        "treatments": ["Fever & Cold", "Vaccination", "Growth Disorders", "Allergies", "Child Nutrition", "Newborn Care", "Childhood Asthma", "Autism"],
        "doctors": [
            {"name": "Dr. Seema Chopra", "spec": "Senior Pediatrician", "exp": 20, "fee": 700, "rating": 5.0, "avail": "Mon, Tue, Wed, Thu, Fri"},
            {"name": "Dr. Alok Sharma", "spec": "Neonatologist (Newborn Expert)", "exp": 15, "fee": 900, "rating": 4.9, "avail": "Mon, Wed, Fri"},
            {"name": "Dr. Nisha Verma", "spec": "Pediatric Nutritionist", "exp": 10, "fee": 600, "rating": 4.7, "avail": "Tue, Thu, Sat"},
            {"name": "Dr. Rohit Kapoor", "spec": "Developmental Pediatrician", "exp": 12, "fee": 800, "rating": 4.8, "avail": "Mon, Tue, Thu"},
        ]
    },

    "👩 Women Health": {
        "department": "Gynecology & Obstetrics",
        "room": "Block F, Floor 2 (Women's Wing)",
        "treatments": ["Pregnancy Care", "PCOD/PCOS", "Menstrual Issues", "Fertility Treatment", "Menopause", "Cervical Cancer Screening", "Laparoscopy", "Normal Delivery"],
        "doctors": [
            {"name": "Dr. Pratibha Singh", "spec": "Senior Gynecologist", "exp": 22, "fee": 800, "rating": 4.9, "avail": "Mon, Tue, Wed, Thu, Fri"},
            {"name": "Dr. Archana Gupta", "spec": "Obstetrician (Pregnancy Expert)", "exp": 17, "fee": 1000, "rating": 4.8, "avail": "Mon, Wed, Fri"},
            {"name": "Dr. Swati Mishra", "spec": "Fertility Specialist", "exp": 14, "fee": 1200, "rating": 4.9, "avail": "Tue, Thu"},
            {"name": "Dr. Kavya Reddy", "spec": "Gynecologic Oncologist", "exp": 16, "fee": 1100, "rating": 4.7, "avail": "Wed, Thu, Sat"},
        ]
    },

    "🧠 Mental Health": {
        "department": "Psychiatry & Psychology",
        "room": "Block G, Floor 3 (Wellness Center)",
        "treatments": ["Depression", "Anxiety", "Stress Management", "OCD", "Bipolar Disorder", "PTSD", "Insomnia", "Addiction Counseling"],
        "doctors": [
            {"name": "Dr. Rajan Mehta", "spec": "Senior Psychiatrist", "exp": 20, "fee": 1000, "rating": 4.9, "avail": "Mon, Tue, Wed, Thu, Fri"},
            {"name": "Dr. Sunita Roy", "spec": "Clinical Psychologist", "exp": 15, "fee": 800, "rating": 4.8, "avail": "Mon, Wed, Fri"},
            {"name": "Dr. Anil Bose", "spec": "Child Psychiatrist", "exp": 12, "fee": 900, "rating": 4.7, "avail": "Tue, Thu, Sat"},
            {"name": "Dr. Meghna Iyer", "spec": "Addiction Specialist", "exp": 10, "fee": 750, "rating": 4.6, "avail": "Wed, Thu"},
        ]
    },

    "🩺 General / Other": {
        "department": "General Medicine",
        "room": "Block A, Floor 1 (OPD)",
        "treatments": ["Fever", "Cold & Flu", "Body Checkup", "Vitamins & Nutrition", "Diabetes", "Thyroid", "Blood Pressure", "General Consultation"],
        "doctors": [
            {"name": "Dr. Ramesh Kumar", "spec": "Senior General Physician", "exp": 25, "fee": 400, "rating": 4.8, "avail": "Mon, Tue, Wed, Thu, Fri"},
            {"name": "Dr. Sunita Joshi", "spec": "Family Medicine Doctor", "exp": 18, "fee": 350, "rating": 4.7, "avail": "Mon, Wed, Fri, Sat"},
            {"name": "Dr. Anil Tiwari", "spec": "Internal Medicine Specialist", "exp": 20, "fee": 500, "rating": 4.9, "avail": "Tue, Thu"},
            {"name": "Dr. Priya Sharma", "spec": "Diabetologist", "exp": 14, "fee": 600, "rating": 4.8, "avail": "Mon, Tue, Thu, Fri"},
        ]
    },

    "🦷 Skin & Hair": {
        "department": "Dermatology",
        "room": "Block B, Floor 1",
        "treatments": ["Acne & Pimples", "Skin Allergy", "Eczema", "Psoriasis", "Hair Fall", "Dandruff", "Vitiligo", "Skin Cancer Screening"],
        "doctors": [
            {"name": "Dr. Divya Kapoor", "spec": "Senior Dermatologist", "exp": 16, "fee": 700, "rating": 4.9, "avail": "Mon, Tue, Wed, Thu, Fri"},
            {"name": "Dr. Sanjay Malhotra", "spec": "Cosmetic Dermatologist", "exp": 12, "fee": 900, "rating": 4.8, "avail": "Mon, Wed, Sat"},
            {"name": "Dr. Ritu Singh", "spec": "Trichologist (Hair Specialist)", "exp": 10, "fee": 600, "rating": 4.7, "avail": "Tue, Thu, Fri"},
            {"name": "Dr. Karan Verma", "spec": "Pediatric Dermatologist", "exp": 8, "fee": 650, "rating": 4.6, "avail": "Wed, Thu, Sat"},
        ]
    },

    "🫀 Kidneys & Urology": {
        "department": "Nephrology & Urology",
        "room": "Block D, Floor 3",
        "treatments": ["Kidney Stones", "UTI", "Kidney Failure", "Dialysis", "Prostate Issues", "Incontinence", "Kidney Transplant", "Renal Diet"],
        "doctors": [
            {"name": "Dr. Vijay Nair", "spec": "Senior Nephrologist", "exp": 19, "fee": 1100, "rating": 4.9, "avail": "Mon, Tue, Wed, Thu, Fri"},
            {"name": "Dr. Ananya Reddy", "spec": "Urologist", "exp": 14, "fee": 1000, "rating": 4.8, "avail": "Mon, Wed, Fri"},
            {"name": "Dr. Sunil Sharma", "spec": "Kidney Transplant Specialist", "exp": 20, "fee": 1500, "rating": 4.9, "avail": "Tue, Thu"},
            {"name": "Dr. Priya Nair", "spec": "Pediatric Nephrologist", "exp": 11, "fee": 900, "rating": 4.7, "avail": "Wed, Thu, Sat"},
        ]
    },
}

# ---------- LOAD APPOINTMENTS ----------
@st.cache_data(ttl=5)
def load_appointments():
    if not os.path.exists(APPOINTMENT_FILE):
        return pd.DataFrame(columns=[
            "ID", "Username", "Patient", "Body Part", "Department",
            "Doctor", "Specialization", "Experience", "Fee",
            "Treatment", "Date", "Time Slot", "Room", "Status"
        ])
    return pd.read_csv(APPOINTMENT_FILE)

# ---------- SAVE APPOINTMENT ----------
def save_appointment(username, patient, body_part, department, doctor_name,
                     doctor_spec, doctor_exp, doctor_fee, treatment,
                     appt_date, time_slot, room):
    df = load_appointments()
    new_id = len(df) + 1
    new_row = {
        "ID": new_id, "Username": username, "Patient": patient,
        "Body Part": body_part, "Department": department,
        "Doctor": doctor_name, "Specialization": doctor_spec,
        "Experience": f"{doctor_exp} yrs", "Fee": f"₹{doctor_fee}",
        "Treatment": treatment, "Date": appt_date,
        "Time Slot": time_slot, "Room": room, "Status": "Booked"
    }
    df = pd.concat([df, pd.DataFrame([new_row])], ignore_index=True)
    df.to_csv(APPOINTMENT_FILE, index=False)
    st.cache_data.clear()
    return new_id

# ---------- CANCEL APPOINTMENT ----------
def cancel_appointment(appt_id):
    df = load_appointments()
    df.loc[df["ID"] == appt_id, "Status"] = "Cancelled"
    df.to_csv(APPOINTMENT_FILE, index=False)
    st.cache_data.clear()

# ---------- RENDER STAR RATING ----------
def render_stars(rating):
    full  = int(rating)
    half  = 1 if (rating - full) >= 0.5 else 0
    empty = 5 - full - half
    return "⭐" * full + "✨" * half + "☆" * empty

# ---------- SHOW APPOINTMENT SECTION ----------
def show_appointment_section(username, user_full_name):
    st.markdown("<div class='section-header'>📅 Specialist Doctor Appointment</div>", unsafe_allow_html=True)

    row1, row2 = st.columns(2)

    with row1:
        st.markdown("<div class='glass-box'>", unsafe_allow_html=True)
        st.markdown("<div class='section-title'>📝 Book Appointment</div>", unsafe_allow_html=True)

        appt_name = st.text_input("👤 Patient Name", value=user_full_name, key="appt_name")

        # Hospital Info
        st.markdown(f"""
        <div style='background:rgba(124,58,237,0.08); border:1px solid rgba(124,58,237,0.2);
             padding:10px 14px; border-radius:12px; margin-bottom:14px; font-size:0.85rem;'>
            🏥 <b style='color:#c4b5fd;'>{HOSPITAL_NAME}</b><br>
            📍 <span style='color:#a89ec9;'>{HOSPITAL_ADDRESS}</span>
        </div>
        """, unsafe_allow_html=True)

        # Step 1
        st.markdown("**Step 1 — Select Body Part / Problem:**")
        body_part = st.selectbox("🏥 Body Part", list(DOCTOR_DATA.keys()))
        dept_info = DOCTOR_DATA[body_part]
        dept      = dept_info["department"]
        room      = dept_info["room"]

        st.markdown(f"""
        <div style='display:flex; gap:10px; margin:8px 0 14px; flex-wrap:wrap;'>
            <span class='dept-badge'>🏨 {dept}</span>
            <span style='background:rgba(16,185,129,0.12); border:1px solid rgba(16,185,129,0.25);
                 color:#6ee7b7; padding:4px 13px; border-radius:20px; font-size:0.78rem; font-weight:600;'>
                📍 {room}
            </span>
        </div>
        """, unsafe_allow_html=True)

        # Step 2
        st.markdown("**Step 2 — Select Treatment:**")
        treatment = st.selectbox("💊 Treatment / Problem", dept_info["treatments"])

        # Step 3 — Show Doctors
        st.markdown("**Step 3 — Select Doctor:**")
        doctors = dept_info["doctors"]

        for doc in doctors:
            stars = render_stars(doc["rating"])
            st.markdown(f"""
            <div class='doctor-info-card' style='padding:12px 14px;'>
                <div style='display:flex; justify-content:space-between; align-items:flex-start;'>
                    <div>
                        <div style='font-weight:700; color:#6ee7b7; font-size:0.92rem;'>👨‍⚕️ {doc["name"]}</div>
                        <div style='color:#a89ec9; font-size:0.8rem; margin-top:2px;'>{doc["spec"]}</div>
                    </div>
                    <div style='text-align:right;'>
                        <div style='color:#fbbf24; font-size:0.82rem;'>{stars} {doc["rating"]}</div>
                        <div style='color:#c4b5fd; font-size:0.8rem; font-weight:700;'>₹{doc["fee"]}</div>
                    </div>
                </div>
                <div style='display:flex; gap:15px; margin-top:8px; font-size:0.78rem; color:#7c74a8;'>
                    <span>🎓 {doc["exp"]} yrs exp</span>
                    <span>📅 {doc["avail"]}</span>
                </div>
            </div>
            """, unsafe_allow_html=True)

        doctor_names = [f"{d['name']} ({d['spec']})" for d in doctors]
        selected_doctor_full = st.selectbox("Choose Doctor", doctor_names)
        selected_idx    = doctor_names.index(selected_doctor_full)
        selected_doctor = doctors[selected_idx]

        # Step 4
        st.markdown("**Step 4 — Select Date & Time:**")
        appt_date = st.date_input("📅 Date", min_value=__import__('datetime').date.today())
        time_slot = st.selectbox("⏰ Time Slot", [
            "🌅 Morning   (9:00 AM - 12:00 PM)",
            "☀️ Afternoon (12:00 PM - 4:00 PM)",
            "🌆 Evening   (4:00 PM - 8:00 PM)"
        ])

        if st.button("✅ Book Appointment", use_container_width=True):
            if appt_name:
                appt_id = save_appointment(
                    username, appt_name, body_part, dept,
                    selected_doctor["name"], selected_doctor["spec"],
                    selected_doctor["exp"], selected_doctor["fee"],
                    treatment, appt_date, time_slot, room
                )
                st.success("✅ Appointment Booked Successfully!")
                st.info(f"📋 Your Appointment ID: **{appt_id}**")
                st.markdown(f"""
                <div class='body-part-card'>
                    🏥 <b>Hospital:</b> {HOSPITAL_NAME}<br>
                    📍 <b>Room:</b> {room}<br>
                    👤 <b>Patient:</b> {appt_name}<br>
                    🏨 <b>Department:</b> {dept}<br>
                    👨‍⚕️ <b>Doctor:</b> {selected_doctor["name"]}<br>
                    🎓 <b>Specialization:</b> {selected_doctor["spec"]}<br>
                    💰 <b>Consultation Fee:</b> ₹{selected_doctor["fee"]}<br>
                    💊 <b>Treatment:</b> {treatment}<br>
                    📅 <b>Date:</b> {appt_date}<br>
                    ⏰ <b>Time:</b> {time_slot}
                </div>
                """, unsafe_allow_html=True)
                st.balloons()
            else:
                st.error("⚠ Please enter patient name!")

        st.markdown("</div>", unsafe_allow_html=True)

    with row2:
        st.markdown("<div class='glass-box'>", unsafe_allow_html=True)
        st.markdown("<div class='section-title'>📋 My Appointments</div>", unsafe_allow_html=True)

        df_appts = load_appointments()
        if not df_appts.empty and "Username" in df_appts.columns:
            df_appts = df_appts[df_appts["Username"] == username]

        if st.button("🔄 Refresh", use_container_width=False):
            st.rerun()

        if not df_appts.empty:
            for _, row in df_appts.iterrows():
                card_class  = "cancelled" if row["Status"] == "Cancelled" else "appt-card"
                status_icon = "❌" if row["Status"] == "Cancelled" else "✅"
                fee_str  = row.get("Fee", "N/A")
                room_str = row.get("Room", "N/A")
                spec_str = row.get("Specialization", "")
                exp_str  = row.get("Experience", "")

                st.markdown(f"""
                <div class='{card_class}'>
                    <div style='display:flex; justify-content:space-between; align-items:center; margin-bottom:8px;'>
                        <span style='font-weight:800; font-size:0.95rem;'>{status_icon} ID: {row['ID']}</span>
                        <span style='background:rgba(251,191,36,0.15); color:#fbbf24; padding:3px 10px;
                             border-radius:20px; font-size:0.75rem; font-weight:700;'>{fee_str}</span>
                    </div>
                    👤 <b>Patient:</b> {row['Patient']}<br>
                    🏥 <b>Body Part:</b> {row['Body Part']}<br>
                    🏨 <b>Department:</b> {row['Department']}<br>
                    👨‍⚕️ <b>Doctor:</b> {row['Doctor']} <span style='color:#a89ec9; font-size:0.8rem;'>— {spec_str}</span><br>
                    🎓 <b>Experience:</b> {exp_str}<br>
                    💊 <b>Treatment:</b> {row['Treatment']}<br>
                    📍 <b>Room:</b> {room_str}<br>
                    📅 <b>Date:</b> {row['Date']} &nbsp;|&nbsp; ⏰ {row['Time Slot']}<br>
                    <span style='font-size:0.78rem; opacity:0.6; margin-top:4px; display:block;'>Status: {row['Status']}</span>
                </div>
                """, unsafe_allow_html=True)

            st.markdown("<br>**❌ Cancel Appointment:**")
            cancel_id = st.number_input("Enter Appointment ID", min_value=1, step=1)
            if st.button("🚫 Cancel Appointment", use_container_width=True):
                cancel_appointment(int(cancel_id))
                st.success(f"✅ Appointment {cancel_id} cancelled!")
                st.rerun()
        else:
            st.markdown("""
            <div style='text-align:center; padding:60px 20px; color:#475569;'>
                <div style='font-size:4rem; margin-bottom:15px;'>📅</div>
                <p style='font-size:1rem; font-weight:500;'>No appointments yet</p>
                <p style='font-size:0.85rem;'>Book your first appointment on the left</p>
            </div>
            """, unsafe_allow_html=True)

        st.markdown("</div>", unsafe_allow_html=True)