import streamlit as st
import streamlit.components.v1 as components
from textwrap import dedent

from templates.page_blocks import render_info_box_title


# ═══════════════════════════════════════════════════════════════
# QUESTION DATA
# ═══════════════════════════════════════════════════════════════

SQLI_QUESTIONS = [
    {
        "id": "sq1",
        "q": "Which feature was identified as the most influential in the SQLi Random Forest model based on impurity-based importance?",
        "options": ["Sentence Length", "OR Count", "Constant Value Count", "UNION Count"],
        "answer": 2,
        "explanation": "Constant Value Count had the highest impurity-based importance (0.453), as malicious payloads frequently contain numeric literals used in conditions like OR 1=1 or UNION SELECT 1,2,3.",
    },
    {
        "id": "sq2",
        "q": "What is the purpose of the -- symbol in a SQL injection payload such as admin' OR 1=1 --?",
        "options": [
            "It concatenates two SQL queries",
            "It comments out the rest of the query",
            "It encrypts the injected payload",
            "It returns all database columns",
        ],
        "answer": 1,
        "explanation": "The double-dash (--) is a SQL comment marker. It causes the database to ignore everything after it, effectively removing the password check from the query.",
    },
    {
        "id": "sq3",
        "q": "Why was Macro-F1 chosen as the primary evaluation metric instead of accuracy?",
        "options": [
            "Accuracy can't handle multi-class",
            "Macro-F1 weights by sample count",
            "Accuracy inflates under class imbalance",
            "F1 is always higher than accuracy",
        ],
        "answer": 2,
        "explanation": "In an imbalanced dataset, a model can achieve high accuracy by predicting the majority class. Macro-F1 averages F1 equally across classes, ensuring poor minority-class performance is not hidden.",
    },
    {
        "id": "sq4",
        "q": "Why is relying on structural features rather than SQL keywords important for model robustness?",
        "options": [
            "Keywords don't appear in payloads",
            "Structural signals generalise better",
            "Firewalls always filter keywords",
            "The dataset has no SQL keywords",
        ],
        "answer": 1,
        "explanation": "Structural features capture how a query is constructed rather than which tokens appear. This makes the model less vulnerable to keyword obfuscation and more likely to generalise to unseen injection variants.",
    },
    {
        "id": "sq5",
        "q": "What did external validation on the Zenodo dataset reveal about the model?",
        "options": [
            "Identical performance to internal test",
            "Performance decreased (distribution shift)",
            "External dataset was too small",
            "Higher performance on external data",
        ],
        "answer": 1,
        "explanation": "External F1 dropped to ~0.78 vs 0.99 internally. The Zenodo dataset contains full SQL statements and different obfuscation styles, exposing sensitivity to structural differences between datasets.",
    },
    {
        "id": "sq6",
        "q": "Which feature caused the largest F1 drop in permutation importance analysis?",
        "options": [
            "Sentence Length",
            "AND Count",
            "Parentheses Count",
            "Special Characters Total",
        ],
        "answer": 2,
        "explanation": "Parentheses Count produced the largest F1 drop (~0.298), slightly exceeding Constant Value Count (~0.294). This highlights cardinality bias in impurity-based measures.",
    },
]

