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
                st.rerun()

    with st.container(border=True, key="sqli_def_box"):
        render_info_box_title("Definition")
        st.write(
            "SQL Injection (SQLi) is a web application attack where an attacker inserts malicious SQL code into an application's input fields in order to manipulate the backend database query. When the application treats this input as normal data rather than code, the injected SQL becomes part of the executed query. This allows attackers to alter query logic, bypass authentication, extract sensitive information, or manipulate database contents."
        )
        st.write(
            "SQL injection occurs at the application layer, typically through HTTP parameters, form inputs, or URL query strings. In practice, attacks involve modifying query structure using logical operators, quotes, comments, or additional SQL statements to force the database to behave in unintended ways. It remains one of the most common and well-documented web application vulnerabilities."
        )

    with st.container(border=True, key="sqli_info_box"):
        render_info_box_title("Payload Example")
        st.write("Example payload: `admin' OR 1=1 --`")
        st.write("This payload attempts to bypass authentication by altering the logic of the SQL query.")
        st.write("A typical login query might look like:")
        st.code("SELECT * FROM users\nWHERE username = 'admin' AND password = 'password'", language="sql")
        st.write("But when the attacker submits the input `admin' OR 1=1 --`, the query becomes:")
        st.code("SELECT * FROM users\nWHERE username = 'admin' OR 1=1 --' AND password='password'", language="sql")
        st.write("The condition `1=1` is always true, which causes the database to return rows regardless of the password value.")
        st.write("The `--` symbol comments out the rest of the query, preventing the password check from executing.")
        st.write("As a result, the attacker may gain access to the application without knowing the correct credentials.")

    with st.container(border=True, key="sqli_detection_box"):
        render_info_box_title("SQLi Detection Approach")
        st.write(
            "In this project, SQL injection is framed as an application-layer intrusion that manipulates database queries through malicious input payloads. Rather than analysing network traffic patterns, the focus is on HTTP request inputs and query strings, examining the structural characteristics of injected payloads such as:"
        )
        render_bullets("""
- Logical operator manipulation (`AND`, `OR`)
- Quote termination (`'`)
- Comment symbols (`--`)
- Abnormal query length
- Unusual combinations of numeric constants and operators
- Parentheses used for logical grouping
""")
        st.write(
            "These structural signals allow the machine learning model to distinguish between benign user input and injection-style query manipulation. The model does not rely on matching specific known attack strings. Instead, it learns the structural composition patterns that characterise malicious queries — such as elevated numeric literal frequency combined with logical operators and quote manipulation — making it capable of detecting previously unseen injection variants that share the same structural profile."
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
            "Emotet is a malware family commonly described as a trojan and botnet loader that spreads through phishing campaigns and infected email attachments. Once executed on a victim machine, it establishes communication with external command-and-control (C2) infrastructure and begins generating malicious network activity. Unlike SQL injection, which occurs at the application layer through malicious input payloads, Emotet operates at the network and host behaviour level."
        )
        st.write(
            "Detection therefore relies on analysing network traffic patterns, connection behaviour, and communication statistics extracted from PCAP data rather than analysing textual payloads. In this project, Emotet detection focuses on identifying behavioural patterns of infected hosts observed in network captures rather than analysing the malware binary itself. This is a key distinction — Emotet uses obfuscation techniques that make static binary analysis unreliable, but its network communication patterns remain consistent and detectable."
        )

    with st.container(border=True, key="emotet_stages_box"):
        render_info_box_title("The Five Stages")
        st.markdown(EMOTET_STAGES_HTML, unsafe_allow_html=True)

    with st.container(border=True, key="emotet_scenario_box"):
        render_info_box_title("Example Scenario")
        st.write("1. **Phishing Email** — The victim receives a legitimate-looking email, often referencing business topics such as invoices, payroll, or shared documents. The email contains an attachment designed to appear trustworthy.")
        st.write("2. **Malicious Attachment** — The user opens the file and enables macros. This triggers embedded VBA code, which silently launches a process chain (typically winword.exe → powershell.exe → rundll32.exe) to download and execute the Emotet payload.")
        st.write("3. **C2 Communication** — The infected host begins establishing outbound connections to command-and-control servers. Emotet embeds a list of C2 IP addresses directly in its configuration, allowing it to connect without DNS resolution. This means it communicates using raw IP addresses rather than domain names.")
        st.write("4. **Beaconing** — The infected machine maintains persistent, low-volume communication with the C2 server, periodically checking in for instructions. This produces a distinctive traffic pattern: regular timing intervals, consistent packet sizes, and repeated connections to the same external IPs — patterns that are not typical of normal browsing behaviour.")
        st.write("5. **Botnet Expansion** — Once established, the C2 server can instruct the infected host to download additional malware modules, harvest credentials, send spam, or attempt lateral movement across the network. This is what makes Emotet a loader — its primary purpose is to serve as a delivery mechanism for secondary threats.")

    with st.container(border=True, key="emotet_frame_box"):
        render_info_box_title("How Emotet is Framed in This Project")
        st.write(
            "Emotet is not just one type of threat — it operates as malware, a trojan, and a botnet loader at the same time. As malware, it infects a host system once a weaponised attachment is opened. As a trojan, it gains access by hiding inside files that appear legitimate, such as invoices or shared documents, relying on the user to open them willingly. As a botnet loader, it maintains a persistent connection to external servers and downloads additional malware on behalf of the attacker, expanding their control over the infected network."
        )
        st.write(
            "Each of these roles leaves a different trace in network traffic. The trojan stage is responsible for the initial compromise, the malware stage produces unusual activity on the host, and the loader stage generates the repeated outbound communication patterns — beaconing, destination diversity, and consistent packet behaviour — that the Emotet section of this model is designed to detect. It is this combination of behaviours, rather than any single indicator, that makes Emotet a strong candidate for behavioural detection."
        )


