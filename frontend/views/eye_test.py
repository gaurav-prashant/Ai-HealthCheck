# ============================================================
# eye_test.py — Eyesight Test (Direct Letter Voice Recognition)
# ============================================================

import streamlit as st
import streamlit.components.v1 as components

EYE_TEST_ROWS = [
    {"line": 1, "label": "20/200", "size": 130, "letters": ["E"],                               "desc": "Very Large"},
    {"line": 2, "label": "20/100", "size": 100, "letters": ["F", "P"],                          "desc": "Large"},
    {"line": 3, "label": "20/70",  "size": 78,  "letters": ["T", "O", "Z"],                     "desc": "Medium Large"},
    {"line": 4, "label": "20/50",  "size": 60,  "letters": ["L", "P", "E", "D"],                "desc": "Medium"},
    {"line": 5, "label": "20/40",  "size": 46,  "letters": ["P", "E", "C", "F", "D"],           "desc": "Normal Large"},
    {"line": 6, "label": "20/30",  "size": 34,  "letters": ["E", "D", "F", "C", "Z", "P"],      "desc": "Normal"},
    {"line": 7, "label": "20/25",  "size": 26,  "letters": ["F", "E", "L", "O", "P", "Z", "D"],"desc": "Good"},
    {"line": 8, "label": "20/20",  "size": 20,  "letters": ["D","E","F","P","O","T","E","C"],   "desc": "Perfect"},
]

# Sound-alike map — common mishears for each letter
SOUNDALIKES = {
    "E": ["E","EE","HE","BE","ME","SEE","KEY","TEA","EA"],
    "F": ["F","EF","FEE","OFF","IF","HALF"],
    "P": ["P","PEE","PE","PIE","BE","DEE"],
    "T": ["T","TEE","TEA","THE","TWO","TO"],
    "O": ["O","OH","OW","OU","ZEO","ZERO","NO","GO"],
    "Z": ["Z","ZEE","ZED","SEE","ZE","ZEBRA"],
    "L": ["L","EL","ELLE","HELL","WELL","BELL"],
    "D": ["D","DEE","THE","DE","DI"],
    "C": ["C","SEE","SEA","SI","CEE"],
}

def assess_vision(results):
    correct = [r["line"] for r in results if r["correct"]]
    if not correct:
        return {"status":"❌ Very Poor Vision","color":"#f87171","bg":"rgba(239,68,68,0.12)","border":"rgba(239,68,68,0.3)","condition":"Severe Vision Impairment","details":"You could not read any lines. Immediate medical attention needed.","advice":["Visit ophthalmologist immediately","Do not drive","Get complete eye examination","Prescription lenses needed"],"doctor":"Ophthalmologist (Emergency)","urgency":"🚨 Emergency"}
    m = max(correct)
    if m >= 8: return {"status":"✅ Perfect Vision (20/20)","color":"#34d399","bg":"rgba(16,185,129,0.12)","border":"rgba(16,185,129,0.3)","condition":"Normal Healthy Vision","details":"Excellent! You have perfect 20/20 vision.","advice":["Eye checkup every 2 years","Wear sunglasses outdoors","20-20-20 rule for screens","Eat vitamin A rich foods"],"doctor":"No specialist needed","urgency":"✅ Routine checkup recommended"}
    if m >= 6: return {"status":"🟡 Good Vision (20/25-30)","color":"#4ade80","bg":"rgba(74,222,128,0.12)","border":"rgba(74,222,128,0.3)","condition":"Slightly Below Perfect","details":"Your vision is good but slightly below perfect 20/20.","advice":["Visit eye doctor","Mild glasses may help","Reduce screen time","Good lighting when reading"],"doctor":"Optometrist","urgency":"📅 Visit within 1-2 months"}
    if m >= 5: return {"status":"🟠 Moderate Vision (20/40)","color":"#fb923c","bg":"rgba(251,146,60,0.12)","border":"rgba(251,146,60,0.3)","condition":"Possible Myopia or Hyperopia","details":"You may have nearsightedness or farsightedness.","advice":["Get prescription glasses","Visit ophthalmologist","Avoid reading in poor light","Consider LASIK"],"doctor":"Ophthalmologist","urgency":"⚠️ Visit within 2-4 weeks"}
    if m >= 3: return {"status":"🔴 Poor Vision (20/50-70)","color":"#fbbf24","bg":"rgba(251,191,36,0.12)","border":"rgba(251,191,36,0.3)","condition":"Significant Refractive Error","details":"Significant vision problems detected.","advice":["See eye doctor soon","Strong prescription glasses","Avoid driving","Comprehensive eye exam"],"doctor":"Ophthalmologist","urgency":"🚨 Urgent — See doctor this week"}
    return {"status":"🔴 Very Poor Vision","color":"#f87171","bg":"rgba(239,68,68,0.12)","border":"rgba(239,68,68,0.3)","condition":"Severe Vision Impairment","details":"Very poor vision. Immediate attention required.","advice":["See ophthalmologist immediately","Complete eye exam","Check for cataracts/glaucoma","Do not delay"],"doctor":"Ophthalmologist (Emergency)","urgency":"🚨 Emergency — See doctor immediately"}