EMOTET_QUESTIONS = [
    {
        "id": "eq1",
        "q": "How does Emotet primarily spread to victim machines?",
        "options": [
            "SQL injection on web servers",
            "Phishing emails with malicious attachments",
            "Brute-force attacks on SSH",
            "DNS poisoning",
        ],
        "answer": 1,
        "explanation": "Emotet spreads through phishing emails with weaponised attachments (typically Word documents with macros). When opened and macros enabled, the infection chain begins.",
    },
    {
        "id": "eq2",
        "q": "What is beaconing in Emotet's network behaviour?",
        "options": [
            "Scanning for open ports",
            "Periodic check-ins with C2 servers",
            "Broadcasting malware on the LAN",
            "Encrypting victim files",
        ],
        "answer": 1,
        "explanation": "Beaconing is the persistent, low-volume communication where the infected host regularly contacts its C2 server. This produces distinctive patterns: regular timing, consistent packet sizes, and repeated connections.",
    },
    {
        "id": "eq3",
        "q": "Why does Emotet use hardcoded IP addresses instead of domain names for C2?",
        "options": [
            "IPs are easier to remember",
            "It works even if DNS is blocked",
            "Domains aren't supported",
            "IPs are faster to connect to",
        ],
        "answer": 1,
        "explanation": "Hardcoded IPs let Emotet communicate without DNS resolution, so it can phone home even when DNS is blocked, monitored, or filtered by security tools.",
    },
    {
        "id": "eq4",
        "q": "What makes static binary analysis unreliable for Emotet detection?",
        "options": [
            "Binaries are too large",
            "Obfuscation makes it look broken on disk",
            "Emotet has no binary files",
            "Tools can't read Windows executables",
        ],
        "answer": 1,
        "explanation": "Emotet uses obfuscation and runtime reconstruction techniques that make static binary analysis less reliable, while its network behaviour remains more stable and observable for detection.",
    },
    {
        "id": "eq5",
        "q": "Why was class_weight='balanced' used for the unified model?",
        "options": [
            "Faster inference speed",
            "Higher penalty for rare Emotet errors",
            "Fewer features needed",
            "Forces majority-class predictions",
        ],
        "answer": 1,
        "explanation": "Emotet has only 555 samples vs 22,358 Normal and 11,382 SQLi. Balanced weighting increases the cost of misclassifying rare classes, preventing the model from ignoring Emotet.",
    },
    {
        "id": "eq6",
        "q": "What was the purpose of group-aware holdout for Emotet validation?",
        "options": [
            "Test a different ML algorithm",
            "Exclude entire PCAPs to prevent leakage",
            "Increase Emotet training samples",
            "Remove duplicate dataset rows",
        ],
        "answer": 1,
        "explanation": "Windows from the same PCAP share traffic patterns. Group holdout ensures all rows from a capture go into either train or test, preventing inflated performance from capture-specific patterns.",
    },
]

COMBINED_QUESTIONS = [
    {
        "id": "cq1",
        "q": "Why combine SQLi and Emotet into one unified model instead of two separate classifiers?",
        "options": [
            "Saves storage space",
            "Forces learning inter-attack distinctions",
            "Binary classifiers can't use tabular data",
            "The attacks always co-occur",
        ],
        "answer": 1,
        "explanation": "A unified model must distinguish Normal vs SQLi, Normal vs Emotet, and SQLi vs Emotet, learning structural differences between attack paradigms rather than only anomaly detection.",
    },
    {
        "id": "cq2",
        "q": "How does the unified dataset handle SQLi and Emotet having different feature families?",
        "options": [
            "Only shared features are kept",
            "PCA combines the features",
            "Cross-domain features are filled with zeros",
            "The model auto-ignores irrelevant features",
        ],
        "answer": 2,
        "explanation": "All 26 features (9 SQLi + 17 Emotet) are present. For each row, the other domain's features are zero-filled. A frozen master feature list ensures consistent schema ordering.",
    },
    {
        "id": "cq3",
        "q": "How might a SQL injection attack lead to Emotet-like network behaviour?",
        "options": [
            "SQLi directly installs Emotet in the browser",
            "SQLi escalates to OS commands, enabling malware and C2",
            "Emotet uses SQLi for credential theft",
            "No connection exists between them",
        ],
        "answer": 1,
        "explanation": "An attacker gaining database privileges through SQLi can leverage stored procedures to execute OS commands, download malware, and establish C2 communication, bridging application-layer exploitation to network-level compromise.",
    },
]

