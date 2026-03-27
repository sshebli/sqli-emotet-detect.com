import streamlit as st
import streamlit.components.v1 as components
from typing import Callable

from templates.page_blocks import (
    render_back_home_button,
    render_bullets,
    render_info_box_title,
    render_page_title,
)
from templates.html_blocks import (
    DATASET_CARDS_HTML,
    DISTRIBUTION_BAR_HTML,
    EMOTET_STAGES_HTML,
    FEATURE_CHIPS_HTML,
    MODEL_COMPARISON_HTML,
    PARAM_CHIPS_HTML,
    PROGRESSION_HTML,
    VALIDATION_CARDS_HTML,
)


HomePageFn = Callable[[str], None]
VoidFn = Callable[[], None]


def render_section_page(title: str, body_text: str, go_home_fn: VoidFn) -> None:
    render_back_home_button(go_home_fn)
    render_page_title(title)
    st.write(body_text)


# ═══════════════════════════════════════════════════════════════
# SQLi INFO PAGE
# ═══════════════════════════════════════════════════════════════
def render_sqli_info_page(go_home_fn: VoidFn, go_page_fn: HomePageFn) -> None:
    render_back_home_button(go_home_fn)

    with st.container(key="sqli_title_row"):
        title_col, button_col = st.columns([0.80, 0.20], gap="small")
        with title_col:
            render_page_title("SQL Injection (SQLi)")
        with button_col:
            if st.button("Test out SQLi Model Here", key="sqli_model_cta", use_container_width=False):
                go_page_fn("sqli_model")

    with st.container(border=True, key="sqli_def_box"):
        render_info_box_title("Definition")
        st.write(
            "SQL Injection (SQLi) is a web application attack in which an attacker inserts malicious "
            "SQL code into user-controlled input fields so that it is interpreted as part of a backend "
            "database query. If the application fails to distinguish between data and executable query "
            "logic, the injected input may alter the intended SQL statement. This can allow an attacker "
            "to bypass authentication, extract sensitive data, modify database contents, or manipulate "
            "application behaviour."
        )
        st.write(
            "SQLi occurs at the application layer, typically through HTTP parameters, form inputs, or "
            "URL query strings. In practice, attacks often manipulate query structure using logical "
            "operators, quotes, comments, or additional SQL fragments to force the database to behave "
            "in unintended ways. It remains one of the most widely studied and well-documented web "
            "application vulnerabilities."
        )

    with st.container(border=True, key="sqli_info_box"):
        render_info_box_title("Payload Example")
        st.write("Example payload: `admin' OR 1=1 --`")
        st.write("This payload attempts to bypass authentication by altering the logical condition of the SQL query.")
        st.write("A typical login query might look like:")
        st.code(
            "SELECT * FROM users\nWHERE username = 'admin' AND password = 'password'",
            language="sql",
        )
        st.write("But when the attacker submits the input `admin' OR 1=1 --`, the query becomes:")
        st.code(
            "SELECT * FROM users\nWHERE username = 'admin' OR 1=1 --' AND password='password'",
            language="sql",
        )
        st.write(
            "The condition `1=1` is always true, causing the query predicate to evaluate as true "
            "regardless of the password value."
        )
        st.write(
            "The `--` sequence comments out the remainder of the query, preventing the intended "
            "password condition from being applied."
        )
        st.write("As a result, the attacker may gain access to the application without knowing the correct credentials.")

    with st.container(border=True, key="sqli_detection_box"):
        render_info_box_title("SQLi Detection Approach")
        st.write(
            "In this project, SQL injection is treated as an application-layer attack characterised "
            "by structural manipulation of database queries through malicious input payloads. Rather "
            "than analysing network traffic patterns, the model focuses on the structure of HTTP "
            "request inputs and query strings, examining indicators commonly associated with injection "
            "behaviour such as:"
        )
        render_bullets("""
- Logical operator manipulation (`AND`, `OR`)
- Quote termination (`'`, `"`)
- Comment symbols (`--`)
- UNION-based extraction attempts
- Abnormal query length
- Unusual combinations of constants and operators
- Parentheses used for logical grouping
""")
        st.write(
            "In the implementation used in this project, these patterns are represented through "
            "engineered structural features such as query length, logical operator counts, quote "
            "counts, parentheses counts, constant value counts, and total special-character usage."
        )
        st.write(
            "These structural signals allow the machine learning model to distinguish between benign "
            "user input and injection-style query manipulation. Rather than relying on exact matches "
            "to known attack strings, the model learns broader structural patterns associated with "
            "malicious payloads, such as elevated constant counts, quote manipulation, logical "
            "operators, and increased query length. This makes it better suited to detecting "
            "previously unseen SQLi variants that share a similar structural profile."
        )


