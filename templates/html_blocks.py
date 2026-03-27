# templates/html_blocks.py
# All inline HTML/CSS blocks used by info_pages.py via components.html().
# Kept separate to keep the layout file clean and readable.

# ─── Shared base reset injected at the top of every block ───
_BASE = """
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');
*{box-sizing:border-box;margin:0;padding:0}
body{background:transparent;font-family:"Inter","Segoe UI",sans-serif;-webkit-font-smoothing:antialiased}
"""

# ═══════════════════════════════════════════════════════════════
# EMOTET STAGES FLOW  (used via st.markdown, not components.html)
# ═══════════════════════════════════════════════════════════════
EMOTET_STAGES_HTML = """
<div class="emotet-flow enhanced-flow">
    <div class="flow-step">
        <div class="flow-icon">📧</div>
        <div class="flow-title">1. Phishing Email</div>
        <div class="flow-desc">Victim receives a legitimate-looking email</div>
    </div>
    <div class="flow-connector"><div class="flow-line"></div><div class="flow-arrow">→</div></div>
    <div class="flow-step">
        <div class="flow-icon">📄</div>
        <div class="flow-title">2. Malicious Attachment</div>
        <div class="flow-desc">User opens the attachment and enables macros</div>
    </div>
    <div class="flow-connector"><div class="flow-line"></div><div class="flow-arrow">→</div></div>
    <div class="flow-step">
        <div class="flow-icon">🌐</div>
        <div class="flow-title">3. C2 Communication</div>
        <div class="flow-desc">Infected host establishes outbound contact with attacker servers</div>
    </div>
    <div class="flow-connector"><div class="flow-line"></div><div class="flow-arrow">→</div></div>
    <div class="flow-step">
        <div class="flow-icon">📡</div>
        <div class="flow-title">4. Beaconing</div>
        <div class="flow-desc">Periodic low-volume check-ins with external infrastructure</div>
    </div>
    <div class="flow-connector"><div class="flow-line"></div><div class="flow-arrow">→</div></div>
    <div class="flow-step">
        <div class="flow-icon">🕸️</div>
        <div class="flow-title">5. Botnet Expansion</div>
        <div class="flow-desc">Downloads additional payloads and supports further malicious activity</div>
    </div>
</div>
"""