# ═══════════════════════════════════════════════════════════════
# RELATIONSHIP PAGE
# ═══════════════════════════════════════════════════════════════
def render_relationship_info_page(go_home_fn: VoidFn) -> None:
    render_back_home_button(go_home_fn)
    render_page_title("Relationship Between SQLi and Emotet")

    with st.container(border=True, key="rs_one"):
        render_info_box_title("Multi-Stage Attack Context")
        st.write("Modern cyber attacks rarely occur as a single isolated event. Instead, they often unfold as multi-stage attack chains, where attackers move through different layers of a system before achieving their objective. Each stage serves a different purpose — initial access, privilege escalation, persistence, lateral movement, and data exfiltration — and each produces different observable indicators.")
        st.write("In this project, SQL injection and Emotet represent two distinct stages of potential compromise occurring at different layers of the attack lifecycle. SQL injection targets the application layer as an initial entry point, while Emotet represents a later-stage network-level threat that maintains persistent access and enables further exploitation.")

    col_left, col_mid, col_right = st.columns([0.9, 1.1, 1.35], gap="large")

    with col_left:
        with st.container(border=True, key="rs_two", height=330):
            render_info_box_title("1. SQLi as an Earlier Stage")
            st.write("SQL injection operates at the application layer, where attackers manipulate web inputs to alter database queries. A successful SQL injection attack can allow attackers to access sensitive database information, retrieve administrative credentials, escalate privileges, or establish a foothold inside the system.")
            st.write("This makes SQL injection a common starting point in broader attack campaigns. Once attackers gain access to internal systems through a vulnerable web application, the attack can progress beyond the application layer into deeper stages involving malware deployment and network-level activity.")

    with col_mid:
        with st.container(border=True, key="rs_three", height=330):
            render_info_box_title("2. Emotet as a Later Behavioural Stage")
            st.write("Emotet represents a later stage in the attack chain, where compromised machines begin communicating with external command-and-control infrastructure and exhibiting abnormal network traffic patterns. At this stage, the attacker has already established access and is now focused on maintaining persistence, downloading additional tools, and expanding control.")
            st.write("Although SQL injection and Emotet operate at different layers of a system, a successful SQL injection attack can serve as the initial compromise vector that enables later malware deployment. For example, an attacker who gains sufficient database privileges through SQL injection may leverage stored procedures or command execution capabilities to download and execute malware on the compromised server, which could then exhibit Emotet-like C2 behaviour.")

    with col_right:
        with st.container(border=True, key="rs_four", height=330):
            render_info_box_title("3. How SQLi Can Progress Toward Malware Deployment")
            st.write("The transition from application-layer exploitation to network-level compromise follows a recognisable pattern. When attackers exploit a vulnerable web application through SQL injection, they may initially gain access to sensitive database information, administrative credentials, or internal system functionality.")
            st.write("In more severe cases, attackers can leverage database features such as stored procedures or command execution capabilities to interact with the underlying operating system. For example, certain database systems support extended stored procedures that allow the execution of system commands. If an attacker gains sufficient privileges through SQL injection, they may use these mechanisms to download and execute external malware on the compromised server.")
            st.write("This represents the bridge between the two attack types covered in this project: what begins as payload manipulation at the application layer can escalate into host-level compromise and network-level malware behaviour.")

    with st.container(border=True, key="rs_five"):
        render_info_box_title("Progression Example")
        st.write("A conceptual bridge from application-layer exploitation to network-level malware behaviour.")
        components.html(PROGRESSION_HTML, height=200, scrolling=False)

    with st.container(border=True, key="rs_six"):
        render_info_box_title("Real-World Context")
        st.write("In real-world attack campaigns, Emotet is most commonly delivered through phishing emails and malicious attachments rather than through SQL injection directly. However, the broader attack lifecycle frequently involves multiple compromise vectors, and web application vulnerabilities such as SQL injection can provide attackers with an initial foothold that eventually leads to malware deployment and network-level compromise.")
        st.write("The purpose of combining these two threats in a single project is not to suggest that SQL injection always leads to Emotet specifically, but rather to demonstrate that different attack stages produce different types of observable behaviour — and that a unified detection model can learn to identify both.")