ALL_SECTIONS = [
    ("SQL Injection", "sqli", SQLI_QUESTIONS),
    ("Emotet", "emotet", EMOTET_QUESTIONS),
    ("Combined — SQLi & Emotet", "combined", COMBINED_QUESTIONS),
]

_ACCENTS = {
    "sqli": {
        "grad": "linear-gradient(135deg, #7C5C8F, #8B6BA0)",
        "bg": "linear-gradient(135deg, rgba(124,92,143,0.10), rgba(140,107,170,0.06)) !important",
        "stripe": "linear-gradient(90deg, #7C5C8F, #8B6BA0)",
        "badge_bg": "rgba(124,92,143,0.12)",
        "badge_c": "#6B5A7D",
        "badge_b": "rgba(124,92,143,0.22)",
        "num_bg": "linear-gradient(135deg, rgba(124,92,143,0.16), rgba(124,92,143,0.08))",
        "num_b": "rgba(124,92,143,0.24)",
        "num_c": "#6B5A7D",
    },
    "emotet": {
        "grad": "linear-gradient(135deg, #2F6F73, #3B8085)",
        "bg": "linear-gradient(135deg, rgba(47,111,115,0.09), rgba(60,140,145,0.05)) !important",
        "stripe": "linear-gradient(90deg, #2F6F73, #3B8085)",
        "badge_bg": "rgba(47,111,115,0.12)",
        "badge_c": "#2F6F73",
        "badge_b": "rgba(47,111,115,0.22)",
        "num_bg": "linear-gradient(135deg, rgba(47,111,115,0.16), rgba(47,111,115,0.08))",
        "num_b": "rgba(47,111,115,0.24)",
        "num_c": "#2F6F73",
    },
    "combined": {
        "grad": "linear-gradient(135deg, #5A2D91, #2F6F73)",
        "bg": "linear-gradient(135deg, rgba(90,45,145,0.08), rgba(47,111,115,0.06)) !important",
        "stripe": "linear-gradient(90deg, #7C5C8F, #2F6F73)",
        "badge_bg": "rgba(90,45,145,0.10)",
        "badge_c": "#5A2D91",
        "badge_b": "rgba(90,45,145,0.20)",
        "num_bg": "linear-gradient(135deg, rgba(90,45,145,0.14), rgba(47,111,115,0.10))",
        "num_b": "rgba(90,45,145,0.22)",
        "num_c": "#5A2D91",
    },
}


# ═══════════════════════════════════════════════════════════════
# QUESTION CARD
# ═══════════════════════════════════════════════════════════════