# ═══════════════════════════════════════════════════════════════
# PROGRESSION BRIDGE  (Relationship page)
# ═══════════════════════════════════════════════════════════════
PROGRESSION_HTML = (
    "<style>"
    + _BASE
    + """
    .prog-wrap { padding: 4px 0 0 0; }

    .prog-labels { display: flex; justify-content: space-between; margin-bottom: 0.55rem; }
    .prog-label { display: inline-block; padding: 0.28rem 0.68rem; border-radius: 999px;
        font-size: 0.7rem; font-weight: 700; letter-spacing: 0.05em; text-transform: uppercase; }
    .prog-label-app { background: rgba(124,92,143,0.11); border: 1px solid rgba(124,92,143,0.20); color: #6B5A7D; }
    .prog-label-net { background: rgba(47,111,115,0.11); border: 1px solid rgba(47,111,115,0.20); color: #3B6F73; }

    .prog-flow { display: grid; grid-template-columns: 1fr 32px 1fr 32px 1fr 32px 1fr 32px 1fr;
        align-items: stretch; gap: 0; margin-bottom: 0.7rem; }

    .prog-card { position: relative; border-radius: 16px; padding: 0.9rem 0.85rem 0.85rem;
        background: linear-gradient(180deg, rgba(252,254,254,0.95), rgba(241,246,247,0.92));
        border: 1px solid rgba(157,176,183,0.30);
        box-shadow: 0 8px 20px rgba(16,24,40,0.045), 0 2px 6px rgba(92,72,125,0.03);
        transition: transform 0.22s ease, box-shadow 0.22s ease, border-color 0.22s ease;
        overflow: hidden; display: flex; flex-direction: column; }
    .prog-card::before { content: ""; position: absolute; top: 0; left: 0; right: 0; height: 3.5px; border-radius: 16px 16px 0 0; }
    .prog-card::after { content: ""; position: absolute; inset: 0; pointer-events: none; border-radius: 16px; opacity: 0.28;
        background-image: linear-gradient(rgba(124,92,143,0.06) 1px, transparent 1px),
            linear-gradient(90deg, rgba(124,92,143,0.06) 1px, transparent 1px);
        background-size: 20px 20px;
        mask-image: radial-gradient(ellipse at 70% 20%, black 0%, transparent 70%);
        -webkit-mask-image: radial-gradient(ellipse at 70% 20%, black 0%, transparent 70%); }
    .prog-card:hover { transform: translateY(-3px);
        box-shadow: 0 14px 28px rgba(16,24,40,0.07), 0 0 14px rgba(124,92,143,0.06);
        border-color: rgba(124,92,143,0.26); }

    .prog-card-1::before { background: linear-gradient(90deg, #7C5C8F, #8B6BA0); }
    .prog-card-2::before { background: linear-gradient(90deg, #8B6BA0, #6E8A8E); }
    .prog-card-3::before { background: linear-gradient(90deg, #6E8A8E, #4E8A8F); }
    .prog-card-4::before { background: linear-gradient(90deg, #4E8A8F, #3B8085); }
    .prog-card-5::before { background: linear-gradient(90deg, #3B8085, #2F6F73); }

    .prog-icon { position: relative; z-index: 1; width: 2.55rem; height: 2.55rem; border-radius: 50%;
        display: flex; align-items: center; justify-content: center; margin-bottom: 0.6rem;
        flex-shrink: 0; box-shadow: 0 4px 12px rgba(92,72,125,0.08); }
    .prog-icon svg { width: 1.15rem; height: 1.15rem; }

    .prog-card-1 .prog-icon { background: linear-gradient(135deg, rgba(124,92,143,0.18), rgba(124,92,143,0.10)); border: 1px solid rgba(124,92,143,0.22); }
    .prog-card-1 .prog-icon svg { stroke: #7C5C8F; fill: none; }
    .prog-card-2 .prog-icon { background: linear-gradient(135deg, rgba(110,98,138,0.16), rgba(110,98,138,0.08)); border: 1px solid rgba(110,98,138,0.20); }
    .prog-card-2 .prog-icon svg { stroke: #6E628A; fill: none; }
    .prog-card-3 .prog-icon { background: linear-gradient(135deg, rgba(78,120,124,0.16), rgba(78,120,124,0.08)); border: 1px solid rgba(78,120,124,0.20); }
    .prog-card-3 .prog-icon svg { stroke: #4E787C; fill: none; }
    .prog-card-4 .prog-icon { background: linear-gradient(135deg, rgba(59,128,133,0.16), rgba(59,128,133,0.08)); border: 1px solid rgba(59,128,133,0.20); }
    .prog-card-4 .prog-icon svg { stroke: #3B8085; fill: none; }
    .prog-card-5 .prog-icon { background: linear-gradient(135deg, rgba(47,111,115,0.18), rgba(47,111,115,0.10)); border: 1px solid rgba(47,111,115,0.22); }
    .prog-card-5 .prog-icon svg { stroke: #2F6F73; fill: none; }

    .prog-card-title { position: relative; z-index: 1; font-size: 0.92rem; font-weight: 700;
        color: #2E3A42; line-height: 1.18; margin-bottom: 0.38rem; letter-spacing: -0.01em; }
    .prog-card-text { position: relative; z-index: 1; font-size: 0.8rem; color: #5E6F78;
        line-height: 1.46; flex-grow: 1; }

    .prog-conn { display: flex; align-items: center; justify-content: center; position: relative; }
    .prog-conn-track { position: absolute; left: 0; right: 0; top: 50%; height: 2px; border-radius: 999px;
        background: rgba(157,176,183,0.22); overflow: hidden; }
    .prog-conn-track::after { content: ""; position: absolute; top: 0; bottom: 0; left: -10px;
        width: 10px; height: 100%; border-radius: 999px;
        background: linear-gradient(90deg, rgba(124,92,143,0.55), rgba(47,111,115,0.45));
        animation: dotSlide 1.8s ease-in-out infinite; }
    @keyframes dotSlide { 0%{left:-10px;opacity:0} 15%{opacity:1} 85%{opacity:1} 100%{left:calc(100% + 2px);opacity:0} }
    .prog-conn-chevron { position: relative; z-index: 1; font-size: 0.75rem; color: rgba(124,92,143,0.40); line-height: 1; }

    .prog-gradient-bar { height: 6px; border-radius: 999px; opacity: 0.35; position: relative; overflow: hidden;
        background: linear-gradient(90deg, #7C5C8F 0%, #8B6BA0 22%, #6E8A8E 44%, #4E8A8F 66%, #3B8085 82%, #2F6F73 100%); }
    .prog-gradient-bar::after { content: ""; position: absolute; top: 0; bottom: 0; width: 120px;
        background: linear-gradient(90deg, rgba(255,255,255,0) 0%, rgba(255,255,255,0.6) 50%, rgba(255,255,255,0) 100%);
        animation: shimmer 3.5s ease-in-out infinite; }
    @keyframes shimmer { 0%{left:-120px} 100%{left:calc(100% + 40px)} }

    @media (max-width: 1100px) {
        .prog-flow { grid-template-columns: 1fr; gap: 0; }
        .prog-conn { min-height: 26px; width: 100%; }
        .prog-conn-track { left: 50%; right: auto; top: 0; bottom: 0; width: 2px; height: 100%; }
        .prog-conn-track::after { top: -10px; left: 0; width: 100%; height: 10px; animation: dotSlideV 1.8s ease-in-out infinite; }
        @keyframes dotSlideV { 0%{top:-10px;opacity:0} 15%{opacity:1} 85%{opacity:1} 100%{top:calc(100% + 2px);opacity:0} }
        .prog-conn-chevron { transform: rotate(90deg); }
        .prog-labels { display: none; }
        .prog-gradient-bar { display: none; }
    }
</style>
<div class="prog-wrap">
    <div class="prog-labels">
        <span class="prog-label prog-label-app">Application Layer</span>
        <span class="prog-label prog-label-net">Network Behaviour Layer</span>
    </div>
    <div class="prog-flow">
        <div class="prog-card prog-card-1">
            <div class="prog-icon"><svg viewBox="0 0 24 24" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M7 20l4-16m2 16l4-16"/><path d="M3 8h18M3 16h18"/></svg></div>
            <div class="prog-card-title">SQLi Entry</div>
            <div class="prog-card-text">The attacker identifies a vulnerable input field and injects malicious SQL to test whether the backend can be manipulated.</div>
        </div>
        <div class="prog-conn"><div class="prog-conn-track"></div><span class="prog-conn-chevron">›</span></div>
        <div class="prog-card prog-card-2">
            <div class="prog-icon"><svg viewBox="0 0 24 24" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><ellipse cx="12" cy="5" rx="9" ry="3"/><path d="M3 5v14c0 1.66 4.03 3 9 3s9-1.34 9-3V5"/><path d="M3 12c0 1.66 4.03 3 9 3s9-1.34 9-3"/></svg></div>
            <div class="prog-card-title">DB Access &amp; Privilege Escalation</div>
            <div class="prog-card-text">Successful injection provides database access and may allow privilege escalation toward broader system control.</div>
        </div>
        <div class="prog-conn"><div class="prog-conn-track"></div><span class="prog-conn-chevron">›</span></div>
        <div class="prog-card prog-card-3">
            <div class="prog-icon"><svg viewBox="0 0 24 24" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><rect x="2" y="4" width="20" height="16" rx="2"/><path d="M6 12l4-4M6 12l4 4"/><path d="M14 16h4"/></svg></div>
            <div class="prog-card-title">OS Command Execution</div>
            <div class="prog-card-text">System-level command execution bridges the transition from application-layer compromise to host-level control.</div>
        </div>
        <div class="prog-conn"><div class="prog-conn-track"></div><span class="prog-conn-chevron">›</span></div>
        <div class="prog-card prog-card-4">
            <div class="prog-icon"><svg viewBox="0 0 24 24" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M12 2L2 7l10 5 10-5-10-5z"/><path d="M2 17l10 5 10-5"/><path d="M2 12l10 5 10-5"/></svg></div>
            <div class="prog-card-title">Malware Execution</div>
            <div class="prog-card-text">External malware is downloaded and executed on the compromised server, creating a persistent foothold.</div>
        </div>
        <div class="prog-conn"><div class="prog-conn-track"></div><span class="prog-conn-chevron">›</span></div>
        <div class="prog-card prog-card-5">
            <div class="prog-icon"><svg viewBox="0 0 24 24" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M12 12m-2 0a2 2 0 1 0 4 0 2 2 0 1 0-4 0"/><path d="M12 2v4m0 12v4"/><path d="M4.93 4.93l2.83 2.83m8.48 8.48l2.83 2.83"/><path d="M2 12h4m12 0h4"/><path d="M4.93 19.07l2.83-2.83m8.48-8.48l2.83-2.83"/></svg></div>
            <div class="prog-card-title">Emotet-Like Behaviour</div>
            <div class="prog-card-text">The infected host begins beaconing, communicating with C2 infrastructure, and exhibiting detectable traffic patterns.</div>
        </div>
    </div>
    <div class="prog-gradient-bar"></div>
</div>
"""
)

