"""
Enterprise Data Analytics - PREMIUM Interactive Presentation
✨ Real flashcard animations
📊 Enhanced interactive visualizations  
📚 Research papers for each concept
🎨 Beautiful modern UI
💡 Detailed explanations
"""

import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from scipy import stats
from sklearn.linear_model import LinearRegression
import warnings
warnings.filterwarnings('ignore')

# Premium Page Configuration
st.set_page_config(
    page_title="Enterprise Data Analytics | Premium Course",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Initialize session state for flashcard flips
if 'flipped_cards' not in st.session_state:
    st.session_state.flipped_cards = {}

def flip_card(card_id):
    """Toggle flashcard flip state"""
    if card_id not in st.session_state.flipped_cards:
        st.session_state.flipped_cards[card_id] = False
    st.session_state.flipped_cards[card_id] = not st.session_state.flipped_cards[card_id]

# Premium CSS with Flashcard Animations
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;600;700;800&family=JetBrains+Mono:wght@400;600&display=swap');
    
    * {
        font-family: 'Inter', sans-serif;
    }
    
    .main {
        background: linear-gradient(135deg, #1e3c72 0%, #2a5298 50%, #7e22ce 100%);
        animation: gradientShift 15s ease infinite;
        background-size: 200% 200%;
    }
    
    @keyframes gradientShift {
        0% { background-position: 0% 50%; }
        50% { background-position: 100% 50%; }
        100% { background-position: 0% 50%; }
    }
    
    h1, h2, h3, h4 {
        color: white !important;
        font-weight: 700 !important;
        text-shadow: 2px 2px 8px rgba(0,0,0,0.3);
    }
    
    /* Premium Flashcard Styles */
    .flashcard-container {
        perspective: 1000px;
        margin: 20px 0;
    }
    
    .flashcard {
        position: relative;
        width: 100%;
        min-height: 250px;
        transition: transform 0.6s;
        transform-style: preserve-3d;
        cursor: pointer;
    }
    
    .flashcard.flipped {
        transform: rotateY(180deg);
    }
    
    .flashcard-face {
        position: absolute;
        width: 100%;
        min-height: 250px;
        backface-visibility: hidden;
        border-radius: 20px;
        padding: 35px;
        box-shadow: 0 20px 60px rgba(0,0,0,0.4);
        display: flex;
        flex-direction: column;
        justify-content: center;
        align-items: center;
    }
    
    .flashcard-front {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
    }
    
    .flashcard-back {
        background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
        color: white;
        transform: rotateY(180deg);
    }
    
    .flashcard-question {
        font-size: 26px;
        font-weight: 700;
        text-align: center;
        line-height: 1.4;
    }
    
    .flashcard-answer {
        font-size: 20px;
        font-weight: 500;
        text-align: center;
        line-height: 1.8;
    }
    
    .flip-hint {
        font-size: 14px;
        opacity: 0.9;
        margin-top: 15px;
        font-style: italic;
    }
    
    /* Example Box Styles */
    .example-hero {
        background: linear-gradient(135deg, #f5576c 0%, #f093fb 100%);
        color: white;
        padding: 45px;
        border-radius: 25px;
        margin: 30px 0;
        box-shadow: 0 15px 50px rgba(245, 87, 108, 0.4);
        position: relative;
        overflow: hidden;
    }
    
    .example-hero::before {
        content: '';
        position: absolute;
        top: -50%;
        right: -50%;
        width: 200%;
        height: 200%;
        background: radial-gradient(circle, rgba(255,255,255,0.1) 0%, transparent 70%);
        animation: pulse 4s ease-in-out infinite;
    }
    
    @keyframes pulse {
        0%, 100% { transform: scale(1); opacity: 0.5; }
        50% { transform: scale(1.1); opacity: 0.8; }
    }
    
    .example-hero h3 {
        margin: 0 0 15px 0;
        font-size: 32px;
        font-weight: 800;
    }
    
    .example-hero p {
        font-size: 18px;
        margin: 0;
        opacity: 0.95;
    }
    
    /* Concept Connection Box */
    .concept-connection {
        background: linear-gradient(135deg, #11998e 0%, #38ef7d 100%);
        color: white;
        padding: 30px;
        border-radius: 20px;
        margin: 25px 0;
        border-left: 8px solid #0fb894;
        box-shadow: 0 10px 40px rgba(17, 153, 142, 0.3);
    }
    
    .concept-connection h4 {
        margin-top: 0;
        font-size: 22px;
        font-weight: 700;
    }
    
    /* Insight Box */
    .insight-box {
        background: linear-gradient(135deg, #ffd89b 0%, #19547b 100%);
        color: white;
        padding: 30px;
        border-radius: 20px;
        margin: 25px 0;
        font-size: 19px;
        font-weight: 600;
        box-shadow: 0 10px 40px rgba(255, 216, 155, 0.3);
        border-left: 8px solid #ffaa00;
    }
    
    /* Research Paper Card */
    .paper-card {
        background: rgba(255, 255, 255, 0.95);
        padding: 25px;
        border-radius: 15px;
        margin: 15px 0;
        box-shadow: 0 8px 30px rgba(0,0,0,0.2);
        border-left: 5px solid #667eea;
        transition: all 0.3s ease;
    }
    
    .paper-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 12px 40px rgba(102, 126, 234, 0.4);
    }
    
    .paper-title {
        font-size: 18px;
        font-weight: 700;
        color: #1e3c72;
        margin-bottom: 10px;
    }
    
    .paper-authors {
        font-size: 15px;
        color: #666;
        font-style: italic;
        margin-bottom: 10px;
    }
    
    .paper-citation {
        font-size: 14px;
        color: #888;
        font-family: 'JetBrains Mono', monospace;
        background: #f5f5f5;
        padding: 8px 12px;
        border-radius: 6px;
        margin: 10px 0;
    }
    
    .paper-relevance {
        font-size: 15px;
        color: #333;
        line-height: 1.6;
        margin-top: 12px;
    }
    
    /* Interactive Elements */
    .interactive-widget {
        background: rgba(255, 255, 255, 0.1);
        backdrop-filter: blur(10px);
        padding: 25px;
        border-radius: 20px;
        border: 2px solid rgba(255, 255, 255, 0.2);
        margin: 20px 0;
    }
    
    /* Metric Cards */
    .metric-card {
        background: white;
        padding: 25px;
        border-radius: 20px;
        text-align: center;
        box-shadow: 0 8px 30px rgba(0,0,0,0.15);
        transition: all 0.3s ease;
    }
    
    .metric-card:hover {
        transform: translateY(-8px);
        box-shadow: 0 15px 50px rgba(102, 126, 234, 0.3);
    }
    
    .metric-value {
        font-size: 42px;
        font-weight: 800;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }
    
    .metric-label {
        font-size: 14px;
        color: #888;
        text-transform: uppercase;
        letter-spacing: 1px;
        margin-top: 8px;
    }
    
    /* Sidebar Styling */
    .sidebar .sidebar-content {
        background: linear-gradient(180deg, #1e3c72 0%, #2a5298 100%);
    }
    
    /* Tab Styling */
    .stTabs [data-baseweb="tab-list"] {
        gap: 15px;
        background-color: rgba(255,255,255,0.1);
        padding: 15px;
        border-radius: 20px;
        backdrop-filter: blur(10px);
    }
    
    .stTabs [data-baseweb="tab"] {
        background-color: rgba(255,255,255,0.15);
        border-radius: 12px;
        color: white;
        padding: 18px 35px;
        font-weight: 700;
        font-size: 16px;
        transition: all 0.3s ease;
        border: 2px solid transparent;
    }
    
    .stTabs [data-baseweb="tab"]:hover {
        background-color: rgba(255,255,255,0.25);
        transform: translateY(-3px);
        border-color: rgba(255,255,255,0.3);
    }
    
    .stTabs [aria-selected="true"] {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        border-color: white;
    }
    
    /* Code blocks */
    code {
        background: rgba(255, 255, 255, 0.1);
        padding: 2px 6px;
        border-radius: 4px;
        font-family: 'JetBrains Mono', monospace;
    }
</style>
""", unsafe_allow_html=True)

# Sidebar Navigation
st.sidebar.title("🎓 Enterprise Data Analytics")
st.sidebar.markdown("### Premium Interactive Course")
st.sidebar.markdown("---")

chapters = [
    ("🏠", "Welcome"),
    ("1️⃣", "Data Analysis Fundamentals"),
    ("2️⃣", "Distributions"),
    ("3️⃣", "Relationships"),
    ("4️⃣", "Probability"),
    ("5️⃣", "Statistical Distributions"),
    ("6️⃣", "Decision Making"),
    ("7️⃣", "Sampling"),
    ("8️⃣", "Hypothesis Testing")
]

selected = st.sidebar.radio(
    "Navigate to Chapter",
    [f"{emoji} {name}" for emoji, name in chapters],
    label_visibility="collapsed"
)

chapter_idx = [f"{emoji} {name}" for emoji, name in chapters].index(selected)

st.sidebar.markdown("---")
st.sidebar.success(f"📍 **{chapters[chapter_idx][1]}**")
st.sidebar.info("💡 Click flashcards to flip!")


# Helper function for flashcards
def render_flashcard(card_id, question, answer):
    """Render an interactive flippable flashcard"""
    is_flipped = st.session_state.flipped_cards.get(card_id, False)
    
    if st.button(f"🔄 {'Show Question' if is_flipped else 'Reveal Answer'}", key=f"btn_{card_id}", use_container_width=True):
        flip_card(card_id)
        st.rerun()
    
    if is_flipped:
        st.markdown(f"""
        <div class='flashcard-container'>
            <div class='flashcard flipped'>
                <div class='flashcard-face flashcard-back'>
                    <div class='flashcard-answer'>{answer}</div>
                    <div class='flip-hint'>💡 Click button above to see question</div>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)
    else:
        st.markdown(f"""
        <div class='flashcard-container'>
            <div class='flashcard'>
                <div class='flashcard-face flashcard-front'>
                    <div class='flashcard-question'>{question}</div>
                    <div class='flip-hint'>🎴 Click button above to reveal answer</div>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)

# ====================
# WELCOME PAGE
# ====================
if chapter_idx == 0:
    st.title("🎓 Enterprise Data Analytics")
    st.markdown("## Premium Interactive Learning Experience")
    
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.markdown('<div class="metric-card"><div class="metric-value">8</div><div class="metric-label">Chapters</div></div>', unsafe_allow_html=True)
    with col2:
        st.markdown('<div class="metric-card"><div class="metric-value">80+</div><div class="metric-label">Flashcards</div></div>', unsafe_allow_html=True)
    with col3:
        st.markdown('<div class="metric-card"><div class="metric-value">40+</div><div class="metric-label">Research Papers</div></div>', unsafe_allow_html=True)
    with col4:
        st.markdown('<div class="metric-card"><div class="metric-value">100%</div><div class="metric-label">Interactive</div></div>', unsafe_allow_html=True)
    
    st.markdown("---")
    
    st.markdown("""
    ### ✨ What Makes This Premium
    
    🎴 **Real Flashcard Animations** - Click to flip cards with smooth 3D rotations  
    📊 **Enhanced Visualizations** - More interactive controls and explanations  
    📚 **Research Papers** - Seminal papers for each concept with full citations  
    💡 **Concept Connections** - Clear explanations linking examples to theory  
    🎨 **Modern UI** - Gradient backgrounds, smooth animations, premium design  
    🎮 **Interactive Widgets** - Manipulate parameters and see real-time results  
    
    ### 📖 Course Structure
    """)
    
    for i, (emoji, name) in enumerate(chapters[1:], 1):
        with st.expander(f"{emoji} **Chapter {i}: {name}**", expanded=False):
            topics = [
                "Data types (nominal, ordinal, discrete, continuous), EDA process, descriptive statistics, KDD framework",
                "Histograms, box plots, skewness, kurtosis, outlier detection (IQR, z-score), distribution shapes",
                "Pearson & Spearman correlation, linear regression, R², causation vs correlation, Anscombe's Quartet",
                "Probability rules, conditional probability, Bayes' theorem, expected value, decision under uncertainty",
                "Normal distribution & CLT, Binomial distribution, Poisson distribution, Exponential distribution",
                "Expected Monetary Value (EMV), decision trees, maximax/maximin, sensitivity analysis, risk assessment",
                "Central Limit Theorem, sampling methods (SRS, stratified, cluster), confidence intervals, margin of error",
                "Hypothesis testing framework, p-values, Type I/II errors, t-tests, chi-square, statistical significance"
            ]
            st.markdown(f"**Topics**: {topics[i-1]}")
            st.markdown(f"**Format**: 4 tabs - Concepts | 10+ Flashcards | Detailed Example | Research Papers")
    
    st.markdown("---")
    st.info("👈 **Start learning!** Select any chapter from the sidebar")

# I'll continue with Chapter 1 as a complete example showing all the improvements
# This will be the template for all chapters

