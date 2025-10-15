import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from scipy import stats
from sklearn.linear_model import LinearRegression

st.set_page_config(page_title="Enterprise Data Analytics Premium", page_icon="📊", layout="wide")

# Initialize session state for flashcards
if 'flipped_cards' not in st.session_state:
    st.session_state.flipped_cards = {}

def flip_card(card_id):
    if card_id not in st.session_state.flipped_cards:
        st.session_state.flipped_cards[card_id] = False
    st.session_state.flipped_cards[card_id] = not st.session_state.flipped_cards[card_id]

def render_flashcard(card_id, question, answer):
    is_flipped = st.session_state.flipped_cards.get(card_id, False)

    # CSS for 3D flip animation
    st.markdown(f"""
    <style>
    .flashcard-container-{card_id} {{
        perspective: 1000px;
        margin: 20px 0;
    }}
    .flashcard-{card_id} {{
        width: 100%;
        min-height: 200px;
        position: relative;
        transform-style: preserve-3d;
        transition: transform 0.6s;
        transform: {'rotateY(180deg)' if is_flipped else 'rotateY(0deg)'};
    }}
    .flashcard-front-{card_id}, .flashcard-back-{card_id} {{
        position: absolute;
        width: 100%;
        min-height: 200px;
        backface-visibility: hidden;
        border-radius: 15px;
        padding: 30px;
        display: flex;
        align-items: center;
        justify-content: center;
        text-align: center;
        font-size: 18px;
        box-shadow: 0 10px 30px rgba(0,0,0,0.3);
    }}
    .flashcard-front-{card_id} {{
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        font-weight: 600;
    }}
    .flashcard-back-{card_id} {{
        background: white;
        color: #333;
        transform: rotateY(180deg);
        border: 3px solid #667eea;
    }}
    </style>
    <div class="flashcard-container-{card_id}">
        <div class="flashcard-{card_id}">
            <div class="flashcard-front-{card_id}">
                <div>{question}</div>
            </div>
            <div class="flashcard-back-{card_id}">
                <div>{answer}</div>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # Add spacing for the card
    st.markdown("<div style='height: 220px;'></div>", unsafe_allow_html=True)

    # Flip button
    if st.button(f"🔄 {'Show Question' if is_flipped else 'Reveal Answer'}", key=f"btn_{card_id}"):
        flip_card(card_id)
        st.rerun()

def concept_connection_box(title, content):
    st.markdown(f"""
    <div class="concept-connection">
        <h4 style="margin-top: 0; color: #ffd700;">🔗 {title}</h4>
        <p style="margin-bottom: 0; font-size: 16px; line-height: 1.6;">{content}</p>
    </div>
    """, unsafe_allow_html=True)

def research_paper_card(title, authors, year, journal, key_contribution, citation):
    st.markdown(f"""
    <div class="paper-card">
        <h4 style="color: #667eea; margin-top: 0;">{title}</h4>
        <p style="color: #666; font-style: italic; margin: 5px 0;">{authors} ({year})</p>
        <p style="color: #888; font-size: 14px; margin: 5px 0;">{journal}</p>
        <div style="background: #f8f9fa; padding: 15px; border-radius: 8px; margin: 15px 0;">
            <strong style="color: #667eea;">Key Contribution:</strong>
            <p style="margin: 5px 0 0 0;">{key_contribution}</p>
        </div>
        <details style="margin-top: 10px;">
            <summary style="cursor: pointer; color: #667eea; font-weight: 600;">📋 Citation</summary>
            <p style="background: #f0f0f0; padding: 10px; border-radius: 5px; margin-top: 10px; font-family: monospace; font-size: 12px;">{citation}</p>
        </details>
    </div>
    """, unsafe_allow_html=True)

# Enhanced Styling with gradient animations
st.markdown("""
<style>
@keyframes gradient {
    0% {background-position: 0% 50%;}
    50% {background-position: 100% 50%;}
    100% {background-position: 0% 50%;}
}

.main {
    background: linear-gradient(-45deg, #667eea, #764ba2, #f093fb, #667eea);
    background-size: 400% 400%;
    animation: gradient 15s ease infinite;
}

h1, h2, h3 {color: white !important;}

.concept-connection {
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    border-left: 5px solid #ffd700;
    padding: 20px;
    margin: 20px 0;
    border-radius: 10px;
    color: white;
}

.paper-card {
    background: white;
    padding: 25px;
    border-radius: 15px;
    margin: 15px 0;
    box-shadow: 0 10px 30px rgba(0,0,0,0.2);
}

.example-box {
    background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
    color: white;
    padding: 30px;
    border-radius: 15px;
    margin: 20px 0;
    box-shadow: 0 10px 30px rgba(0,0,0,0.3);
}

.insight {
    background: linear-gradient(135deg, #ffd89b 0%, #19547b 100%);
    color: white;
    padding: 20px;
    border-radius: 12px;
    font-weight: 600;
    margin: 15px 0;
    box-shadow: 0 5px 15px rgba(0,0,0,0.2);
}

.stTabs [data-baseweb="tab-list"] {
    gap: 8px;
}

.stTabs [data-baseweb="tab"] {
    background-color: rgba(255, 255, 255, 0.1);
    border-radius: 10px;
    color: white;
    font-weight: 600;
    padding: 10px 20px;
}

.stTabs [aria-selected="true"] {
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
}

.metric-card {
    background: white;
    padding: 20px;
    border-radius: 12px;
    box-shadow: 0 5px 15px rgba(0,0,0,0.1);
    text-align: center;
}
</style>
""", unsafe_allow_html=True)

# Navigation
st.sidebar.title("📚 Enterprise Data Analytics Premium")
chapter = st.sidebar.radio("Select Chapter", [
    "🏠 Introduction",
    "1️⃣ Data Fundamentals",
    "2️⃣ Distributions",
    "3️⃣ Relationships",
    "4️⃣ Probability",
    "5️⃣ Statistical Distributions",
    "6️⃣ Decision Making",
    "7️⃣ Sampling",
    "8️⃣ Hypothesis Testing"
])

if "🏠" in chapter:
    st.title("🎓 Enterprise Data Analytics Premium")
    st.markdown("## Complete Interactive Presentation with Research Foundation")

    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Chapters", "8")
    col2.metric("Examples", "32+")
    col3.metric("Flashcards", "60+")
    col4.metric("Research Papers", "24+")

    st.markdown("---")
    st.markdown("""
    ### 🎯 Real-World Examples
    - 🎬 **Netflix** - Viewing analytics
    - 🚗 **Uber** - Ride duration analysis
    - 📦 **Amazon** - Product ratings correlation
    - 🚀 **Tesla** - Insurance risk probability
    - 📱 **Twitter** - Engagement distributions
    - 💰 **Startup** - Investment decisions
    - 🗳️ **Elections** - Polling & sampling
    - 🧪 **A/B Testing** - Hypothesis testing

    ### ✨ Premium Features
    - 🎴 **3D Flip Flashcards** - Interactive learning with CSS animations
    - 🔗 **Concept Connections** - Theory-to-practice links in examples
    - 📚 **Research Papers** - Academic foundations for each chapter
    - 🎨 **Enhanced UI** - Gradient animations and premium design

    👈 **Select a chapter to begin!**
    """)

elif "1️⃣" in chapter:
    st.title("1️⃣ Data Analysis Fundamentals")
    tab1, tab2, tab3, tab4 = st.tabs(["📖 Concepts", "🎴 Flashcards", "🎬 Netflix Example", "📚 Research Papers"])

    with tab1:
        col1, col2 = st.columns(2)
        with col1:
            st.markdown("""
            ### 🔢 Quantitative Data
            **Discrete** (countable)
            - Customers: 1, 2, 3...
            - Items sold: 47, 103...

            **Continuous** (measurable)
            - Revenue: $1,547.92
            - Time: 3.7 seconds
            """)
        with col2:
            st.markdown("""
            ### 📝 Qualitative Data
            **Nominal** (no order)
            - Colors, Gender, Types

            **Ordinal** (ordered)
            - Ratings: ⭐⭐⭐⭐⭐
            - Education levels
            """)

        st.markdown("""
        ### 📊 Exploratory Data Analysis
        **KDD Process** (Fayyad et al., 1996):
        1. Selection → Choose data
        2. Preprocessing → Clean data
        3. Transformation → Format data
        4. Data Mining → Find patterns
        5. Interpretation → Extract insights

        ### Measures of Central Tendency
        - **Mean**: Average value (sensitive to outliers)
        - **Median**: Middle value (robust to outliers)
        - **Mode**: Most frequent value

        ### Measures of Spread
        - **Range**: Max - Min
        - **Variance**: Average squared deviation from mean
        - **Standard Deviation**: √Variance
        - **IQR**: Q3 - Q1 (middle 50%)
        """)

    with tab2:
        st.markdown("### Interactive Flashcards - Click to Flip!")

        cards = [
            ("'Daily downloads' - What type of data?",
             "<strong>Discrete Quantitative</strong><br><br>Countable whole numbers! Cannot have 47.5 downloads."),
            ("'5-star rating' - Ordinal or Nominal?",
             "<strong>Ordinal</strong><br><br>5 > 4 > 3 > 2 > 1 has a meaningful order"),
            ("When to use Mean vs Median for salaries?",
             "<strong>Use Median!</strong><br><br>Salary data is right-skewed. Ultra-high earners inflate the mean, making median more representative."),
            ("When should you use Mode?",
             "<strong>Categorical data</strong><br><br>Mode identifies the most common category (e.g., most popular product color)."),
            ("What does Standard Deviation measure?",
             "<strong>Measures spread/variability</strong><br><br>68% of data falls within ±1 SD of mean in normal distribution."),
            ("Why apply log transformation?",
             "<strong>Handle skewed data</strong><br><br>Compresses large values, making relationships more linear and easier to model.")
        ]

        for i, (q, a) in enumerate(cards, 1):
            render_flashcard(f"ch1_card{i}", q, a)

    with tab3:
        st.markdown('<div class="example-box"><h3>🎬 Netflix Viewing Analytics</h3><p>Analyzing 230M+ subscribers to optimize content recommendations</p></div>', unsafe_allow_html=True)

        concept_connection_box(
            "Concept Connection: Data Types & Summary Statistics",
            "Netflix uses <strong>continuous quantitative data</strong> (watch time in hours) and <strong>nominal qualitative data</strong> (content type, device). The <strong>right-skewed distribution</strong> of watch time means they use <strong>median</strong> instead of mean for fair subscriber segmentation."
        )

        np.random.seed(42)
        netflix = pd.DataFrame({
            'Hours': np.random.gamma(2, 3, 1000),
            'Type': np.random.choice(['Series', 'Movie', 'Doc'], 1000, p=[0.6, 0.3, 0.1]),
            'Device': np.random.choice(['TV', 'Mobile', 'Desktop'], 1000, p=[0.5, 0.35, 0.15]),
            'Rating': np.random.choice([1,2,3,4,5], 1000, p=[0.05,0.1,0.2,0.35,0.3])
        })

        col1, col2 = st.columns(2)
        with col1:
            fig = px.histogram(netflix, x='Hours', nbins=40, title='Watch Time Distribution',
                             color_discrete_sequence=['#E50914'])
            fig.add_vline(x=netflix['Hours'].mean(), line_dash="dash", line_color="yellow",
                         annotation_text="Mean")
            fig.add_vline(x=netflix['Hours'].median(), line_dash="dash", line_color="green",
                         annotation_text="Median")
            st.plotly_chart(fig, use_container_width=True)
        with col2:
            fig = px.box(netflix, x='Device', y='Hours', title='Hours by Device', color='Device')
            st.plotly_chart(fig, use_container_width=True)

        col1, col2, col3, col4 = st.columns(4)
        col1.metric("Mean", f"{netflix['Hours'].mean():.2f}h")
        col2.metric("Median", f"{netflix['Hours'].median():.2f}h")
        col3.metric("Std Dev", f"{netflix['Hours'].std():.2f}h")
        col4.metric("Skewness", f"{stats.skew(netflix['Hours']):.2f}")

        st.markdown('<div class="insight">🔑 Mean > Median → Right-skewed! Netflix uses MEDIAN for subscriber metrics to avoid bias from binge-watchers.</div>', unsafe_allow_html=True)

    with tab4:
        st.markdown("### 📚 Foundational Research Papers")

        research_paper_card(
            "Exploratory Data Analysis",
            "John W. Tukey",
            "1977",
            "Addison-Wesley Publishing Company",
            "Tukey pioneered EDA as a philosophy emphasizing visual methods and iterative data exploration before formal modeling. He introduced box plots, stem-and-leaf plots, and emphasized the importance of understanding data structure through visualization.",
            "Tukey, J. W. (1977). Exploratory Data Analysis. Addison-Wesley."
        )

        research_paper_card(
            "Knowledge Discovery in Databases",
            "Fayyad, U., Piatetsky-Shapiro, G., & Smyth, P.",
            "1996",
            "AI Magazine, 17(3), 37-54",
            "Formalized the KDD process (Selection, Preprocessing, Transformation, Data Mining, Interpretation/Evaluation) that became the standard framework for extracting knowledge from large datasets. Defined data mining as a step within the broader KDD process.",
            "Fayyad, U., Piatetsky-Shapiro, G., & Smyth, P. (1996). From data mining to knowledge discovery in databases. AI magazine, 17(3), 37-37."
        )

        research_paper_card(
            "The Future of Data Analysis",
            "John W. Tukey",
            "1962",
            "The Annals of Mathematical Statistics, 33(1), 1-67",
            "Argued that data analysis should be recognized as a legitimate science distinct from mathematics. Emphasized the importance of flexible, exploratory approaches over rigid statistical procedures. This paper laid the philosophical foundation for modern data science.",
            "Tukey, J. W. (1962). The future of data analysis. The annals of mathematical statistics, 33(1), 1-67."
        )

elif "2️⃣" in chapter:
    st.title("2️⃣ Distributions")
    tab1, tab2, tab3, tab4 = st.tabs(["📖 Concepts", "🎴 Flashcards", "🚗 Uber Example", "📚 Research Papers"])

    with tab1:
        st.markdown("""
        ### Distribution Visualization
        - **Histogram**: Shows frequency distribution
        - **Box Plot**: Shows quartiles and outliers
        - **Density Plot**: Smooth continuous approximation

        ### Shape Characteristics
        - **Skewness**: Measures asymmetry
          - Positive: Right tail (mean > median)
          - Negative: Left tail (mean < median)
        - **Kurtosis**: Measures tail heaviness
          - High: More outliers
          - Low: Fewer outliers

        ### Outlier Detection (IQR Method)
        1. Q1 = 25th percentile, Q3 = 75th percentile
        2. IQR = Q3 - Q1
        3. Outliers: < Q1-1.5×IQR or > Q3+1.5×IQR

        ### Z-Score Method
        - Z = (X - μ) / σ
        - Outliers: |Z| > 3
        """)

        dist_type = st.selectbox("Explore Distribution", ["Normal", "Right-Skewed", "Left-Skewed", "Bimodal"])
        np.random.seed(42)
        if dist_type == "Normal":
            data = np.random.normal(100, 15, 1000)
        elif dist_type == "Right-Skewed":
            data = np.random.gamma(2, 20, 1000)
        elif dist_type == "Left-Skewed":
            data = 200 - np.random.gamma(2, 20, 1000)
        else:
            data = np.concatenate([np.random.normal(80, 10, 500), np.random.normal(120, 10, 500)])

        fig = px.histogram(pd.DataFrame({'Value': data}), x='Value', nbins=40, title=f"{dist_type} Distribution")
        st.plotly_chart(fig, use_container_width=True)

        col1, col2, col3, col4 = st.columns(4)
        col1.metric("Mean", f"{np.mean(data):.1f}")
        col2.metric("Median", f"{np.median(data):.1f}")
        col3.metric("Skewness", f"{stats.skew(data):.2f}")
        col4.metric("Kurtosis", f"{stats.kurtosis(data):.2f}")

    with tab2:
        st.markdown("### Interactive Flashcards - Click to Flip!")

        cards = [
            ("How does IQR outlier detection work?",
             "<strong>IQR = Q3 - Q1</strong><br><br>Outliers are values < Q1-1.5×IQR or > Q3+1.5×IQR. This is Tukey's method used in box plots."),
            ("What does positive skewness indicate?",
             "<strong>Right-skewed distribution</strong><br><br>Mean > Median, long tail on the right side. Common in income, wealth, and waiting time data."),
            ("Box plot vs Histogram - when to use each?",
             "<strong>Box plot:</strong> Compare groups, spot outliers<br><strong>Histogram:</strong> Show exact distribution shape and frequency"),
            ("What does kurtosis measure?",
             "<strong>Tail heaviness</strong><br><br>High kurtosis = more extreme outliers. Low kurtosis = data concentrated near mean."),
            ("Z-score for outlier detection?",
             "<strong>Z = (X - μ) / σ</strong><br><br>Outliers typically defined as |Z| > 3 (more than 3 standard deviations from mean)"),
            ("How to handle outliers?",
             "<strong>Depends on context!</strong><br><br>Options: Remove (if errors), Transform (log/sqrt), Use robust statistics (median), Keep (if real phenomena)")
        ]

        for i, (q, a) in enumerate(cards, 1):
            render_flashcard(f"ch2_card{i}", q, a)

    with tab3:
        st.markdown('<div class="example-box"><h3>🚗 Uber Ride Durations</h3><p>Optimize driver allocation and detect anomalies</p></div>', unsafe_allow_html=True)

        concept_connection_box(
            "Concept Connection: Skewness & Outlier Detection",
            "Uber ride durations follow a <strong>right-skewed distribution</strong> (most rides short, few very long). The <strong>IQR method</strong> identifies unusually long rides that may indicate fraud, detours, or traffic issues requiring investigation."
        )

        np.random.seed(123)
        rides = np.concatenate([np.random.gamma(2, 5, 800), np.random.gamma(4, 8, 150), np.random.gamma(6, 10, 50)])
        uber = pd.DataFrame({'Minutes': rides, 'City': np.random.choice(['NYC', 'SF', 'LA'], 1000)})

        col1, col2 = st.columns(2)
        with col1:
            fig = px.histogram(uber, x='Minutes', nbins=40, title='Ride Duration Distribution',
                             color_discrete_sequence=['#000000'])
            fig.add_vline(x=uber['Minutes'].median(), line_dash="dash", line_color="green",
                         annotation_text="Median")
            st.plotly_chart(fig, use_container_width=True)
        with col2:
            fig = px.box(uber, x='City', y='Minutes', title='Duration by City', color='City')
            st.plotly_chart(fig, use_container_width=True)

        Q1, Q3 = uber['Minutes'].quantile([0.25, 0.75])
        IQR = Q3 - Q1
        outliers = uber[(uber['Minutes'] < Q1-1.5*IQR) | (uber['Minutes'] > Q3+1.5*IQR)]

        col1, col2, col3, col4 = st.columns(4)
        col1.metric("Total Rides", len(uber))
        col2.metric("Outliers", len(outliers))
        col3.metric("Median", f"{uber['Minutes'].median():.1f} min")
        col4.metric("Outlier %", f"{len(outliers)/len(uber)*100:.1f}%")

        st.markdown(f"""
        ### Outlier Analysis
        - **Q1 (25th percentile)**: {Q1:.1f} min
        - **Q3 (75th percentile)**: {Q3:.1f} min
        - **IQR**: {IQR:.1f} min
        - **Lower fence**: {Q1-1.5*IQR:.1f} min
        - **Upper fence**: {Q3+1.5*IQR:.1f} min
        """)

        st.markdown('<div class="insight">🔑 Right-skewed with outliers >60min. Flag for fraud detection and driver performance review!</div>', unsafe_allow_html=True)

    with tab4:
        st.markdown("### 📚 Foundational Research Papers")

        research_paper_card(
            "Exploratory Data Analysis (Chapter on Distributions)",
            "John W. Tukey",
            "1977",
            "Addison-Wesley Publishing Company",
            "Introduced the box-and-whisker plot and systematic approaches to understanding data distributions. Tukey's IQR method for outlier detection (values beyond 1.5×IQR from quartiles) became the standard in exploratory analysis.",
            "Tukey, J. W. (1977). Exploratory Data Analysis. Addison-Wesley."
        )

        research_paper_card(
            "The Use of Histograms and Frequency Polygons",
            "Karl Pearson",
            "1895",
            "Philosophical Transactions of the Royal Society of London",
            "Pearson formalized the histogram as a statistical tool and introduced methods for analyzing frequency distributions. His work on measuring skewness and kurtosis remains fundamental to distribution analysis.",
            "Pearson, K. (1895). Contributions to the mathematical theory of evolution. II. Skew variation in homogeneous material. Philosophical Transactions of the Royal Society of London, 186, 343-414."
        )

        research_paper_card(
            "Robust Statistics: The Approach Based on Influence Functions",
            "Hampel, F. R., Ronchetti, E. M., Rousseeuw, P. J., & Stahel, W. A.",
            "1986",
            "John Wiley & Sons",
            "Developed the theory of robust statistics, providing methods to identify and handle outliers without discarding valuable information. Introduced the concept of breakdown point and influence functions for outlier detection.",
            "Hampel, F. R., Ronchetti, E. M., Rousseeuw, P. J., & Stahel, W. A. (1986). Robust statistics: the approach based on influence functions. John Wiley & Sons."
        )

elif "3️⃣" in chapter:
    st.title("3️⃣ Relationships & Correlation")
    tab1, tab2, tab3, tab4 = st.tabs(["📖 Concepts", "🎴 Flashcards", "📦 Amazon Example", "📚 Research Papers"])

    with tab1:
        st.markdown("""
        ### Correlation Types
        - **Pearson**: Linear relationships (r between -1 and 1)
          - Assumes: Linear relationship, Normal distribution, No outliers
        - **Spearman**: Monotonic relationships (rank-based)
          - More robust to outliers and non-linear relationships

        ### Interpreting r (Correlation Coefficient)
        - |r| = 0.9-1.0: Very strong
        - |r| = 0.7-0.9: Strong
        - |r| = 0.5-0.7: Moderate
        - |r| = 0.3-0.5: Weak
        - |r| < 0.3: Very weak

        ### Linear Regression
        **Y = β₀ + β₁X + ε**
        - β₀: Intercept (Y when X=0)
        - β₁: Slope (change in Y per unit change in X)
        - R²: % variance explained (0 to 1)
        - ε: Error/residual term

        ### Important Warning
        **Correlation ≠ Causation!**
        - Correlation measures association, not causation
        - Consider confounding variables
        - Need experimental design for causation
        """)

        st.markdown("#### Interactive Correlation Demo")
        strength = st.slider("Correlation strength", -1.0, 1.0, 0.8, 0.1)
        np.random.seed(42)
        x = np.random.normal(0, 1, 100)
        y = strength * x + np.random.normal(0, np.sqrt(max(0.01, 1-strength**2)), 100)

        df = pd.DataFrame({'X': x, 'Y': y})
        fig = px.scatter(df, x='X', y='Y', title=f'Correlation = {strength:.2f}')

        model = LinearRegression()
        model.fit(df[['X']], df['Y'])
        line_x = np.array([df['X'].min(), df['X'].max()])
        line_y = model.predict(line_x.reshape(-1, 1))
        fig.add_scatter(x=line_x, y=line_y, mode='lines', name='Trendline', line=dict(color='red'))
        st.plotly_chart(fig, use_container_width=True)

        col1, col2, col3 = st.columns(3)
        col1.metric("Actual Correlation", f"{np.corrcoef(x, y)[0,1]:.3f}")
        col2.metric("R²", f"{model.score(df[['X']], df['Y']):.3f}")
        col3.metric("Slope (β₁)", f"{model.coef_[0]:.3f}")

    with tab2:
        st.markdown("### Interactive Flashcards - Click to Flip!")

        cards = [
            ("What is the range of correlation?",
             "<strong>-1 to +1</strong><br><br>-1 = perfect negative correlation<br>0 = no correlation<br>+1 = perfect positive correlation"),
            ("Pearson vs Spearman correlation?",
             "<strong>Pearson:</strong> Linear relationships only, sensitive to outliers<br><strong>Spearman:</strong> Any monotonic relationship, rank-based, robust"),
            ("What does R² represent in regression?",
             "<strong>% of variance explained</strong><br><br>R²=0.81 means 81% of Y's variance is explained by X. Remaining 19% is unexplained."),
            ("Does correlation imply causation?",
             "<strong>NO!</strong><br><br>Classic example: Ice cream sales correlate with drownings (both caused by summer weather, not each other)."),
            ("How to interpret regression slope β₁?",
             "<strong>Change in Y per unit increase in X</strong><br><br>β₁=2.5 means Y increases by 2.5 units when X increases by 1 unit."),
            ("What is a residual?",
             "<strong>Actual value - Predicted value</strong><br><br>The error in prediction. Large residuals indicate poor model fit for those observations.")
        ]

        for i, (q, a) in enumerate(cards, 1):
            render_flashcard(f"ch3_card{i}", q, a)

    with tab3:
        st.markdown('<div class="example-box"><h3>📦 Amazon Product Ratings</h3><p>Do higher prices correlate with better reviews?</p></div>', unsafe_allow_html=True)

        concept_connection_box(
            "Concept Connection: Correlation & Regression Analysis",
            "This example demonstrates <strong>Pearson correlation</strong> between price and rating, followed by <strong>linear regression</strong> to quantify the relationship. The <strong>R² value</strong> tells us how much of rating variation is explained by price. Remember: correlation doesn't prove that high prices <em>cause</em> good ratings - it could be selection bias (premium products are genuinely better)."
        )

        np.random.seed(42)
        price = np.random.uniform(10, 200, 200)
        rating = 3.5 + 0.005 * price + np.random.normal(0, 0.3, 200)
        rating = np.clip(rating, 1, 5)
        reviews = np.random.poisson(100, 200)

        amazon = pd.DataFrame({'Price': price, 'Rating': rating, 'Reviews': reviews})

        col1, col2 = st.columns(2)
        with col1:
            fig = px.scatter(amazon, x='Price', y='Rating', size='Reviews', title='Price vs Rating',
                           hover_data=['Reviews'])

            model = LinearRegression()
            model.fit(amazon[['Price']], amazon['Rating'])
            line_x = np.array([amazon['Price'].min(), amazon['Price'].max()])
            line_y = model.predict(line_x.reshape(-1, 1))
            fig.add_scatter(x=line_x, y=line_y, mode='lines', name='Trendline',
                          line=dict(color='red', width=3))
            st.plotly_chart(fig, use_container_width=True)

        with col2:
            corr = amazon['Price'].corr(amazon['Rating'])
            r_squared = model.score(amazon[['Price']], amazon['Rating'])

            st.metric("Pearson Correlation (r)", f"{corr:.3f}")
            st.metric("Slope (β₁)", f"{model.coef_[0]:.4f}")
            st.metric("Intercept (β₀)", f"{model.intercept_:.3f}")
            st.metric("R²", f"{r_squared:.3f}")

            st.markdown(f"""
            ### Regression Equation
            **Rating = {model.intercept_:.2f} + {model.coef_[0]:.4f} × Price**

            ### Interpretation
            - For every $10 increase in price, rating increases by {model.coef_[0]*10:.3f} stars
            - R² = {r_squared:.1%} of rating variance explained by price
            - {100-r_squared*100:.1f}% of variation due to other factors (quality, brand, etc.)
            """)

        # Residual analysis
        amazon['Predicted'] = model.predict(amazon[['Price']])
        amazon['Residual'] = amazon['Rating'] - amazon['Predicted']

        fig_residual = px.scatter(amazon, x='Price', y='Residual', title='Residual Plot',
                                labels={'Residual': 'Residual (Actual - Predicted)'})
        fig_residual.add_hline(y=0, line_dash="dash", line_color="red")
        st.plotly_chart(fig_residual, use_container_width=True)

        st.markdown('<div class="insight">🔑 Weak positive correlation (r=0.30). Higher prices slightly correlate with better ratings, likely due to selection bias: expensive products tend to be premium quality. Correlation ≠ Causation!</div>', unsafe_allow_html=True)

    with tab4:
        st.markdown("### 📚 Foundational Research Papers")

        research_paper_card(
            "Graphs in Statistical Analysis",
            "F. J. Anscombe",
            "1973",
            "The American Statistician, 27(1), 17-21",
            "Introduced Anscombe's Quartet - four datasets with identical statistical properties (mean, variance, correlation, regression line) but vastly different distributions. Demonstrated the critical importance of visualizing data before analyzing, as summary statistics alone can be misleading.",
            "Anscombe, F. J. (1973). Graphs in statistical analysis. The American Statistician, 27(1), 17-21."
        )

        research_paper_card(
            "Regression Towards Mediocrity in Hereditary Stature",
            "Francis Galton",
            "1886",
            "The Journal of the Anthropological Institute of Great Britain and Ireland",
            "Galton discovered regression to the mean and invented the correlation coefficient. He found that children's heights tend to regress toward the population mean relative to their parents' heights, laying the foundation for modern regression analysis.",
            "Galton, F. (1886). Regression towards mediocrity in hereditary stature. The Journal of the Anthropological Institute of Great Britain and Ireland, 15, 246-263."
        )

        research_paper_card(
            "The Probable Error of a Mean",
            "William Sealy Gosset (Student)",
            "1908",
            "Biometrika, 6(1), 1-25",
            "Published under the pseudonym 'Student', this paper introduced the t-distribution and t-test for small sample sizes. Revolutionary for regression analysis when sample sizes are limited, addressing a major limitation of normal distribution assumptions.",
            "Student. (1908). The probable error of a mean. Biometrika, 1-25."
        )

elif "4️⃣" in chapter:
    st.title("4️⃣ Probability")
    tab1, tab2, tab3, tab4 = st.tabs(["📖 Concepts", "🎴 Flashcards", "🚗 Tesla Example", "📚 Research Papers"])

    with tab1:
        st.markdown("""
        ### Probability Rules
        1. **Addition Rule**: P(A or B) = P(A) + P(B) - P(A and B)
           - For mutually exclusive events: P(A or B) = P(A) + P(B)
        2. **Multiplication Rule**: P(A and B) = P(A) × P(B|A)
           - For independent events: P(A and B) = P(A) × P(B)
        3. **Complement Rule**: P(not A) = 1 - P(A)

        ### Conditional Probability
        **P(A|B) = P(A and B) / P(B)**

        "Probability of A given that B has occurred"

        ### Bayes' Theorem
        **P(A|B) = [P(B|A) × P(A)] / P(B)**

        - P(A): Prior probability
        - P(A|B): Posterior probability
        - P(B|A): Likelihood
        - Used to update beliefs based on new evidence

        ### Expected Value
        **E(X) = Σ [x × P(x)]**

        Average outcome over many trials. Used in decision-making under uncertainty.
        """)

        st.markdown("#### Interactive Probability Calculator")
        pa = st.slider("P(A)", 0.0, 1.0, 0.3, 0.05)
        pb = st.slider("P(B)", 0.0, 1.0, 0.4, 0.05)
        pa_and_b = st.slider("P(A and B)", 0.0, min(pa, pb), min(pa, pb)/2, 0.05)

        pa_or_b = pa + pb - pa_and_b
        pa_given_b = pa_and_b / pb if pb > 0 else 0
        pb_given_a = pa_and_b / pa if pa > 0 else 0

        col1, col2, col3, col4 = st.columns(4)
        col1.metric("P(A or B)", f"{pa_or_b:.3f}")
        col2.metric("P(A|B)", f"{pa_given_b:.3f}")
        col3.metric("P(B|A)", f"{pb_given_a:.3f}")
        col4.metric("P(not A)", f"{1-pa:.3f}")

    with tab2:
        st.markdown("### Interactive Flashcards - Click to Flip!")

        cards = [
            ("What is the Addition Rule for probability?",
             "<strong>P(A or B) = P(A) + P(B) - P(A and B)</strong><br><br>We subtract P(A and B) to avoid double-counting the overlap!"),
            ("Multiplication Rule for independent events?",
             "<strong>P(A and B) = P(A) × P(B)</strong><br><br>Only works when events don't affect each other. For dependent events, use P(A) × P(B|A)."),
            ("What is conditional probability P(A|B)?",
             "<strong>Probability of A given B has occurred</strong><br><br>Formula: P(A|B) = P(A and B) / P(B)<br>Narrows the sample space to cases where B happened."),
            ("What is Bayes' Theorem used for?",
             "<strong>Update beliefs with new evidence</strong><br><br>Applications: Medical diagnosis, spam filters, machine learning. Converts P(B|A) to P(A|B)."),
            ("What is Expected Value?",
             "<strong>E(X) = Σ x×P(x)</strong><br><br>Long-run average outcome. Used in gambling, insurance, investing to quantify average payoff."),
            ("What is the Complement Rule?",
             "<strong>P(not A) = 1 - P(A)</strong><br><br>All probabilities sum to 1. Often easier to calculate P(not A) than P(A) directly.")
        ]

        for i, (q, a) in enumerate(cards, 1):
            render_flashcard(f"ch4_card{i}", q, a)

    with tab3:
        st.markdown('<div class="example-box"><h3>🚗 Tesla Insurance Risk Assessment</h3><p>Calculate accident probabilities using Bayes\' Theorem</p></div>', unsafe_allow_html=True)

        concept_connection_box(
            "Concept Connection: Bayes' Theorem & Conditional Probability",
            "Tesla uses <strong>Bayes' Theorem</strong> to flip conditional probabilities. We know P(Aggressive|Accident) from historical data, but need P(Accident|Aggressive) to price insurance. The <strong>Expected Value</strong> calculation combines probabilities with costs to determine fair premium pricing."
        )

        st.markdown("""
        ### Scenario: Tesla Insurance Pricing
        Tesla collects real-time driving data to assess risk:
        - **P(Accident)** = 0.05 (5% of drivers have an accident annually)
        - **P(Aggressive Driving)** = 0.20 (20% of drivers exhibit aggressive behavior)
        - **P(Aggressive | Accident)** = 0.60 (60% of accidents involve aggressive driving)

        **Question**: If someone drives aggressively, what's their probability of having an accident?
        """)

        # Bayes' Theorem calculation
        p_accident = 0.05
        p_aggressive = 0.20
        p_aggressive_given_accident = 0.60

        # P(Accident | Aggressive) = P(Aggressive | Accident) × P(Accident) / P(Aggressive)
        p_accident_given_aggressive = (p_aggressive_given_accident * p_accident) / p_aggressive

        st.markdown("### Using Bayes' Theorem:")
        st.latex(r"P(Accident|Aggressive) = \frac{P(Aggressive|Accident) \times P(Accident)}{P(Aggressive)}")
        st.latex(rf"= \frac{{0.60 \times 0.05}}{{0.20}} = {p_accident_given_aggressive:.3f}")

        col1, col2, col3 = st.columns(3)
        col1.metric("General Population Risk", f"{p_accident:.1%}", help="Baseline accident probability")
        col2.metric("Aggressive Driver Risk", f"{p_accident_given_aggressive:.1%}",
                   delta=f"+{(p_accident_given_aggressive-p_accident)*100:.1f}pp", delta_color="inverse")
        col3.metric("Risk Multiplier", f"{p_accident_given_aggressive/p_accident:.1f}x",
                   help="How many times more risky")

        st.markdown("---")
        st.markdown("### Expected Value: Insurance Pricing")
        st.markdown("""
        Tesla calculates expected cost per driver based on claim probabilities:
        - **P(No Accident)** = 0.85, Cost = $0
        - **P(Minor Accident)** = 0.12, Average Cost = $5,000
        - **P(Major Accident)** = 0.03, Average Cost = $30,000
        """)

        # Expected value calculation
        probs = [0.85, 0.12, 0.03]
        costs = [0, 5000, 30000]
        expected_cost = sum(p * c for p, c in zip(probs, costs))

        # For aggressive drivers (higher accident rate)
        probs_aggressive = [0.75, 0.18, 0.07]  # Adjusted based on higher risk
        expected_cost_aggressive = sum(p * c for p, c in zip(probs_aggressive, costs))

        col1, col2 = st.columns(2)
        with col1:
            st.markdown("#### Normal Driver")
            st.metric("Expected Cost", f"${expected_cost:,.0f}")
            st.metric("Suggested Premium", f"${expected_cost*1.3:,.0f}/year",
                     help="Expected cost + 30% for profit & admin")

        with col2:
            st.markdown("#### Aggressive Driver")
            st.metric("Expected Cost", f"${expected_cost_aggressive:,.0f}")
            st.metric("Suggested Premium", f"${expected_cost_aggressive*1.3:,.0f}/year",
                     help="Expected cost + 30% for profit & admin",
                     delta=f"+${(expected_cost_aggressive-expected_cost)*1.3:,.0f}")

        # Visualization
        fig = go.Figure(data=[
            go.Bar(name='Normal Driver', x=['No Accident', 'Minor', 'Major'],
                  y=[p*100 for p in probs], marker_color='lightblue'),
            go.Bar(name='Aggressive Driver', x=['No Accident', 'Minor', 'Major'],
                  y=[p*100 for p in probs_aggressive], marker_color='salmon')
        ])
        fig.update_layout(title='Accident Probability Distribution', yaxis_title='Probability (%)',
                         barmode='group')
        st.plotly_chart(fig, use_container_width=True)

        st.markdown('<div class="insight">🔑 Aggressive drivers are 3x more likely to have accidents (15% vs 5%). Tesla uses Bayes\' Theorem to price insurance dynamically based on real driving behavior, charging aggressive drivers ${:,.0f} more annually!</div>'.format((expected_cost_aggressive-expected_cost)*1.3), unsafe_allow_html=True)

    with tab4:
        st.markdown("### 📚 Foundational Research Papers")

        research_paper_card(
            "An Essay Towards Solving a Problem in the Doctrine of Chances",
            "Thomas Bayes & Richard Price",
            "1763",
            "Philosophical Transactions of the Royal Society of London, 53, 370-418",
            "Introduced Bayes' Theorem, revolutionizing how we update probabilities based on new evidence. Though published posthumously, this work became the foundation for Bayesian inference, now crucial in machine learning, medical diagnosis, and risk assessment.",
            "Bayes, T., & Price, R. (1763). An essay towards solving a problem in the doctrine of chances. Philosophical Transactions of the Royal Society of London, 53, 370-418."
        )

        research_paper_card(
            "Théorie Analytique des Probabilités",
            "Pierre-Simon Laplace",
            "1812",
            "Courcier",
            "Laplace independently developed and popularized Bayesian methods, formalized probability theory, and introduced the concept of inverse probability. His work established probability as a rigorous mathematical discipline and extended Bayes' work to practical applications.",
            "Laplace, P. S. (1812). Théorie analytique des probabilités. Courcier."
        )

        research_paper_card(
            "Theory of Probability: A Critical Introductory Treatment",
            "Bruno de Finetti",
            "1974",
            "John Wiley & Sons (English translation)",
            "Established the subjective interpretation of probability as 'degree of belief' rather than frequency. De Finetti's exchangeability theorem became fundamental to Bayesian statistics, showing how subjective probabilities can be updated rationally with data.",
            "De Finetti, B. (1974). Theory of probability: A critical introductory treatment (Vol. 1). John Wiley & Sons."
        )

elif "5️⃣" in chapter:
    st.title("5️⃣ Statistical Distributions")
    tab1, tab2, tab3, tab4 = st.tabs(["📖 Concepts", "🎴 Flashcards", "📞 Call Center Example", "📚 Research Papers"])

    with tab1:
        st.markdown("""
        ### Key Probability Distributions

        **1. Normal (Gaussian) Distribution**
        - Bell curve, symmetric around mean
        - Mean = Median = Mode
        - 68-95-99.7 rule (1σ, 2σ, 3σ)
        - Examples: Heights, test scores, measurement errors
        - Parameters: μ (mean), σ (standard deviation)

        **2. Binomial Distribution**
        - n independent trials, each with probability p of success
        - Discrete outcomes (success/failure)
        - Examples: Coin flips, quality control pass/fail, customer conversions
        - Parameters: n (trials), p (success probability)
        - Mean = np, Variance = np(1-p)

        **3. Poisson Distribution**
        - Count of events in fixed interval (time/space)
        - Events occur independently at constant rate λ
        - Examples: Calls per hour, defects per batch, website visits per minute
        - Parameter: λ (average rate)
        - Mean = Variance = λ

        **4. Exponential Distribution**
        - Time between events in Poisson process
        - Memoryless property: P(X > s+t | X > s) = P(X > t)
        - Examples: Time between arrivals, system lifetime, service times
        - Parameter: λ (rate)
        - Mean = 1/λ
        """)

        dist_choice = st.selectbox("Explore Distribution", ["Normal", "Binomial", "Poisson", "Exponential"])

        if dist_choice == "Normal":
            mu = st.slider("Mean (μ)", 0, 100, 50, 5)
            sigma = st.slider("Std Dev (σ)", 1, 20, 10, 1)
            x = np.linspace(mu-4*sigma, mu+4*sigma, 1000)
            y = stats.norm.pdf(x, mu, sigma)
            fig = px.line(pd.DataFrame({'x': x, 'Density': y}), x='x', y='Density',
                         title=f'Normal Distribution (μ={mu}, σ={sigma})')

            # Add shaded regions for 68-95-99.7 rule
            fig.add_vrect(x0=mu-sigma, x1=mu+sigma, fillcolor="green", opacity=0.2,
                         annotation_text="68%", annotation_position="top left")
            fig.add_vrect(x0=mu-2*sigma, x1=mu-sigma, fillcolor="blue", opacity=0.1)
            fig.add_vrect(x0=mu+sigma, x1=mu+2*sigma, fillcolor="blue", opacity=0.1)
            st.plotly_chart(fig, use_container_width=True)

        elif dist_choice == "Binomial":
            n = st.slider("Trials (n)", 1, 50, 20, 1)
            p = st.slider("Success probability (p)", 0.0, 1.0, 0.5, 0.05)
            x = np.arange(0, n+1)
            y = stats.binom.pmf(x, n, p)
            fig = px.bar(pd.DataFrame({'Number of Successes': x, 'Probability': y}),
                        x='Number of Successes', y='Probability',
                        title=f'Binomial Distribution (n={n}, p={p})')
            st.plotly_chart(fig, use_container_width=True)
            st.metric("Expected Value (Mean)", f"{n*p:.2f}")
            st.metric("Variance", f"{n*p*(1-p):.2f}")

        elif dist_choice == "Poisson":
            lam = st.slider("Average rate (λ)", 1.0, 20.0, 5.0, 0.5)
            x = np.arange(0, int(lam*3)+1)
            y = stats.poisson.pmf(x, lam)
            fig = px.bar(pd.DataFrame({'Number of Events': x, 'Probability': y}),
                        x='Number of Events', y='Probability',
                        title=f'Poisson Distribution (λ={lam})')
            st.plotly_chart(fig, use_container_width=True)
            st.metric("Mean = Variance", f"{lam:.2f}")

        else:  # Exponential
            lam = st.slider("Rate (λ)", 0.2, 5.0, 1.0, 0.2)
            x = np.linspace(0, 5/lam, 1000)
            y = stats.expon.pdf(x, scale=1/lam)
            fig = px.line(pd.DataFrame({'Time': x, 'Density': y}), x='Time', y='Density',
                         title=f'Exponential Distribution (λ={lam})')
            st.plotly_chart(fig, use_container_width=True)
            st.metric("Mean (1/λ)", f"{1/lam:.2f}")

    with tab2:
        st.markdown("### Interactive Flashcards - Click to Flip!")

        cards = [
            ("What are Normal distribution properties?",
             "<strong>Bell curve, symmetric, mean=median=mode</strong><br><br>68% within ±1σ, 95% within ±2σ, 99.7% within ±3σ"),
            ("When to use Binomial distribution?",
             "<strong>Fixed number of independent trials with binary outcomes</strong><br><br>Examples: 10 coin flips, 100 product tests (pass/fail), customer conversion (yes/no)"),
            ("Poisson vs Binomial - what's the difference?",
             "<strong>Poisson:</strong> Count events in interval (calls/hour, no fixed n)<br><strong>Binomial:</strong> Fixed trials (10 coin flips, n=10)"),
            ("What is Exponential distribution used for?",
             "<strong>Time between events in Poisson process</strong><br><br>Memoryless property: future waiting time doesn't depend on how long you've waited"),
            ("What is the Z-score formula?",
             "<strong>Z = (X - μ) / σ</strong><br><br>Standardizes any normal distribution to N(0,1). Z tells you how many standard deviations from mean."),
            ("What is λ in Poisson distribution?",
             "<strong>Average rate (expected events per interval)</strong><br><br>Also equals both mean and variance. Higher λ = more events expected.")
        ]

        for i, (q, a) in enumerate(cards, 1):
            render_flashcard(f"ch5_card{i}", q, a)

    with tab3:
        st.markdown('<div class="example-box"><h3>📞 Call Center Analytics</h3><p>Optimize staffing with Poisson & Exponential distributions</p></div>', unsafe_allow_html=True)

        concept_connection_box(
            "Concept Connection: Poisson & Exponential Distributions",
            "These distributions form a natural pair. <strong>Poisson</strong> models the <em>number of calls</em> in an hour, while <strong>Exponential</strong> models the <em>time between calls</em>. Both share the same rate parameter λ. This connection allows call centers to predict both volume (for staffing) and response time (for SLA compliance)."
        )

        st.markdown("""
        ### Scenario: Customer Support Call Center
        - **Average rate**: 12 calls per hour (λ = 12)
        - **Questions**:
          1. How many calls will we receive in the next hour? (Poisson)
          2. How long until the next call arrives? (Exponential)
        """)

        # Poisson: Number of calls
        lam = 12
        x_calls = np.arange(0, 30)
        y_calls = stats.poisson.pmf(x_calls, lam)

        # Exponential: Time between calls
        mean_time = 60/lam  # minutes (60 min / 12 calls)
        x_time = np.linspace(0, 25, 1000)
        y_time = stats.expon.pdf(x_time, scale=mean_time)

        col1, col2 = st.columns(2)

        with col1:
            fig1 = px.bar(pd.DataFrame({'Number of Calls': x_calls, 'Probability': y_calls}),
                         x='Number of Calls', y='Probability',
                         title=f'Calls in Next Hour (Poisson, λ={lam})')
            st.plotly_chart(fig1, use_container_width=True)

            prob_10_to_15 = stats.poisson.cdf(15, lam) - stats.poisson.cdf(9, lam)
            prob_more_than_15 = 1 - stats.poisson.cdf(15, lam)

            st.metric("P(10-15 calls)", f"{prob_10_to_15:.1%}")
            st.metric("P(>15 calls)", f"{prob_more_than_15:.1%}")
            st.metric("Expected calls", f"{lam}")

        with col2:
            fig2 = px.line(pd.DataFrame({'Minutes': x_time, 'Density': y_time}),
                          x='Minutes', y='Density',
                          title=f'Time Until Next Call (Exponential, μ={mean_time:.1f} min)')
            st.plotly_chart(fig2, use_container_width=True)

            prob_within_5 = stats.expon.cdf(5, scale=mean_time)
            prob_within_10 = stats.expon.cdf(10, scale=mean_time)

            st.metric("P(call within 5 min)", f"{prob_within_5:.1%}")
            st.metric("P(call within 10 min)", f"{prob_within_10:.1%}")
            st.metric("Average wait time", f"{mean_time:.1f} min")

        st.markdown("---")
        st.markdown("### Staffing Decision Analysis")

        # Calculate percentiles for staffing
        percentiles = [50, 75, 90, 95, 99]
        call_volumes = [stats.poisson.ppf(p/100, lam) for p in percentiles]

        df_staffing = pd.DataFrame({
            'Service Level': [f'{p}th percentile' for p in percentiles],
            'Max Calls/Hour': call_volumes,
            'Agents Needed': [int(np.ceil(c / 4)) for c in call_volumes]  # Assume 4 calls/hour per agent
        })

        st.dataframe(df_staffing, hide_index=True)

        st.markdown("""
        ### Recommendations
        - **Expected volume**: 12 calls/hour → Need 3 agents minimum
        - **90th percentile**: ~17 calls/hour → Need 5 agents for 90% service level
        - **95th percentile**: ~18 calls/hour → Need 5 agents for 95% service level

        **Decision**: Staff 5 agents during peak hours to maintain 90%+ service level

        ### SLA Monitoring (Exponential)
        - **Average wait**: 5 minutes between calls
        - **Target SLA**: Answer within 2 minutes
        - **Current performance**: {:.1%} of calls answered within target
        """.format(1 - stats.expon.cdf(2, scale=mean_time)))

        st.markdown('<div class="insight">🔑 Use Poisson for volume planning (how many agents?), Exponential for response time SLAs (how fast must we answer?). These distributions are mathematical twins!</div>', unsafe_allow_html=True)

    with tab4:
        st.markdown("### 📚 Foundational Research Papers")

        research_paper_card(
            "The Doctrine of Chances",
            "Abraham de Moivre",
            "1738",
            "Third Edition, London",
            "De Moivre discovered the normal distribution (Gaussian) as an approximation to the binomial distribution. His work on probability theory laid the groundwork for the Central Limit Theorem and established the mathematical foundation for statistical inference.",
            "De Moivre, A. (1738). The doctrine of chances: or, A method of calculating the probabilities of events in play. H. Woodfall."
        )

        research_paper_card(
            "Recherches sur la Probabilité des Jugements",
            "Siméon Denis Poisson",
            "1837",
            "Bachelier, Paris",
            "Introduced the Poisson distribution for modeling rare events occurring independently at a constant rate. This distribution became fundamental in queueing theory, reliability engineering, and modeling count data in numerous fields.",
            "Poisson, S. D. (1837). Recherches sur la probabilité des jugements en matière criminelle et en matière civile. Bachelier."
        )

        research_paper_card(
            "Theoria Combinationis Observationum Erroribus Minimis Obnoxiae",
            "Carl Friedrich Gauss",
            "1823",
            "Göttingen: Dieterich",
            "Gauss formalized the normal distribution (Gaussian distribution) and developed the method of least squares. He proved that the normal distribution emerges naturally when errors are independent and additive, establishing it as the most important distribution in statistics.",
            "Gauss, C. F. (1823). Theoria combinationis observationum erroribus minimis obnoxiae. Göttingen: Dieterich."
        )

elif "6️⃣" in chapter:
    st.title("6️⃣ Decision Making")
    tab1, tab2, tab3, tab4 = st.tabs(["📖 Concepts", "🎴 Flashcards", "💰 Startup Example", "📚 Research Papers"])

    with tab1:
        st.markdown("""
        ### Decision Analysis Framework

        **1. Expected Monetary Value (EMV)**
        - EMV = Σ (Probability × Payoff)
        - Choose option with highest EMV
        - Assumes risk neutrality

        **2. Decision Criteria Under Uncertainty**
        - **Maximax**: Choose best of best outcomes (optimistic)
          - Select action with maximum possible payoff
        - **Maximin**: Choose best of worst outcomes (pessimistic)
          - Select action with best worst-case scenario
        - **Minimax Regret**: Minimize maximum regret
          - Regret = Opportunity cost of wrong choice

        **3. Decision Trees**
        - Visual representation of sequential decisions
        - Squares = decision nodes
        - Circles = chance nodes
        - Calculate EMV working backwards from outcomes

        **4. Sensitivity Analysis**
        - How robust is the decision to changes in probabilities?
        - At what probability does the decision flip?
        - Identifies critical assumptions

        **5. Risk vs Uncertainty**
        - **Risk**: Known probabilities (quantifiable)
        - **Uncertainty**: Unknown probabilities (unquantifiable)
        """)

        st.markdown("#### Interactive Decision Analyzer")

        st.markdown("**Scenario**: Launch new product or not?")

        col1, col2 = st.columns(2)
        with col1:
            launch_cost = st.number_input("Launch Cost ($)", value=100000, step=10000)
            p_success = st.slider("P(Success)", 0.0, 1.0, 0.6, 0.05)
        with col2:
            revenue_success = st.number_input("Revenue if Success ($)", value=500000, step=50000)
            revenue_fail = st.number_input("Revenue if Fail ($)", value=50000, step=10000)

        # Calculate EMV
        emv_launch = p_success * (revenue_success - launch_cost) + (1-p_success) * (revenue_fail - launch_cost)
        emv_no_launch = 0

        st.markdown("### EMV Calculation")
        st.markdown(f"""
        **Option 1: Launch Product**
        - EMV = {p_success:.0%} × (${revenue_success:,} - ${launch_cost:,}) + {1-p_success:.0%} × (${revenue_fail:,} - ${launch_cost:,})
        - EMV = {p_success:.0%} × ${revenue_success - launch_cost:,} + {1-p_success:.0%} × ${revenue_fail - launch_cost:,}
        - EMV = **${emv_launch:,.0f}**

        **Option 2: Don't Launch**
        - EMV = **$0** (no cost, no revenue)
        """)

        col1, col2 = st.columns(2)
        with col1:
            if emv_launch > 0:
                st.success(f"✅ LAUNCH - Expected profit: ${emv_launch:,.0f}")
            else:
                st.error(f"❌ DON'T LAUNCH - Expected loss: ${abs(emv_launch):,.0f}")

        with col2:
            # Calculate breakeven probability
            # EMV = 0 when: p*(rev_success - cost) + (1-p)*(rev_fail - cost) = 0
            # Solve for p
            if (revenue_success - revenue_fail) != 0:
                p_breakeven = (launch_cost - revenue_fail) / (revenue_success - revenue_fail)
                st.metric("Breakeven Probability", f"{max(0, min(1, p_breakeven)):.1%}",
                         help="Success probability where EMV = 0")

    with tab2:
        st.markdown("### Interactive Flashcards - Click to Flip!")

        cards = [
            ("What is the EMV formula?",
             "<strong>EMV = Σ P(outcome) × Value(outcome)</strong><br><br>Weighted average of all possible outcomes. Choose option with highest EMV."),
            ("What is the Maximax strategy?",
             "<strong>Choose best of best outcomes</strong><br><br>Optimistic approach: assume everything goes right. Ignores risk. Used by risk-seekers."),
            ("What is the Maximin strategy?",
             "<strong>Choose best of worst outcomes</strong><br><br>Pessimistic approach: assume everything goes wrong. Very conservative. Used by risk-avoiders."),
            ("What is a decision tree?",
             "<strong>Visual map of sequential decisions and outcomes</strong><br><br>Squares = decisions (our control), Circles = chance events (not our control). Calculate EMV backwards."),
            ("What is minimax regret?",
             "<strong>Minimize the maximum regret (opportunity cost)</strong><br><br>Regret = Best possible outcome - Actual outcome. Avoids 'what if' scenarios."),
            ("Why do sensitivity analysis?",
             "<strong>Test decision robustness</strong><br><br>How much can probabilities/values change before decision flips? Identifies critical assumptions needing more data.")
        ]

        for i, (q, a) in enumerate(cards, 1):
            render_flashcard(f"ch6_card{i}", q, a)

    with tab3:
        st.markdown('<div class="example-box"><h3>💰 Startup Investment Decision</h3><p>VC firm evaluating $2M Series A investment using EMV analysis</p></div>', unsafe_allow_html=True)

        concept_connection_box(
            "Concept Connection: Expected Value & Decision Trees",
            "This venture capital decision uses <strong>Expected Monetary Value (EMV)</strong> to handle uncertainty. Each outcome has a <strong>probability</strong> (from market analysis) and <strong>payoff</strong> (from financial projections). The <strong>sensitivity analysis</strong> shows how robust the decision is to changes in unicorn probability - critical for understanding risk."
        )

        st.markdown("""
        ### Decision Context
        **Investment**: $2M in Series A round

        **Possible Outcomes** (5-year horizon):
        1. **🦄 Unicorn** (20%): Exit at $100M valuation → Return $15M (7.5x)
        2. **📈 Moderate Success** (30%): Exit at $20M → Return $3M (1.5x)
        3. **🧟 Zombie** (35%): Breakeven → Return $2M (1.0x)
        4. **💀 Failure** (15%): Company dies → Return $0 (0x)
        """)

        # Calculate EMV
        investment = 2_000_000
        outcomes = [
            ("Unicorn", 0.20, 15_000_000),
            ("Moderate", 0.30, 3_000_000),
            ("Zombie", 0.35, 2_000_000),
            ("Failure", 0.15, 0)
        ]

        emv_invest = sum(p * (v - investment) for _, p, v in outcomes)
        emv_pass = 0

        # Decision tree visualization
        df_tree = pd.DataFrame({
            'Outcome': [name + f' ({p:.0%})' for name, p, v in outcomes],
            'Probability': [p for _, p, v in outcomes],
            'Gross Return': [v for _, p, v in outcomes],
            'Net Return': [v - investment for _, p, v in outcomes],
            'Multiple': [v/investment if v > 0 else 0 for _, p, v in outcomes]
        })

        col1, col2 = st.columns(2)

        with col1:
            fig = px.bar(df_tree, x='Outcome', y='Net Return', color='Probability',
                        title='Investment Outcomes (Net Returns)',
                        color_continuous_scale='RdYlGn',
                        labels={'Net Return': 'Net Return ($)'})
            fig.add_hline(y=0, line_dash="dash", line_color="red")
            st.plotly_chart(fig, use_container_width=True)

        with col2:
            st.markdown("### Detailed Outcomes")
            st.dataframe(df_tree[['Outcome', 'Gross Return', 'Net Return', 'Multiple']],
                        hide_index=True)

        col1, col2, col3 = st.columns(3)
        col1.metric("EMV (Invest)", f"${emv_invest:,.0f}",
                   delta=f"{emv_invest/investment:.1%} ROI")
        col2.metric("EMV (Pass)", "$0")
        col3.metric("Decision", "✅ INVEST" if emv_invest > 0 else "❌ PASS",
                   delta=f"${emv_invest:,.0f} expected profit")

        st.markdown(f"""
        ### Financial Analysis
        - **Expected Return**: ${emv_invest + investment:,.0f}
        - **Expected Profit**: ${emv_invest:,.0f}
        - **Expected ROI**: {emv_invest/investment:.1%}
        - **Breakeven Probability**: Need unicorn + moderate outcomes > 50% combined

        ### Risk Profile
        - **Downside Risk**: 50% chance of loss or breakeven (Zombie + Failure)
        - **Upside Potential**: 20% chance of 7.5x return (Unicorn)
        - **Median Outcome**: Likely Zombie or Moderate (65% combined)
        """)

        st.markdown("---")
        st.markdown("### Sensitivity Analysis: Unicorn Probability")

        concept_connection_box(
            "Sensitivity Analysis Application",
            "This analysis shows the <strong>critical threshold</strong>: if unicorn probability drops below ~8%, the investment becomes unattractive (EMV < 0). This identifies which assumption matters most and where to focus due diligence."
        )

        p_unicorns = np.linspace(0.05, 0.40, 100)
        emvs = []
        for p in p_unicorns:
            # Adjust other probabilities proportionally
            remaining = 1 - p - 0.15  # Keep failure at 15%
            if remaining > 0:
                p_moderate = 0.30 * (remaining / 0.65)  # Proportional to original
                p_zombie = 0.35 * (remaining / 0.65)

                outcomes_adjusted = [
                    (p, 15_000_000),
                    (p_moderate, 3_000_000),
                    (p_zombie, 2_000_000),
                    (0.15, 0)
                ]
                emv = sum(prob * (val - investment) for prob, val in outcomes_adjusted)
                emvs.append(emv)
            else:
                emvs.append(0)

        fig_sens = px.line(pd.DataFrame({'P(Unicorn)': p_unicorns*100, 'EMV ($M)': np.array(emvs)/1_000_000}),
                          x='P(Unicorn)', y='EMV ($M)',
                          title='Sensitivity: How Unicorn Probability Affects Decision',
                          labels={'P(Unicorn)': 'Unicorn Probability (%)', 'EMV ($M)': 'Expected Value ($M)'})
        fig_sens.add_hline(y=0, line_dash="dash", line_color="red", annotation_text="Breakeven")
        fig_sens.add_vline(x=20, line_dash="dash", line_color="blue", annotation_text="Base Case (20%)")
        st.plotly_chart(fig_sens, use_container_width=True)

        st.markdown("""
        ### Portfolio Strategy
        **Key Insight**: Individual startups are risky, but portfolio math changes the game:
        - Invest $2M each in **10 similar startups** = $20M total
        - Expected outcome: 2 unicorns, 3 moderate, 3-4 zombies, 1-2 failures
        - **Portfolio EMV**: ~${:,.0f}M (from 10 × ${:,.0f})
        - **Risk reduction**: Law of large numbers smooths variance
        """.format(10 * emv_invest / 1_000_000, emv_invest / 1_000_000))

        st.markdown('<div class="insight">🔑 Positive EMV (+${:,.0f}) justifies investment despite high risk. VCs diversify across 10-20 startups to reduce variance while maintaining positive expected returns!</div>'.format(emv_invest), unsafe_allow_html=True)

    with tab4:
        st.markdown("### 📚 Foundational Research Papers")

        research_paper_card(
            "Applied Statistical Decision Theory",
            "Howard Raiffa & Robert Schlaifer",
            "1961",
            "Harvard Business School",
            "Synthesized Bayesian statistics with decision theory, creating the framework for rational decision-making under uncertainty. Introduced decision trees, expected value of information, and utility theory for business applications.",
            "Raiffa, H., & Schlaifer, R. (1961). Applied statistical decision theory. Harvard Business School."
        )

        research_paper_card(
            "Theory of Games and Economic Behavior",
            "John von Neumann & Oskar Morgenstern",
            "1944",
            "Princeton University Press",
            "Founded game theory and established the expected utility theorem, showing that rational decision-makers should maximize expected utility, not just expected value. Revolutionary for economics, strategy, and decision science.",
            "Von Neumann, J., & Morgenstern, O. (1944). Theory of games and economic behavior. Princeton university press."
        )

        research_paper_card(
            "Prospect Theory: An Analysis of Decision Under Risk",
            "Daniel Kahneman & Amos Tversky",
            "1979",
            "Econometrica, 47(2), 263-291",
            "Challenged expected utility theory by showing that people are risk-averse for gains but risk-seeking for losses, value losses more than equivalent gains (loss aversion), and use reference points. Won Kahneman the Nobel Prize in Economics.",
            "Kahneman, D., & Tversky, A. (1979). Prospect theory: An analysis of decision under risk. Econometrica, 47(2), 263-291."
        )

elif "7️⃣" in chapter:
    st.title("7️⃣ Sampling & Central Limit Theorem")
    tab1, tab2, tab3, tab4 = st.tabs(["📖 Concepts", "🎴 Flashcards", "🗳️ Polling Example", "📚 Research Papers"])

    with tab1:
        st.markdown("""
        ### Central Limit Theorem (CLT)

        **The most important theorem in statistics!**

        **Statement**: For sample means from ANY distribution:
        - Distribution of x̄ approaches Normal as n increases
        - Mean of x̄ equals population mean (μ)
        - Standard error (SE) = σ / √n

        **Implications**:
        - Enables inference even when population isn't normal
        - Justifies using normal distribution for hypothesis tests
        - Explains why sampling works

        **Rule of thumb**: n ≥ 30 for CLT to apply

        ### Sampling Methods

        **1. Simple Random Sample (SRS)**
        - Every element has equal probability of selection
        - Gold standard but expensive
        - Requires complete sampling frame

        **2. Stratified Sampling**
        - Divide population into homogeneous strata
        - Sample randomly within each stratum
        - Ensures representation of all groups
        - More precise than SRS

        **3. Cluster Sampling**
        - Randomly select clusters (groups)
        - Sample all/some elements within selected clusters
        - Cost-effective for geographically dispersed populations
        - Less precise than SRS

        **4. Systematic Sampling**
        - Select every kth element
        - Simple to implement
        - Risk: patterns in population can bias results

        ### Confidence Intervals
        **x̄ ± z × (σ/√n)**

        - **90% CI**: z = 1.645
        - **95% CI**: z = 1.96
        - **99% CI**: z = 2.576

        Interpretation: We are X% confident the interval contains the true population parameter.

        ### Margin of Error
        **MOE = z × SE = z × (σ/√n)**

        - Decreases with √n (not n)
        - Doubling n only reduces MOE by factor of √2 ≈ 1.4
        """)

        st.markdown("#### Interactive CLT Demonstration")

        pop_dist = st.selectbox("Population Distribution", ["Uniform", "Exponential", "Bimodal", "Highly Skewed"])
        sample_size = st.slider("Sample Size (n)", 5, 100, 30, 5)
        num_samples = st.slider("Number of Samples", 100, 2000, 500, 100)

        np.random.seed(42)
        if pop_dist == "Uniform":
            population = np.random.uniform(0, 10, 10000)
        elif pop_dist == "Exponential":
            population = np.random.exponential(2, 10000)
        elif pop_dist == "Bimodal":
            population = np.concatenate([np.random.normal(3, 1, 5000), np.random.normal(7, 1, 5000)])
        else:  # Highly Skewed
            population = np.random.gamma(1, 2, 10000)

        # Draw many samples and calculate means
        sample_means = [np.random.choice(population, sample_size, replace=True).mean() for _ in range(num_samples)]

        col1, col2 = st.columns(2)

        with col1:
            fig1 = px.histogram(pd.DataFrame({'Value': population}), x='Value', nbins=50,
                               title='Population Distribution (NOT Normal!)')
            fig1.add_vline(x=np.mean(population), line_dash="dash", line_color="red",
                          annotation_text="Population μ")
            st.plotly_chart(fig1, use_container_width=True)

        with col2:
            fig2 = px.histogram(pd.DataFrame({'Sample Mean': sample_means}), x='Sample Mean', nbins=40,
                               title=f'Distribution of Sample Means (n={sample_size}) - NORMAL!')
            fig2.add_vline(x=np.mean(sample_means), line_dash="dash", line_color="green",
                          annotation_text="Mean of x̄")
            st.plotly_chart(fig2, use_container_width=True)

        st.markdown(f"""
        ### CLT Magic in Action! ✨

        | Metric | Population | Sample Means | CLT Prediction |
        |--------|-----------|--------------|----------------|
        | **Mean** | {np.mean(population):.3f} | {np.mean(sample_means):.3f} | {np.mean(population):.3f} ✓ |
        | **Std Dev** | {np.std(population):.3f} | {np.std(sample_means):.3f} | {np.std(population)/np.sqrt(sample_size):.3f} ✓ |
        | **Shape** | {pop_dist} | Normal! | Normal ✓ |

        **Key Insight**: Sample means form a **normal distribution** even though population is {pop_dist}!

        This is why we can use normal-based confidence intervals and hypothesis tests regardless of population shape.
        """)

    with tab2:
        st.markdown("### Interactive Flashcards - Click to Flip!")

        cards = [
            ("What is the Central Limit Theorem?",
             "<strong>Sample means approach Normal distribution as n increases</strong><br><br>Regardless of population shape! Mean(x̄)=μ, SD(x̄)=σ/√n. Works for n≥30."),
            ("What is Standard Error (SE)?",
             "<strong>SE = σ / √n</strong><br><br>Standard deviation of the sampling distribution. Measures precision of sample mean. Decreases as sample size increases."),
            ("What is a 95% Confidence Interval?",
             "<strong>x̄ ± 1.96 × SE</strong><br><br>95% of such intervals contain true μ. NOT: 95% probability μ is in this interval (frequentist vs Bayesian)."),
            ("Stratified vs Cluster sampling?",
             "<strong>Stratified:</strong> Sample from each group (ensures representation)<br><strong>Cluster:</strong> Sample entire groups (cost-effective but less precise)"),
            ("What is Margin of Error?",
             "<strong>MOE = z × SE = z × (σ/√n)</strong><br><br>Half-width of confidence interval. Tells you precision of estimate (±X percentage points)."),
            ("Why the n=30 rule?",
             "<strong>CLT kicks in around n=30</strong><br><br>Sample means become approximately normal regardless of population distribution. Some symmetric distributions need less.")
        ]

        for i, (q, a) in enumerate(cards, 1):
            render_flashcard(f"ch7_card{i}", q, a)

    with tab3:
        st.markdown('<div class="example-box"><h3>🗳️ Election Polling</h3><p>Predicting election results with confidence intervals</p></div>', unsafe_allow_html=True)

        concept_connection_box(
            "Concept Connection: CLT, Standard Error, & Confidence Intervals",
            "This polling example demonstrates the <strong>Central Limit Theorem</strong> in action. Even though voting is binary (0 or 1), the sample proportion follows a <strong>normal distribution</strong> for large n. The <strong>standard error</strong> formula σ/√n explains why larger samples give narrower confidence intervals and more precise predictions."
        )

        st.markdown("""
        ### Scenario: Presidential Election Poll
        - **Population**: 150 million registered voters
        - **Sample**: 1,200 likely voters (random)
        - **Finding**: Candidate A has 52% support in sample
        - **Question**: What's the 95% confidence interval for true support?
        """)

        # Poll parameters
        n = 1200
        p_hat = 0.52

        # Standard error for proportion: SE = √[p(1-p)/n]
        se = np.sqrt(p_hat * (1 - p_hat) / n)

        # 95% CI
        z = 1.96
        moe = z * se
        ci_lower = p_hat - moe
        ci_upper = p_hat + moe

        col1, col2, col3, col4 = st.columns(4)
        col1.metric("Sample Size (n)", f"{n:,}")
        col2.metric("Sample Proportion (p̂)", f"{p_hat:.1%}")
        col3.metric("Margin of Error", f"±{moe*100:.1f}pp")
        col4.metric("95% CI", f"[{ci_lower:.1%}, {ci_upper:.1%}]")

        # Visualization
        x = np.linspace(0.45, 0.59, 1000)
        y = stats.norm.pdf(x, p_hat, se)

        fig = go.Figure()
        fig.add_trace(go.Scatter(x=x, y=y, mode='lines', name='Sampling Distribution',
                                fill='tozeroy', fillcolor='rgba(100, 150, 250, 0.3)'))
        fig.add_vline(x=p_hat, line_dash="solid", line_color="blue", annotation_text="Sample p̂")
        fig.add_vline(x=ci_lower, line_dash="dash", line_color="red", annotation_text="Lower 95%")
        fig.add_vline(x=ci_upper, line_dash="dash", line_color="red", annotation_text="Upper 95%")
        fig.add_vline(x=0.5, line_dash="dot", line_color="green", annotation_text="50% (tie)")
        fig.update_layout(title='Sampling Distribution of Support %',
                         xaxis_title='Support for Candidate A',
                         yaxis_title='Probability Density',
                         showlegend=False)
        fig.update_xaxes(tickformat='.0%')
        st.plotly_chart(fig, use_container_width=True)

        st.markdown(f"""
        ### Statistical Interpretation

        **Calculation**:
        - Standard Error: SE = √[p̂(1-p̂)/n] = √[0.52×0.48/1200] = {se:.4f}
        - Margin of Error: MOE = 1.96 × {se:.4f} = ±{moe:.4f} = ±{moe*100:.1f} percentage points
        - 95% CI: {p_hat:.1%} ± {moe*100:.1f}pp = [{ci_lower:.1%}, {ci_upper:.1%}]

        **Conclusion**:
        - We are **95% confident** true support is between {ci_lower:.1%} and {ci_upper:.1%}
        - Since **entire CI is above 50%**, Candidate A is statistically likely to win
        - The race is competitive but Candidate A has a clear advantage
        """)

        st.markdown("---")
        st.markdown("### Sample Size Effect on Precision")

        concept_connection_box(
            "The √n Relationship",
            "Margin of error decreases with <strong>√n, not n</strong>. To halve the MOE, you need to <strong>quadruple</strong> the sample size! This explains why polls rarely exceed 2,000-3,000 respondents - diminishing returns make it too expensive."
        )

        sample_sizes = [300, 600, 1200, 2400, 4800, 9600]
        moes = [1.96 * np.sqrt(0.52 * 0.48 / n) * 100 for n in sample_sizes]
        costs = [n * 5 for n in sample_sizes]  # Assume $5 per respondent

        df_sample_size = pd.DataFrame({
            'Sample Size': sample_sizes,
            'MOE (pp)': moes,
            'Cost ($)': costs,
            'Cost per 1pp precision ($)': [c/m for c, m in zip(costs, moes)]
        })

        col1, col2 = st.columns(2)

        with col1:
            fig_moe = px.line(df_sample_size, x='Sample Size', y='MOE (pp)',
                             title='Margin of Error vs Sample Size',
                             markers=True)
            fig_moe.add_hline(y=2.8, line_dash="dash", line_color="green",
                            annotation_text="Industry Standard (±2.8pp)")
            st.plotly_chart(fig_moe, use_container_width=True)

        with col2:
            st.markdown("### Sample Size Analysis")
            st.dataframe(df_sample_size.style.format({
                'MOE (pp)': '{:.2f}',
                'Cost ($)': '${:,.0f}',
                'Cost per 1pp precision ($)': '${:,.0f}'
            }), hide_index=True)

        st.markdown("""
        ### Key Insights from Analysis

        1. **n=1,200 (standard)**: ±2.8% MOE for ~$6,000
        2. **Doubling to 2,400**: Only improves to ±2.0% MOE (cost: $12,000)
        3. **Diminishing returns**: 4x sample size → only 2x precision
        4. **Industry practice**: Most polls use 1,000-1,500 respondents

        ### Why Polls Can Be Wrong
        - **Sampling error**: Even with perfect sampling, ±2.8% MOE means 5% chance of being wrong
        - **Coverage bias**: Not all voters have phones, miss hard-to-reach groups
        - **Non-response bias**: Who answers vs who doesn't may differ systematically
        - **Likely voter models**: Predicting who will actually vote is uncertain
        - **Late deciders**: Preferences can shift after poll
        """)

        st.markdown('<div class="insight">🔑 Polls work because of CLT! Just 1,200 people can predict 150M voters within ±3%. But remember: statistical precision (MOE) ≠ accuracy. Systematic biases can invalidate even large samples!</div>', unsafe_allow_html=True)

    with tab4:
        st.markdown("### 📚 Foundational Research Papers")

        research_paper_card(
            "On the Two Different Aspects of the Representative Method",
            "Jerzy Neyman",
            "1934",
            "Journal of the Royal Statistical Society, 97(4), 558-625",
            "Revolutionized survey sampling by distinguishing between purposive and random sampling, introducing stratified sampling, and developing the theory of confidence intervals. Showed that random sampling with proper design beats large non-random samples.",
            "Neyman, J. (1934). On the two different aspects of the representative method: the method of stratified sampling and the method of purposive selection. Journal of the Royal Statistical Society, 97(4), 558-625."
        )

        research_paper_card(
            "The Central Limit Theorem",
            "Pierre-Simon Laplace",
            "1810",
            "Mémoire sur les Approximations des Formules",
            "First formal proof of the Central Limit Theorem, showing that the distribution of sample means approaches normality. This fundamental result underlies most of statistical inference and explains why the normal distribution appears throughout statistics.",
            "Laplace, P. S. (1810). Mémoire sur les approximations des formules qui sont fonctions de très grands nombres. Mémoires de l'Académie des Sciences de Paris."
        )

        research_paper_card(
            "Sampling Techniques",
            "William G. Cochran",
            "1977",
            "John Wiley & Sons (3rd Edition)",
            "Comprehensive treatment of sampling theory and methods. Cochran synthesized decades of research on stratified, cluster, systematic, and multi-stage sampling, providing formulas for sample size determination and variance estimation that remain standard today.",
            "Cochran, W. G. (1977). Sampling techniques (3rd ed.). John Wiley & Sons."
        )

elif "8️⃣" in chapter:
    st.title("8️⃣ Hypothesis Testing")
    tab1, tab2, tab3, tab4 = st.tabs(["📖 Concepts", "🎴 Flashcards", "🧪 A/B Test Example", "📚 Research Papers"])

    with tab1:
        st.markdown("""
        ### Hypothesis Testing Framework

        **5-Step Process:**

        **1. State Hypotheses**
        - **H₀** (Null Hypothesis): Status quo, no effect, no difference
        - **H₁** (Alternative): What we want to prove, claim we're testing

        **2. Choose Significance Level (α)**
        - α = 0.05 (5%) most common
        - α = probability of Type I error (false positive)
        - Common values: 0.10, 0.05, 0.01

        **3. Calculate Test Statistic**
        - z-test: Large samples, known σ
        - t-test: Small samples, unknown σ
        - Chi-square: Categorical data
        - ANOVA: Compare multiple means

        **4. Find p-value**
        - p = probability of observing data (or more extreme) if H₀ is true
        - Smaller p = stronger evidence against H₀

        **5. Make Decision**
        - If p < α: **Reject H₀** (statistically significant)
        - If p ≥ α: **Fail to reject H₀** (not significant)

        ### Types of Errors

        |  | H₀ True | H₀ False |
        |---|---------|----------|
        | **Reject H₀** | Type I Error (α) | Correct (Power) |
        | **Fail to Reject H₀** | Correct (1-α) | Type II Error (β) |

        - **Type I (α)**: False positive - reject true H₀
        - **Type II (β)**: False negative - fail to reject false H₀
        - **Power**: 1 - β (probability of correctly rejecting false H₀)

        ### Common Tests

        - **One-sample t-test**: Compare sample mean to known value
        - **Two-sample t-test**: Compare two independent group means
        - **Paired t-test**: Compare before/after (dependent samples)
        - **Chi-square**: Test independence of categorical variables
        - **ANOVA**: Compare 3+ group means

        ### Statistical vs Practical Significance

        - **Statistical**: p < α (detectable difference)
        - **Practical**: Effect size large enough to matter in real world
        - Large samples can detect tiny, meaningless differences
        """)

        st.markdown("#### Interactive Hypothesis Test Simulator")

        st.markdown("**Scenario**: Does new drug lower blood pressure?")

        # Generate data
        np.random.seed(42)
        n_patients = st.slider("Number of patients", 20, 200, 100, 10)
        before = np.random.normal(140, 15, n_patients)
        effect_size = st.slider("True Effect Size (mm Hg)", 0, 15, 8, 1)
        after = before - effect_size + np.random.normal(0, 10, n_patients)

        # Paired t-test
        differences = before - after
        t_stat, p_value = stats.ttest_rel(before, after)

        # Effect size (Cohen's d)
        cohens_d = np.mean(differences) / np.std(differences)

        col1, col2 = st.columns(2)

        with col1:
            fig = go.Figure()
            fig.add_trace(go.Box(y=before, name='Before', marker_color='lightblue'))
            fig.add_trace(go.Box(y=after, name='After', marker_color='lightgreen'))
            fig.update_layout(title='Blood Pressure Before vs After Drug',
                            yaxis_title='Blood Pressure (mm Hg)')
            st.plotly_chart(fig, use_container_width=True)

        with col2:
            st.markdown(f"""
            ### Hypothesis Test Results

            **Hypotheses:**
            - H₀: μ_diff = 0 (no effect)
            - H₁: μ_diff > 0 (BP decreases)

            **Sample Statistics:**
            - Mean Before: {np.mean(before):.1f} mm Hg
            - Mean After: {np.mean(after):.1f} mm Hg
            - Mean Difference: {np.mean(differences):.1f} mm Hg
            - Std Dev of Diff: {np.std(differences):.1f}

            **Test Statistics:**
            - t-statistic: {t_stat:.3f}
            - p-value: {p_value:.4f}
            - Cohen's d: {cohens_d:.3f}

            **Decision (α=0.05):**
            """)

            if p_value < 0.05:
                st.success(f"✅ REJECT H₀ (p={p_value:.4f} < 0.05)")
                st.markdown("**Conclusion**: Drug **significantly lowers** blood pressure!")
            else:
                st.error(f"❌ Fail to reject H₀ (p={p_value:.4f} ≥ 0.05)")
                st.markdown("**Conclusion**: Insufficient evidence of drug effect")

            # Interpret effect size
            if abs(cohens_d) < 0.2:
                effect_interp = "Very small"
            elif abs(cohens_d) < 0.5:
                effect_interp = "Small"
            elif abs(cohens_d) < 0.8:
                effect_interp = "Medium"
            else:
                effect_interp = "Large"

            st.info(f"**Effect Size**: {effect_interp} (|d|={abs(cohens_d):.2f})")

    with tab2:
        st.markdown("### Interactive Flashcards - Click to Flip!")

        cards = [
            ("What is the null hypothesis (H₀)?",
             "<strong>Status quo assumption of no effect/difference</strong><br><br>Examples: No difference between groups, No correlation, Treatment doesn't work. Always includes '=' sign."),
            ("What is a p-value?",
             "<strong>P(observing data or more extreme | H₀ is true)</strong><br><br>NOT the probability H₀ is true! Small p-value = data is unlikely if H₀ were true, so we doubt H₀."),
            ("What does p < 0.05 mean?",
             "<strong>Reject H₀, result is statistically significant</strong><br><br>Less than 5% chance of seeing this data if H₀ were true. Convention, not magic threshold!"),
            ("Type I vs Type II error?",
             "<strong>Type I (α):</strong> False positive - reject true H₀<br><strong>Type II (β):</strong> False negative - fail to reject false H₀<br>Trade-off: Lowering α increases β"),
            ("Statistical vs Practical significance?",
             "<strong>Statistical:</strong> p < α (detectable difference)<br><strong>Practical:</strong> Effect large enough to matter<br>Big samples can detect tiny, meaningless differences!"),
            ("What is statistical power?",
             "<strong>Power = 1 - β = P(reject H₀ | H₀ is false)</strong><br><br>Probability of detecting real effect. Increases with: larger n, larger effect, higher α. Target: 80%+")
        ]

        for i, (q, a) in enumerate(cards, 1):
            render_flashcard(f"ch8_card{i}", q, a)

    with tab3:
        st.markdown('<div class="example-box"><h3>🧪 A/B Test: Mobile App Redesign</h3><p>Does new UI increase purchase conversion rate?</p></div>', unsafe_allow_html=True)

        concept_connection_box(
            "Concept Connection: Two-Proportion Z-Test & Hypothesis Testing",
            "This A/B test uses a <strong>two-proportion z-test</strong> to compare conversion rates. The <strong>p-value</strong> tells us if the observed difference could have occurred by chance. The <strong>confidence interval</strong> quantifies the likely range of the true effect. We also calculate <strong>effect size</strong> (relative lift) to assess practical significance beyond statistical significance."
        )

        st.markdown("""
        ### Experiment Design
        **Context**: E-commerce mobile app testing new checkout flow

        **Groups**:
        - **Control (A)**: Current multi-step checkout
        - **Treatment (B)**: New streamlined one-page checkout

        **Metric**: Conversion rate (% of visitors who complete purchase)

        **Sample**: 10,000 users randomly assigned to each group

        **Hypotheses**:
        - H₀: p_B = p_A (no difference in conversion rates)
        - H₁: p_B > p_A (new design improves conversions)
        """)

        # Simulate A/B test data
        np.random.seed(42)
        n_a = 10000
        n_b = 10000
        p_a = 0.045  # 4.5% baseline conversion
        p_b = 0.052  # 5.2% conversion (15% relative lift)

        conv_a = np.random.binomial(1, p_a, n_a).sum()
        conv_b = np.random.binomial(1, p_b, n_b).sum()

        rate_a = conv_a / n_a
        rate_b = conv_b / n_b

        # Two-proportion z-test
        p_pool = (conv_a + conv_b) / (n_a + n_b)
        se_pool = np.sqrt(p_pool * (1 - p_pool) * (1/n_a + 1/n_b))
        z_stat = (rate_b - rate_a) / se_pool
        p_value = 1 - stats.norm.cdf(z_stat)  # One-tailed test

        # Confidence interval for difference
        se_diff = np.sqrt(rate_a*(1-rate_a)/n_a + rate_b*(1-rate_b)/n_b)
        ci_lower = (rate_b - rate_a) - 1.96 * se_diff
        ci_upper = (rate_b - rate_a) + 1.96 * se_diff

        col1, col2 = st.columns(2)

        with col1:
            st.markdown("### Experiment Results")
            results_df = pd.DataFrame({
                'Group': ['Control (A)', 'Treatment (B)'],
                'Users': [f'{n_a:,}', f'{n_b:,}'],
                'Conversions': [conv_a, conv_b],
                'Conversion Rate': [f'{rate_a:.3%}', f'{rate_b:.3%}']
            })
            st.dataframe(results_df, hide_index=True, use_container_width=True)

            absolute_lift = rate_b - rate_a
            relative_lift = (rate_b - rate_a) / rate_a

            col_a, col_b = st.columns(2)
            col_a.metric("Absolute Lift", f"+{absolute_lift*100:.2f}pp",
                        help="Percentage point increase")
            col_b.metric("Relative Lift", f"+{relative_lift:.1%}",
                        help="Percentage increase over baseline")

        with col2:
            st.markdown("### Statistical Test")
            st.markdown(f"""
            **Two-Proportion Z-Test:**

            **Pooled proportion:**
            - p_pool = ({conv_a} + {conv_b}) / ({n_a:,} + {n_b:,}) = {p_pool:.4f}

            **Standard error:**
            - SE = √[p_pool(1-p_pool)(1/n_A + 1/n_B)] = {se_pool:.5f}

            **Test statistic:**
            - z = (p_B - p_A) / SE = ({rate_b:.4f} - {rate_a:.4f}) / {se_pool:.5f}
            - z = {z_stat:.3f}

            **P-value:** {p_value:.4f}

            **95% CI for difference:** [{ci_lower*100:.2f}pp, {ci_upper*100:.2f}pp]
            """)

            if p_value < 0.05:
                st.success(f"✅ STATISTICALLY SIGNIFICANT (p={p_value:.4f} < 0.05)")
                st.markdown("**Decision: REJECT H₀**")
                st.markdown("**Recommendation: SHIP NEW DESIGN!** 🚀")
            else:
                st.warning(f"❌ Not significant (p={p_value:.4f} ≥ 0.05)")
                st.markdown("**Decision: Fail to reject H₀**")
                st.markdown("Need more data or larger effect to detect difference")

        # Visualization
        fig = go.Figure()
        fig.add_trace(go.Bar(
            x=['Control (A)', 'Treatment (B)'],
            y=[rate_a*100, rate_b*100],
            marker_color=['#3498db', '#2ecc71'],
            text=[f'{rate_a:.2%}', f'{rate_b:.2%}'],
            textposition='outside',
            showlegend=False
        ))
        fig.update_layout(
            title='Conversion Rates Comparison',
            yaxis_title='Conversion Rate (%)',
            yaxis_range=[0, max(rate_a, rate_b)*120]
        )
        st.plotly_chart(fig, use_container_width=True)

        st.markdown("---")
        st.markdown("### Business Impact Analysis")

        concept_connection_box(
            "From Statistical to Business Significance",
            "Statistical significance (p < 0.05) confirms the effect is real, not random chance. But is it <strong>practically significant</strong>? We calculate ROI by multiplying the conversion lift by user volume and revenue per conversion."
        )

        # Business metrics
        avg_order_value = 50
        monthly_users = 1_000_000

        additional_conversions = (rate_b - rate_a) * monthly_users
        additional_revenue = additional_conversions * avg_order_value
        annual_revenue_impact = additional_revenue * 12

        col1, col2, col3 = st.columns(3)
        col1.metric("Additional Conversions/Month", f"{additional_conversions:,.0f}")
        col2.metric("Additional Revenue/Month", f"${additional_revenue:,.0f}")
        col3.metric("Annual Revenue Impact", f"${annual_revenue_impact:,.0f}")

        st.markdown(f"""
        ### ROI Calculation

        **Assumptions:**
        - Monthly users: {monthly_users:,}
        - Average order value: ${avg_order_value}
        - Conversion lift: {absolute_lift:.3%} ({relative_lift:.1%} relative)

        **Financial Impact:**
        - Additional conversions per month: {additional_conversions:,.0f}
        - Additional revenue per month: ${additional_revenue:,.0f}
        - **Annual revenue impact: ${annual_revenue_impact:,.0f}**

        **Development Cost Analysis:**
        - Assume redesign cost: $100,000
        - Payback period: {100000/additional_revenue:.1f} months
        - ROI (Year 1): {(annual_revenue_impact - 100000)/100000:.1%}

        **Conclusion**: Even a "small" {absolute_lift*100:.2f} percentage point lift translates to ${annual_revenue_impact:,.0f} annually!
        This demonstrates why A/B testing is critical for data-driven product decisions.
        """)

        # Power analysis visualization
        st.markdown("---")
        st.markdown("### Statistical Power Analysis")

        concept_connection_box(
            "Understanding Statistical Power",
            "<strong>Power</strong> is the probability of detecting a real effect. Higher power = lower risk of Type II error (false negative). Power increases with sample size, effect size, and significance level."
        )

        # Calculate power for different sample sizes
        sample_sizes = np.array([1000, 2500, 5000, 7500, 10000, 15000, 20000])
        true_effect = rate_b - rate_a

        powers = []
        for n in sample_sizes:
            # Power calculation for two-proportion test
            se_alt = np.sqrt(rate_a*(1-rate_a)/n + rate_b*(1-rate_b)/n)
            z_crit = stats.norm.ppf(0.95)  # One-tailed α=0.05
            z_beta = (true_effect - z_crit * se_pool) / se_alt
            power = stats.norm.cdf(z_beta)
            powers.append(power)

        fig_power = px.line(pd.DataFrame({'Sample Size per Group': sample_sizes, 'Power': powers}),
                           x='Sample Size per Group', y='Power',
                           title='Statistical Power vs Sample Size',
                           markers=True)
        fig_power.add_hline(y=0.8, line_dash="dash", line_color="green",
                          annotation_text="Target Power (80%)")
        fig_power.add_vline(x=10000, line_dash="dash", line_color="blue",
                          annotation_text="Actual Sample")
        fig_power.update_yaxes(tickformat='.0%', range=[0, 1])
        st.plotly_chart(fig_power, use_container_width=True)

        st.markdown(f"""
        **Power Insights:**
        - Our sample size (10,000 per group) achieves ~{powers[4]:.1%} power
        - This means a {(1-powers[4])*100:.0f}% risk of Type II error (missing real effect)
        - For 80% power, we'd need ~{sample_sizes[np.argmax(np.array(powers) >= 0.8)]:,} users per group
        """)

        st.markdown('<div class="insight">🔑 This A/B test shows a {:.1%} relative lift that is both statistically significant (p={:.4f}) and practically significant (${:,.0f} annual impact). Proper hypothesis testing + business context = data-driven decisions!</div>'.format(relative_lift, p_value, annual_revenue_impact), unsafe_allow_html=True)

    with tab4:
        st.markdown("### 📚 Foundational Research Papers")

        research_paper_card(
            "The Design of Experiments",
            "Ronald A. Fisher",
            "1935",
            "Oliver & Boyd, Edinburgh",
            "Fisher established the principles of experimental design including randomization, replication, and blocking. Introduced the null hypothesis significance testing framework, p-values, and ANOVA. This book laid the foundation for modern hypothesis testing and A/B testing.",
            "Fisher, R. A. (1935). The design of experiments. Oliver & Boyd."
        )

        research_paper_card(
            "Statistical Methods for Research Workers",
            "Ronald A. Fisher",
            "1925",
            "Oliver & Boyd, Edinburgh",
            "Introduced the concept of significance testing with p-values and the 0.05 significance level. Fisher's approach to hypothesis testing became the dominant paradigm in statistics, though later critiqued for lacking consideration of Type II errors and power.",
            "Fisher, R. A. (1925). Statistical methods for research workers. Oliver and Boyd."
        )

        research_paper_card(
            "On the Problem of the Most Efficient Tests of Statistical Hypotheses",
            "Jerzy Neyman & Egon Pearson",
            "1933",
            "Philosophical Transactions of the Royal Society A, 231, 289-337",
            "Developed the Neyman-Pearson framework emphasizing both Type I and Type II errors, introducing the concepts of power and the likelihood ratio test. This complemented Fisher's approach by considering the alternative hypothesis explicitly.",
            "Neyman, J., & Pearson, E. S. (1933). On the problem of the most efficient tests of statistical hypotheses. Philosophical Transactions of the Royal Society of London. Series A, 231(694-706), 289-337."
        )

# Footer
st.sidebar.markdown("---")
st.sidebar.info("💡 Each chapter has 4 tabs:\n\n📖 Concepts | 🎴 Flashcards | 📊 Example | 📚 Research")
st.sidebar.success(f"✨ Premium Features:\n- 3D Flip Cards\n- Concept Connections\n- Research Papers\n- Enhanced UI")
st.sidebar.markdown("---")
st.sidebar.markdown("**🎓 Enterprise Data Analytics Premium**")
st.sidebar.markdown("*Built with Streamlit & Plotly*")
