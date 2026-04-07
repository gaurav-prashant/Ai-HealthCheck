# ============================================================
# styles.py — "Same to Same" Light UI (v8.0)
# Matches "Same to Same" Mockup Image exactly
# ============================================================

def get_css():
    return """
<style>
@import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@300;400;500;600;700;800&family=Outfit:wght@400;600;800&display=swap');

:root {
    --p-blue: #0369a1;
    --p-sky: #eff6ff;
    --p-teal: #0891b2;
    --card-bg: #ffffff;
    --card-shadow: 0 4px 6px -1px rgb(0 0 0 / 0.05), 0 2px 4px -2px rgb(0 0 0 / 0.05);
    --text-main: #0f172a;
    --text-mute: #64748b;
}

/* ── GLOBAL RESET ── */
* { font-family: 'Plus Jakarta Sans', sans-serif !important; }

.stApp {
    background: #f8fafc !important;
    background-image: radial-gradient(circle at 0% 0%, #eff6ff 0%, #ffffff 100%) !important;
    color: var(--text-main);
}

.block-container { padding: 1.5rem 1rem !important; max-width: 1300px !important; }

/* ── BENTO CARDS ── */
.bento-card {
    background: var(--card-bg);
    border: 1px solid #f1f5f9;
    border-radius: 20px;
    padding: 18px;
    box-shadow: var(--card-shadow);
    height: 100%;
    margin-bottom: 0px;
}

.card-title {
    font-family: 'Outfit', sans-serif !important;
    font-size: 1rem;
    font-weight: 700;
    color: #475569;
    margin-bottom: 12px;
    display: flex;
    justify-content: space-between;
}

/* ── GAUGE / METER ── */
.gauge-container { text-align: center; padding: 15px 0; }
.gauge-val { font-size: 2.2rem; font-weight: 800; color: #10b981; line-height: 1; }
.gauge-lab { font-size: 0.75rem; color: #94a3b8; }

/* ── MEDICINE ITEM ── */
.med-row {
    background: #f8fafc;
    border-radius: 12px;
    padding: 10px 14px;
    display: flex;
    align-items: center;
    gap: 12px;
    margin-bottom: 8px;
    border: 1px solid #f1f5f9;
}
.med-info { flex: 1; }
.med-name { font-size: 0.85rem; font-weight: 700; color: #0f172a; }
.med-details { font-size: 0.7rem; color: #94a3b8; }
.med-check { 
    width: 22px; height: 22px; 
    border-radius: 50%; border: 2px solid #cbd5e1;
    display: flex; align-items: center; justify-content: center;
}
.med-check.active { background: #10b981; border-color: #10b981; color: white; font-size: 0.7rem; }

/* ── ICON BUTTONS ── */
.btn-grid { display: grid; grid-template-columns: repeat(2, 1fr); gap: 8px; }
.btn-tile {
    background: white; border: 1px solid #e2e8f0;
    border-radius: 12px; padding: 12px 10px;
    text-align: center; cursor: pointer;
}
.btn-tile:hover { background: #f8fafc; border-color: #cbd5e1; }

.btn-upload {
    background: #0369a1; color: white;
    font-size: 0.75rem; font-weight: 700;
    border-radius: 6px; padding: 8px;
    margin-top: 8px; text-align: center;
    cursor: pointer;
}

/* ── BOTTOM FOOTER ── */
.footer-nav {
    position: fixed; bottom: 0; left: 0; right: 0;
    background: white; border-top: 1px solid #f1f5f9;
    padding: 10px 20px; display: flex; justify-content: space-around;
    z-index: 999;
}
.foot-item { text-align: center; color: #94a3b8; font-size: 1.4rem; cursor: pointer; }
.foot-item.active { color: #0369a1; }
.foot-label { display: block; font-size: 0.6rem; margin-top: 2px; font-weight: 600; }

/* ── STREAMLIT OVERRIDES ── */
.stButton > button {
    background: white !important; border: 1px solid #e2e8f0 !important;
    border-radius: 10px !important; color: #475569 !important;
    font-size: 0.85rem !important; font-weight: 700 !important;
}
.stTextInput > div > div > input {
    background: #f8fafc !important; border: 1px solid #f1f5f9 !important;
    border-radius: 8px !important; font-size: 0.85rem !important;
}

</style>
"""