# ═══════════════════════════════════════════════════════════════
# PIPELINE PAGE BLOCKS
# ═══════════════════════════════════════════════════════════════

DATASET_CARDS_HTML = (
    "<style>"
    + _BASE
    + """
    .ds-row{display:grid;grid-template-columns:1fr 1fr 1fr;gap:10px;margin-top:10px}
    .ds-card{border-radius:14px;padding:0.7rem 0.85rem 0.65rem;
        background:linear-gradient(135deg,#F6F0FB,#EDE5F6);
        border:1px solid rgba(138,112,184,0.28);box-shadow:0 5px 14px rgba(92,72,125,0.07)}
    .ds-label{font-size:0.64rem;font-weight:700;color:#6C5A7E;text-transform:uppercase;letter-spacing:0.05em;margin-bottom:0.1rem}
    .ds-value{font-size:1.4rem;font-weight:800;color:#3D2B5A;letter-spacing:-0.03em;line-height:1.1;font-variant-numeric:tabular-nums}
    .ds-sub{font-size:0.7rem;color:#493F57;margin-top:0.05rem;line-height:1.25}
    .ds-detail{font-size:0.68rem;color:#5E6F78;line-height:1.3;margin-top:0.25rem}
</style>
<div class="ds-row">
    <div class="ds-card">
        <div class="ds-label">SQLi — Kaggle</div>
        <div class="ds-value">30,919</div>
        <div class="ds-sub">labelled entries</div>
        <div class="ds-detail">19,537 benign · 11,382 malicious</div>
    </div>
    <div class="ds-card">
        <div class="ds-label">Emotet — Unit42 PCAPs</div>
        <div class="ds-value">555</div>
        <div class="ds-sub">behavioural windows</div>
        <div class="ds-detail">5 infection traces + Stratosphere normals</div>
    </div>
    <div class="ds-card">
        <div class="ds-label">External Validation — Zenodo</div>
        <div class="ds-value">20,000</div>
        <div class="ds-sub">held-out SQLi evaluation</div>
        <div class="ds-detail">10k benign · 10k malicious (never trained)</div>
    </div>
</div>
"""
)

