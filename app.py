"""
app.py — Streamlit Dashboard
AI-Powered Resume & ATS Optimizer

Dark Emerald & Obsidian themed ATS diagnostic dashboard with interactive
Plotly charts, comprehensive skill audit, actionable recommendations,
and Google Gemini AI tailoring.
"""

import os
from dotenv import load_dotenv

# Load local .env if present
load_dotenv()

import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from extractor import extract_text_from_pdf, extract_skills_from_text, extract_skills_from_jd
from matcher import run_matching, ATSReport
from taxonomy import SKILL_TAXONOMY
from recommendations import (
    get_skill_recommendation,
    get_skill_interview_details,
    generate_full_gemini_audit,
    parse_gemini_sections,
    call_gemini_api,
    compare_resume_with_jd_gemini,
    get_gemini_tailored_optimization,
)

# ══════════════════════════════════════════════════════════════
# PAGE CONFIG
# ══════════════════════════════════════════════════════════════
st.set_page_config(
    page_title="ATS Resume Optimizer — AI Project",
    page_icon="🧬",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ══════════════════════════════════════════════════════════════
# DARK EMERALD & OBSIDIAN THEME — PREMIUM CUSTOM CSS
# ══════════════════════════════════════════════════════════════
CUSTOM_CSS = """
<style>
/* ── Import Google Font ─────────────────────────────── */
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800;900&display=swap');
@import url('https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@400;500;600&display=swap');

/* ── Root Variables ─────────────────────────────────── */
:root {
    --bg-base: #0B0F12;
    --bg-surface: #101820;
    --bg-card: #151F2B;
    --bg-card-hover: #1A2836;
    --border-subtle: #1E3040;
    --border-glow: rgba(16,185,129,0.25);
    --accent-emerald: #10B981;
    --accent-emerald-bright: #34D399;
    --accent-emerald-deep: #059669;
    --accent-emerald-glow: rgba(16,185,129,0.15);
    --accent-amber: #F59E0B;
    --accent-amber-glow: rgba(245,158,11,0.12);
    --accent-rose: #F43F5E;
    --accent-rose-glow: rgba(244,63,94,0.12);
    --text-primary: #F1F5F9;
    --text-secondary: #CBD5E1;
    --text-muted: #94A3B8;
    --text-dim: #64748B;
    --glass-bg: rgba(15,25,35,0.65);
    --glass-border: rgba(255,255,255,0.04);
}

/* ── Global Body & Container ────────────────────────── */
html, body, [data-testid="stAppViewContainer"],
[data-testid="stApp"] {
    background: var(--bg-base) !important;
    color: var(--text-primary) !important;
    font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif !important;
}

/* ── Animated Mesh Background ───────────────────────── */
[data-testid="stAppViewContainer"]::before {
    content: '';
    position: fixed;
    top: 0; left: 0; right: 0; bottom: 0;
    background:
        radial-gradient(ellipse 80% 60% at 10% 20%, rgba(16,185,129,0.04) 0%, transparent 60%),
        radial-gradient(ellipse 60% 50% at 85% 75%, rgba(5,150,105,0.03) 0%, transparent 55%),
        radial-gradient(ellipse 50% 40% at 50% 10%, rgba(16,185,129,0.025) 0%, transparent 50%);
    pointer-events: none;
    z-index: 0;
    animation: meshShift 20s ease-in-out infinite alternate;
}
@keyframes meshShift {
    0%   { opacity: 0.7; }
    50%  { opacity: 1;   }
    100% { opacity: 0.8; }
}

[data-testid="stHeader"] {
    background: rgba(11,15,18,0.75) !important;
    backdrop-filter: blur(20px) saturate(1.8);
    border-bottom: 1px solid rgba(30,48,64,0.5);
}

/* ── Main Content ───────────────────────────────────── */
.main .block-container {
    padding-top: 2rem !important;
}

/* ── Sidebar ────────────────────────────────────────── */
[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #0D1520 0%, #101820 40%, #0F1A24 100%) !important;
    border-right: 1px solid var(--border-subtle) !important;
}
[data-testid="stSidebar"]::before {
    content: '';
    position: absolute;
    top: 0; left: 0; right: 0;
    height: 200px;
    background: radial-gradient(ellipse at 50% 0%, rgba(16,185,129,0.06) 0%, transparent 70%);
    pointer-events: none;
}
[data-testid="stSidebar"] * {
    color: var(--text-primary) !important;
}
[data-testid="stSidebar"] .stMarkdown p,
[data-testid="stSidebar"] label {
    color: var(--text-muted) !important;
}
[data-testid="stSidebar"] h1,
[data-testid="stSidebar"] h2,
[data-testid="stSidebar"] h3 {
    color: var(--text-primary) !important;
}

/* ── Headings ───────────────────────────────────────── */
h1, h2, h3, h4 {
    color: var(--text-primary) !important;
    font-family: 'Inter', sans-serif !important;
    letter-spacing: -0.025em;
}
h1 { font-weight: 900 !important; }
h2 { font-weight: 700 !important; }
h3 { font-weight: 600 !important; }

/* ── Metric Cards ───────────────────────────────────── */
[data-testid="stMetric"],
[data-testid="metric-container"] {
    background: linear-gradient(160deg, var(--bg-card) 0%, #1A2836 100%) !important;
    border: 1px solid var(--border-subtle) !important;
    border-radius: 16px !important;
    padding: 22px 24px !important;
    box-shadow: 0 4px 24px rgba(0,0,0,0.3), inset 0 1px 0 rgba(255,255,255,0.03) !important;
    transition: all 0.35s cubic-bezier(0.4, 0, 0.2, 1);
    position: relative;
    overflow: hidden;
}
[data-testid="stMetric"]::before {
    content: '';
    position: absolute;
    top: 0; left: 0; right: 0;
    height: 3px;
    background: linear-gradient(90deg, var(--accent-emerald), var(--accent-emerald-deep));
    opacity: 0;
    transition: opacity 0.3s ease;
}
[data-testid="stMetric"]:hover {
    transform: translateY(-3px);
    border-color: rgba(16,185,129,0.2) !important;
    box-shadow: 0 12px 40px rgba(0,0,0,0.4), 0 0 20px var(--accent-emerald-glow) !important;
}
[data-testid="stMetric"]:hover::before {
    opacity: 1;
}
[data-testid="stMetricLabel"] {
    color: var(--text-muted) !important;
    font-weight: 600 !important;
    font-size: 0.72rem !important;
    text-transform: uppercase;
    letter-spacing: 0.08em;
}
[data-testid="stMetricValue"] {
    color: var(--text-primary) !important;
    font-weight: 800 !important;
    font-size: 1.9rem !important;
    font-family: 'Inter', sans-serif !important;
}

/* ── Buttons ────────────────────────────────────────── */
.stButton > button {
    background: linear-gradient(135deg, #10B981 0%, #059669 50%, #047857 100%) !important;
    color: #FFFFFF !important;
    border: none !important;
    border-radius: 12px !important;
    font-weight: 700 !important;
    font-size: 0.95rem !important;
    padding: 0.75rem 1.8rem !important;
    letter-spacing: 0.03em;
    transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1) !important;
    box-shadow: 0 4px 16px rgba(16,185,129,0.35), inset 0 1px 0 rgba(255,255,255,0.15) !important;
    text-shadow: 0 1px 2px rgba(0,0,0,0.2);
    position: relative;
    overflow: hidden;
}
.stButton > button::before {
    content: '';
    position: absolute;
    top: 0; left: -100%; right: 0; bottom: 0;
    width: 200%;
    background: linear-gradient(90deg, transparent 0%, rgba(255,255,255,0.1) 50%, transparent 100%);
    transition: left 0.5s ease;
}
.stButton > button:hover {
    transform: translateY(-2px) scale(1.01);
    box-shadow: 0 8px 28px rgba(16,185,129,0.5), inset 0 1px 0 rgba(255,255,255,0.2) !important;
}
.stButton > button:hover::before {
    left: 100%;
}
.stButton > button:active {
    transform: translateY(0px) scale(0.99);
}

/* ── File Uploader ──────────────────────────────────── */
[data-testid="stFileUploader"] {
    background: var(--bg-card) !important;
    border: 2px dashed var(--border-subtle) !important;
    border-radius: 14px !important;
    padding: 18px !important;
    transition: all 0.3s ease;
}
[data-testid="stFileUploader"]:hover {
    border-color: var(--accent-emerald) !important;
    box-shadow: 0 0 16px var(--accent-emerald-glow);
}
[data-testid="stFileUploader"] section {
    background-color: transparent !important;
}
[data-testid="stFileUploader"] section > button {
    background: rgba(16,185,129,0.12) !important;
    color: var(--accent-emerald-bright) !important;
    border: 1px solid rgba(16,185,129,0.25) !important;
    border-radius: 8px !important;
}
[data-testid="stFileUploader"] small {
    color: var(--text-dim) !important;
}

/* ── Text Areas & Inputs ────────────────────────────── */
textarea, input, [data-testid="stTextArea"] textarea {
    background: var(--bg-card) !important;
    color: var(--text-primary) !important;
    border: 1px solid var(--border-subtle) !important;
    border-radius: 12px !important;
    font-family: 'Inter', sans-serif !important;
    font-size: 0.9rem !important;
    transition: all 0.3s ease;
}
textarea:focus, input:focus {
    border-color: var(--accent-emerald) !important;
    box-shadow: 0 0 0 3px var(--accent-emerald-glow), 0 0 20px rgba(16,185,129,0.08) !important;
}
textarea::placeholder {
    color: var(--text-dim) !important;
    font-style: italic;
}

/* ── Sliders ────────────────────────────────────────── */
[data-testid="stSlider"] [role="slider"] {
    background-color: var(--accent-emerald) !important;
    box-shadow: 0 0 8px var(--accent-emerald-glow);
}

/* ── Expander ───────────────────────────────────────── */
[data-testid="stExpander"] {
    background: var(--bg-card) !important;
    border: 1px solid var(--border-subtle) !important;
    border-radius: 14px !important;
    transition: border-color 0.3s ease;
}
[data-testid="stExpander"]:hover {
    border-color: rgba(16,185,129,0.15) !important;
}
[data-testid="stExpander"] summary {
    color: var(--text-primary) !important;
    font-weight: 500 !important;
}

/* ── Dividers ───────────────────────────────────────── */
hr {
    border-color: var(--border-subtle) !important;
    opacity: 0.4;
}

/* ── Scrollbar ──────────────────────────────────────── */
::-webkit-scrollbar { width: 6px; }
::-webkit-scrollbar-track { background: var(--bg-base); }
::-webkit-scrollbar-thumb {
    background: var(--border-subtle);
    border-radius: 3px;
}
::-webkit-scrollbar-thumb:hover { background: var(--text-dim); }

/* ── Plotly Chart Container ─────────────────────────── */
[data-testid="stPlotlyChart"] {
    background-color: transparent !important;
    border-radius: 16px;
}

/* ── Column gap helper ──────────────────────────────── */
[data-testid="stHorizontalBlock"] {
    gap: 16px !important;
}

/* ══════════════════════════════════════════════════════
   CUSTOM COMPONENT STYLES
   ══════════════════════════════════════════════════════ */

/* ── Animated Gradient Glow Border ──────────────────── */
@keyframes borderGlow {
    0%, 100% { border-color: rgba(16,185,129,0.2); }
    50%      { border-color: rgba(16,185,129,0.4); }
}

/* ── Hero Card ──────────────────────────────────────── */
.hero-card {
    background: linear-gradient(135deg, #0C1620 0%, #111D28 35%, #162232 70%, #1A2836 100%);
    border: 1px solid var(--border-subtle);
    border-radius: 20px;
    padding: 44px 48px;
    margin-bottom: 32px;
    box-shadow:
        0 1px 0 0 rgba(255,255,255,0.03) inset,
        0 20px 60px -12px rgba(0,0,0,0.5),
        0 0 40px rgba(16,185,129,0.03);
    position: relative;
    overflow: hidden;
}
/* Animated glow orbs */
.hero-card::before {
    content: '';
    position: absolute;
    top: -100px;
    right: -80px;
    width: 350px;
    height: 350px;
    background: radial-gradient(circle, rgba(16,185,129,0.08) 0%, rgba(16,185,129,0.02) 40%, transparent 70%);
    pointer-events: none;
    animation: orbFloat 8s ease-in-out infinite alternate;
}
.hero-card::after {
    content: '';
    position: absolute;
    bottom: -120px;
    left: -60px;
    width: 300px;
    height: 300px;
    background: radial-gradient(circle, rgba(5,150,105,0.05) 0%, transparent 65%);
    pointer-events: none;
    animation: orbFloat 10s ease-in-out infinite alternate-reverse;
}
@keyframes orbFloat {
    0%   { transform: translate(0, 0) scale(1); }
    100% { transform: translate(20px, -15px) scale(1.1); }
}

.hero-title {
    font-size: 2.2rem;
    font-weight: 900;
    color: #F8FAFC;
    margin: 0 0 10px 0;
    letter-spacing: -0.04em;
    line-height: 1.15;
    position: relative;
    z-index: 1;
}
.hero-title .accent {
    background: linear-gradient(135deg, #34D399 0%, #10B981 50%, #059669 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
}
.hero-subtitle {
    font-size: 1rem;
    color: #94A3B8;
    margin: 0 0 20px 0;
    font-weight: 400;
    line-height: 1.6;
    max-width: 600px;
    position: relative;
    z-index: 1;
}
.hero-authors {
    font-size: 0.82rem;
    color: #64748B;
    margin: 0;
    display: flex;
    gap: 8px;
    flex-wrap: wrap;
    position: relative;
    z-index: 1;
}
.hero-divider {
    width: 48px;
    height: 3px;
    background: linear-gradient(90deg, var(--accent-emerald), transparent);
    border-radius: 2px;
    margin: 16px 0;
    position: relative;
    z-index: 1;
}

/* ── Badge ──────────────────────────────────────────── */
.badge {
    display: inline-flex;
    align-items: center;
    gap: 6px;
    padding: 5px 14px;
    border-radius: 20px;
    font-size: 0.75rem;
    font-weight: 600;
    letter-spacing: 0.03em;
    transition: all 0.25s ease;
}
.badge-emerald {
    background: rgba(16,185,129,0.1);
    color: #34D399;
    border: 1px solid rgba(16,185,129,0.2);
}
.badge-emerald:hover {
    background: rgba(16,185,129,0.18);
    border-color: rgba(16,185,129,0.35);
    box-shadow: 0 0 12px rgba(16,185,129,0.15);
}
.badge-amber {
    background: rgba(245,158,11,0.1);
    color: #FBBF24;
    border: 1px solid rgba(245,158,11,0.2);
}
.badge-rose {
    background: rgba(244,63,94,0.1);
    color: #FB7185;
    border: 1px solid rgba(244,63,94,0.2);
}
.badge-slate {
    background: rgba(148,163,184,0.07);
    color: #94A3B8;
    border: 1px solid rgba(148,163,184,0.12);
    transition: all 0.25s ease;
}
.badge-slate:hover {
    background: rgba(16,185,129,0.08);
    color: var(--accent-emerald-bright);
    border-color: rgba(16,185,129,0.2);
}

/* ── Status Pills ───────────────────────────────────── */
.status-exact  { color: #34D399; font-weight: 700; }
.status-fuzzy  { color: #FBBF24; font-weight: 700; }
.status-missing { color: #FB7185; font-weight: 700; }

/* ── Step Cards ─────────────────────────────────────── */
.step-card {
    background: linear-gradient(160deg, var(--bg-card) 0%, #1A2836 100%);
    border: 1px solid var(--border-subtle);
    border-radius: 18px;
    padding: 36px 28px 30px;
    text-align: center;
    transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1);
    position: relative;
    overflow: hidden;
    box-shadow: 0 4px 20px rgba(0,0,0,0.25);
}
.step-card::before {
    content: '';
    position: absolute;
    top: 0; left: 0; right: 0;
    height: 3px;
    background: linear-gradient(90deg, transparent, var(--accent-emerald), transparent);
    opacity: 0;
    transition: opacity 0.4s ease;
}
.step-card:hover {
    transform: translateY(-6px);
    border-color: rgba(16,185,129,0.25);
    box-shadow: 0 16px 48px rgba(0,0,0,0.35), 0 0 24px var(--accent-emerald-glow);
}
.step-card:hover::before {
    opacity: 1;
}
.step-card .step-icon {
    width: 56px;
    height: 56px;
    margin: 0 auto 16px;
    border-radius: 16px;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 1.5rem;
    background: rgba(16,185,129,0.08);
    border: 1px solid rgba(16,185,129,0.15);
    transition: all 0.3s ease;
}
.step-card:hover .step-icon {
    background: rgba(16,185,129,0.15);
    border-color: rgba(16,185,129,0.3);
    transform: scale(1.08);
    box-shadow: 0 0 20px rgba(16,185,129,0.12);
}
.step-card .step-num {
    position: absolute;
    top: 14px;
    right: 18px;
    font-size: 3rem;
    font-weight: 900;
    color: rgba(16,185,129,0.06);
    line-height: 1;
    pointer-events: none;
}
.step-card .step-title {
    font-weight: 700;
    color: #F1F5F9;
    margin-bottom: 8px;
    font-size: 1.05rem;
}
.step-card .step-desc {
    color: #94A3B8;
    font-size: 0.85rem;
    line-height: 1.5;
}

/* ── Glass Panel ────────────────────────────────────── */
.glass-panel {
    background: var(--glass-bg);
    backdrop-filter: blur(12px) saturate(1.5);
    border: 1px solid var(--glass-border);
    border-radius: 18px;
    padding: 28px 32px;
    box-shadow: 0 8px 32px rgba(0,0,0,0.25);
    position: relative;
}
.glass-panel::before {
    content: '';
    position: absolute;
    top: 0; left: 0; right: 0;
    height: 1px;
    background: linear-gradient(90deg, transparent, rgba(255,255,255,0.06), transparent);
}

/* ── Checklist Card ─────────────────────────────────── */
.checklist-card {
    background: linear-gradient(160deg, var(--bg-card) 0%, #1A2836 100%);
    border: 1px solid var(--border-subtle);
    border-radius: 16px;
    padding: 28px 32px;
    margin-top: 12px;
    box-shadow: 0 4px 20px rgba(0,0,0,0.2);
    position: relative;
    overflow: hidden;
}
.checklist-card::before {
    content: '';
    position: absolute;
    top: 0; left: 0; right: 0;
    height: 1px;
    background: linear-gradient(90deg, transparent, rgba(255,255,255,0.04), transparent);
}
.checklist-item {
    display: flex;
    align-items: center;
    padding: 12px 0;
    border-bottom: 1px solid rgba(30,48,64,0.4);
    font-size: 0.92rem;
    color: var(--text-primary);
    transition: all 0.2s ease;
}
.checklist-item:hover {
    padding-left: 8px;
}
.checklist-item:last-child { border-bottom: none; }
.checklist-icon {
    width: 26px;
    height: 26px;
    border-radius: 8px;
    display: inline-flex;
    align-items: center;
    justify-content: center;
    margin-right: 14px;
    font-size: 0.8rem;
    font-weight: 700;
    flex-shrink: 0;
}
.checklist-icon-rose {
    background: rgba(244,63,94,0.12);
    color: #FB7185;
    border: 1px solid rgba(244,63,94,0.2);
}

/* ── Skill Recommendation Cards ────────────────────── */
.recommendation-card {
    background: linear-gradient(145deg, #151F2B 0%, #101820 100%);
    border: 1px solid rgba(30,48,64,0.7);
    border-radius: 12px;
    padding: 16px 20px;
    margin-bottom: 12px;
    transition: all 0.25s ease;
}
.recommendation-card:hover {
    border-color: rgba(16,185,129,0.3);
    box-shadow: 0 4px 20px rgba(0,0,0,0.25);
}
.bullet-preview {
    background: rgba(11,15,18,0.75);
    border-left: 3px solid #10B981;
    border-radius: 0 8px 8px 0;
    padding: 12px 16px;
    font-size: 0.88rem;
    color: #CBD5E1;
    margin: 8px 0;
    line-height: 1.55;
    font-family: 'Inter', sans-serif;
}
.gemini-panel {
    background: linear-gradient(145deg, rgba(16,24,32,0.95), rgba(21,31,43,0.95));
    border: 1px solid rgba(56,189,248,0.3);
    border-radius: 16px;
    padding: 24px;
    margin-top: 16px;
    box-shadow: 0 8px 32px rgba(0,0,0,0.3);
}

/* ── Section Headers ────────────────────────────────── */
.section-header {
    display: flex;
    align-items: center;
    gap: 12px;
    margin-bottom: 20px;
    padding-bottom: 12px;
    border-bottom: 1px solid rgba(30,48,64,0.5);
}
.section-header .section-icon {
    width: 36px;
    height: 36px;
    border-radius: 10px;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 1.1rem;
}
.section-header .section-title {
    font-size: 1.15rem;
    font-weight: 700;
    color: var(--text-primary);
    margin: 0;
}
.section-header .section-subtitle {
    font-size: 0.8rem;
    color: var(--text-dim);
    margin: 2px 0 0 0;
}

/* ── Audit Table ────────────────────────────────────── */
.audit-table-wrap {
    overflow-x: auto;
    border-radius: 16px;
    border: 1px solid var(--border-subtle);
    box-shadow: 0 4px 24px rgba(0,0,0,0.2);
}
.audit-table {
    width: 100%;
    border-collapse: collapse;
    font-size: 0.88rem;
}
.audit-table th {
    background: linear-gradient(180deg, #1A2836, #162232);
    color: var(--accent-emerald);
    font-weight: 700;
    text-transform: uppercase;
    font-size: 0.72rem;
    letter-spacing: 0.07em;
    padding: 16px 18px;
    text-align: left;
    border-bottom: 2px solid rgba(16,185,129,0.3);
    position: sticky;
    top: 0;
}
.audit-table td {
    background: var(--bg-card);
    color: var(--text-primary);
    padding: 14px 18px;
    border-bottom: 1px solid rgba(30,48,64,0.3);
    transition: background 0.2s ease;
    vertical-align: middle;
}
.audit-table tr:hover td {
    background: #1A2836;
}
.audit-table tr:last-child td {
    border-bottom: none;
}

/* ── Score Bar ──────────────────────────────────────── */
.score-bar-bg {
    flex: 1;
    background: rgba(15,25,35,0.7);
    border-radius: 6px;
    height: 10px;
    max-width: 130px;
    overflow: hidden;
    border: 1px solid rgba(30,48,64,0.3);
}
.score-bar-fill {
    height: 100%;
    border-radius: 6px;
    transition: width 0.6s cubic-bezier(0.4, 0, 0.2, 1);
    position: relative;
}
.score-bar-fill::after {
    content: '';
    position: absolute;
    top: 0; right: 0; bottom: 0;
    width: 20px;
    background: linear-gradient(90deg, transparent, rgba(255,255,255,0.15));
    border-radius: 0 6px 6px 0;
}

/* ── Sidebar Score Summary ──────────────────────────── */
.sidebar-score-card {
    background: linear-gradient(160deg, var(--bg-card) 0%, #1A2836 100%);
    border: 1px solid var(--border-subtle);
    border-radius: 16px;
    padding: 24px;
    text-align: center;
    box-shadow: 0 4px 20px rgba(0,0,0,0.25);
    position: relative;
    overflow: hidden;
}
.sidebar-score-card::before {
    content: '';
    position: absolute;
    top: -60px; left: 50%;
    transform: translateX(-50%);
    width: 200px; height: 200px;
    border-radius: 50%;
    pointer-events: none;
}

/* ── Tech Stack Footer ──────────────────────────────── */
.tech-stack {
    text-align: center;
    margin-top: 40px;
    padding: 32px 20px;
    border-top: 1px solid rgba(30,48,64,0.3);
}
.tech-stack .badges {
    display: flex;
    justify-content: center;
    flex-wrap: wrap;
    gap: 8px;
    margin-bottom: 16px;
}
.tech-stack .tagline {
    color: #475569;
    font-size: 0.78rem;
    letter-spacing: 0.04em;
}

/* ── Animations ─────────────────────────────────────── */
@keyframes fadeInUp {
    from { opacity: 0; transform: translateY(20px); }
    to   { opacity: 1; transform: translateY(0); }
}
@keyframes fadeIn {
    from { opacity: 0; }
    to   { opacity: 1; }
}
@keyframes slideInLeft {
    from { opacity: 0; transform: translateX(-24px); }
    to   { opacity: 1; transform: translateX(0); }
}
@keyframes pulse {
    0%, 100% { opacity: 1; }
    50%      { opacity: 0.7; }
}
.animate-in {
    animation: fadeInUp 0.55s ease-out both;
}
.animate-delay-1 { animation-delay: 0.1s; }
.animate-delay-2 { animation-delay: 0.2s; }
.animate-delay-3 { animation-delay: 0.3s; }
.animate-fade { animation: fadeIn 0.6s ease-out both; }
.animate-slide { animation: slideInLeft 0.5s ease-out both; }

/* ── Perfect Score Celebration ───────────────────────── */
@keyframes shimmer {
    0%   { background-position: -200% center; }
    100% { background-position: 200% center; }
}
.perfect-text {
    background: linear-gradient(90deg, #34D399, #10B981, #6EE7B7, #10B981, #34D399);
    background-size: 200% auto;
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
    animation: shimmer 3s linear infinite;
}

/* ── Spinner & Loading ──────────────────────────────── */
.stSpinner > div {
    border-color: var(--accent-emerald) !important;
}

/* ── Toast / Alert Messages ─────────────────────────── */
[data-testid="stAlert"] {
    background: var(--bg-card) !important;
    border: 1px solid var(--border-subtle) !important;
    border-radius: 12px !important;
    color: var(--text-primary) !important;
}

/* ── Tabs ────────────────────────────────────────────── */
.stTabs [data-baseweb="tab-list"] {
    gap: 6px;
    background: var(--bg-surface) !important;
    border-radius: 14px;
    padding: 5px;
    border: 1px solid var(--border-subtle);
}
.stTabs [data-baseweb="tab"] {
    border-radius: 10px !important;
    color: var(--text-muted) !important;
    font-weight: 500 !important;
    transition: all 0.25s ease;
}
.stTabs [aria-selected="true"] {
    background: var(--bg-card) !important;
    color: var(--accent-emerald-bright) !important;
    box-shadow: 0 2px 8px rgba(0,0,0,0.2);
}
</style>
"""

st.markdown(CUSTOM_CSS, unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════
# HERO HEADER
# ══════════════════════════════════════════════════════════════
st.markdown("""
<div class="hero-card animate-in">
    <div class="hero-title">
        <span class="accent">AI-Powered</span> Resume &amp;<br>ATS Optimizer
    </div>
    <div class="hero-divider"></div>
    <div class="hero-subtitle">
        Intelligent Resume Intelligence &amp; ATS Diagnostic Engine &mdash; Comprehensive skill alignment, semantic gap detection, and actionable resume optimization.
    </div>
</div>
""", unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════
# SIDEBAR
# ══════════════════════════════════════════════════════════════
with st.sidebar:
    st.markdown("""
    <div style="text-align:center;margin-bottom:8px;">
        <div style="font-size:1.4rem;font-weight:800;color:#F1F5F9;letter-spacing:-0.03em;">ATS Optimizer</div>
        <div style="font-size:0.72rem;color:#64748B;text-transform:uppercase;letter-spacing:0.1em;margin-top:2px;">Configuration Panel</div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("---")
    st.markdown("#### 📄 Resume Input")
    uploaded_pdf = st.file_uploader(
        "Upload your resume (PDF)",
        type=["pdf"],
        help="Upload a PDF resume to extract skills automatically.",
    )

    with st.expander("Or paste resume text manually"):
        manual_resume_text = st.text_area(
            "Resume text",
            height=180,
            placeholder="Paste your resume content here...",
        )

    st.markdown("---")
    st.markdown("#### 🎯 Target Job Description")
    jd_text = st.text_area(
        "Paste the Job Description",
        height=220,
        placeholder="Paste the full job description here to extract required skills...",
    )

    # ── Silently initialize API Key in background ───────
    raw_env_key = os.environ.get("GEMINI_API_KEY", "")
    secret_key = ""
    try:
        if hasattr(st, "secrets") and "GEMINI_API_KEY" in st.secrets:
            secret_key = str(st.secrets["GEMINI_API_KEY"])
    except Exception:
        pass

    active_gemini_key = (raw_env_key or secret_key).strip()
    match_threshold = 80
    partial_threshold = 60

    st.markdown("---")
    run_clicked = st.button("🚀 Run Full AI Diagnostic", use_container_width=True, type="primary")

    st.markdown("""
    <div style="margin-top:20px;padding:14px;background:rgba(15,25,35,0.7);border:1px solid #1E3040;border-radius:12px;text-align:center;">
        <div style="font-size:0.68rem;text-transform:uppercase;letter-spacing:0.12em;color:#10B981;font-weight:700;margin-bottom:6px;">Project Author</div>
        <div style="font-size:0.76rem;color:#CBD5E1;line-height:1.6;">
            <div style="font-weight:600;color:#F1F5F9;">Vinayak Mamtani</div>
        </div>
        <div style="margin-top:8px;font-size:0.68rem;color:#10B981;font-weight:600;">100% Explainable Rule-Based ATS</div>
    </div>
    """, unsafe_allow_html=True)


# ══════════════════════════════════════════════════════════════
# CHART HELPERS
# ══════════════════════════════════════════════════════════════

def render_gauge(score: float) -> go.Figure:
    """Create a premium Plotly gauge chart for the ATS score."""
    if score >= 75:
        bar_color = "#10B981"
        text_color = "#34D399"
    elif score >= 50:
        bar_color = "#F59E0B"
        text_color = "#FBBF24"
    else:
        bar_color = "#F43F5E"
        text_color = "#FB7185"

    fig = go.Figure(go.Indicator(
        mode="gauge+number",
        value=score,
        number={
            "suffix": "%",
            "font": {"size": 56, "color": text_color, "family": "Inter, sans-serif", "weight": 800},
        },
        title={
            "text": "<b>OVERALL ATS MATCH SCORE</b>",
            "font": {"size": 12, "color": "#64748B", "family": "Inter, sans-serif"},
        },
        gauge={
            "axis": {
                "range": [0, 100],
                "tickwidth": 1,
                "tickcolor": "rgba(30,48,64,0.4)",
                "tickfont": {"color": "#475569", "size": 10},
                "dtick": 20,
            },
            "bar": {"color": bar_color, "thickness": 0.75},
            "bgcolor": "#111D28",
            "borderwidth": 0,
            "steps": [
                {"range": [0, 40], "color": "rgba(244,63,94,0.08)"},
                {"range": [40, 60], "color": "rgba(245,158,11,0.06)"},
                {"range": [60, 80], "color": "rgba(16,185,129,0.05)"},
                {"range": [80, 100], "color": "rgba(16,185,129,0.1)"},
            ],
            "threshold": {
                "line": {"color": "#F1F5F9", "width": 2.5},
                "thickness": 0.85,
                "value": score,
            },
        },
    ))
    fig.update_layout(
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font={"family": "Inter, sans-serif"},
        height=280,
        margin=dict(l=24, r=24, t=70, b=10),
    )
    return fig


def render_donut(exact: int, fuzzy: int, missing: int) -> go.Figure:
    """Create a premium Plotly donut chart for skill distribution."""
    labels = ["Exact Match", "Fuzzy Match", "Missing"]
    values = [exact, fuzzy, missing]
    colors = ["#10B981", "#F59E0B", "#F43F5E"]

    fig = go.Figure(data=[go.Pie(
        labels=labels,
        values=values,
        hole=0.6,
        marker=dict(
            colors=colors,
            line=dict(color="#0B0F12", width=4),
        ),
        textfont=dict(size=12, color="#F1F5F9", family="Inter, sans-serif"),
        textinfo="label+percent",
        hoverinfo="label+value+percent",
        pull=[0.02, 0.02, 0.05],
        rotation=90,
    )])

    total = exact + fuzzy + missing
    fig.update_layout(
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font={"family": "Inter, sans-serif", "color": "#94A3B8"},
        showlegend=True,
        legend=dict(
            orientation="h",
            yanchor="bottom", y=-0.18,
            xanchor="center", x=0.5,
            font=dict(color="#94A3B8", size=11),
        ),
        height=300,
        margin=dict(l=16, r=16, t=24, b=48),
        annotations=[dict(
            text=f"<b>{total}</b><br><span style='font-size:10px;color:#64748B'>TOTAL</span>",
            x=0.5, y=0.5,
            font=dict(size=22, color="#94A3B8", family="Inter, sans-serif"),
            showarrow=False,
        )],
    )
    return fig


def render_category_bar(report: ATSReport) -> go.Figure:
    """Create a horizontal bar chart showing skill matches by category."""
    cat_stats: dict[str, dict] = {}
    for r in report.skill_results:
        cat = SKILL_TAXONOMY.get(r.required_skill, {}).get("category", "Other")
        if cat not in cat_stats:
            cat_stats[cat] = {"exact": 0, "fuzzy": 0, "missing": 0}
        if r.status == "Exact Match":
            cat_stats[cat]["exact"] += 1
        elif r.status == "Fuzzy Match":
            cat_stats[cat]["fuzzy"] += 1
        else:
            cat_stats[cat]["missing"] += 1

    categories = sorted(cat_stats.keys())
    exact_vals = [cat_stats[c]["exact"] for c in categories]
    fuzzy_vals = [cat_stats[c]["fuzzy"] for c in categories]
    missing_vals = [cat_stats[c]["missing"] for c in categories]

    fig = go.Figure()
    fig.add_trace(go.Bar(
        y=categories, x=exact_vals, name="Exact Match",
        orientation='h', marker_color="#10B981",
        text=exact_vals, textposition='inside',
        textfont=dict(color="#fff", size=11, family="Inter"),
    ))
    fig.add_trace(go.Bar(
        y=categories, x=fuzzy_vals, name="Fuzzy Match",
        orientation='h', marker_color="#F59E0B",
        text=fuzzy_vals, textposition='inside',
        textfont=dict(color="#fff", size=11, family="Inter"),
    ))
    fig.add_trace(go.Bar(
        y=categories, x=missing_vals, name="Missing",
        orientation='h', marker_color="#F43F5E",
        text=missing_vals, textposition='inside',
        textfont=dict(color="#fff", size=11, family="Inter"),
    ))
    fig.update_layout(
        barmode='stack',
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font=dict(family="Inter, sans-serif", color="#94A3B8"),
        height=max(180, len(categories) * 44),
        margin=dict(l=10, r=20, t=10, b=10),
        legend=dict(
            orientation="h", yanchor="bottom", y=1.05,
            xanchor="center", x=0.5,
            font=dict(color="#94A3B8", size=11),
        ),
        xaxis=dict(
            showgrid=True, gridcolor="rgba(30,48,64,0.3)",
            zeroline=False, tickfont=dict(color="#64748B"),
        ),
        yaxis=dict(
            tickfont=dict(color="#CBD5E1", size=12),
            automargin=True,
        ),
        bargap=0.25,
    )
    return fig


# ══════════════════════════════════════════════════════════════
# RENDER RESULTS (4 RECRUITER TABS + FULL AUDIT EXPORT)
# ══════════════════════════════════════════════════════════════

def render_results(
    report: ATSReport,
    resume_text: str = "",
    jd_text: str = "",
    gemini_api_key: str = "",
    gemini_audit: dict = None,
):
    """
    Render recruiter-grade results across 4 dedicated tabs:
    - Tab 1: Executive Match & Metric Dashboard
    - Tab 2: Skill Matrix & Gap Analysis
    - Tab 3: Project Depth & Bullet Rewrites
    - Tab 4: Interview Prep Questions
    Plus interactive full audit report export.
    """
    if gemini_audit is None:
        gemini_audit = {}

    # Score color
    if report.ats_score >= 75:
        sc = "#10B981"
        label = "STRONG RECRUITER MATCH"
    elif report.ats_score >= 50:
        sc = "#F59E0B"
        label = "MODERATE ALIGNMENT"
    else:
        sc = "#F43F5E"
        label = "CRITICAL GAP DETECTED"

    # ── Metric Row ───────────────────────────────────────
    m1, m2, m3, m4, m5 = st.columns(5)
    m1.metric("ATS Match Score", f"{report.ats_score}%")
    m2.metric("Total JD Skills", report.total_jd_skills)
    m3.metric("Exact Matches", report.exact_count)
    m4.metric("Fuzzy Variants", report.fuzzy_count)
    m5.metric("Missing Skills", report.missing_count)

    st.markdown("<br>", unsafe_allow_html=True)

    # ── Master Results Navigation Tabs (Recruiter Grade) ─
    tab_exec, tab_matrix, tab_depth, tab_interview = st.tabs([
        "📊 Tab 1: Executive Match & Metric Dashboard",
        "🧬 Tab 2: Skill Matrix & Gap Analysis",
        "🛠️ Tab 3: Project Depth & Bullet Rewrites",
        "🎯 Tab 4: Interview Prep Questions",
    ])

    # ══════════════════════════════════════════════════════
    # TAB 1: EXECUTIVE MATCH & METRIC DASHBOARD
    # ══════════════════════════════════════════════════════
    with tab_exec:
        g_left, g_right = st.columns([3, 2])
        with g_left:
            st.plotly_chart(render_gauge(report.ats_score), use_container_width=True)
        with g_right:
            st.markdown(f"""
            <div class="glass-panel animate-in" style="margin-top:12px;">
                <div style="text-align:center;">
                    <div style="font-size:0.7rem;text-transform:uppercase;letter-spacing:0.1em;color:{sc};font-weight:700;margin-bottom:4px;">{label}</div>
                    <div style="font-size:3rem;font-weight:900;color:{sc};line-height:1;">{report.ats_score}%</div>
                    <div style="font-size:0.8rem;color:#64748B;margin-top:6px;">ATS Semantic Compatibility Score</div>
                </div>
                <div style="margin-top:20px;display:grid;grid-template-columns:1fr 1fr 1fr;gap:8px;text-align:center;">
                    <div style="background:rgba(16,185,129,0.08);border-radius:10px;padding:12px 8px;">
                        <div style="font-size:1.4rem;font-weight:800;color:#34D399;">{report.exact_count}</div>
                        <div style="font-size:0.68rem;color:#64748B;text-transform:uppercase;letter-spacing:0.05em;margin-top:2px;">Exact</div>
                    </div>
                    <div style="background:rgba(245,158,11,0.08);border-radius:10px;padding:12px 8px;">
                        <div style="font-size:1.4rem;font-weight:800;color:#FBBF24;">{report.fuzzy_count}</div>
                        <div style="font-size:0.68rem;color:#64748B;text-transform:uppercase;letter-spacing:0.05em;margin-top:2px;">Fuzzy</div>
                    </div>
                    <div style="background:rgba(244,63,94,0.08);border-radius:10px;padding:12px 8px;">
                        <div style="font-size:1.4rem;font-weight:800;color:#FB7185;">{report.missing_count}</div>
                        <div style="font-size:0.68rem;color:#64748B;text-transform:uppercase;letter-spacing:0.05em;margin-top:2px;">Missing</div>
                    </div>
                </div>
            </div>
            """, unsafe_allow_html=True)

        st.markdown("<br>", unsafe_allow_html=True)

        # Candidate Executive Overview
        st.markdown("""
        <div class="section-header animate-in">
            <div class="section-icon" style="background:rgba(16,185,129,0.1);border:1px solid rgba(16,185,129,0.2);">
                <span style="font-size:1rem;">👤</span>
            </div>
            <div>
                <div class="section-title">Candidate Executive Overview</div>
                <div class="section-subtitle">Candidate identity, verified years of experience vs. requirements, and senior recruiter posture</div>
            </div>
        </div>
        """, unsafe_allow_html=True)

        exec_overview = gemini_audit.get("executive_overview", "")
        if exec_overview:
            st.markdown("""
            <div class="gemini-panel animate-in">
            """, unsafe_allow_html=True)
            st.markdown(exec_overview)
            st.markdown("</div>", unsafe_allow_html=True)
        elif not gemini_api_key:
            st.info("Candidate Executive Overview will display once analysis is generated.")
        else:
            st.info("Candidate Executive Overview will display once generated.")

        st.markdown("<br>", unsafe_allow_html=True)

        # Visual charts row
        vcol1, vcol2 = st.columns(2)
        with vcol1:
            st.markdown("##### Skill Match Distribution")
            st.plotly_chart(render_donut(report.exact_count, report.fuzzy_count, report.missing_count), use_container_width=True)
        with vcol2:
            st.markdown("##### Category Alignment Breakdown")
            st.plotly_chart(render_category_bar(report), use_container_width=True)

    # ══════════════════════════════════════════════════════
    # TAB 2: SKILL MATRIX & GAP ANALYSIS
    # ══════════════════════════════════════════════════════
    with tab_matrix:
        st.markdown("""
        <div class="section-header animate-in">
            <div class="section-icon" style="background:rgba(16,185,129,0.1);border:1px solid rgba(16,185,129,0.2);">
                <span style="font-size:1rem;">🧬</span>
            </div>
            <div>
                <div class="section-title">Technical &amp; Domain Alignment Matrix</div>
                <div class="section-subtitle">Concrete evidence-backed skills audit, hard gaps, and adjacent technology translations</div>
            </div>
        </div>
        """, unsafe_allow_html=True)

        tech_matrix = gemini_audit.get("technical_matrix", "")
        if tech_matrix:
            st.markdown("""
            <div class="gemini-panel animate-in">
            """, unsafe_allow_html=True)
            st.markdown(tech_matrix)
            st.markdown("</div>", unsafe_allow_html=True)
        elif not gemini_api_key:
            st.info("Recruiter-grade alignment matrix will display once analysis is generated.")

        st.markdown("<br>", unsafe_allow_html=True)

        # Interactive Skill-by-Skill Audit Table
        st.markdown("""
        <div class="section-header animate-in">
            <div class="section-icon" style="background:rgba(56,189,248,0.1);border:1px solid rgba(56,189,248,0.2);">
                <span style="font-size:1rem;">🔍</span>
            </div>
            <div>
                <div class="section-title">Interactive Skill-by-Skill Audit Table</div>
                <div class="section-subtitle">Breakdown of each required skill match, matched term, and action needed</div>
            </div>
        </div>
        """, unsafe_allow_html=True)

        audit_data = []
        for r in report.skill_results:
            cat = SKILL_TAXONOMY.get(r.required_skill, {}).get("category", "General")
            if r.status == "Exact Match":
                status_display = "✅ Exact Match"
                action_display = "Covered — Strong ATS keyword alignment"
            elif r.status == "Fuzzy Match":
                status_display = "🔶 Fuzzy Match"
                action_display = f"Standardize phrasing to exact term: '{r.required_skill}'"
            else:
                status_display = "❌ Missing"
                action_display = f"Critical Gap — Add '{r.required_skill}' to skills/experience"

            audit_data.append({
                "Required Skill": r.required_skill,
                "Category": cat,
                "Status": status_display,
                "Matched in Resume": r.matched_resume_term if r.matched_resume_term else "—",
                "Match %": r.similarity_score,
                "Action Needed": action_display,
            })

        df = pd.DataFrame(audit_data)

        filter_choice = st.radio(
            "Filter Skills by Status:",
            [
                f"All Skills ({len(df)})",
                f"✅ Exact Matches ({report.exact_count})",
                f"🔶 Fuzzy Matches ({report.fuzzy_count})",
                f"❌ Missing Skills ({report.missing_count})",
            ],
            horizontal=True,
            key="audit_filter_radio",
        )

        if "Exact" in filter_choice:
            display_df = df[df["Status"].str.contains("Exact")]
        elif "Fuzzy" in filter_choice:
            display_df = df[df["Status"].str.contains("Fuzzy")]
        elif "Missing" in filter_choice:
            display_df = df[df["Status"].str.contains("Missing")]
        else:
            display_df = df

        st.dataframe(
            display_df,
            use_container_width=True,
            hide_index=True,
            column_config={
                "Required Skill": st.column_config.TextColumn("Required Skill", width="medium"),
                "Category": st.column_config.TextColumn("Category", width="small"),
                "Status": st.column_config.TextColumn("Status", width="small"),
                "Matched in Resume": st.column_config.TextColumn("Matched in Resume", width="small"),
                "Match %": st.column_config.ProgressColumn(
                    "Match %",
                    min_value=0,
                    max_value=100,
                    format="%d%%",
                    width="small",
                ),
                "Action Needed": st.column_config.TextColumn("Action Needed", width="large"),
            },
            height=min(len(display_df) * 38 + 42, 520),
        )

    # ══════════════════════════════════════════════════════
    # TAB 3: PROJECT DEPTH & BULLET REWRITES
    # ══════════════════════════════════════════════════════
    with tab_depth:
        st.markdown("""
        <div class="section-header animate-in">
            <div class="section-icon" style="background:rgba(245,158,11,0.1);border:1px solid rgba(245,158,11,0.2);">
                <span style="font-size:1rem;">🛠️</span>
            </div>
            <div>
                <div class="section-title">Project &amp; Impact Depth Audit</div>
                <div class="section-subtitle">Production readiness, engineering metrics check, and weak verb elimination</div>
            </div>
        </div>
        """, unsafe_allow_html=True)

        project_depth = gemini_audit.get("project_depth", "")
        if project_depth:
            st.markdown("""
            <div class="gemini-panel animate-in">
            """, unsafe_allow_html=True)
            st.markdown(project_depth)
            st.markdown("</div>", unsafe_allow_html=True)
        elif not gemini_api_key:
            st.info("Project depth analysis will display once analysis is generated.")

        st.markdown("<br>", unsafe_allow_html=True)

        # Actionable Bullet-Point Rewrites
        st.markdown("""
        <div class="section-header animate-in">
            <div class="section-icon" style="background:rgba(16,185,129,0.1);border:1px solid rgba(16,185,129,0.2);">
                <span style="font-size:1rem;">✍️</span>
            </div>
            <div>
                <div class="section-title">Actionable Bullet-Point Rewrites (Google XYZ Formula)</div>
                <div class="section-subtitle">Optimized resume achievements structured as 'Accomplished [X] as measured by [Y], by doing [Z]'</div>
            </div>
        </div>
        """, unsafe_allow_html=True)

        bullet_rewrites = gemini_audit.get("bullet_rewrites", "")
        if bullet_rewrites:
            st.markdown("""
            <div class="gemini-panel animate-in">
            """, unsafe_allow_html=True)
            st.markdown(bullet_rewrites)
            st.markdown("</div>", unsafe_allow_html=True)

            with st.expander("📄 Quick Copy Optimized Bullet Points", expanded=False):
                st.code(bullet_rewrites, language="markdown")
        elif not gemini_api_key:
            st.info("Automated bullet point rewrites will display once analysis is generated.")

        # Additional curated bullet points for missing skills
        if report.missing_skills:
            st.markdown("<br>", unsafe_allow_html=True)
            with st.expander(f"📚 View Additional Curated Achievement Bullets for {report.missing_count} Missing Skills", expanded=False):
                for skill in report.missing_skills:
                    cat = SKILL_TAXONOMY.get(skill, {}).get("category", "General")
                    rec = get_skill_recommendation(skill, cat)
                    st.markdown(f"""
                    <div class="recommendation-card">
                        <div style="display:flex;justify-content:space-between;align-items:center;margin-bottom:6px;">
                            <span style="font-weight:700;color:#34D399;">+ {skill}</span>
                            <span style="color:#64748B;font-size:0.75rem;">{cat}</span>
                        </div>
                        <div style="font-size:0.78rem;color:#94A3B8;margin-bottom:6px;"><strong>Placement Strategy:</strong> {rec['action']}</div>
                        <div class="bullet-preview">{rec['bullet']}</div>
                    </div>
                    """, unsafe_allow_html=True)

    # ══════════════════════════════════════════════════════
    # ══════════════════════════════════════════════════════
    # TAB 4: INTERVIEW PREP QUESTIONS
    # ══════════════════════════════════════════════════════
    with tab_interview:
        st.markdown("""
        <div class="section-header animate-in">
            <div class="section-icon" style="background:rgba(244,63,94,0.1);border:1px solid rgba(244,63,94,0.2);">
                <span style="font-size:1rem;">🎯</span>
            </div>
            <div>
                <div class="section-title">Technical &amp; Behavioral Interview Readiness Studio</div>
                <div class="section-subtitle">Role-tailored screening questions, gap-defense talking points, and behavioral STAR frameworks</div>
            </div>
        </div>
        """, unsafe_allow_html=True)

        interview_questions = gemini_audit.get("interview_questions", "")
        if interview_questions:
            st.markdown("""
            <div style="font-size:0.95rem;font-weight:700;color:#34D399;margin-bottom:10px;">
                🤖 AI Recruiter Targeted Screening Questions
            </div>
            """, unsafe_allow_html=True)
            st.markdown("""
            <div class="gemini-panel animate-in" style="margin-top:0px;margin-bottom:20px;">
            """, unsafe_allow_html=True)
            st.markdown(interview_questions)
            st.markdown("</div>", unsafe_allow_html=True)

            with st.expander("📄 Quick Copy AI Interview Questions", expanded=False):
                st.code(interview_questions, language="markdown")

            st.markdown("<br>", unsafe_allow_html=True)

        # ── 1. Gap-Defense Strategy for Missing Skills ────────
        st.markdown("""
        <div class="section-header animate-in">
            <div class="section-icon" style="background:rgba(244,63,94,0.1);border:1px solid rgba(244,63,94,0.2);">
                <span style="font-size:1rem;">🛡️</span>
            </div>
            <div>
                <div class="section-title">Gap-Defense Strategy (How to Defend Missing Skills)</div>
                <div class="section-subtitle">The ATS flagged these competencies as missing from your resume. Interviewers will test if you can adapt quickly. Use these pivot strategies:</div>
            </div>
        </div>
        """, unsafe_allow_html=True)

        if report.missing_skills:
            for skill in report.missing_skills:
                cat = SKILL_TAXONOMY.get(skill, {}).get("category", "General")
                q_info = get_skill_interview_details(skill, cat)
                st.markdown(f"""
                <div class="recommendation-card animate-in">
                    <div style="display:flex;justify-content:space-between;align-items:center;margin-bottom:8px;">
                        <span style="font-weight:800;font-size:1rem;color:#FB7185;">Missing Competency: {skill}</span>
                        <span class="badge badge-rose">{cat}</span>
                    </div>
                    <div style="background:rgba(244,63,94,0.06);border-left:3px solid #F43F5E;border-radius:0 8px 8px 0;padding:10px 14px;margin-bottom:10px;">
                        <div style="font-size:0.75rem;text-transform:uppercase;letter-spacing:0.06em;color:#FB7185;font-weight:700;">Expected Interview Question:</div>
                        <div style="font-size:0.9rem;font-weight:600;color:#F1F5F9;margin-top:2px;">"{q_info['question']}"</div>
                    </div>
                    <div style="display:grid;grid-template-columns:1fr;gap:8px;font-size:0.83rem;color:#CBD5E1;margin-bottom:8px;">
                        <div>
                            <span style="color:#F59E0B;font-weight:700;">🔍 What They're Assessing:</span> {q_info['intent']}
                        </div>
                        <div>
                            <span style="color:#34D399;font-weight:700;">💡 Recommended Pivot Strategy:</span> {q_info['pivot']}
                        </div>
                        <div>
                            <span style="color:#38BDF8;font-weight:700;">🏷️ Key Terminology to Drop In:</span> <code style="color:#38BDF8;background:rgba(56,189,248,0.1);padding:2px 6px;border-radius:4px;">{q_info['key_terms']}</code>
                        </div>
                    </div>
                </div>
                """, unsafe_allow_html=True)
        else:
            st.markdown("""
            <div style="padding:16px;background:rgba(16,185,129,0.08);border:1px solid rgba(16,185,129,0.2);border-radius:12px;color:#34D399;font-weight:600;font-size:0.9rem;">
                🎉 Zero Critical Skill Gaps Detected — All target skills extracted from the Job Description were matched in your profile!
            </div>
            """, unsafe_allow_html=True)

        st.markdown("<br>", unsafe_allow_html=True)

        # ── 2. Deep-Dive Technical Drilldown on Matched Skills ─
        matched_skills_list = [r.required_skill for r in report.exact_skills + report.fuzzy_skills]
        if matched_skills_list:
            st.markdown("""
            <div class="section-header animate-in">
                <div class="section-icon" style="background:rgba(56,189,248,0.1);border:1px solid rgba(56,189,248,0.2);">
                    <span style="font-size:1rem;">⚡</span>
                </div>
                <div>
                    <div class="section-title">Deep-Dive Technical Drilldown on Your Matched Stack</div>
                    <div class="section-subtitle">Senior engineers and tech leads will probe your hands-on production depth on these confirmed skills:</div>
                </div>
            </div>
            """, unsafe_allow_html=True)

            # Show top matched skills (up to 5)
            for skill in matched_skills_list[:5]:
                cat = SKILL_TAXONOMY.get(skill, {}).get("category", "General")
                q_info = get_skill_interview_details(skill, cat)
                with st.expander(f"⚡ Technical Drilldown: {skill} ({cat})", expanded=False):
                    st.markdown(f"**Likely Technical Screening Question:**")
                    st.markdown(f"> *\"{q_info['question']}\"*")
                    st.markdown(f"**What Senior Interviewers Evaluate:**")
                    st.markdown(f"- {q_info['intent']}")
                    st.markdown(f"**Key Concepts & Tradeoffs to Articulate:**")
                    st.markdown(f"- Recommended keywords: `{q_info['key_terms']}`")
                    st.markdown(f"- {q_info['pivot']}")

            st.markdown("<br>", unsafe_allow_html=True)

        # ── 3. Behavioral STAR Framework Masterclass ──────────
        st.markdown("""
        <div class="section-header animate-in">
            <div class="section-icon" style="background:rgba(245,158,11,0.1);border:1px solid rgba(245,158,11,0.2);">
                <span style="font-size:1rem;">🗣️</span>
            </div>
            <div>
                <div class="section-title">Behavioral Engineering Scenarios (STAR Method)</div>
                <div class="section-subtitle">Structured answers for the 4 most common behavioral questions asked by engineering managers:</div>
            </div>
        </div>
        """, unsafe_allow_html=True)

        bcol1, bcol2 = st.columns(2)

        with bcol1:
            with st.expander("🚨 Scenario 1: Production Outage / Critical Bug", expanded=False):
                st.markdown("""
                **Question:** *"Tell me about a time when a critical bug or service outage occurred. How did you diagnose and resolve it?"*

                - **Situation (S):** High-traffic microservice began dropping requests, or latency spiked 10x during peak hours.
                - **Task (T):** Prevent data loss, restore SLA within 15 minutes, and identify root cause without making unverified changes.
                - **Action (A):** Checked monitoring alerts (logs, APM traces), isolated broken commit or database bottleneck, rolled back deployment or enabled feature flag, then deployed hotfix with automated regression tests.
                - **Result (R):** Restored 99.9% uptime in <12 minutes; authored a blameless post-mortem and added synthetic integration tests to prevent recurrence.
                """)

            with bcol2:
                with st.expander("⚖️ Scenario 2: Architectural Disagreement", expanded=False):
                    st.markdown("""
                    **Question:** *"Describe a situation where you disagreed with a senior engineer or team member on technical design. How did you resolve it?"*

                    - **Situation (S):** Team was divided between a complex distributed microservice setup vs extending an existing modular monolith.
                    - **Task (T):** Deliver on business milestones without escalating interpersonal tension or overengineering prematurely.
                    - **Action (A):** Created a lightweight proof-of-concept (POC) benchmarking latency and developer velocity. Documented quantitative trade-offs in an Architecture Decision Record (ADR).
                    - **Result (R):** Built team consensus around data-backed metrics; saved an estimated 3 weeks of premature infrastructure setup.
                    """)

        bcol3, bcol4 = st.columns(2)

        with bcol3:
            with st.expander("⏱️ Scenario 3: Tight Deadlines vs Technical Debt", expanded=False):
                st.markdown("""
                **Question:** *"How do you balance rapid feature delivery against code quality and technical debt?"*

                - **Situation (S):** Product management required a critical integration launched within 10 days for a pilot customer.
                - **Task (T):** Ship on time while isolating shortcuts so they don't compromise core system stability.
                - **Action (A):** Applied the Adapter Pattern to isolate third-party APIs, prioritized essential unit test coverage on financial/auth flows, and created tracked Jira backlog items for the remaining refactoring.
                - **Result (R):** Successfully hit the client deadline; paid down the 2 deferred refactoring tickets in the subsequent sprint without incident.
                """)

        with bcol4:
            with st.expander("📈 Scenario 4: Diagnosing a Scalability Bottleneck", expanded=False):
                st.markdown("""
                **Question:** *"Walk me through a performance bottleneck you investigated and how you measured the improvement."*

                - **Situation (S):** API response times degraded to >1200ms when database records grew beyond 500,000 entries.
                - **Task (T):** Bring endpoint p95 latency below 100ms without tripling database hardware costs.
                - **Action (A):** Ran `EXPLAIN ANALYZE`, discovered missing composite indexes causing sequential full-table scans, introduced Redis caching for read-heavy endpoints, and paginated large response payloads.
                - **Result (R):** Cut average latency from 1,200ms to 42ms (96% reduction) and reduced database CPU load by 55%.
                """)

        st.markdown("<br>", unsafe_allow_html=True)

        # ── 4. Interactive Interview Rehearsal Checklist ───────
        st.markdown("""
        <div class="section-header animate-in">
            <div class="section-icon" style="background:rgba(16,185,129,0.1);border:1px solid rgba(16,185,129,0.2);">
                <span style="font-size:1rem;">📋</span>
            </div>
            <div>
                <div class="section-title">Pre-Interview Rehearsal Checklist</div>
                <div class="section-subtitle">Track your preparation milestones before the technical screen:</div>
            </div>
        </div>
        """, unsafe_allow_html=True)

        st.checkbox("🎯 1. Mastered the 2-minute 'Walk me through your background' elevator pitch tailored to this role", key="chk_pitch")
        st.checkbox("🛡️ 2. Prepared pivot narratives for all flagged missing skills using adjacent technologies", key="chk_gaps")
        st.checkbox("⚡ 3. Reviewed core systems trade-offs (concurrency, caching, database indexing, latency vs throughput)", key="chk_tradeoffs")
        st.checkbox("🗣️ 4. Formulated at least two concrete STAR stories with quantifiable engineering metrics", key="chk_star")
        st.checkbox("❓ 5. Prepared 3 intelligent questions to ask the interviewer (e.g. deployment frequency, tech debt policy)", key="chk_questions")

    # ══════════════════════════════════════════════════════
    # INTERACTIVE FULL AUDIT EXPORT BUTTON
    # ══════════════════════════════════════════════════════
    st.markdown("<br><hr>", unsafe_allow_html=True)
    dcol1, dcol2 = st.columns([2, 1])
    with dcol1:
        st.markdown("""
        <div style="font-weight:700;font-size:1.15rem;color:#F1F5F9;margin-bottom:4px;">📥 Export Recruiter-Grade Audit Report</div>
        <div style="font-size:0.84rem;color:#94A3B8;">Download the comprehensive critique, semantic alignment matrix, Google XYZ bullet rewrites, and interview preparation questions as a Markdown (.md) report.</div>
        """, unsafe_allow_html=True)
    with dcol2:
        raw_audit_text = (gemini_audit or {}).get("raw", "")
        report_export = f"""# ATS RESUME & RECRUITER-GRADE AUDIT REPORT

## 📊 Objective ATS Metrics
- Overall ATS Match Score: {report.ats_score}%
- Total Target Skills in Job Description: {report.total_jd_skills}
- Exact Matches Detected: {report.exact_count}
- Fuzzy / Adjacent Matches: {report.fuzzy_count}
- Missing Key Competencies: {report.missing_count}

{raw_audit_text}
"""
        st.download_button(
            label="📥 Download Full Audit Report (.md)",
            data=report_export,
            file_name="recruiter_ats_audit_report.md",
            mime="text/markdown",
            use_container_width=True,
            type="primary",
        )


# ══════════════════════════════════════════════════════
# EXECUTION PIPELINE
# ══════════════════════════════════════════════════════

if run_clicked:
    # ── Validate inputs ──────────────────────────────────
    resume_text = ""
    if uploaded_pdf is not None:
        with st.spinner("Extracting text from PDF..."):
            try:
                resume_text = extract_text_from_pdf(uploaded_pdf)
            except RuntimeError as e:
                st.error(f"PDF extraction failed: {e}")
    elif manual_resume_text and manual_resume_text.strip():
        resume_text = manual_resume_text.strip()

    if not resume_text:
        st.warning("Please upload a PDF resume or paste resume text in the sidebar.")
        st.stop()

    if not jd_text or not jd_text.strip():
        st.warning("Please paste a Job Description in the sidebar.")
        st.stop()

    # Determine active key silently in background
    active_key = (active_gemini_key or os.environ.get("GEMINI_API_KEY", "")).strip()
    if not active_key and hasattr(st, "secrets"):
        active_key = str(st.secrets.get("GEMINI_API_KEY", "")).strip()

    # ── Run matching pipeline ────────────────────────────
    with st.spinner("Extracting skills & running ATS diagnostics..."):
        resume_skills = extract_skills_from_text(resume_text)
        jd_skills = extract_skills_from_jd(jd_text)

    if not jd_skills:
        st.warning("No recognized skills found in the Job Description. Try a more detailed JD.")
        st.stop()

    if not resume_skills:
        st.info("No taxonomy skills detected in resume. The matching will show all JD skills as missing.")

    report = run_matching(
        jd_skills=jd_skills,
        resume_skills=resume_skills,
        match_threshold=match_threshold,
        partial_threshold=partial_threshold,
    )

    # ── Gemini AI Deep Recruiter Audit ───────────────────
    gemini_audit = {}
    if active_key:
        with st.spinner("🤖 Recruiter AI performing exhaustive line-by-line semantic evaluation..."):
            gemini_audit = generate_full_gemini_audit(
                resume_text=resume_text,
                jd_text=jd_text,
                api_key=active_key,
                model="gemini-2.5-flash",
            )
            st.session_state["gemini_audit"] = gemini_audit

    render_results(
        report=report,
        resume_text=resume_text,
        jd_text=jd_text,
        gemini_api_key=active_key,
        gemini_audit=gemini_audit,
    )

    # ── Sidebar summary ──────────────────────────────────
    with st.sidebar:
        st.markdown("---")
        st.markdown("#### Results Summary")
        score_color = "#10B981" if report.ats_score >= 75 else ("#F59E0B" if report.ats_score >= 50 else "#F43F5E")
        glow = f"0 0 30px rgba({','.join(str(int(score_color[i:i+2], 16)) for i in (1,3,5))},0.2)"

        st.markdown(f"""
        <div class="sidebar-score-card" style="border-color:rgba({','.join(str(int(score_color[i:i+2], 16)) for i in (1,3,5))},0.2);">
            <div style="font-size:0.68rem;text-transform:uppercase;letter-spacing:0.1em;color:{score_color};font-weight:700;margin-bottom:4px;">ATS Score</div>
            <div style="font-size:2.8rem;font-weight:900;color:{score_color};line-height:1;text-shadow:{glow};">{report.ats_score}%</div>
            <div style="margin-top:16px;display:flex;justify-content:space-around;font-size:0.78rem;">
                <div>
                    <span style="color:#34D399;font-weight:800;font-size:1.1rem;">{report.exact_count}</span>
                    <br><span style="color:#475569;font-size:0.68rem;">EXACT</span>
                </div>
                <div style="width:1px;background:#1E3040;"></div>
                <div>
                    <span style="color:#FBBF24;font-weight:800;font-size:1.1rem;">{report.fuzzy_count}</span>
                    <br><span style="color:#475569;font-size:0.68rem;">FUZZY</span>
                </div>
                <div style="width:1px;background:#1E3040;"></div>
                <div>
                    <span style="color:#FB7185;font-weight:800;font-size:1.1rem;">{report.missing_count}</span>
                    <br><span style="color:#475569;font-size:0.68rem;">MISSING</span>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)

else:
    # ══════════════════════════════════════════════════════
    # WELCOME STATE
    # ══════════════════════════════════════════════════════
    st.markdown("<br>", unsafe_allow_html=True)

    wcol1, wcol2, wcol3 = st.columns(3)

    with wcol1:
        st.markdown("""
        <div class="step-card animate-in">
            <div class="step-num">1</div>
            <div class="step-icon">&#128196;</div>
            <div class="step-title">Upload Resume</div>
            <div class="step-desc">Upload a PDF or paste your resume text in the sidebar panel.</div>
        </div>
        """, unsafe_allow_html=True)

    with wcol2:
        st.markdown("""
        <div class="step-card animate-in animate-delay-1">
            <div class="step-num">2</div>
            <div class="step-icon">&#127919;</div>
            <div class="step-title">Paste Job Description</div>
            <div class="step-desc">Paste the target JD to automatically identify required skills.</div>
        </div>
        """, unsafe_allow_html=True)

    with wcol3:
        st.markdown("""
        <div class="step-card animate-in animate-delay-2">
            <div class="step-num">3</div>
            <div class="step-icon">&#128640;</div>
            <div class="step-title">Run Diagnostic</div>
            <div class="step-desc">Get your ATS match score, skill audit, and optimization tips.</div>
        </div>
        """, unsafe_allow_html=True)

    # ── How It Works ─────────────────────────────────────
    st.markdown("<br>", unsafe_allow_html=True)

    st.markdown("""
    <div class="glass-panel animate-in animate-delay-3" style="max-width:800px;margin:0 auto;">
        <div style="text-align:center;margin-bottom:20px;">
            <div style="font-size:0.68rem;text-transform:uppercase;letter-spacing:0.12em;color:#10B981;font-weight:700;margin-bottom:6px;">How It Works</div>
            <div style="font-size:1.3rem;font-weight:800;color:#F1F5F9;letter-spacing:-0.02em;">Intelligent ATS Diagnostic Pipeline</div>
        </div>
        <div style="display:flex;align-items:center;justify-content:center;gap:12px;flex-wrap:wrap;margin-bottom:0px;">
            <div style="background:rgba(16,185,129,0.08);border:1px solid rgba(16,185,129,0.15);border-radius:10px;padding:10px 16px;text-align:center;">
                <div style="font-size:0.72rem;color:#34D399;font-weight:600;">1. EXTRACT</div>
                <div style="font-size:0.75rem;color:#94A3B8;margin-top:2px;">PDF &rarr; Text</div>
            </div>
            <div style="color:#283545;font-size:1.2rem;">&rarr;</div>
            <div style="background:rgba(16,185,129,0.08);border:1px solid rgba(16,185,129,0.15);border-radius:10px;padding:10px 16px;text-align:center;">
                <div style="font-size:0.72rem;color:#34D399;font-weight:600;">2. NORMALIZE</div>
                <div style="font-size:0.75rem;color:#94A3B8;margin-top:2px;">Curated Lexicon</div>
            </div>
            <div style="color:#283545;font-size:1.2rem;">&rarr;</div>
            <div style="background:rgba(16,185,129,0.08);border:1px solid rgba(16,185,129,0.15);border-radius:10px;padding:10px 16px;text-align:center;">
                <div style="font-size:0.72rem;color:#34D399;font-weight:600;">3. ALIGN</div>
                <div style="font-size:0.75rem;color:#94A3B8;margin-top:2px;">Fuzzy String Distance</div>
            </div>
            <div style="color:#283545;font-size:1.2rem;">&rarr;</div>
            <div style="background:rgba(16,185,129,0.08);border:1px solid rgba(16,185,129,0.15);border-radius:10px;padding:10px 16px;text-align:center;">
                <div style="font-size:0.72rem;color:#34D399;font-weight:600;">4. OPTIMIZE</div>
                <div style="font-size:0.75rem;color:#94A3B8;margin-top:2px;">ATS Score &amp; AI Tailoring</div>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # ── Tech Stack & Authors Display ─────────────────────
    st.markdown("""
    <div class="tech-stack animate-fade">
        <div class="badges">
            <span class="badge badge-slate">Streamlit</span>
            <span class="badge badge-slate">pdfplumber</span>
            <span class="badge badge-slate">thefuzz</span>
            <span class="badge badge-slate">Plotly</span>
            <span class="badge badge-slate">AI Recruiter Engine</span>
            <span class="badge badge-slate">Rule-Based NLP</span>
        </div>
        <div class="tagline" style="margin-bottom: 8px;">
            Intelligent Resume Diagnostics &middot; Token-Sorted Matching &middot; AI Tailored Optimization
        </div>
        <div style="font-size:0.75rem;color:#94A3B8;margin-top:6px;">
            Developed by <span style="color:#10B981;font-weight:600;">Vinayak Mamtani</span>
        </div>
    </div>
    """, unsafe_allow_html=True)
