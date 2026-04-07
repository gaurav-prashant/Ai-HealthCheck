# ============================================================
# medicine_reminder.py — Upgraded Medicine Reminder
# All Features: Stock, Dose Log, Missed Alert, AI Info, Refill
# ============================================================

import streamlit as st
import streamlit.components.v1 as components
from datetime import datetime, date
from groq import Groq
import os
from dotenv import load_dotenv
load_dotenv(r"C:\AI_Health\.env")

groq_client = Groq(api_key=os.getenv("GROQ_API_KEY"))

# ── AI Medicine Info ──
def get_medicine_info(name):
    try:
        resp = groq_client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[{"role": "user", "content": f"""Give brief info about medicine: {name}
Format exactly like this (no extra text):
USE: [what it treats in 1 line]
DOSE: [typical dose]
SIDE EFFECTS: [top 3 side effects]
PRECAUTIONS: [top 2 precautions]
FOOD: [take before/after food]"""}],
            max_tokens=200, temperature=0.3
        )
        return resp.choices[0].message.content
    except:
        return None

def get_smart_intake_advice(name):
    try:
        resp = groq_client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[{"role": "user", "content": f"""Provide professional intake advice for {name}. 
Focus on: 
1. Before/After food. 
2. Things to avoid (e.g. alcohol, dairy). 
Max 2 short sentences. No extra text."""}],
            max_tokens=100, temperature=0.3
        )
        return resp.choices[0].message.content
    except:
        return "Take as directed by your physician."