DISTRIBUTION_BAR_HTML = (
    "<style>"
    + _BASE
    + """
    .dist-bar{display:flex;border-radius:8px;overflow:hidden;height:22px}
    .dist-seg{display:flex;align-items:center;justify-content:center;font-size:0.64rem;font-weight:700;color:#fff;letter-spacing:0.02em}
    .dist-seg-normal{background:#8B9DA6;flex:22358}
    .dist-seg-sqli{background:#7C5C8F;flex:11382}
    .dist-seg-emotet{background:#2F6F73;flex:555;min-width:48px}
    .dist-legend{display:flex;gap:1.2rem;margin-top:6px}
    .dist-legend-item{display:flex;align-items:center;gap:6px;font-size:0.92rem;color:#3D4F5A;font-weight:600}
    .dist-dot{width:11px;height:11px;border-radius:3px}
</style>
<div class="dist-bar">
    <div class="dist-seg dist-seg-normal">Normal 65%</div>
    <div class="dist-seg dist-seg-sqli">SQLi 33%</div>
    <div class="dist-seg dist-seg-emotet">1.6%</div>
</div>
<div class="dist-legend">
    <div class="dist-legend-item"><div class="dist-dot" style="background:#8B9DA6"></div>Normal (22,358)</div>
    <div class="dist-legend-item"><div class="dist-dot" style="background:#7C5C8F"></div>SQLi (11,382)</div>
    <div class="dist-legend-item"><div class="dist-dot" style="background:#2F6F73"></div>Emotet (555)</div>
</div>
"""
)