def _render_q(q: dict, index: int, section_id: str) -> bool:
    """Render one question inside a column. Returns True if correct."""
    key = q["id"]
    state_key = f"quiz_{key}"
    a = _ACCENTS[section_id]

    answered = state_key in st.session_state
    selected = st.session_state.get(state_key, None)

    st.markdown(
        f"""
        <div style="display:flex;align-items:flex-start;gap:0.55rem;margin-bottom:0.58rem;">
            <span style="display:inline-flex;align-items:center;justify-content:center;flex-shrink:0;
                width:2rem;height:2rem;border-radius:50%;font-size:0.82rem;font-weight:800;
                background:{a['num_bg']};border:1.5px solid {a['num_b']};color:{a['num_c']};">
                {index}
            </span>
            <span style="font-size:0.95rem;font-weight:600;color:#2E3A42;line-height:1.42;padding-top:0.15rem;">
                {q["q"]}
            </span>
        </div>
        """,
        unsafe_allow_html=True,
    )

    if not answered:
        st.markdown(
            """
            <style>
            div[class*="st-key-qc_"] .stButton{
                margin-top:-4px !important;
                margin-bottom:-4px !important;
            }
            </style>
            <div style="margin-left:2.7rem;">
            """,
            unsafe_allow_html=True,
        )
        for i, option in enumerate(q["options"]):
            if st.button(option, key=f"{key}_o{i}", use_container_width=False):
                st.session_state[state_key] = i
                st.rerun()
        st.markdown("</div>", unsafe_allow_html=True)
    else:
        correct = q["answer"]
        is_correct = selected == correct

        for i, option in enumerate(q["options"]):
            if i == correct:
                st.markdown(
                    f'<div style="margin-left:2.7rem;padding:0.44rem 0.8rem;border-radius:10px;margin-bottom:6px;'
                    f'background:rgba(47,111,115,0.08);border:1.5px solid rgba(47,111,115,0.30);'
                    f'font-size:0.88rem;color:#23605F;font-weight:600;line-height:1.4;">✓ {option}</div>',
                    unsafe_allow_html=True,
                )
            elif i == selected and not is_correct:
                st.markdown(
                    f'<div style="margin-left:2.7rem;padding:0.44rem 0.8rem;border-radius:10px;margin-bottom:6px;'
                    f'background:rgba(180,60,60,0.06);border:1.5px solid rgba(180,60,60,0.25);'
                    f'font-size:0.88rem;color:#7A3030;font-weight:600;line-height:1.4;">✗ {option}</div>',
                    unsafe_allow_html=True,
                )
            else:
                st.markdown(
                    f'<div style="margin-left:2.7rem;padding:0.44rem 0.8rem;border-radius:10px;margin-bottom:6px;'
                    f'background:rgba(240,244,248,0.5);border:1px solid rgba(157,176,183,0.18);'
                    f'font-size:0.88rem;color:#7A8A93;line-height:1.4;">{option}</div>',
                    unsafe_allow_html=True,
                )

        tag = (
            '<span style="display:inline-block;padding:0.15rem 0.48rem;border-radius:999px;'
            'font-size:0.68rem;font-weight:700;margin-right:0.4rem;'
        )
        if is_correct:
            tag += 'background:rgba(47,111,115,0.10);color:#2F6F73;border:1px solid rgba(47,111,115,0.20);">CORRECT</span>'
        else:
            tag += 'background:rgba(180,60,60,0.08);color:#8B3A3A;border:1px solid rgba(180,60,60,0.18);">INCORRECT</span>'

        st.markdown(
            f'<div style="margin-left:2.7rem;margin-top:0.62rem;padding:0.72rem 0.9rem;border-radius:11px;'
            f'background:linear-gradient(135deg,rgba(252,250,255,0.55),rgba(245,252,252,0.55));'
            f'border:1px solid rgba(138,112,184,0.12);font-size:0.86rem;color:#4D5F69;line-height:1.5;">'
            f'{tag}{q["explanation"]}</div>',
            unsafe_allow_html=True,
        )

        return is_correct

    return False


# ═══════════════════════════════════════════════════════════════
# MAIN RENDERER
# ═══════════════════════════════════════════════════════════════

def _sync_quiz_row_heights(card_ids: list[str], row_token: str) -> None:
    """Force exactly equal heights for one rendered quiz row."""
    if not card_ids:
        return

    js_ids = ", ".join([f'"qc_{cid}"' for cid in card_ids])

    components.html(
        f"""
        <script>
        (function() {{
            const CARD_KEYS = [{js_ids}];
            const ROW_TOKEN = "{row_token}";

            function getCardEl(doc, key) {{
                const root = doc.querySelector(`.st-key-${{key}}`);
                if (!root) return null;
                return root.querySelector('div[data-testid="stVerticalBlockBorderWrapper"]');
            }}

            function reset(cards) {{
                cards.forEach((card) => {{
                    card.style.height = "auto";
                    card.style.minHeight = "0px";

                    const inner = card.querySelector('div[data-testid="stVerticalBlock"]');
                    if (inner) {{
                        inner.style.height = "auto";
                        inner.style.minHeight = "0px";
                    }}
                }});
            }}

            function equalise() {{
                const doc = window.parent.document;
                const cards = CARD_KEYS
                    .map((key) => getCardEl(doc, key))
                    .filter(Boolean);

                if (!cards.length) return;

                reset(cards);

                let maxHeight = 0;
                cards.forEach((card) => {{
                    const h = Math.ceil(card.getBoundingClientRect().height);
                    if (h > maxHeight) maxHeight = h;
                }});

                cards.forEach((card) => {{
                    card.style.height = `${{maxHeight}}px`;
                    card.style.minHeight = `${{maxHeight}}px`;

                    const inner = card.querySelector('div[data-testid="stVerticalBlock"]');
                    if (inner) {{
                        inner.style.height = "100%";
                        inner.style.minHeight = "100%";
                    }}
                }});
            }}

            function run() {{
                equalise();
                requestAnimationFrame(equalise);
                setTimeout(equalise, 60);
                setTimeout(equalise, 180);
                setTimeout(equalise, 360);
            }}

            run();
            window.addEventListener("resize", run);

            const doc = window.parent.document;
            const observer = new MutationObserver(() => run());
            observer.observe(doc.body, {{ childList: true, subtree: true }});
        }})();
        </script>
        """,
        height=0,
        scrolling=False,
    )