# ═══════════════════════════════════════════════════════════════
# EMOTET INFO PAGE
# ═══════════════════════════════════════════════════════════════
def render_emotet_info_page(go_home_fn: VoidFn) -> None:
    render_back_home_button(go_home_fn)
    render_page_title("Emotet")

    with st.container(border=True, key="emotet_def_box"):
        render_info_box_title("Definition")
        st.write(
            "Emotet is a malware family commonly described as a trojan, loader, and botnet threat "
            "that spreads primarily through phishing emails and malicious attachments. Once executed "
            "on a victim host, it establishes communication with external command-and-control (C2) "
            "infrastructure and begins generating malicious network activity. Unlike SQL injection, "
            "which occurs at the application layer through input payloads, Emotet operates at the "
            "network and host-behaviour level."
        )
        st.write(
            "Detection therefore relies on analysing network traffic patterns, connection behaviour, "
            "and communication statistics extracted from PCAP-derived logs rather than analysing "
            "textual payloads. In this project, Emotet detection focuses on identifying behavioural "
            "patterns of infected hosts observed in network captures rather than analysing the "
            "malware binary itself. This distinction is important because Emotet uses obfuscation "
            "and frequent code changes that reduce the reliability of static binary analysis, while "
            "its network communication patterns remain more stable and detectable."
        )

    with st.container(border=True, key="emotet_stages_box"):
        render_info_box_title("Typical Emotet Infection Stages")
        st.markdown(EMOTET_STAGES_HTML, unsafe_allow_html=True)

    with st.container(border=True, key="emotet_scenario_box"):
        render_info_box_title("Example Scenario")
        st.write(
            "1. **Phishing Email** — The victim receives a legitimate-looking email, often "
            "referencing invoices, payroll, or shared business documents. The message includes an "
            "attachment designed to appear trustworthy."
        )
        st.write(
            "2. **Malicious Attachment** — The user opens the attachment and enables macros. This "
            "triggers embedded code that launches a process chain used to download and execute the "
            "Emotet payload."
        )
        st.write(
            "3. **C2 Communication** — The infected host begins establishing outbound connections to "
            "command-and-control servers. Emotet often embeds a list of C2 IP addresses directly in "
            "its configuration, allowing communication without relying on DNS resolution."
        )
        st.write(
            "4. **Beaconing** — The infected machine maintains persistent, low-volume communication "
            "with the C2 server, periodically checking for instructions. This produces a distinctive "
            "traffic pattern characterised by regular timing intervals, repeated connections, and "
            "consistent packet behaviour."
        )
        st.write(
            "5. **Botnet Expansion** — Once established, the C2 server can instruct the infected "
            "host to download additional payloads, harvest credentials, send spam, or support "
            "lateral movement. This is what makes Emotet a loader: its primary role is to deliver "
            "or enable further malicious activity."
        )

    with st.container(border=True, key="emotet_frame_box"):
        render_info_box_title("How Emotet is Framed in This Project")
        st.write(
            "In this project, Emotet is treated as a behavioural network threat rather than as a "
            "static malware sample. The focus is not on reverse-engineering the binary itself, but "
            "on identifying the communication patterns an infected host produces once compromise has "
            "occurred. This includes repeated outbound connections, destination diversity, protocol "
            "usage, timing variation, and consistent traffic characteristics visible in connection logs."
        )
        st.write(
            "In the implementation used in this project, these behaviours are represented through "
            "engineered network features such as connection volume, protocol ratios, inter-arrival "
            "timing variation, average byte and packet counts, reset and rejection ratios, and "
            "destination diversity. The Emotet component of the system is therefore designed to "
            "detect behavioural signals across network traffic windows rather than any single "
            "signature or payload artifact."
        )


