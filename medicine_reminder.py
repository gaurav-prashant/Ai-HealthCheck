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

def show_medicine_reminder():
    st.markdown("<div class='section-header'>💊 Medicine Reminder</div>", unsafe_allow_html=True)

    # ── SESSION STATE INIT ──
    if "reminders"   not in st.session_state: st.session_state.reminders   = []
    if "dose_log"    not in st.session_state: st.session_state.dose_log    = []
    if "med_info"    not in st.session_state: st.session_state.med_info    = {}

    # ── TABS ──
    tab1, tab2, tab3, tab4 = st.tabs([
        "💊 Reminders", "📋 Dose Log", "📦 Stock Tracker", "ℹ️ Medicine Info"
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

            tc1, tc2 = st.columns(2)
            with tc1:
                med_hour = st.selectbox("⏰ Hour", [f"{h:02d}" for h in range(24)],
                    index=datetime.now().hour)
            with tc2:
                med_min  = st.selectbox("🕐 Minute", ["00","05","10","15","20","25","30","35","40","45","50","55"],
                    index=0)
            med_time_str = f"{med_hour}:{med_min}"
            med_freq  = st.selectbox("🔁 Frequency", [
                "Once Daily", "Twice Daily", "Three Times Daily",
                "Every 6 Hours", "Every 8 Hours", "As Needed"
            ])
            med_note  = st.text_input("📝 Note",           placeholder="e.g. After food")
            med_stock = st.number_input("📦 Tablets in Stock", min_value=0, value=30)
            med_refill = st.date_input("🔔 Refill Reminder Date", value=date.today())

            if st.button("➕ Add Medicine", use_container_width=True):
                if med_name.strip():
                    st.session_state.reminders.append({
                        "name":        med_name.strip(),
                        "dose":        med_dose.strip() or "1 tablet",
                        "time":        med_time_str,
                        "freq":        med_freq,
                        "note":        med_note.strip(),
                        "taken":       False,
                        "stock":       med_stock,
                        "refill_date": str(med_refill),
                        "missed":      False,
                        "added":       datetime.now().strftime("%Y-%m-%d %H:%M"),
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

                    # Check refill alert
                    refill_alert = ""
                    try:
                        days_left = (date.fromisoformat(r["refill_date"]) - date.today()).days
                        if days_left <= 3:
                            refill_alert = f"⚠️ Refill in {days_left} day(s)!"
                        elif days_left <= 7:
                            refill_alert = f"🔔 Refill in {days_left} days"
                    except:
                        pass

                    # Stock alert
                    stock_alert = ""
                    if r.get("stock", 99) <= 5:
                        stock_alert = f"📦 Only {r['stock']} left!"

                    # Card color
                    if r["taken"]:
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
                                    📏 {r["dose"]} &nbsp;·&nbsp; ⏰ {r["time"]} &nbsp;·&nbsp; 🔁 {r["freq"]}
                                    {"&nbsp;·&nbsp; 📝 " + r["note"] if r["note"] else ""}
                                </div>
                                {"<div style='font-size:0.78rem; color:#f87171; margin-top:4px;'>" + refill_alert + "</div>" if refill_alert else ""}
                                {"<div style='font-size:0.78rem; color:#fbbf24; margin-top:2px;'>" + stock_alert + "</div>" if stock_alert else ""}
                            </div>
                            <span style='background:rgba(0,0,0,0.2); color:{bc};
                                 padding:4px 10px; border-radius:20px; font-size:0.75rem;
                                 font-weight:700; white-space:nowrap; margin-left:8px;'>
                                {badge}
                            </span>
                        </div>
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
                                # Log the dose
                                st.session_state.dose_log.append({
                                    "name":      r["name"],
                                    "dose":      r["dose"],
                                    "time":      r["time"],
                                    "taken_at":  datetime.now().strftime("%Y-%m-%d %H:%M"),
                                    "status":    "✅ Taken"
                                })
                                # Reduce stock
                                if st.session_state.reminders[i]["stock"] > 0:
                                    st.session_state.reminders[i]["stock"] -= 1
                            st.rerun()
                    with bc2:
                        if st.button("🔔 Test Alarm", key=f"alarm_{i}", use_container_width=True):
                            st.session_state[f"play_alarm_{i}"] = True
                            st.rerun()
                    with bc3:
                        if st.button("❌ Miss", key=f"miss_{i}", use_container_width=True):
                            st.session_state.reminders[i]["missed"] = True
                            st.session_state.reminders[i]["taken"]  = False
                            st.session_state.dose_log.append({
                                "name":     r["name"],
                                "dose":     r["dose"],
                                "time":     r["time"],
                                "taken_at": datetime.now().strftime("%Y-%m-%d %H:%M"),
                                "status":   "❌ Missed"
                            })
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
                            function beep(f,s,d){{
                                var o=ctx.createOscillator(),g=ctx.createGain();
                                o.connect(g);g.connect(ctx.destination);
                                o.frequency.value=f;o.type='sine';
                                g.gain.setValueAtTime(0.4,ctx.currentTime+s);
                                g.gain.exponentialRampToValueAtTime(0.001,ctx.currentTime+s+d);
                                o.start(ctx.currentTime+s);o.stop(ctx.currentTime+s+d);
                            }}
                            beep(880,0.0,0.3);beep(660,0.3,0.3);
                            beep(880,0.6,0.3);beep(1100,0.9,0.5);
                            var u=new SpeechSynthesisUtterance(
                                'Medicine reminder. Time to take {r["name"]}. Dose: {r["dose"]}.');
                            u.lang='en-US';u.rate=0.9;
                            setTimeout(function(){{window.speechSynthesis.speak(u);}},1600);
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
                                st.session_state.dose_log.append({
                                    "name": r["name"], "dose": r["dose"],
                                    "time": r["time"],
                                    "taken_at": datetime.now().strftime("%Y-%m-%d %H:%M"),
                                    "status": "✅ Taken"
                                })
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
            </style>
            </head>
            <body>
            <div style="text-align:center; padding:16px;">

                <div id="clock" style="font-size:3rem; font-weight:900; color:#a78bfa;
                     letter-spacing:6px; margin-bottom:4px; font-family:'Arial Black',Arial;">
                    --:--:--
                </div>
                <div id="dateStr" style="color:#7c74a8; font-size:0.85rem; margin-bottom:14px;"></div>

                <div id="nextDose" style="background:rgba(124,58,237,0.15);
                     border:1px solid rgba(124,58,237,0.3); border-radius:14px;
                     padding:12px 16px; font-size:0.9rem; color:#d4d0f0; margin-bottom:12px;">
                    ⏳ Loading reminders...
                </div>

                <div id="alarmBox" style="display:none; background:rgba(239,68,68,0.2);
                     border:3px solid #f87171; border-radius:16px; padding:20px;
                     animation:pulse 0.8s infinite; margin-bottom:10px;">
                    <div style="font-size:2rem; animation:ring 0.5s infinite;">🔔</div>
                    <div style="font-size:1.3rem; font-weight:900; color:#f87171; margin:8px 0;">
                        MEDICINE TIME!
                    </div>
                    <div id="alarmMsg" style="color:#fca5a5; font-size:0.9rem;"></div>
                    <button onclick="dismissAlarm()" style="margin-top:12px;
                        background:rgba(239,68,68,0.3); border:2px solid #f87171;
                        color:white; padding:8px 20px; border-radius:10px;
                        cursor:pointer; font-weight:700; font-size:0.9rem;">
                        ✅ Dismiss
                    </button>
                </div>

            </div>

            <script>
            var reminders = {rem_js_str};
            var fired     = {{}};
            var alarmActive = false;

            function pad(n) {{ return n < 10 ? '0' + n : '' + n; }}

            function tick() {{
                var now  = new Date();
                var hh   = pad(now.getHours());
                var mm   = pad(now.getMinutes());
                var ss   = pad(now.getSeconds());
                var days = ['Sunday','Monday','Tuesday','Wednesday','Thursday','Friday','Saturday'];
                var mons = ['Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec'];

                document.getElementById('clock').innerText = hh + ':' + mm + ':' + ss;
                document.getElementById('dateStr').innerText =
                    days[now.getDay()] + ', ' + now.getDate() + ' ' +
                    mons[now.getMonth()] + ' ' + now.getFullYear();

                var curTime = hh + ':' + mm;
                var nextFound = false;

                for (var i = 0; i < reminders.length; i++) {{
                    var r = reminders[i];
                    var key = r.time + '|' + r.name;

                    // Fire alarm at exact minute match
                    if (r.time === curTime && !fired[key] && ss === '00') {{
                        fired[key] = true;
                        fireAlarm(r);
                    }}

                    // Show next upcoming dose
                    if (!nextFound && r.time > curTime) {{
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

                        document.getElementById('nextDose').innerHTML =
                            '⏰ Next: <b style="color:#fbbf24;">' + r.name + '</b>' +
                            ' at <b style="color:#a78bfa;">' + r.time + '</b>' +
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
                alarmActive = true;

                // Sound alarm
                try {{
                    var ctx = new (window.AudioContext || window.webkitAudioContext)();
                    function beep(f, s, d) {{
                        var o = ctx.createOscillator();
                        var g = ctx.createGain();
                        o.connect(g);
                        g.connect(ctx.destination);
                        o.frequency.value = f;
                        o.type = 'sine';
                        g.gain.setValueAtTime(0.6, ctx.currentTime + s);
                        g.gain.exponentialRampToValueAtTime(0.001, ctx.currentTime + s + d);
                        o.start(ctx.currentTime + s);
                        o.stop(ctx.currentTime + s + d + 0.1);
                    }}
                    // Alarm pattern
                    for (var rep = 0; rep < 3; rep++) {{
                        beep(880,  rep*1.2 + 0.0, 0.25);
                        beep(1100, rep*1.2 + 0.3, 0.25);
                        beep(880,  rep*1.2 + 0.6, 0.25);
                        beep(1320, rep*1.2 + 0.9, 0.35);
                    }}
                }} catch(e) {{}}

                // Voice announcement
                try {{
                    window.speechSynthesis.cancel();
                    var msg = 'Medicine reminder! Time to take ' + r.name + '. Dose: ' + r.dose + '. Please take your medicine now.';
                    var u   = new SpeechSynthesisUtterance(msg);
                    u.lang  = 'en-US';
                    u.rate  = 0.85;
                    u.pitch = 1.1;
                    setTimeout(function() {{ window.speechSynthesis.speak(u); }}, 1000);
                }} catch(e) {{}}

                // Show alarm box
                document.getElementById('alarmBox').style.display = 'block';
                document.getElementById('alarmMsg').innerHTML =
                    '💊 <b>' + r.name + '</b> &nbsp;·&nbsp; ' + r.dose +
                    ' &nbsp;·&nbsp; ⏰ ' + r.time;
                document.getElementById('nextDose').style.display = 'none';

                // Auto dismiss after 60 seconds
                setTimeout(dismissAlarm, 60000);
            }}

            function dismissAlarm() {{
                alarmActive = false;
                document.getElementById('alarmBox').style.display  = 'none';
                document.getElementById('nextDose').style.display  = 'block';
                window.speechSynthesis.cancel();
            }}

            // Reset fired alarms at midnight
            function resetAtMidnight() {{
                var now  = new Date();
                var msUntilMidnight = new Date(
                    now.getFullYear(), now.getMonth(), now.getDate()+1, 0, 0, 0
                ) - now;
                setTimeout(function() {{
                    fired = {{}};
                    resetAtMidnight();
                }}, msUntilMidnight);
            }}

            resetAtMidnight();
            setInterval(tick, 1000);
            tick();
            </script>
            </body>
            </html>
            """, height=300, scrolling=False)

    # ════════════════════════════════
    # TAB 2 — DOSE LOG
    # ════════════════════════════════
    with tab2:
        st.markdown("<div class='section-title'>📋 Dose History Log</div>", unsafe_allow_html=True)

        if not st.session_state.dose_log:
            st.markdown("""
            <div style='text-align:center; padding:60px;
                 background:rgba(255,255,255,0.02); border-radius:16px;
                 border:1px dashed rgba(255,255,255,0.08);'>
                <div style='font-size:3rem; margin-bottom:12px;'>📋</div>
                <p style='color:#6b7280;'>No dose history yet.</p>
                <p style='color:#4b5563; font-size:0.82rem;'>Mark medicines as taken to log them here.</p>
            </div>
            """, unsafe_allow_html=True)
        else:
            # Stats
            total_log  = len(st.session_state.dose_log)
            taken_log  = sum(1 for d in st.session_state.dose_log if "Taken" in d["status"])
            missed_log = total_log - taken_log
            rate       = int(taken_log / total_log * 100) if total_log > 0 else 0

            st.markdown(f"""
            <div style='display:flex; gap:12px; margin-bottom:18px; flex-wrap:wrap;'>
                <div style='flex:1; min-width:120px; text-align:center;
                     background:rgba(99,102,241,0.1); border:1px solid rgba(99,102,241,0.25);
                     border-radius:14px; padding:14px;'>
                    <div style='font-size:1.8rem; font-weight:900; color:#818cf8;'>{total_log}</div>
                    <div style='font-size:0.75rem; color:#a89ec9;'>Total Doses</div>
                </div>
                <div style='flex:1; min-width:120px; text-align:center;
                     background:rgba(16,185,129,0.1); border:1px solid rgba(16,185,129,0.25);
                     border-radius:14px; padding:14px;'>
                    <div style='font-size:1.8rem; font-weight:900; color:#34d399;'>{taken_log}</div>
                    <div style='font-size:0.75rem; color:#a89ec9;'>Taken</div>
                </div>
                <div style='flex:1; min-width:120px; text-align:center;
                     background:rgba(239,68,68,0.1); border:1px solid rgba(239,68,68,0.25);
                     border-radius:14px; padding:14px;'>
                    <div style='font-size:1.8rem; font-weight:900; color:#f87171;'>{missed_log}</div>
                    <div style='font-size:0.75rem; color:#a89ec9;'>Missed</div>
                </div>
                <div style='flex:1; min-width:120px; text-align:center;
                     background:rgba(245,158,11,0.1); border:1px solid rgba(245,158,11,0.25);
                     border-radius:14px; padding:14px;'>
                    <div style='font-size:1.8rem; font-weight:900; color:#fbbf24;'>{rate}%</div>
                    <div style='font-size:0.75rem; color:#a89ec9;'>Adherence</div>
                </div>
            </div>
            """, unsafe_allow_html=True)

            # Log entries
            for entry in reversed(st.session_state.dose_log):
                is_taken = "Taken" in entry["status"]
                bg     = "rgba(16,185,129,0.07)" if is_taken else "rgba(239,68,68,0.07)"
                border = "rgba(16,185,129,0.2)"  if is_taken else "rgba(239,68,68,0.2)"
                color  = "#34d399" if is_taken else "#f87171"
                st.markdown(f"""
                <div style='background:{bg}; border:1px solid {border};
                     border-radius:12px; padding:12px 16px; margin-bottom:8px;
                     display:flex; justify-content:space-between; align-items:center;'>
                    <div>
                        <span style='color:#f0edff; font-weight:700;'>💊 {entry["name"]}</span>
                        <span style='color:#a89ec9; font-size:0.8rem;'> · {entry["dose"]} · ⏰ {entry["time"]}</span>
                    </div>
                    <div style='text-align:right;'>
                        <div style='color:{color}; font-weight:700; font-size:0.85rem;'>{entry["status"]}</div>
                        <div style='color:#7c74a8; font-size:0.75rem;'>{entry["taken_at"]}</div>
                    </div>
                </div>
                """, unsafe_allow_html=True)

            st.markdown("<br>", unsafe_allow_html=True)
            lc1, lc2 = st.columns(2)
            with lc1:
                log_text = "\n".join([
                    f"{e['taken_at']} | {e['name']} | {e['dose']} | {e['status']}"
                    for e in st.session_state.dose_log
                ])
                st.download_button("📄 Download Log", data=log_text,
                    file_name="dose_log.txt", mime="text/plain", use_container_width=True)
            with lc2:
                if st.button("🗑️ Clear Log", use_container_width=True):
                    st.session_state.dose_log = []
                    st.rerun()

    # ════════════════════════════════
    # TAB 3 — STOCK TRACKER
    # ════════════════════════════════
    with tab3:
        st.markdown("<div class='section-title'>📦 Medicine Stock Tracker</div>", unsafe_allow_html=True)

        if not st.session_state.reminders:
            st.markdown("""
            <div style='text-align:center; padding:60px;
                 background:rgba(255,255,255,0.02); border-radius:16px;
                 border:1px dashed rgba(255,255,255,0.08);'>
                <div style='font-size:3rem; margin-bottom:12px;'>📦</div>
                <p style='color:#6b7280;'>No medicines added yet.</p>
            </div>
            """, unsafe_allow_html=True)
        else:
            for i, r in enumerate(st.session_state.reminders):
                stock = r.get("stock", 0)
                if stock <= 0:
                    bg, border, color, label = "rgba(239,68,68,0.1)", "rgba(239,68,68,0.3)", "#f87171", "❌ OUT OF STOCK"
                elif stock <= 5:
                    bg, border, color, label = "rgba(239,68,68,0.08)", "rgba(239,68,68,0.2)", "#f87171", "🚨 Critical Low"
                elif stock <= 10:
                    bg, border, color, label = "rgba(245,158,11,0.08)", "rgba(245,158,11,0.2)", "#fbbf24", "⚠️ Low Stock"
                else:
                    bg, border, color, label = "rgba(16,185,129,0.08)", "rgba(16,185,129,0.2)", "#34d399", "✅ Good"

                # Refill days
                try:
                    days_left = (date.fromisoformat(r["refill_date"]) - date.today()).days
                    refill_str = f"Refill in {days_left} day(s)" if days_left >= 0 else "Refill overdue!"
                    refill_color = "#f87171" if days_left <= 3 else "#fbbf24" if days_left <= 7 else "#6ee7b7"
                except:
                    refill_str, refill_color = "No refill date", "#7c74a8"

                st.markdown(f"""
                <div style='background:{bg}; border:1px solid {border};
                     border-radius:16px; padding:16px 18px; margin-bottom:12px;'>
                    <div style='display:flex; justify-content:space-between; align-items:center; margin-bottom:10px;'>
                        <div>
                            <div style='font-size:1rem; font-weight:700; color:#f0edff;'>💊 {r["name"]}</div>
                            <div style='font-size:0.8rem; color:#a89ec9;'>{r["dose"]} · {r["freq"]}</div>
                        </div>
                        <div style='text-align:right;'>
                            <div style='font-size:1.6rem; font-weight:900; color:{color};'>{stock}</div>
                            <div style='font-size:0.72rem; color:#a89ec9;'>tablets left</div>
                        </div>
                    </div>
                    <div style='background:rgba(0,0,0,0.2); border-radius:8px; height:8px; margin-bottom:8px;'>
                        <div style='background:{color}; width:{min(stock*2, 100)}%;
                             height:8px; border-radius:8px;'></div>
                    </div>
                    <div style='display:flex; justify-content:space-between; font-size:0.78rem;'>
                        <span style='color:{color}; font-weight:700;'>{label}</span>
                        <span style='color:{refill_color};'>🔔 {refill_str}</span>
                    </div>
                </div>
                """, unsafe_allow_html=True)

                sc1, sc2 = st.columns(2)
                with sc1:
                    add_stock = st.number_input("Add tablets", min_value=1, value=30,
                        key=f"add_stock_{i}", label_visibility="collapsed")
                with sc2:
                    if st.button(f"➕ Add Stock", key=f"addst_{i}", use_container_width=True):
                        st.session_state.reminders[i]["stock"] += add_stock
                        st.rerun()

    # ════════════════════════════════
    # TAB 4 — MEDICINE INFO
    # ════════════════════════════════
    with tab4:
        st.markdown("<div class='section-title'>ℹ️ AI Medicine Information</div>", unsafe_allow_html=True)

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
        else:
            st.markdown("""
            <div style='text-align:center; padding:50px;
                 background:rgba(255,255,255,0.02); border-radius:16px;
                 border:1px dashed rgba(255,255,255,0.08);'>
                <div style='font-size:3rem; margin-bottom:12px;'>💊</div>
                <p style='color:#6b7280;'>Search a medicine above to see its information</p>
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
        <div style='flex:1; min-width:160px; background:rgba(16,185,129,0.07);
             border:1px solid rgba(16,185,129,0.2); padding:10px 12px;
             border-radius:11px; font-size:0.8rem; color:#6ee7b7;'>
            📦 Stock auto-reduces when marked taken
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