FEATURE_CHIPS_HTML = (
    "<style>"
    + _BASE
    + """
    .fe-section{margin-bottom:1.1rem}
    .fe-section:last-child{margin-bottom:0}
    .fe-heading{font-size:0.92rem;font-weight:700;color:#3D4F5A;margin-bottom:0.38rem;display:flex;align-items:center;gap:0.35rem}
    .fe-count{display:inline-block;padding:0.14rem 0.48rem;border-radius:999px;font-size:0.72rem;font-weight:700;letter-spacing:0.03em}
    .fe-count-sqli{background:rgba(124,92,143,0.12);color:#6B5A7D}
    .fe-count-emotet{background:rgba(47,111,115,0.12);color:#2F6F73}
    .fe-chips{display:flex;flex-wrap:wrap;gap:6px}
    .fe-chip{display:inline-block;padding:0.3rem 0.6rem;border-radius:8px;font-size:0.88rem;font-weight:600;line-height:1;font-family:"SF Mono","Fira Code","Consolas",monospace}
    .fe-chip-sqli{background:rgba(248,245,252,0.7);border:1px solid rgba(138,112,184,0.20);color:#5A2D91}
    .fe-chip-emotet{background:rgba(235,248,248,0.7);border:1px solid rgba(47,111,115,0.20);color:#2F6F73}
    .fe-desc{font-size:0.86rem;color:#5E6F78;line-height:1.4;margin-top:0.3rem}
</style>
<div class="fe-section">
    <div class="fe-heading">SQLi Features <span class="fe-count fe-count-sqli">9 structural</span></div>
    <div class="fe-chips">
        <span class="fe-chip fe-chip-sqli">Sentence Length</span>
        <span class="fe-chip fe-chip-sqli">AND Count</span>
        <span class="fe-chip fe-chip-sqli">OR Count</span>
        <span class="fe-chip fe-chip-sqli">UNION Count</span>
        <span class="fe-chip fe-chip-sqli">Single Quote</span>
        <span class="fe-chip fe-chip-sqli">Double Quote</span>
        <span class="fe-chip fe-chip-sqli">Constant Values</span>
        <span class="fe-chip fe-chip-sqli">Parentheses</span>
        <span class="fe-chip fe-chip-sqli">Special Chars</span>
    </div>
    <div class="fe-desc">Structural composition of input strings — how the query is built rather than what keywords it contains.</div>
</div>
<div class="fe-section">
    <div class="fe-heading">Emotet Features <span class="fe-count fe-count-emotet">17 behavioural</span></div>
    <div class="fe-chips">
        <span class="fe-chip fe-chip-emotet">conn_count</span>
        <span class="fe-chip fe-chip-emotet">unique_dst_ip</span>
        <span class="fe-chip fe-chip-emotet">unique_dst_port</span>
        <span class="fe-chip fe-chip-emotet">mean_duration</span>
        <span class="fe-chip fe-chip-emotet">std_duration</span>
        <span class="fe-chip fe-chip-emotet">mean_orig_bytes</span>
        <span class="fe-chip fe-chip-emotet">mean_resp_bytes</span>
        <span class="fe-chip fe-chip-emotet">mean_orig_pkts</span>
        <span class="fe-chip fe-chip-emotet">mean_resp_pkts</span>
        <span class="fe-chip fe-chip-emotet">tcp_ratio</span>
        <span class="fe-chip fe-chip-emotet">udp_ratio</span>
        <span class="fe-chip fe-chip-emotet">dns_ratio</span>
        <span class="fe-chip fe-chip-emotet">ssl_ratio</span>
        <span class="fe-chip fe-chip-emotet">http_ratio</span>
        <span class="fe-chip fe-chip-emotet">rej_ratio</span>
        <span class="fe-chip fe-chip-emotet">rst_ratio</span>
        <span class="fe-chip fe-chip-emotet">interarrival_std</span>
    </div>
    <div class="fe-desc">Derived from Zeek connection logs — traffic volume, flow statistics, protocol ratios, and timing variability.</div>
</div>
"""
)