# ═══════════════════════════════════════════════════════════════
# RELATIONSHIP PAGE
# ═══════════════════════════════════════════════════════════════
def render_relationship_info_page(go_home_fn: VoidFn) -> None:
    render_back_home_button(go_home_fn)
    render_page_title("Relationship Between SQLi and Emotet")

    with st.container(border=True, key="rs_one"):
        render_info_box_title("Multi-Stage Attack Context")
        st.write(
            "Modern cyber attacks rarely occur as single isolated events. Instead, they often unfold "
            "as multi-stage attack chains, in which attackers move through different layers of a "
            "system before achieving their objective. Each stage serves a different purpose, such as "
            "initial access, privilege escalation, persistence, lateral movement, or data exfiltration, "
            "and each produces different observable indicators."
        )
        st.write(
            "In this project, SQL injection and Emotet represent two distinct stages of potential "
            "compromise occurring at different layers of the attack lifecycle. SQL injection targets "
            "the application layer as an initial entry vector, while Emotet represents a later-stage "
            "network-level threat associated with persistence and post-compromise activity."
        )

    col_left, col_mid, col_right = st.columns([0.9, 1.1, 1.35], gap="large")

    with col_left:
        with st.container(border=True, key="rs_two"):
            render_info_box_title("1. SQLi as an Initial Access Stage")
            st.write(
                "SQL injection operates at the application layer, where attackers manipulate web "
                "inputs to alter database queries. A successful SQLi attack may allow access to "
                "sensitive information, credential material, or elevated privileges, providing an "
                "initial foothold in the target system."
            )
            st.write(
                "This makes SQLi a plausible entry point in a broader attack chain. Once attackers "
                "gain access through a vulnerable web application, the compromise may progress "
                "beyond the application layer into later stages involving malware deployment, "
                "persistence, or network-level activity."
            )

    with col_mid:
        with st.container(border=True, key="rs_three"):
            render_info_box_title("2. Emotet as a Post-Compromise Behavioural Stage")
            st.write(
                "Emotet represents a later-stage behavioural threat in which compromised hosts begin "
                "communicating with external command-and-control infrastructure and exhibiting "
                "abnormal network traffic patterns. At this stage, the attacker is typically focused "
                "on maintaining persistence, downloading additional payloads, or expanding control."
            )
            st.write(
                "Although SQLi and Emotet operate at different layers of a system, a successful SQLi "
                "compromise can in some cases create conditions that enable later malware deployment. "
                "For example, stored procedures or command-execution capabilities may allow the "
                "attacker to move from database compromise toward host-level control and subsequent "
                "C2-style behaviour."
            )

    with col_right:
        with st.container(border=True, key="rs_four"):
            render_info_box_title("3. How SQLi Can Progress Toward Malware Deployment")
            st.write(
                "The transition from application-layer exploitation to network-level compromise "
                "follows a recognisable progression. When attackers exploit a vulnerable web "
                "application through SQL injection, they may initially gain access to sensitive "
                "database contents, administrative credentials, or internal system functionality."
            )
            st.write(
                "In more severe cases, database features such as stored procedures or "
                "command-execution capabilities can be abused to interact with the underlying "
                "operating system. If the attacker gains sufficient privileges, these mechanisms may "
                "be used to download and execute external malware on the compromised server."
            )
            st.write(
                "This represents the conceptual bridge between the two attack types examined in this "
                "project: what begins as payload manipulation at the application layer can escalate "
                "into host-level compromise and network-level malware behaviour."
            )

    with st.container(border=True, key="rs_five"):
        render_info_box_title("Progression Example")
        st.write("A conceptual bridge from application-layer exploitation to network-level malware behaviour.")
        components.html(PROGRESSION_HTML, height=200, scrolling=False)

    with st.container(border=True, key="rs_six"):
        render_info_box_title("Real-World Context")
        st.write(
            "In real-world attack campaigns, Emotet is most commonly delivered through phishing "
            "emails and malicious attachments rather than through SQL injection directly. However, "
            "broader attack lifecycles frequently involve multiple compromise vectors, and web "
            "application vulnerabilities such as SQL injection can still provide attackers with an "
            "initial foothold that later enables malware deployment or network-level compromise."
        )
        st.write(
            "The purpose of combining these two threats in a single project is not to suggest that "
            "SQL injection typically leads to Emotet specifically, but to demonstrate that different "
            "attack stages produce different forms of observable behaviour — and that a unified "
            "detection model can be designed to identify both."
        )