def show_medicine_reminder():
    st.markdown("""
        <div class="section-header">
            <img src="https://img.icons8.com/fluency/96/clock.png" width="50" style="margin-bottom: 10px;">
            <br>
            💊 Medicine Reminder
        </div>
    """, unsafe_allow_html=True)

    # ── SESSION STATE INIT ──
    if "reminders"   not in st.session_state: st.session_state.reminders   = []
    if "dose_log"    not in st.session_state: st.session_state.dose_log    = []
    if "med_info"    not in st.session_state: st.session_state.med_info    = {}

    # ── TABS ──
    tab1, tab2 = st.tabs([
        "💊 Reminders", "💡 Smart Intake Guide"
    ])

    # ════════════════════════════════
    # TAB 1 — REMINDERS
    # ════════════════════════════════
    with tab1:
        col1, col2 = st.columns([1, 2])

        with col1:
            st.markdown("<div class='glass-box'>", unsafe_allow_html=True)
            st.markdown("<div class='section-title'>➕ Add Medicine</div>", unsafe_allow_html=True)

            med_name  = st.text_input("💊 Medicine Name",  placeholder="e.g. Paracetamol")
            
            med_dose  = st.text_input("📏 Dose",           placeholder="e.g. 500mg, 1 tablet")

            tc1, tc2, tc3 = st.columns([1, 1, 1])
            with tc1:
                current_hour_24 = datetime.now().hour
                current_hour_12 = current_hour_24 % 12
                if current_hour_12 == 0: current_hour_12 = 12
                med_hour = st.selectbox("⏰ Hour", [f"{h:02d}" for h in range(1, 13)],
                    index=current_hour_12 - 1)
            with tc2:
                med_min  = st.selectbox("🕐 Minute", [f"{m:02d}" for m in range(60)],
                    index=datetime.now().minute)
            with tc3:
                current_ampm = "PM" if current_hour_24 >= 12 else "AM"
                med_ampm = st.selectbox("☀️/🌙", ["AM", "PM"], index=0 if current_ampm == "AM" else 1)

            # Convert to 24-hour for internal storage
            h24 = int(med_hour)
            if med_ampm == "PM" and h24 < 12: h24 += 12
            if med_ampm == "AM" and h24 == 12: h24 = 0
            med_time_str = f"{h24:02d}:{med_min}"
            med_freq  = st.selectbox("🔁 Frequency", [
                "Once Daily", "Twice Daily", "Three Times Daily",
                "Every 6 Hours", "Every 8 Hours", "As Needed"
            ])
            
            med_duration = st.selectbox("📅 Duration", [
                "7 Days", "14 Days", "30 Days (One Month)", 
                "60 Days", "90 Days", "Ongoing (Chronic)"
            ])
            
            med_note  = st.text_input("📝 Note",           placeholder="e.g. After food")

            if st.button("➕ Add Medicine", use_container_width=True):
                if med_name.strip():
                    # Fetch Smart Intake Advice
                    with st.spinner(f"🧠 AI analyzing intake for {med_name}..."):
                        intake_advice = get_smart_intake_advice(med_name)

                    # Calculate End Date
                    days = 9999
                    if "7" in med_duration:   days = 7
                    elif "14" in med_duration: days = 14
                    elif "30" in med_duration: days = 30
                    elif "60" in med_duration: days = 60
                    elif "90" in med_duration: days = 90
                    
                    start_dt = datetime.now()
                    
                    st.session_state.reminders.append({
                        "name":        med_name.strip(),
                        "dose":        med_dose.strip() or "1 tablet",
                        "time":        med_time_str,
                        "freq":        med_freq,
                        "duration":    med_duration,
                        "start_date":  start_dt.strftime("%Y-%m-%d"),
                        "days_total":  days,
                        "note":        med_note.strip(),
                        "intake":      intake_advice,
                        "taken":       False,
                        "missed":      False,
                        "added":       start_dt.strftime("%Y-%m-%d %H:%M"),
                    })
                    st.success(f"✅ {med_name} added!")
                    st.rerun()
                else:
                    st.warning("⚠️ Enter medicine name!")
            st.markdown("</div>", unsafe_allow_html=True)

            # Summary
            total   = len(st.session_state.reminders)
            taken   = sum(1 for r in st.session_state.reminders if r["taken"])
            missed  = sum(1 for r in st.session_state.reminders if r.get("missed"))
            pending = total - taken

            st.markdown(f"""
            <div class='glass-box'>
                <div class='section-title'>📊 Today's Summary</div>
                <div style='display:grid; grid-template-columns:1fr 1fr; gap:8px; margin-top:8px;'>
                    <div style='text-align:center; background:rgba(99,102,241,0.1);
                         border:1px solid rgba(99,102,241,0.25); border-radius:12px; padding:10px;'>
                        <div style='font-size:1.6rem; font-weight:900; color:#818cf8;'>{total}</div>
                        <div style='font-size:0.72rem; color:#a89ec9;'>Total</div>
                    </div>
                    <div style='text-align:center; background:rgba(16,185,129,0.1);
                         border:1px solid rgba(16,185,129,0.25); border-radius:12px; padding:10px;'>
                        <div style='font-size:1.6rem; font-weight:900; color:#34d399;'>{taken}</div>
                        <div style='font-size:0.72rem; color:#a89ec9;'>Taken</div>
                    </div>
                    <div style='text-align:center; background:rgba(245,158,11,0.1);
                         border:1px solid rgba(245,158,11,0.25); border-radius:12px; padding:10px;'>
                        <div style='font-size:1.6rem; font-weight:900; color:#fbbf24;'>{pending}</div>
                        <div style='font-size:0.72rem; color:#a89ec9;'>Pending</div>
                    </div>
                    <div style='text-align:center; background:rgba(239,68,68,0.1);
                         border:1px solid rgba(239,68,68,0.25); border-radius:12px; padding:10px;'>
                        <div style='font-size:1.6rem; font-weight:900; color:#f87171;'>{missed}</div>
                        <div style='font-size:0.72rem; color:#a89ec9;'>Missed</div>
                    </div>
                </div>
            </div>
            """, unsafe_allow_html=True)

        with col2:
            st.markdown("<div class='section-title'>⏰ Active Reminders</div>", unsafe_allow_html=True)

            if not st.session_state.reminders:
                st.markdown("""
                <div style='text-align:center; padding:60px 20px;
                     background:rgba(255,255,255,0.02); border-radius:16px;
                     border:1px dashed rgba(255,255,255,0.08);'>
                    <div style='font-size:4rem; margin-bottom:16px;'>💊</div>
                    <p style='color:#6b7280;'>No reminders yet. Add medicines on the left.</p>
                </div>
                """, unsafe_allow_html=True)
            else:
                today_str = str(date.today())
                for i, r in enumerate(st.session_state.reminders):
                    # Safety defaults for legacy data
                    s_date = r.get("start_date", r.get("added", datetime.now().strftime("%Y-%m-%d")))[:10]
                    d_total = r.get("days_total", 9999)

                    # Calculate Days Remaining
                    try:
                        dt_start = datetime.strptime(s_date, "%Y-%m-%d")
                        days_passed = (datetime.now() - dt_start).days
                    except:
                        days_passed = 0
                        
                    days_left   = max(0, d_total - days_passed)
                    is_expired  = days_left <= 0 and d_total < 5000
                    
                    progress = 0
                    if d_total < 5000:
                        progress = min(100, int((days_passed / d_total) * 100))

                    # Card color
                    if is_expired:
                        bg, border = "rgba(107,114,128,0.1)",  "rgba(107,114,128,0.3)"
                        badge, bc  = "🏁 Finished",           "#9ca3af"
                    elif r["taken"]:
                        bg, border = "rgba(16,185,129,0.08)",  "rgba(16,185,129,0.25)"
                        badge, bc  = "✅ Taken",               "#34d399"
                    elif r.get("missed"):
                        bg, border = "rgba(239,68,68,0.08)",   "rgba(239,68,68,0.25)"
                        badge, bc  = "❌ Missed",              "#f87171"
                    else:
                        bg, border = "rgba(99,102,241,0.08)",  "rgba(99,102,241,0.2)"
                        badge, bc  = "⏳ Pending",             "#fbbf24"

                    st.markdown(f"""
                    <div style='background:{bg}; border:1px solid {border};
                         border-radius:16px; padding:14px 16px; margin-bottom:10px;'>
                        <div style='display:flex; justify-content:space-between; align-items:flex-start;'>
                            <div>
                                <div style='font-size:1rem; font-weight:700; color:#f0edff;'>
                                    💊 {r["name"]}
                                </div>
                                <div style='font-size:0.8rem; color:#a89ec9; margin-top:3px;'>
                                    📏 {r["dose"]} &nbsp;·&nbsp; ⏰ {datetime.strptime(r["time"], "%H:%M").strftime("%I:%M %p")} &nbsp;·&nbsp; 🔁 {r["freq"]}
                                    {"&nbsp;·&nbsp; 📝 " + r["note"] if r["note"] else ""}
                                </div>
                                {f'''<div style='margin-top:6px; font-size:0.75rem; color:#818cf8; font-weight:600;'>
                                    📅 {days_left} Days Remaining ({progress}% Complete)
                                </div>
                                <div style='width:100%; height:4px; background:rgba(255,255,255,0.05); border-radius:2px; margin-top:4px;'>
                                    <div style='width:{progress}%; height:100%; background:linear-gradient(90deg, #818cf8, #c4b5fd); border-radius:2px;'></div>
                                </div>''' if r["days_total"] < 5000 else "<div style='margin-top:6px; font-size:0.75rem; color:#34d399;'>🔄 Ongoing Treatment</div>"}
                            </div>
                            <span style='background:rgba(0,0,0,0.2); color:{bc};
                                 padding:4px 10px; border-radius:20px; font-size:0.75rem;
                                 font-weight:700; white-space:nowrap; margin-left:8px;'>
                                {badge}
                            </span>
                        </div>
                        {f'''<div style='margin-top:10px; padding:8px 12px; background:rgba(129,140,248,0.1); border:1px solid rgba(129,140,248,0.2); border-radius:10px; font-size:0.8rem; color:#c4b5fd;'>
                            <span style='font-weight:700; color:#818cf8;'>🧠 AI INTAKE GUIDE:</span> {r["intake"]}
                        </div>''' if r.get("intake") else ""}
                    </div>
                    """, unsafe_allow_html=True)

                    bc1, bc2, bc3, bc4 = st.columns([2, 2, 1, 1])
                    with bc1:
                        label = "✅ Mark Taken" if not r["taken"] else "↩️ Undo Taken"
                        if st.button(label, key=f"take_{i}", use_container_width=True):
                            was_taken = st.session_state.reminders[i]["taken"]
                            st.session_state.reminders[i]["taken"]  = not was_taken
                            st.session_state.reminders[i]["missed"] = False
                            if not was_taken:
                                st.toast(f"✅ Dose taken: {r['name']}")
                            st.rerun()
                    with bc2:
                        if st.button("🔔 Test Alarm", key=f"alarm_{i}", use_container_width=True):
                            st.session_state[f"play_alarm_{i}"] = True
                            st.rerun()
                    with bc3:
                        if st.button("❌ Miss", key=f"miss_{i}", use_container_width=True):
                            st.session_state.reminders[i]["missed"] = True
                            st.session_state.reminders[i]["taken"]  = False
                            st.rerun()
                    with bc4:
                        if st.button("🗑️", key=f"del_{i}", use_container_width=True):
                            st.session_state.reminders.pop(i)
                            st.rerun()

                    # Play alarm
                    if st.session_state.get(f"play_alarm_{i}"):
                        components.html(f"""
                        <script>
                        (function() {{
                            var ctx = new (window.AudioContext || window.webkitAudioContext)();
                            function beep(start, freq, dur) {{
                                var osc  = ctx.createOscillator();
                                var gain = ctx.createGain();
                                osc.type = 'square';
                                osc.frequency.setValueAtTime(freq, start);
                                gain.gain.setValueAtTime(0, start);
                                gain.gain.linearRampToValueAtTime(0.7, start + 0.02);
                                gain.gain.exponentialRampToValueAtTime(0.01, start + dur);
                                osc.connect(gain); gain.connect(ctx.destination);
                                osc.start(start); osc.stop(start + dur);
                            }}
                            var t = ctx.currentTime;
                            beep(t,        880,  0.15);
                            beep(t + 0.22, 880,  0.15);
                            beep(t + 0.44, 1047, 0.30);
                            var u = new SpeechSynthesisUtterance('Medicine reminder. Time to take {r["name"]}. Dose: {r["dose"]}.');
                            u.lang='en-US'; u.rate=0.9; u.volume=1;
                            setTimeout(function(){{window.speechSynthesis.speak(u);}}, 1000);
                        }})();
                        </script>
                        """, height=0)
                        st.session_state[f"play_alarm_{i}"] = False

            if st.session_state.reminders:
                st.markdown("<br>", unsafe_allow_html=True)
                rc1, rc2 = st.columns(2)
                with rc1:
                    if st.button("✅ Mark All Taken", use_container_width=True):
                        for i, r in enumerate(st.session_state.reminders):
                            if not r["taken"]:
                                st.session_state.reminders[i]["taken"] = True
                        st.rerun()
                with rc2:
                    if st.button("🗑️ Clear All", use_container_width=True):
                        st.session_state.reminders = []
                        st.rerun()

            # Live clock
            st.markdown("<br>", unsafe_allow_html=True)
            st.markdown("<div class='section-title'>🕐 Live Clock & Auto Alert</div>", unsafe_allow_html=True)

            rem_js_list = []
            for r in st.session_state.reminders:
                if not r["taken"]:
                    name = r["name"].replace("'", "\\'").replace('"', '\\"')
                    dose = r["dose"].replace("'", "\\'").replace('"', '\\"')
                    rem_js_list.append(f'{{"name":"{name}","dose":"{dose}","time":"{r["time"]}"}}'  )
            rem_js_str = "[" + ",".join(rem_js_list) + "]"

            components.html(f"""
            <!DOCTYPE html>
            <html>
            <head>
            <style>
                body {{ margin:0; background:transparent; font-family:Arial,sans-serif; }}
                @keyframes pulse {{ 0%,100%{{opacity:1}} 50%{{opacity:0.4}} }}
                @keyframes ring  {{ 0%{{transform:rotate(-15deg)}} 50%{{transform:rotate(15deg)}} 100%{{transform:rotate(-15deg)}} }}
                @keyframes bgFlash {{ 0%, 100% {{ background: rgba(239, 68, 68, 0.2); }} 50% {{ background: rgba(239, 68, 68, 0.5); }} }}
            </style>
            </head>
            <body>
            <div style="text-align:center; padding:16px;">

                <div id="clock" style="font-size:3rem; font-weight:900; color:#a78bfa;
                     letter-spacing:4px; margin-bottom:4px; font-family:'Arial Black',Arial;">
                    --:--:-- --
                </div>
                <div id="dateStr" style="color:#7c74a8; font-size:0.85rem; margin-bottom:14px;"></div>

                <div id="nextDose" style="background:rgba(124,58,237,0.15);
                     border:1px solid rgba(124,58,237,0.3); border-radius:14px;
                     padding:12px 16px; font-size:0.9rem; color:#d4d0f0; margin-bottom:12px;">
                    ⏳ Loading reminders...
                </div>

                <div id="alarmBox" style="display:none; border:3px solid #f87171; border-radius:16px; padding:20px;
                     animation:pulse 0.8s infinite, bgFlash 0.5s infinite; margin-bottom:10px;">
                    <div style="font-size:2.5rem; animation:ring 0.3s infinite;">🚨</div>
                    <div style="font-size:1.5rem; font-weight:900; color:#f87171; margin:8px 0;">
                        TIME FOR YOUR MEDICINE!
                    </div>
                    <div id="alarmMsg" style="color:#ffffff; font-size:1.1rem; font-weight:bold; background:rgba(0,0,0,0.3); padding:10px; border-radius:8px;"></div>
                    <button onclick="dismissAlarm()" style="margin-top:15px;
                        background:#f87171; border:none;
                        color:white; padding:12px 30px; border-radius:10px;
                        cursor:pointer; font-weight:900; font-size:1.1rem; box-shadow: 0 4px 15px rgba(248,113,113,0.4);">
                        ✅ I HAVE TAKEN IT
                    </button>
                    <div style="margin-top:10px; font-size:0.8rem; color:#fca5a5;">(Alarm will auto-stop in 2 minutes)</div>
                </div>

            </div>

            <script>
            var reminders = {rem_js_str};
            var firedByMinute = {{}}; // Track which alarms fired for each minute to prevent duplicates
            var alarmActive = false;
            var audioCtx = null;
            var sirenInterval = null;

            function pad(n) {{ return n < 10 ? '0' + n : '' + n; }}

            function format12(h, m, s) {{
                var ampm = h >= 12 ? 'PM' : 'AM';
                h = h % 12;
                h = h ? h : 12;
                return pad(h) + ':' + pad(m) + ':' + pad(s) + ' ' + ampm;
            }}

            function tick() {{
                var now  = new Date();
                var hh   = now.getHours();
                var mm   = now.getMinutes();
                var ss   = now.getSeconds();
                var days = ['Sunday','Monday','Tuesday','Wednesday','Thursday','Friday','Saturday'];
                var mons = ['Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec'];

                document.getElementById('clock').innerText = format12(hh, mm, ss);
                document.getElementById('dateStr').innerText =
                    days[now.getDay()] + ', ' + now.getDate() + ' ' +
                    mons[now.getMonth()] + ' ' + now.getFullYear();

                var curTime24 = pad(hh) + ':' + pad(mm);
                var nextFound = false;

                for (var i = 0; i < reminders.length; i++) {{
                    var r = reminders[i];
                    var minuteKey = curTime24 + '|' + r.name;

                    // Trigger alarm if time matches and it hasn't fired in THIS specific minute yet
                    if (r.time === curTime24 && !firedByMinute[minuteKey]) {{
                        firedByMinute[minuteKey] = true;
                        fireAlarm(r);
                    }}

                    // Show next upcoming dose
                    if (!nextFound && r.time > curTime24) {{
                        var parts   = r.time.split(':');
                        var rDate   = new Date();
                        rDate.setHours(parseInt(parts[0]), parseInt(parts[1]), 0, 0);
                        var diffMs  = rDate - now;
                        var diffMin = Math.floor(diffMs / 60000);
                        var diffHr  = Math.floor(diffMin / 60);
                        var remMin  = diffMin % 60;

                        var timeLeft = diffHr > 0
                            ? diffHr + 'h ' + remMin + 'min'
                            : diffMin + ' min';

                        // Format r.time for display
                        var rParts = r.time.split(':');
                        var rh = parseInt(rParts[0]);
                        var rampm = rh >= 12 ? 'PM' : 'AM';
                        var rh12 = rh % 12 || 12;
                        var rDisp = pad(rh12) + ':' + rParts[1] + ' ' + rampm;

                        document.getElementById('nextDose').innerHTML =
                            '⏰ Next: <b style="color:#fbbf24;">' + r.name + '</b>' +
                            ' at <b style="color:#a78bfa;">' + rDisp + '</b>' +
                            ' · in <b style="color:#34d399;">' + timeLeft + '</b>';
                        nextFound = true;
                    }}
                }}

                if (!nextFound && !alarmActive) {{
                    if (reminders.length === 0) {{
                        document.getElementById('nextDose').innerHTML =
                            '<span style="color:#7c74a8;">💊 No pending reminders</span>';
                    }} else {{
                        document.getElementById('nextDose').innerHTML =
                            '<span style="color:#34d399;">✅ All medicines done for today!</span>';
                    }}
                }}
            }}

            function fireAlarm(r) {{
                if (alarmActive) return;
                alarmActive = true;

                // Create Audio Context on user interaction if needed, but here we try immediate
                if (!audioCtx) audioCtx = new (window.AudioContext || window.webkitAudioContext)();

                function playChime() {{
                    var now = audioCtx.currentTime;
                    function beep(start, freq, dur) {{
                        var osc  = audioCtx.createOscillator();
                        var gain = audioCtx.createGain();
                        osc.type = 'square';
                        osc.frequency.setValueAtTime(freq, start);
                        gain.gain.setValueAtTime(0, start);
                        gain.gain.linearRampToValueAtTime(0.7, start + 0.02);
                        gain.gain.exponentialRampToValueAtTime(0.01, start + dur);
                        osc.connect(gain); gain.connect(audioCtx.destination);
                        osc.start(start); osc.stop(start + dur + 0.05);
                    }}
                    // Triple-beep hospital pattern: beep-beep-BEEP
                    beep(now,        880,  0.15);
                    beep(now + 0.22, 880,  0.15);
                    beep(now + 0.44, 1047, 0.30);
                }}

                // Play immediately then repeat every 1000ms
                playChime();
                sirenInterval = setInterval(playChime, 1000);

                // Voice announcement
                try {{
                    window.speechSynthesis.cancel();
                    var msg = 'Attention! Medicine time for ' + r.name + '. Dose: ' + r.dose + '. Please take your medicine now.';
                    var u   = new SpeechSynthesisUtterance(msg);
                    u.lang  = 'en-US';
                    u.rate  = 0.9;
                    u.pitch = 1.0;
                    window.speechSynthesis.speak(u);
                }} catch(e) {{}}

                // Show alarm box
                document.getElementById('alarmBox').style.display = 'block';
                var rParts = r.time.split(':');
                var rh12 = (parseInt(rParts[0]) % 12) || 12;
                var rampm = parseInt(rParts[0]) >= 12 ? 'PM' : 'AM';
                var rDisp = pad(rh12) + ':' + rParts[1] + ' ' + rampm;
                
                document.getElementById('alarmMsg').innerHTML =
                    '💊 ' + r.name + '<br>' + r.dose + '<br>⏰ ' + rDisp;
                document.getElementById('nextDose').style.display = 'none';

                // Auto dismiss after 2 minutes
                setTimeout(dismissAlarm, 120000);
            }}

            function dismissAlarm() {{
                alarmActive = false;
                document.getElementById('alarmBox').style.display  = 'none';
                document.getElementById('nextDose').style.display  = 'block';
                if (sirenInterval) clearInterval(sirenInterval);
                window.speechSynthesis.cancel();
            }}

            // Clean up firedByMinute at midnight
            setInterval(function() {{
                var now = new Date();
                if (now.getHours() === 0 && now.getMinutes() === 0 && now.getSeconds() === 0) {{
                    firedByMinute = {{}};
                }}
            }}, 1000);

            setInterval(tick, 1000);
            tick();
            </script>
            </body>
            </html>
            """, height=350, scrolling=False)

    # ════════════════════════════════
    # TAB 2 — SMART INTAKE GUIDE
    # ════════════════════════════════
    with tab2:
        st.markdown("""
            <div style='text-align:center; padding:20px; background:linear-gradient(90deg, rgba(129,140,248,0.1), rgba(124,58,237,0.1)); border-radius:20px; border:1px solid rgba(124,58,237,0.2); margin-bottom:20px;'>
                <div style='font-size:2rem;'>💡</div>
                <div style='font-size:1.5rem; font-weight:800; color:#c4b5fd;'>Smart Intake Oracle</div>
                <div style='font-size:0.85rem; color:#a89ec9;'>Professional guidance on how to maximize your health and minimize risks.</div>
            </div>
        """, unsafe_allow_html=True)

        st.markdown("<div class='section-title'>🔍 Medicine Intake Deep-Dive</div>", unsafe_allow_html=True)

        st.markdown("""
        <div style='background:rgba(99,102,241,0.08); border:1px solid rgba(99,102,241,0.2);
             padding:10px 14px; border-radius:12px; margin-bottom:16px;
             font-size:0.83rem; color:#c4b5fd;'>
            🤖 Type any medicine name — AI will tell you what it does, side effects & precautions
        </div>
        """, unsafe_allow_html=True)

        ic1, ic2 = st.columns([2, 1])
        with ic1:
            search_med = st.text_input("🔍 Medicine Name", placeholder="e.g. Metformin, Lisinopril...")
        with ic2:
            st.markdown("<br>", unsafe_allow_html=True)
            search_btn = st.button("🔍 Get Info", use_container_width=True)

        if search_btn and search_med.strip():
            with st.spinner(f"🤖 Getting info for {search_med}..."):
                info = get_medicine_info(search_med.strip())
            if info:
                st.session_state.med_info[search_med.strip()] = info

        # --- SMART INTERACTION CHECKER ---
        st.markdown("<hr style='border-color:rgba(255,255,255,0.08); margin:24px 0;'>", unsafe_allow_html=True)
        st.markdown("<div class='section-title'>🛡️ Smart Interaction Checker</div>", unsafe_allow_html=True)
        
        active_meds = [r["name"] for r in st.session_state.reminders]
        if len(active_meds) > 1:
            st.markdown(f"**Checking interactions for:** {', '.join(active_meds)}")
            if st.button("🔍 Check for Drug-Drug Interactions", use_container_width=True, type="primary"):
                with st.spinner("🧠 AI analyzing multi-drug synergy/risks..."):
                    try:
                        resp = groq_client.chat.completions.create(
                            model="llama-3.3-70b-versatile",
                            messages=[{"role": "user", "content": f"""Analyze potential drug-drug interactions for these medicines: {', '.join(active_meds)}. 
1. If no major risks, say "No significant interactions found."
2. If risks exist, explain clearly in simple terms.
Max 3 sentences. No extra text."""}],
                            max_tokens=250, temperature=0.3
                        )
                        st.session_state.interaction_result = resp.choices[0].message.content
                    except:
                        st.session_state.interaction_result = "⚠️ AI consultation failed. Consult a pharmacist."
            
            if "interaction_result" in st.session_state:
                st.warning(st.session_state.interaction_result)
        else:
            st.info("💡 Add at least 2 medicines to use the Interaction Checker.")
        # ---------------------------------

        # Show all searched medicines
        if st.session_state.med_info:
            for mname, minfo in st.session_state.med_info.items():
                lines = minfo.strip().split("\n")
                st.markdown(f"""
                <div style='background:rgba(124,58,237,0.08); border:1px solid rgba(124,58,237,0.2);
                     border-radius:16px; padding:18px; margin-bottom:14px;'>
                    <div style='font-size:1rem; font-weight:800; color:#c4b5fd; margin-bottom:12px;'>
                        💊 {mname}
                    </div>
                """, unsafe_allow_html=True)

                colors = {
                    "USE":          ("#6ee7b7", "rgba(16,185,129,0.08)"),
                    "DOSE":         ("#fbbf24", "rgba(245,158,11,0.08)"),
                    "SIDE EFFECTS": ("#f87171", "rgba(239,68,68,0.08)"),
                    "PRECAUTIONS":  ("#fb923c", "rgba(251,146,60,0.08)"),
                    "FOOD":         ("#818cf8", "rgba(99,102,241,0.08)"),
                }

                for line in lines:
                    line = line.strip()
                    if not line:
                        continue
                    matched = False
                    for key, (tc, bg) in colors.items():
                        if line.startswith(key + ":"):
                            label = key
                            value = line[len(key)+1:].strip()
                            st.markdown(f"""
                            <div style='background:{bg}; border-radius:10px;
                                 padding:8px 12px; margin-bottom:6px; font-size:0.85rem;'>
                                <span style='color:{tc}; font-weight:700;'>{label}:</span>
                                <span style='color:#d4d0f0;'> {value}</span>
                            </div>
                            """, unsafe_allow_html=True)
                            matched = True
                            break
                    if not matched:
                        st.markdown(f"""
                        <div style='color:#a89ec9; font-size:0.83rem; padding:4px 8px;'>{line}</div>
                        """, unsafe_allow_html=True)

                st.markdown("</div>", unsafe_allow_html=True)

            if st.button("🗑️ Clear All Info", use_container_width=True):
                st.session_state.med_info = {}
                st.rerun()
        # --- COMMON INTAKE HACKS ---
        st.markdown("<hr style='border-color:rgba(255,255,255,0.08); margin:24px 0;'>", unsafe_allow_html=True)
        st.markdown("<div class='section-title'>⚡ Common Intake Hacks</div>", unsafe_allow_html=True)
        
        hacks = [
            ("🥛 The Dairy Rule", "Most antibiotics (like Tetracycline) interact with Calcium. Avoid milk for 2 hours before/after."),
            ("🍊 Vitamin C Boost", "Iron supplements are absorbed 2x better when taken with Vitamin C (Orange juice)."),
            ("🍔 The Fat Factor", "Fat-soluble vitamins (A, D, E, K) need a small meal for better absorption."),
            ("☕ Caffeine Alert", "Avoid coffee with Iron or Calcium supplements; it blocks their path!"),
        ]
        
        h_cols = st.columns(2)
        for idx, (ti, de) in enumerate(hacks):
            with h_cols[idx % 2]:
                st.markdown(f"""
                <div style='background:rgba(255,255,255,0.03); border:1px solid rgba(255,255,255,0.08); 
                     border-radius:12px; padding:12px; margin-bottom:10px;'>
                    <div style='font-weight:700; color:#fbbf24; font-size:0.9rem;'>{ti}</div>
                    <div style='font-size:0.75rem; color:#a89ec9; margin-top:4px;'>{de}</div>
                </div>
                """, unsafe_allow_html=True)

    # Bottom tips
    st.markdown("""
    <div style='display:flex; gap:10px; margin-top:16px; flex-wrap:wrap;'>
        <div style='flex:1; min-width:160px; background:rgba(99,102,241,0.07);
             border:1px solid rgba(99,102,241,0.2); padding:10px 12px;
             border-radius:11px; font-size:0.8rem; color:#818cf8;'>
            🔔 App must be <b>open</b> for alarms
        </div>
        <div style='flex:1; min-width:160px; background:rgba(245,158,11,0.07);
             border:1px solid rgba(245,158,11,0.2); padding:10px 12px;
             border-radius:11px; font-size:0.8rem; color:#fbbf24;'>
            📋 All doses logged in Dose Log tab
        </div>
        <div style='flex:1; min-width:160px; background:rgba(239,68,68,0.07);
             border:1px solid rgba(239,68,68,0.2); padding:10px 12px;
             border-radius:11px; font-size:0.8rem; color:#fca5a5;'>
            ⚠️ AI info is for reference only
        </div>
    </div>
    """, unsafe_allow_html=True)