# ═══════════════════════════════════════════════════════════════
# ML PIPELINE PAGE
# ═══════════════════════════════════════════════════════════════
def render_pipeline_info_page(go_home_fn: VoidFn = None) -> None:
    render_page_title("ML Pipeline Content")

    # ── 1. Dataset ──
    with st.container(border=True, key="pipeline_two"):
        render_info_box_title("Dataset")
        st.write("Multiple datasets were used to construct the training data for this project, covering two different attack domains.")
        components.html(DATASET_CARDS_HTML, height=110, scrolling=False)
        st.write("**Unified Dataset** -- The final unified dataset combines both domains into a single table with three classes: Normal (y=0), SQLi (y=1), and Emotet (y=2). The full dataset contains 34,295 rows — 22,358 Normal, 11,382 SQLi, and 555 Emotet. A balanced version with 555 samples per class was also constructed.")
        components.html(DISTRIBUTION_BAR_HTML, height=45, scrolling=False)

    # ── 2. Feature Engineering ──
    with st.container(border=True, key="pipeline_three"):
        render_info_box_title("Feature Engineering")
        st.write("Before training, raw data was transformed into numerical features. The two attack domains produce structurally different feature families. The unified dataset contains 26 feature columns; when an SQLi row is present, Emotet columns are filled with zeros and vice versa.")
        components.html(FEATURE_CHIPS_HTML, height=165, scrolling=False)

    # ── 3. Model Selection ──
    with st.container(border=True, key="pipeline_four"):
        render_info_box_title("Model Selection")
        st.write("The classification model used in this project is a Random Forest classifier. It was compared against logistic regression on the unified dataset.")
        components.html(MODEL_COMPARISON_HTML, height=102, scrolling=False)
        st.write("**Why Random Forest** -- Random Forest was selected because the feature space contains non-linear relationships and interactions between multiple feature types. SQLi detection depends on combinations of features — for example, a single OR in an input is not necessarily malicious, but OR combined with elevated quote counts, constant values, and parentheses strongly suggests injection. These interaction effects cannot be captured by a linear model. Additionally, Random Forest is resistant to overfitting through bagging, handles heterogeneous feature distributions without requiring feature scaling, and provides built-in feature importance scores that support model interpretability.")
        st.write("**Why a Unified Model** -- Rather than building separate models for SQLi and Emotet, this project trains a single Random Forest classifier on the combined feature set. This forces the model to learn not only the difference between attacks and normal traffic, but also the distinction between different attack types — reflecting a more realistic deployment scenario.")

    # ── 4. Training Configuration ──
    with st.container(border=True, key="pipeline_five"):
        render_info_box_title("Training Configuration")
        st.write("The final model uses 300 decision trees with the following hyperparameters:")
        st.markdown(PARAM_CHIPS_HTML, unsafe_allow_html=True)
        st.write("**Class Weighting** -- The class_weight=\"balanced\" parameter addresses the significant class imbalance in the dataset, particularly the underrepresentation of Emotet (555 samples compared to 22,358 Normal and 11,382 SQLi). Balanced weighting automatically increases the penalty for misclassifying rare classes during training.")
        st.write("**Hyperparameter Tuning** -- Tuning was conducted in two stages using 5-fold stratified cross-validation on the internal dataset only. Stage 1 evaluated structural regularisation parameters (max_depth, min_samples_leaf, min_samples_split). Stage 2 held the Stage 1 winners fixed and evaluated max_features and class_weight. The tuned model showed improved internal stability but performed marginally worse on external validation. As a result, the baseline configuration was selected as the final production model, prioritising cross-dataset robustness over internal optimisation.")

    # ── 5. Validation Overview ──
    with st.container(border=True, key="pipeline_six"):
        render_info_box_title("Validation Overview")
        st.write("Several validation techniques were used to ensure the model performs reliably and generalises to unseen data.")
        components.html(VALIDATION_CARDS_HTML, height=195, scrolling=False)

    # ── 6. Evaluation Metrics ──
    with st.container(border=True, key="pipeline_seven"):
        render_info_box_title("Evaluation Metrics")
        st.write("Three complementary metrics were used to evaluate model performance, each addressing a different aspect of classification quality under class imbalance. For detailed evaluation metrics, see the **Explainability** tab.")
        st.write("**Macro-F1** is the primary metric — it computes F1 independently for each class and averages equally, so poor Emotet performance cannot be masked by strong majority-class results. **ROC-AUC** evaluates ranking quality across all classification thresholds, measuring whether the model reliably ranks malicious samples above benign ones. **PR-AUC** provides a stricter assessment specifically for the rare Emotet class, where ROC-AUC can appear high even when precision collapses.")