MODEL_COMPARISON_HTML = (
    "<style>"
    + _BASE
    + """
    .mc-row{display:grid;grid-template-columns:1fr 1fr;gap:10px;margin-top:10px}
    .mc-card{border-radius:14px;padding:0.75rem 0.9rem 0.7rem;border:1px solid rgba(157,176,183,0.26);box-shadow:0 5px 12px rgba(16,24,40,0.03);position:relative;overflow:hidden}
    .mc-card::before{content:"";position:absolute;top:0;left:0;right:0;height:3px}
    .mc-winner{background:linear-gradient(180deg,rgba(47,111,115,0.05),rgba(252,254,254,0.96))}
    .mc-winner::before{background:linear-gradient(90deg,#2F6F73,#3B8085)}
    .mc-loser{background:linear-gradient(180deg,rgba(180,175,185,0.05),rgba(252,254,254,0.96))}
    .mc-loser::before{background:#B4AFB9}
    .mc-top{display:flex;align-items:center;gap:0.5rem;margin-bottom:0.45rem}
    .mc-badge{padding:0.15rem 0.45rem;border-radius:999px;font-size:0.56rem;font-weight:700;letter-spacing:0.04em;text-transform:uppercase}
    .mc-winner .mc-badge{background:rgba(47,111,115,0.12);color:#2F6F73;border:1px solid rgba(47,111,115,0.18)}
    .mc-loser .mc-badge{background:rgba(140,140,150,0.10);color:#787480;border:1px solid rgba(140,140,150,0.16)}
    .mc-name{font-size:0.95rem;font-weight:800;color:#2E3A42;letter-spacing:-0.02em}
    .mc-metrics{display:flex;gap:1rem}
    .mc-ml{font-size:0.56rem;font-weight:700;color:#25282C;text-transform:uppercase;letter-spacing:0.04em}
    .mc-mv{font-size:1rem;font-weight:800;color:#2E3A42;font-variant-numeric:tabular-nums;letter-spacing:-0.01em}
    .mc-loser .mc-mv{color:#787480}
</style>
<div class="mc-row">
    <div class="mc-card mc-winner">
        <div class="mc-top"><div class="mc-name">Random Forest</div><div class="mc-badge">Selected</div></div>
        <div class="mc-metrics">
            <div><div class="mc-ml">Macro-F1</div><div class="mc-mv">0.970</div></div>
            <div><div class="mc-ml">F1 SQLi</div><div class="mc-mv">0.991</div></div>
            <div><div class="mc-ml">F1 Emotet</div><div class="mc-mv">0.926</div></div>
        </div>
    </div>
    <div class="mc-card mc-loser">
        <div class="mc-top"><div class="mc-name">Logistic Regression</div><div class="mc-badge">Compared</div></div>
        <div class="mc-metrics">
            <div><div class="mc-ml">Macro-F1</div><div class="mc-mv">0.786</div></div>
            <div><div class="mc-ml">F1 SQLi</div><div class="mc-mv">0.924</div></div>
            <div><div class="mc-ml">F1 Emotet</div><div class="mc-mv">0.501</div></div>
        </div>
    </div>
</div>
"""
)

PARAM_CHIPS_HTML = """
<div style="display:flex; flex-wrap:wrap; gap:6px; margin-top:0.2rem; margin-bottom:0.5rem;">
    <span style="display:inline-flex;align-items:center;gap:4px;padding:0.22rem 0.55rem;border-radius:8px;background:rgba(248,245,252,0.7);border:1px solid rgba(138,112,184,0.20);font-size:0.76rem;color:#4D5F69;">
        <strong style="color:#5A2D91;font-family:'SF Mono','Fira Code',monospace;font-weight:700;">n_estimators</strong>&nbsp;300</span>
    <span style="display:inline-flex;align-items:center;gap:4px;padding:0.22rem 0.55rem;border-radius:8px;background:rgba(248,245,252,0.7);border:1px solid rgba(138,112,184,0.20);font-size:0.76rem;color:#4D5F69;">
        <strong style="color:#5A2D91;font-family:'SF Mono','Fira Code',monospace;font-weight:700;">max_depth</strong>&nbsp;None</span>
    <span style="display:inline-flex;align-items:center;gap:4px;padding:0.22rem 0.55rem;border-radius:8px;background:rgba(248,245,252,0.7);border:1px solid rgba(138,112,184,0.20);font-size:0.76rem;color:#4D5F69;">
        <strong style="color:#5A2D91;font-family:'SF Mono','Fira Code',monospace;font-weight:700;">min_samples_leaf</strong>&nbsp;1</span>
    <span style="display:inline-flex;align-items:center;gap:4px;padding:0.22rem 0.55rem;border-radius:8px;background:rgba(248,245,252,0.7);border:1px solid rgba(138,112,184,0.20);font-size:0.76rem;color:#4D5F69;">
        <strong style="color:#5A2D91;font-family:'SF Mono','Fira Code',monospace;font-weight:700;">min_samples_split</strong>&nbsp;2</span>
    <span style="display:inline-flex;align-items:center;gap:4px;padding:0.22rem 0.55rem;border-radius:8px;background:rgba(248,245,252,0.7);border:1px solid rgba(138,112,184,0.20);font-size:0.76rem;color:#4D5F69;">
        <strong style="color:#5A2D91;font-family:'SF Mono','Fira Code',monospace;font-weight:700;">max_features</strong>&nbsp;"sqrt"</span>
    <span style="display:inline-flex;align-items:center;gap:4px;padding:0.22rem 0.55rem;border-radius:8px;background:rgba(248,245,252,0.7);border:1px solid rgba(138,112,184,0.20);font-size:0.76rem;color:#4D5F69;">
        <strong style="color:#5A2D91;font-family:'SF Mono','Fira Code',monospace;font-weight:700;">class_weight</strong>&nbsp;"balanced"</span>
</div>
"""