def show_eye_test():

    for k, v in {
        "eye_started": False, "eye_line": 0, "eye_letter": 0,
        "eye_results": [], "eye_done": False, "eye_which": "Both Eyes",
        "eye_letter_results": []
    }.items():
        if k not in st.session_state:
            st.session_state[k] = v

    # ══ NOT STARTED ══
    if not st.session_state.eye_started and not st.session_state.eye_done:
        st.markdown("<div class='section-header'>👁️ Eyesight Voice Test</div>", unsafe_allow_html=True)

        col1, col2 = st.columns(2)
        with col1:
            st.markdown("<div class='glass-box'>", unsafe_allow_html=True)
            st.markdown("<div class='section-title'>⚙️ Settings</div>", unsafe_allow_html=True)
            eye = st.selectbox("👁️ Which Eye", ["Both Eyes", "Left Eye Only", "Right Eye Only"])
            st.session_state.eye_which = eye

            st.markdown("""
            <div style='background:rgba(99,102,241,0.1); border:1px solid rgba(99,102,241,0.25);
                 padding:14px; border-radius:12px; margin:10px 0;
                 font-size:0.85rem; color:#d4d0f0; line-height:2;'>
                📏 Hold device <b style='color:#fbbf24;'>2 feet (60cm) away</b><br>
                👁️ A letter appears — <b style='color:#a78bfa;'>say it out loud</b><br>
                🎤 Click the mic button and speak clearly<br>
                ✅ Or use YES / NO buttons as backup
            </div>
            """, unsafe_allow_html=True)

            if st.button("👁️ Start Eye Test", use_container_width=True):
                st.session_state.eye_started        = True
                st.session_state.eye_line           = 0
                st.session_state.eye_letter         = 0
                st.session_state.eye_results        = []
                st.session_state.eye_letter_results = []
                st.session_state.eye_done           = False
                st.rerun()
            st.markdown("</div>", unsafe_allow_html=True)

        with col2:
            st.markdown("<div class='glass-box'>", unsafe_allow_html=True)
            st.markdown("<div class='section-title'>📊 Vision Scale</div>", unsafe_allow_html=True)
            for row in EYE_TEST_ROWS:
                sz = min(row["size"]//3, 32)
                st.markdown(f"""
                <div style='display:flex; justify-content:space-between; align-items:center;
                     padding:7px 12px; background:rgba(255,255,255,0.03);
                     border-radius:9px; margin-bottom:5px; font-size:0.83rem;'>
                    <span style='color:#7c74a8;'>Line {row["line"]}</span>
                    <span style='font-size:{sz}px; color:white; font-weight:900;
                         font-family:Arial Black;'>{" ".join(row["letters"][:3])}</span>
                    <span style='color:#c4b5fd; font-weight:700;'>{row["label"]}</span>
                </div>
                """, unsafe_allow_html=True)
            st.markdown("</div>", unsafe_allow_html=True)

    # ══ TEST IN PROGRESS ══
    elif st.session_state.eye_started and not st.session_state.eye_done:

        line_idx   = st.session_state.eye_line
        letter_idx = st.session_state.eye_letter

        if line_idx >= len(EYE_TEST_ROWS):
            st.session_state.eye_done    = True
            st.session_state.eye_started = False
            st.rerun()

        row     = EYE_TEST_ROWS[line_idx]
        letters = row["letters"]

        if letter_idx >= len(letters):
            lc = sum(st.session_state.eye_letter_results)
            lt = len(st.session_state.eye_letter_results)
            st.session_state.eye_results.append({
                "line": row["line"], "label": row["label"],
                "correct": lc >= lt * 0.6, "score": f"{lc}/{lt}"
            })
            st.session_state.eye_letter         = 0
            st.session_state.eye_line           += 1
            st.session_state.eye_letter_results = []
            st.rerun()

        current    = letters[letter_idx]
        # Build JS soundalikes array
        sa_list    = SOUNDALIKES.get(current, [current])
        sa_js      = str(sa_list).replace("'", '"')

        total_done = sum(len(EYE_TEST_ROWS[i]["letters"]) for i in range(line_idx)) + letter_idx
        total_all  = sum(len(r["letters"]) for r in EYE_TEST_ROWS)
        progress   = total_done / total_all

        st.markdown("<div class='section-header'>👁️ Eyesight Voice Test</div>", unsafe_allow_html=True)

        st.markdown(f"""
        <div style='margin-bottom:16px;'>
            <div style='display:flex; justify-content:space-between; margin-bottom:6px;
                 font-size:0.82rem; color:#a89ec9;'>
                <span>Line {line_idx+1}/{len(EYE_TEST_ROWS)} — Letter {letter_idx+1}/{len(letters)}</span>
                <span>{row["label"]} · {row["desc"]}</span>
            </div>
            <div style='background:rgba(124,58,237,0.15); border-radius:10px; height:10px;'>
                <div style='background:linear-gradient(90deg,#7c3aed,#a78bfa,#fbbf24);
                     width:{int(progress*100)}%; height:10px; border-radius:10px;'></div>
            </div>
        </div>
        """, unsafe_allow_html=True)

        col1, col2 = st.columns([1, 1])

        with col1:
            st.markdown("<div class='glass-box'>", unsafe_allow_html=True)
            font_size = row["size"]
            st.markdown(f"""
            <div style='text-align:center; background:white; border-radius:20px;
                 padding:50px 20px; margin-bottom:16px;
                 border:2px solid rgba(124,58,237,0.3);'>
                <div style='font-size:{font_size}px; font-weight:900; color:#1a1a2e;
                     letter-spacing:{max(4,font_size//6)}px;
                     font-family:"Arial Black",Arial,sans-serif;
                     line-height:1.1; user-select:none;'>
                    {current}
                </div>
                <div style='color:#888; font-size:12px; margin-top:12px; font-family:Arial;'>
                    Line {line_idx+1} · {row["label"]}
                </div>
            </div>
            <div style='text-align:center; padding:10px;
                 background:rgba(124,58,237,0.08); border-radius:12px;
                 border:1px solid rgba(124,58,237,0.2);'>
                <div style='color:#a78bfa; font-size:0.9rem; font-weight:600;'>
                    👁️ Look at the letter above
                </div>
                <div style='color:#7c74a8; font-size:0.78rem; margin-top:4px;'>
                    Click mic and say the letter out loud →
                </div>
            </div>
            """, unsafe_allow_html=True)
            st.markdown("</div>", unsafe_allow_html=True)

        with col2:
            st.markdown("<div class='glass-box'>", unsafe_allow_html=True)

            components.html(f"""
            <div style="font-family:Arial,sans-serif; text-align:center; padding:10px;">

                <button id="micBtn" onclick="startListening()" style="
                    background:linear-gradient(135deg,#3b0764,#581c87,#7c3aed);
                    border:3px solid rgba(196,181,253,0.5); color:white;
                    padding:18px 40px; font-size:1.1rem; font-weight:700;
                    border-radius:50px; cursor:pointer; width:100%;
                    box-shadow:0 6px 24px rgba(124,58,237,0.5);
                    margin-bottom:14px;">
                    🎤 Speak the Letter
                </button>

                <div id="status" style="color:#7c74a8; font-size:0.85rem;
                     margin-bottom:10px; min-height:22px;"></div>

                <div id="heardBox" style="display:none; padding:14px; border-radius:14px;
                     font-size:1rem; margin-bottom:12px; font-weight:600;"></div>

                <div id="resultBtns" style="display:none; margin-top:8px;">
                    <button onclick="markResult(true)" style="
                        background:linear-gradient(135deg,#064e3b,#059669);
                        border:none; color:white; padding:12px; font-size:0.95rem;
                        font-weight:700; border-radius:12px; cursor:pointer;
                        width:48%; margin-right:4%;">✅ Correct</button>
                    <button onclick="markResult(false)" style="
                        background:linear-gradient(135deg,#7f1d1d,#dc2626);
                        border:none; color:white; padding:12px; font-size:0.95rem;
                        font-weight:700; border-radius:12px; cursor:pointer;
                        width:48%;">❌ Wrong</button>
                </div>
            </div>

            <script>
            var expected   = "{current}".toUpperCase();
            var soundalikes = {sa_js};

            function clean(s) {{
                return s.toUpperCase().replace(/[^A-Z]/g, '');
            }}

            function isMatch(heard) {{
                var h = clean(heard);
                // Exact letter match
                if (h === expected) return true;
                // Single char that matches
                if (h.length === 1 && h === expected) return true;
                // Heard starts with expected letter
                if (h.length > 0 && h[0] === expected) return true;
                // Check soundalikes
                for (var s of soundalikes) {{
                    if (h === clean(s)) return true;
                    if (h.startsWith(clean(s))) return true;
                }}
                return false;
            }}

            function startListening() {{
                if (!('webkitSpeechRecognition' in window) && !('SpeechRecognition' in window)) {{
                    document.getElementById('status').innerHTML =
                        '<span style="color:#f87171;">❌ Use Chrome browser for voice!</span>';
                    document.getElementById('resultBtns').style.display = 'block';
                    return;
                }}

                var SR  = window.SpeechRecognition || window.webkitSpeechRecognition;
                var rec = new SR();
                rec.lang            = 'en-US';
                rec.interimResults  = false;
                rec.maxAlternatives = 10;
                rec.continuous      = false;

                document.getElementById('micBtn').style.background =
                    'linear-gradient(135deg,#065f46,#059669)';
                document.getElementById('micBtn').innerHTML = '🔴 Listening...';
                document.getElementById('status').innerHTML =
                    '<span style="color:#34d399; font-weight:700;">🎤 Say the letter!</span>';
                document.getElementById('heardBox').style.display   = 'none';
                document.getElementById('resultBtns').style.display = 'none';

                rec.onresult = function(e) {{
                    // Collect ALL alternatives for best accuracy
                    var alts = [];
                    for (var i = 0; i < e.results[0].length; i++) {{
                        alts.push(e.results[0][i].transcript.trim());
                    }}

                    var heard     = alts[0];
                    var isCorrect = false;

                    // Check every alternative
                    for (var alt of alts) {{
                        if (isMatch(alt)) {{ isCorrect = true; break; }}
                    }}

                    showResult(heard, isCorrect);
                }};

                rec.onerror = function(e) {{
                    document.getElementById('micBtn').style.background =
                        'linear-gradient(135deg,#3b0764,#581c87,#7c3aed)';
                    document.getElementById('micBtn').innerHTML = '🎤 Speak the Letter';
                    if (e.error === 'no-speech') {{
                        document.getElementById('status').innerHTML =
                            '<span style="color:#fbbf24;">⚠️ Nothing heard. Try again!</span>';
                    }} else if (e.error === 'not-allowed') {{
                        document.getElementById('status').innerHTML =
                            '<span style="color:#f87171;">❌ Allow mic in browser settings!</span>';
                        document.getElementById('resultBtns').style.display = 'block';
                    }} else {{
                        document.getElementById('status').innerHTML =
                            '<span style="color:#fbbf24;">⚠️ ' + e.error + ' — try again!</span>';
                    }}
                }};

                rec.onend = function() {{
                    document.getElementById('micBtn').style.background =
                        'linear-gradient(135deg,#3b0764,#581c87,#7c3aed)';
                    document.getElementById('micBtn').innerHTML = '🎤 Speak the Letter';
                }};

                rec.start();
            }}

            function showResult(heard, isCorrect) {{
                var box = document.getElementById('heardBox');
                box.style.display = 'block';
                document.getElementById('status').innerHTML = '';

                if (isCorrect) {{
                    box.style.background = 'rgba(5,150,105,0.15)';
                    box.style.border     = '2px solid rgba(16,185,129,0.4)';
                    box.style.color      = '#34d399';
                    box.innerHTML        = '✅ Heard: <b>' + heard + '</b> — Correct!';
                    var u = new SpeechSynthesisUtterance('Correct!');
                    u.lang='en-US'; u.rate=1.1;
                    window.speechSynthesis.cancel();
                    window.speechSynthesis.speak(u);
                    setTimeout(function() {{ sendResult('correct'); }}, 1200);
                }} else {{
                    box.style.background = 'rgba(239,68,68,0.12)';
                    box.style.border     = '2px solid rgba(239,68,68,0.35)';
                    box.style.color      = '#f87171';
                    box.innerHTML        = '❌ Heard: <b>' + (heard||'unclear') +
                        '</b> — Expected letter: <b style="font-size:1.3rem;">' + expected + '</b>';
                    var u = new SpeechSynthesisUtterance('Wrong. Try again.');
                    u.lang='en-US'; u.rate=0.9;
                    window.speechSynthesis.cancel();
                    window.speechSynthesis.speak(u);
                    document.getElementById('resultBtns').style.display = 'block';
                }}
            }}

            function markResult(isCorrect) {{
                sendResult(isCorrect ? 'correct' : 'wrong');
            }}

            function sendResult(result) {{
                window.parent.postMessage({{
                    type: 'streamlit:setComponentValue', value: result
                }}, '*');
            }}

            setTimeout(function() {{
                var u = new SpeechSynthesisUtterance('Look at the letter and say it out loud');
                u.lang='en-US'; u.rate=0.88;
                window.speechSynthesis.speak(u);
            }}, 400);
            </script>
            """, height=320)

            st.markdown("""
            <div style='text-align:center; color:#4b5563; font-size:0.78rem; margin:8px 0 6px;'>
                — Or use manual buttons —
            </div>
            """, unsafe_allow_html=True)

            mc1, mc2 = st.columns(2)
            with mc1:
                if st.button("✅ Can Read It", key=f"yes_{line_idx}_{letter_idx}", use_container_width=True):
                    st.session_state.eye_letter_results.append(1)
                    st.session_state.eye_letter += 1
                    st.rerun()
            with mc2:
                if st.button("❌ Cannot Read", key=f"no_{line_idx}_{letter_idx}", use_container_width=True):
                    st.session_state.eye_letter_results.append(0)
                    st.session_state.eye_letter += 1
                    st.rerun()

            done_c = sum(st.session_state.eye_letter_results)
            done_t = len(st.session_state.eye_letter_results)
            if done_t > 0:
                cl = "#34d399" if done_c/done_t >= 0.6 else "#f87171"
                st.markdown(f"""
                <div style='margin-top:12px; padding:12px; text-align:center;
                     background:rgba(124,58,237,0.08); border-radius:12px;
                     border:1px solid rgba(124,58,237,0.15);'>
                    <div style='color:#a89ec9; font-size:0.75rem;'>This Line Score</div>
                    <div style='color:{cl}; font-size:1.8rem; font-weight:900;'>{done_c}/{done_t}</div>
                </div>
                """, unsafe_allow_html=True)

            st.markdown("<br>", unsafe_allow_html=True)
            if st.button("⏹ Stop & See Results", use_container_width=True):
                if st.session_state.eye_letter_results:
                    lc = sum(st.session_state.eye_letter_results)
                    lt = len(st.session_state.eye_letter_results)
                    st.session_state.eye_results.append({
                        "line": row["line"], "label": row["label"],
                        "correct": lc >= lt * 0.6, "score": f"{lc}/{lt}"
                    })
                st.session_state.eye_done    = True
                st.session_state.eye_started = False
                st.rerun()

            st.markdown("</div>", unsafe_allow_html=True)

    # ══ RESULTS ══
    elif st.session_state.eye_done:
        results = st.session_state.eye_results
        a       = assess_vision(results)
        correct = len([r for r in results if r["correct"]])
        total   = len(results)

        st.markdown("<div class='section-header'>👁️ Your Eye Test Results</div>", unsafe_allow_html=True)

        st.markdown(f"""
        <div style='background:{a["bg"]}; border:2px solid {a["border"]};
             padding:32px; border-radius:22px; text-align:center; margin-bottom:24px;'>
            <div style='font-size:4rem; margin-bottom:12px;'>👁️</div>
            <div style='font-size:2.2rem; font-weight:900; color:{a["color"]}; margin-bottom:8px;'>
                {a["status"]}
            </div>
            <div style='font-size:1.05rem; color:#d4d0f0; margin-bottom:10px;'>{a["condition"]}</div>
            <div style='font-size:0.88rem; color:#a89ec9;'>✅ Read {correct} of {total} lines correctly</div>
        </div>
        """, unsafe_allow_html=True)

        col1, col2 = st.columns(2)
        with col1:
            st.markdown(f"""
            <div class='glass-box'>
                <div class='section-title'>📋 Assessment</div>
                <div style='background:rgba(255,255,255,0.04); padding:12px; border-radius:10px; margin-bottom:8px;'>
                    <div style='color:#a89ec9; font-size:0.75rem;'>Condition</div>
                    <div style='color:{a["color"]}; font-weight:700;'>{a["condition"]}</div>
                </div>
                <div style='background:rgba(255,255,255,0.04); padding:12px; border-radius:10px; margin-bottom:8px;'>
                    <div style='color:#a89ec9; font-size:0.75rem;'>Details</div>
                    <div style='color:#d4d0f0; font-size:0.86rem; line-height:1.6;'>{a["details"]}</div>
                </div>
                <div style='background:rgba(16,185,129,0.08); border:1px solid rgba(16,185,129,0.2);
                     padding:12px; border-radius:10px; margin-bottom:8px;'>
                    <div style='color:#a89ec9; font-size:0.75rem;'>Recommended Doctor</div>
                    <div style='color:#6ee7b7; font-weight:700;'>👨‍⚕️ {a["doctor"]}</div>
                </div>
                <div style='background:rgba(245,158,11,0.08); border:1px solid rgba(245,158,11,0.2);
                     padding:12px; border-radius:10px;'>
                    <div style='color:#a89ec9; font-size:0.75rem;'>Urgency</div>
                    <div style='color:#fbbf24; font-weight:700;'>{a["urgency"]}</div>
                </div>
            </div>
            """, unsafe_allow_html=True)

            st.markdown("<div class='glass-box'>", unsafe_allow_html=True)
            st.markdown("<div class='section-title'>📊 Line by Line</div>", unsafe_allow_html=True)
            for r in results:
                ic = "✅" if r["correct"] else "❌"
                cl = "#34d399" if r["correct"] else "#f87171"
                st.markdown(f"""
                <div style='display:flex; justify-content:space-between; padding:7px 12px;
                     background:rgba(255,255,255,0.03); border-radius:9px; margin-bottom:5px;
                     font-size:0.85rem;'>
                    <span style='color:#a89ec9;'>Line {r["line"]} — {r["label"]}</span>
                    <span style='color:{cl}; font-weight:700;'>{ic} {r.get("score","")}</span>
                </div>
                """, unsafe_allow_html=True)
            st.markdown("</div>", unsafe_allow_html=True)

        with col2:
            st.markdown("<div class='glass-box'>", unsafe_allow_html=True)
            st.markdown("<div class='section-title'>💡 Recommendations</div>", unsafe_allow_html=True)
            for adv in a["advice"]:
                st.markdown(f"""
                <div style='background:rgba(124,58,237,0.08); border:1px solid rgba(124,58,237,0.15);
                     padding:10px 14px; border-radius:10px; margin-bottom:8px;
                     color:#c4b5fd; font-size:0.87rem;'>💡 {adv}</div>
                """, unsafe_allow_html=True)
            st.markdown("</div>", unsafe_allow_html=True)

            st.markdown("""
            <div class='glass-box'>
                <div class='section-title'>👁️ Daily Eye Care</div>
                <div style='font-size:0.86rem; line-height:2.1;'>
                    <div style='color:#6ee7b7;'>🥕 Eat carrots, spinach & citrus</div>
                    <div style='color:#6ee7b7;'>💧 Drink 8 glasses of water daily</div>
                    <div style='color:#6ee7b7;'>📱 20-20-20 rule for screens</div>
                    <div style='color:#6ee7b7;'>😴 Get 7-8 hours of sleep</div>
                    <div style='color:#6ee7b7;'>☀️ UV protection sunglasses</div>
                    <div style='color:#6ee7b7;'>🔆 Good lighting when reading</div>
                    <div style='color:#6ee7b7;'>👁️ Eye checkup every 1-2 years</div>
                </div>
            </div>
            """, unsafe_allow_html=True)

        st.markdown("<br>", unsafe_allow_html=True)
        c1, c2 = st.columns(2)
        with c1:
            if st.button("🔄 Retake Test", use_container_width=True):
                for k in ["eye_started","eye_done","eye_line","eye_letter",
                          "eye_results","eye_letter_results"]:
                    if k in ["eye_started","eye_done"]: st.session_state[k] = False
                    elif k in ["eye_line","eye_letter"]: st.session_state[k] = 0
                    else: st.session_state[k] = []
                st.rerun()
        with c2:
            rpt = f"""EYESIGHT TEST REPORT
====================
Result    : {a["status"]}
Condition : {a["condition"]}
Lines OK  : {correct}/{total}
Details   : {a["details"]}
Doctor    : {a["doctor"]}
Urgency   : {a["urgency"]}
Advice    : {" | ".join(a["advice"])}

Note: Basic screening only. See an eye doctor for proper diagnosis."""
            st.download_button("📄 Download Report", data=rpt,
                file_name="eye_test_report.txt", mime="text/plain", use_container_width=True)