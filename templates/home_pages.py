import streamlit as st
from typing import Callable, Dict, List

from templates.page_blocks import (
    markdown_block,
    render_info_box_title,
    render_paragraph,
    render_section_heading,
)


HomePageFn = Callable[[str], None]


HOME_CARDS: List[Dict[str, str]] = [
    {"title": "SQL Injection", "button_key": "sqli_info_btn", "target_page": "sqli"},
    {"title": "Emotet", "button_key": "emotet_btn", "target_page": "emotet"},
    {
        "title": "Relationship Between SQLi and Emotet",
        "button_key": "relationship_btn",
        "target_page": "relationship",
    },
]


def render_dashboard_hero() -> None:
    markdown_block(
        """
        <div class="top-network-banner">
            <div class="network-grid"></div>
            <div class="network-glow network-glow-1"></div>
            <div class="network-glow network-glow-2"></div>
            <div class="network-scan"></div>
        </div>

        <div class="hero-title-wrap">
            <div class="hero-title-row">
                <div>
                    <div class="hero-title">Cross-Layer Attack Detection: SQLi and Emotet</div>
                    <div class="hero-caption">
                        Corresponding Paper: <em>A Machine Learning Approach to Multi-Stage Cyber-Attack Detection: SQL Injection and Emotet Behaviour Analysis</em>
                    </div>
                </div>
                <div class="hero-eyebrow">Interactive Security Analysis Dashboard</div>
            </div>
        </div>
        """
    )

    markdown_block('<div class="section-divider"></div>')


def render_home_intro() -> None:
    render_section_heading("Interactive Exploration of Multi-Stage Cyber-Attack Detection")

    render_paragraph(
        "This dashboard provides an interactive environment for exploring the machine learning models developed in this project. Rather than presenting results only through static figures and tables, it allows users to interact with simplified model simulations and observe how the detection system responds to different inputs.",
        style="margin-top: 0; margin-bottom: 0.55rem; color: #5F6C73;",
    )

    render_paragraph(
        "The project focuses on two forms of malicious activity: <strong>SQL Injection (SQLi)</strong>, an application-layer attack identified through structural characteristics of input queries, and <strong>Emotet behaviour</strong>, a network-layer threat identified through anomalous communication patterns in traffic data. These represent different stages of a potential cyber attack, with SQLi acting as an initial compromise vector and Emotet representing post-compromise malware behaviour.",
        style="margin-top: 0; margin-bottom: 0.55rem; color: #5F6C73;",
    )

    render_paragraph(
        "By analysing both within a unified model, the project demonstrates how machine learning can support multi-stage attack detection. Users can examine how the models interpret different features, experiment with simulated inputs, and observe how behavioural changes influence predictions.",
        style="margin-top: 0; margin-bottom: 0.8rem; color: #5F6C73;",
    )

    render_section_heading("Explore the Sections")

    render_paragraph(
        "Select any of the sections below to learn about specific attack behaviours, examine how the unified machine learning model operates, and understand the reasoning behind the system's predictions.",
        style="margin-top: 0; margin-bottom: 0.55rem;",
    )

    markdown_block(
        """
        <ul style="margin-top: -0.75rem; margin-bottom: 1rem; padding-left: 2rem; color: #5F6C73;">
            <li style="margin-bottom: 0.3rem;">
                <strong>SQL Injection</strong> – explains what SQLi is, how it operates at the application layer, and how the model detects malicious query patterns using engineered payload features. The standalone SQLi classifier can also be explored from this section.
            </li>
            <li style="margin-bottom: 0.3rem;">
                <strong>Emotet</strong> – introduces Emotet as a malware family, explains how it behaves at the network layer, and describes the behavioural features extracted from network traffic captures to detect infected hosts.
            </li>
            <li style="margin-bottom: 0.3rem;">
                <strong>Relationship Between SQLi and Emotet</strong> – explains how these two attack behaviours can form part of a broader multi-stage attack scenario, and why detecting both within a single model is valuable for security monitoring.
            </li>
        </ul>
        """
    )


def render_home_card(
    title: str,
    button_key: str,
    target_page: str,
    go_page_fn: HomePageFn,
) -> None:
    with st.container(key=f"{button_key}_wrap"):
        if st.button(title, key=button_key, use_container_width=True):
            go_page_fn(target_page)
            st.rerun()


def render_home_card_grid(go_page_fn: HomePageFn) -> None:
    with st.container(key="home_card_grid"):
        spacer_left, *card_cols, spacer_right = st.columns([0.08, 1, 1, 1, 0.08], gap="large")

        for col, card in zip(card_cols, HOME_CARDS):
            with col:
                render_home_card(
                    title=card["title"],
                    button_key=card["button_key"],
                    target_page=card["target_page"],
                    go_page_fn=go_page_fn,
                )


def render_home_about_sections() -> None:
    st.markdown("<div style='height: 0.8rem;'></div>", unsafe_allow_html=True)

    render_section_heading("About This Project")

    col1, col2, col3, col4 = st.columns(4, gap="medium")

    with col1:
        with st.container(border=True, key="about_abstract_box", height=310):
            render_info_box_title("Abstract")
            st.write(
                "This project presents a machine learning pipeline for detecting multi-stage "
                "cyber attacks, combining SQL injection detection at the application layer with "
                "Emotet malware behaviour analysis at the network layer. Nine structural features "
                "are extracted from SQL payloads, and seventeen behavioural features are derived "
                "from Zeek connection logs. These are merged into a unified 26-feature space, and a "
                "Random Forest classifier is trained to distinguish between Normal traffic, SQLi "
                "attacks, and Emotet malware behaviour."
            )

    with col2:
        with st.container(border=True, key="about_overview_box", height=310):
            render_info_box_title("Project Overview")
            st.write(
                "The system was developed in two phases: a binary SQLi classifier as a baseline, "
                "followed by a unified multi-class model classifying input as Normal, SQLi, or "
                "Emotet. The multi-class formulation requires the model to distinguish between "
                "lexical payload patterns and behavioural network anomalies. An interactive "
                "Streamlit dashboard provides feature-level sliders, probability visualisations, "
                "and feature importance displays for model explainability."
            )

    with col3:
        with st.container(border=True, key="about_objective_box", height=310):
            render_info_box_title("Research Objective")
            st.write(
                "To design, implement, and evaluate an end-to-end machine learning pipeline for "
                "multi-stage cyber-attack detection, demonstrating feature engineering across attack "
                "domains, unified multi-class classification using Random Forest, rigorous "
                "evaluation through stratified cross-validation, external dataset validation, "
                "group-aware holdout, and an interactive dashboard for model explainability."
            )

    with col4:
        with st.container(border=True, key="about_problem_box", height=310):
            render_info_box_title("Problem Statement")
            st.write(
                "Real-world attacks frequently combine techniques across layers: an attacker may "
                "exploit SQLi for initial access, then deploy Emotet for persistence. Despite "
                "this, detection systems are typically designed in isolation, with no shared "
                "framework. This project addresses that gap by developing a unified classification "
                "system that labels input as Normal, SQLi, or Emotet."
            )