def render_quiz_tab() -> None:
    st.markdown(
        dedent("""
        <div class="page-title-wrap">
            <h1 class="page-title">Quiz</h1>
        </div>
        """).strip(),
        unsafe_allow_html=True,
    )

    st.markdown(
        """
        <p style="color: #5A6772; margin-top: -0.2rem; margin-bottom: 0.55rem; font-size: 1.02rem; line-height: 1.42;">
        Test your understanding of the concepts covered in this project. The quiz contains <strong>15 multiple-choice questions</strong> across three sections:
        SQL injection detection, Emotet network behaviour, and their combined relationship.
        </p>
        <p style="color: #5A6772; margin-top: 0rem; margin-bottom: 0.7rem; font-size: 0.98rem; line-height: 1.42;">
        <strong>Select an answer for each question and the correct answer and explanation will be revealed immediately.
        Your score is tracked below.</strong>
        </p>
        """,
        unsafe_allow_html=True,
    )
    st.markdown('<div class="section-divider"></div>', unsafe_allow_html=True)

    if st.button("Reset Quiz", key="quiz_reset_btn"):
        for _, _, qs in ALL_SECTIONS:
            for q in qs:
                sk = f"quiz_{q['id']}"
                if sk in st.session_state:
                    del st.session_state[sk]
        st.rerun()

    q_num = 1
    total_correct = 0
    total_answered = 0
    total_qs = sum(len(qs) for _, _, qs in ALL_SECTIONS)

    for section_name, section_id, questions in ALL_SECTIONS:
        a = _ACCENTS[section_id]

        st.markdown(
            f"""
            <div style="margin-top:1.25rem;margin-bottom:1.05rem;display:flex;align-items:center;gap:0.55rem;">
                <div style="height:3.5px;width:30px;border-radius:999px;background:{a['stripe']};"></div>
                <span style="font-size:1.55rem;font-weight:700;color:#2E3A42;letter-spacing:-0.02em;">
                    {section_name}
                </span>
                <span style="padding:0.15rem 0.46rem;border-radius:999px;font-size:0.62rem;font-weight:700;
                    background:{a['badge_bg']};color:{a['badge_c']};border:1px solid {a['badge_b']};
                    letter-spacing:0.03em;">
                    {len(questions)} QUESTIONS
                </span>
            </div>
            """,
            unsafe_allow_html=True,
        )

        cols_per_row = 3
        for row_start in range(0, len(questions), cols_per_row):
            batch = questions[row_start:row_start + cols_per_row]
            cols = st.columns(cols_per_row, gap="medium", vertical_alignment="top")

            row_card_ids = []

            for col_idx, q in enumerate(batch):
                state_key = f"quiz_{q['id']}"
                answered = state_key in st.session_state
                row_card_ids.append(q["id"])

                with cols[col_idx]:
                    with st.container(border=True, key=f"qc_{q['id']}"):
                        result = _render_q(q, q_num, section_id)

                if answered:
                    total_answered += 1
                    if result:
                        total_correct += 1

                q_num += 1

            _sync_quiz_row_heights(
                row_card_ids,
                f"{section_id}_{row_start}",
            )

    all_done = total_answered == total_qs

    # Updated progress summary after questions
    pct_answered = round((total_answered / total_qs) * 100) if total_qs else 0
    st.markdown(
        f"""
        <div style="margin-top:0.5rem;margin-bottom:1.15rem;padding:0.78rem 0.95rem;border-radius:14px;
            background:linear-gradient(135deg, rgba(252,250,255,0.55), rgba(245,252,252,0.55));
            border:1px solid rgba(138,112,184,0.12);">
            <div style="display:flex;justify-content:space-between;align-items:center;gap:0.8rem;flex-wrap:wrap;">
                <div style="font-size:0.92rem;color:#4D5F69;font-weight:600;">
                    Progress: <span style="color:#2E3A42;">{total_answered} / {total_qs}</span> answered
                </div>
                <div style="font-size:0.88rem;color:#5E6F78;">
                    {total_correct} correct so far · {pct_answered}% completed
                </div>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    if total_answered > 0:
        st.markdown(
            """
            <div style="margin-top:1.25rem;margin-bottom:1.05rem;display:flex;align-items:center;gap:0.55rem;">
                <div style="height:3.5px;width:30px;border-radius:999px;background:linear-gradient(90deg,#5A2D91,#2F6F73);"></div>
                <span style="font-size:1.45rem;font-weight:700;color:#2E3A42;letter-spacing:-0.02em;">Results</span>
            </div>
            """,
            unsafe_allow_html=True,
        )

        with st.container(border=True, key="quiz_score_box"):
            if all_done:
                pct = round((total_correct / total_qs) * 100)
                if pct == 100:
                    msg = "Perfect score — outstanding work."
                elif pct >= 80:
                    msg = "Strong understanding of the core concepts."
                elif pct >= 60:
                    msg = "Good foundation — review the sections you missed."
                else:
                    msg = "Consider revisiting the information pages and trying again."

                components.html(
                    f"""
                    <style>
                        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700;800&display=swap');
                        *{{box-sizing:border-box;margin:0;padding:0}}
                        body{{background:transparent;font-family:"Inter",sans-serif}}
                        .sw{{text-align:center;padding:1.05rem 0 0.65rem 0}}
                        .sb{{font-size:3rem;font-weight:800;letter-spacing:-0.04em;
                            background:linear-gradient(135deg,#5A2D91,#2F6F73);
                            -webkit-background-clip:text;-webkit-text-fill-color:transparent;
                            background-clip:text;line-height:1.1}}
                        .sl{{font-size:0.88rem;color:#5E6F78;margin-top:0.3rem;font-weight:500}}
                        .st{{height:12px;border-radius:999px;background:rgba(157,176,183,0.16);
                            margin:0.95rem auto 0;max-width:420px;overflow:hidden}}
                        .sf{{height:100%;border-radius:999px;background:linear-gradient(90deg,#7C5C8F,#2F6F73);transition:width 0.6s ease}}
                        .sm{{font-size:0.95rem;color:#4D5F69;margin-top:0.75rem;font-weight:500}}
                    </style>
                    <div class="sw">
                        <div class="sb">{total_correct} / {total_qs}</div>
                        <div class="sl">{pct}% correct</div>
                        <div class="st"><div class="sf" style="width:{pct}%"></div></div>
                        <div class="sm">{msg}</div>
                    </div>
                    """,
                    height=180,
                    scrolling=False,
                )
            else:
                st.write(
                    f"**{total_answered}** of **{total_qs}** questions answered "
                    f"(**{total_correct}** correct so far). Complete all questions to see your final score."
                )