VALIDATION_CARDS_HTML = (
    "<style>"
    + _BASE
    + """
    .vg{display:grid;grid-template-columns:1fr 1fr 1fr;gap:8px}
    .vc{border-radius:12px;padding:0.7rem 0.8rem 0.65rem;background:linear-gradient(180deg,rgba(252,254,254,0.95),rgba(241,246,247,0.92));border:1px solid rgba(157,176,183,0.24);box-shadow:0 3px 10px rgba(16,24,40,0.03);position:relative;overflow:hidden}
    .vc::before{content:"";position:absolute;top:0;left:0;right:0;height:2.5px;background:linear-gradient(90deg,rgba(124,92,143,0.42),rgba(47,111,115,0.32))}
    .vc-icon{width:1.7rem;height:1.7rem;border-radius:50%;display:flex;align-items:center;justify-content:center;margin-bottom:0.32rem;background:linear-gradient(135deg,rgba(124,92,143,0.11),rgba(47,111,115,0.07));border:1px solid rgba(124,92,143,0.14)}
    .vc-icon svg{width:0.85rem;height:0.85rem;stroke:#5A4878;fill:none;stroke-width:2;stroke-linecap:round;stroke-linejoin:round}
    .vc-title{font-size:0.98rem;font-weight:700;color:#2E3A42;margin-bottom:0.12rem;line-height:1.2}
    .vc-desc{font-size:0.9rem;color:#374247;line-height:1.35}
</style>
<div class="vg">
    <div class="vc"><div class="vc-icon"><svg viewBox="0 0 24 24"><path d="M4 4h16v16H4z"/><path d="M4 12h16"/><path d="M12 4v16"/></svg></div><div class="vc-title">5-Fold Stratified CV</div><div class="vc-desc">Stability across data partitions</div></div>
    <div class="vc"><div class="vc-icon"><svg viewBox="0 0 24 24"><path d="M3 12h4l3-9 4 18 3-9h4"/></svg></div><div class="vc-title">Train-Test Gap</div><div class="vc-desc">Overfitting measurement</div></div>
    <div class="vc"><div class="vc-icon"><svg viewBox="0 0 24 24"><rect x="3" y="3" width="7" height="7"/><rect x="14" y="3" width="7" height="7"/><rect x="3" y="14" width="7" height="7"/><rect x="14" y="14" width="7" height="7"/></svg></div><div class="vc-title">Group-Aware Holdout</div><div class="vc-desc">Prevent capture-level leakage</div></div>
    <div class="vc"><div class="vc-icon"><svg viewBox="0 0 24 24"><path d="M21 12a9 9 0 11-6.22-8.56"/><path d="M21 3v6h-6"/></svg></div><div class="vc-title">External Validation</div><div class="vc-desc">Independent Zenodo test set</div></div>
    <div class="vc"><div class="vc-icon"><svg viewBox="0 0 24 24"><path d="M16 3h5v5"/><path d="M8 3H3v5"/><path d="M12 22v-6"/><path d="M21 3l-9 9"/><path d="M3 3l9 9"/></svg></div><div class="vc-title">Model Comparison</div><div class="vc-desc">RF vs LR vs Decision Tree</div></div>
    <div class="vc"><div class="vc-icon"><svg viewBox="0 0 24 24"><path d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10z"/></svg></div><div class="vc-title">Permutation Importance</div><div class="vc-desc">No spurious feature shortcuts</div></div>
</div>
"""
)