# ═══════════════════════════════════════════════════════════════
# ML PIPELINE PAGE
# ═══════════════════════════════════════════════════════════════
def render_pipeline_info_page(go_home_fn: VoidFn = None) -> None:
    render_page_title("ML Pipeline Content")

    # ── 1. Dataset ──
    with st.container(border=True, key="pipeline_two"):
        render_info_box_title("Dataset")
        st.write(
            "Multiple datasets were used across training, validation, and external evaluation for this project, "
            "covering two different attack domains."
        )
        components.html(DATASET_CARDS_HTML, height=110, scrolling=False)
        st.write(
            "**Unified Dataset** -- The final unified dataset combines both domains into a single table with three classes: "
            "Normal (y=0), SQLi (y=1), and Emotet (y=2). The final grouped dataset contains 34,295 rows — 22,358 Normal, "
            "11,382 SQLi, and 555 Emotet. A balanced sampled version was also constructed for comparison experiments."
        )
        components.html(DISTRIBUTION_BAR_HTML, height=45, scrolling=False)

    # ── 2. Feature Engineering ──
    with st.container(border=True, key="pipeline_three"):
        render_info_box_title("Feature Engineering")
        st.write(
            "Before training, raw data was transformed into numerical features. The two attack domains produce "
            "structurally different feature families. The unified dataset contains 26 feature columns; when an SQLi "
            "row is present, Emotet columns are filled with zeros and vice versa."
        )
        components.html(FEATURE_CHIPS_HTML, height=195, scrolling=False)

    # ── 3. Model Selection ──
    with st.container(border=True, key="pipeline_four"):
        render_info_box_title("Model Selection")
        st.write(
            "The classification model used in this project is a Random Forest classifier. It was compared "
            "against logistic regression on the unified dataset."
        )
        components.html(MODEL_COMPARISON_HTML, height=102, scrolling=False)
        st.write(
            "**Why Random Forest** -- Random Forest was selected because the feature space contains non-linear "
            "relationships and interactions between multiple feature types. SQLi detection depends on combinations "
            "of features — for example, a single OR in an input is not necessarily malicious, but OR combined with "
            "elevated quote counts, constant values, and parentheses strongly suggests injection. These interaction "
            "effects cannot be captured by a linear model. Additionally, Random Forest is resistant to overfitting "
            "through bagging, handles heterogeneous feature distributions without requiring feature scaling, and "
            "provides built-in feature importance scores that support model interpretability."
        )
        st.write(
            "**Why a Unified Model** -- Rather than building separate models for SQLi and Emotet, this project "
            "trains a single Random Forest classifier on the combined feature set. This forces the model to learn "
            "not only the difference between attacks and normal traffic, but also the distinction between different "
            "attack types — reflecting a more realistic deployment scenario."
        )

    # ── 4. Training Configuration ──
    with st.container(border=True, key="pipeline_five"):
        render_info_box_title("Training Configuration")
        st.write("The final model uses 300 decision trees with the following hyperparameters:")
        st.markdown(PARAM_CHIPS_HTML, unsafe_allow_html=True)
        st.write(
            '**Class Weighting** -- The class_weight="balanced" parameter addresses the class imbalance in the '
            "unified dataset, particularly the smaller Emotet class (555 samples compared to 22,358 Normal and "
            "11,382 SQLi). Balanced weighting automatically increases the penalty for misclassifying less frequent "
            "classes during training, helping the model learn minority-class patterns without altering the original "
            "class distribution."
        )
        st.write(
            "**Hyperparameter Tuning** -- Tuning was conducted in two stages using 5-fold stratified cross-validation "
            "on the internal dataset only. Stage 1 evaluated structural regularisation parameters (max_depth, "
            "min_samples_leaf, min_samples_split). Stage 2 held the Stage 1 winners fixed and evaluated max_features "
            'and class_weight. The tuned model showed improved internal stability but performed marginally worse on '
            "external validation. As a result, the baseline configuration was selected as the final production model, "
            "prioritising cross-dataset robustness over internal optimisation."
        )

    # ── 5. Validation Overview ──
    with st.container(border=True, key="pipeline_six"):
        render_info_box_title("Validation Overview")
        st.write(
            "Several validation techniques were used to ensure the model performs reliably and generalises to unseen data."
        )
        components.html(VALIDATION_CARDS_HTML, height=200, scrolling=False)

    # ── 6. Evaluation Metrics ──
    with st.container(border=True, key="pipeline_seven"):
        render_info_box_title("Evaluation Metrics")
        st.write(
            "Three complementary metrics were used to evaluate model performance, each addressing a different aspect "
            "of classification quality under class imbalance. For detailed evaluation metrics, see the **Explainability** tab."
        )
        st.write(
            "**Macro-F1** is the primary metric — it computes F1 independently for each class and averages equally, "
            "so poor Emotet performance cannot be masked by strong majority-class results. **ROC-AUC** evaluates "
            "ranking quality across all classification thresholds, measuring whether the model reliably ranks malicious "
            "samples above benign ones. **PR-AUC** provides a stricter assessment specifically for the rarer Emotet "
            "class, where ROC-AUC can appear high even when precision collapses."
        )