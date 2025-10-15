import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from scipy import stats
from sklearn.linear_model import LinearRegression

st.set_page_config(page_title="Enterprise Data Analytics", page_icon="📊", layout="wide")

# Initialize session state
if 'flipped_cards' not in st.session_state:
    st.session_state.flipped_cards = {}

def flip_card(card_id):
    if card_id not in st.session_state.flipped_cards:
        st.session_state.flipped_cards[card_id] = False
    st.session_state.flipped_cards[card_id] = not st.session_state.flipped_cards[card_id]

def render_flashcard(card_id, question, answer):
    is_flipped = st.session_state.flipped_cards.get(card_id, False)

    # Render flashcard visual
    st.markdown(f"""
    <style>
    .flashcard-container {{
        perspective: 1000px;
        width: 100%;
        height: 200px;
        margin-bottom: 15px;
    }}
    .flashcard-{card_id} {{
        position: relative;
        width: 100%;
        height: 100%;
        transform-style: preserve-3d;
        transition: transform 0.6s ease;
        transform: {'rotateY(180deg)' if is_flipped else 'rotateY(0deg)'};
    }}
    .flashcard-side {{
        position: absolute;
        width: 100%;
        height: 100%;
        backface-visibility: hidden;
        border-radius: 12px;
        padding: 20px;
        display: flex;
        align-items: center;
        justify-content: center;
        text-align: center;
        font-size: 14px;
        box-shadow: 0 4px 15px rgba(0,0,0,0.2);
        cursor: pointer;
    }}
    .flashcard-front {{
        background: linear-gradient(135deg, #2563eb 0%, #3b82f6 100%);
        color: white;
    }}
    .flashcard-back {{
        background: linear-gradient(135deg, #059669 0%, #10b981 100%);
        color: white;
        transform: rotateY(180deg);
    }}
    .flashcard-{card_id}:hover {{
        transform: {'rotateY(180deg) scale(1.02)' if is_flipped else 'rotateY(0deg) scale(1.02)'};
    }}
    </style>
    <div class="flashcard-container">
        <div class="flashcard-{card_id}">
            <div class="flashcard-side flashcard-front">
                <div><strong>{question}</strong></div>
            </div>
            <div class="flashcard-side flashcard-back">
                <div>{answer}</div>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # Simple click button below
    if st.button("Click to flip", key=f"flip_{card_id}", use_container_width=True):
        flip_card(card_id)
        st.rerun()

def concept_connection_box(title, content):
    st.markdown(f"""
    <div style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
         border-left: 5px solid #ffd700; padding: 20px; margin: 20px 0;
         border-radius: 10px; color: white;">
        <h4 style="color: #ffd700; margin-top: 0;">{title}</h4>
        <p style="margin-bottom: 0;">{content}</p>
    </div>
    """, unsafe_allow_html=True)

def research_paper_card(title, authors, year, journal, contribution, citation, link=None):
    with st.expander(f"📄 {title} ({year})"):
        st.markdown(f"""
        **Authors:** {authors}
        **Published:** {journal}

        **Key Contribution:**
        {contribution}

        **Citation:**
        `{citation}`
        """)

        if link:
            # Determine link type
            if "doi.org" in link:
                link_text = "Access Paper (DOI)"
            elif "archive.org" in link or "gallica.bnf.fr" in link:
                link_text = "Access Paper (Archive)"
            else:
                link_text = "Access Paper"
            st.markdown(f"**🔗 [{link_text}]({link})**")

def render_navigation(current_chapter, chapters):
    """Render chapter progress info"""
    current_index = chapters.index(current_chapter)

    if current_chapter != "Home":
        st.markdown("---")
        progress = (current_index) / (len(chapters) - 1)
        st.progress(progress)

        col1, col2, col3 = st.columns(3)
        with col1:
            if current_index > 1:
                st.info(f"← Previous: {chapters[current_index - 1]}")
        with col2:
            st.success(f"Chapter {current_index} of {len(chapters) - 1}")
        with col3:
            if current_index < len(chapters) - 1:
                st.info(f"Next: {chapters[current_index + 1]} →")

# Styling
st.markdown("""
<style>
@keyframes gradientShift {
    0% {background-position: 0% 50%;}
    50% {background-position: 100% 50%;}
    100% {background-position: 0% 50%;}
}
.main {
    background: linear-gradient(135deg, #667eea 0%, #764ba2 50%, #f093fb 100%);
    background-size: 200% 200%;
    animation: gradientShift 15s ease infinite;
}
h1, h2, h3 {color: white !important;}
.example-box {
    background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
    color: white;
    padding: 30px;
    border-radius: 15px;
    margin: 20px 0;
}
.insight {
    background: linear-gradient(135deg, #ffd89b 0%, #19547b 100%);
    color: white;
    padding: 20px;
    border-radius: 12px;
    font-weight: 600;
    margin: 15px 0;
}
.paper-card {
    background: white;
    padding: 25px;
    border-radius: 15px;
    margin: 15px 0;
    box-shadow: 0 10px 30px rgba(0,0,0,0.2);
}
</style>
""", unsafe_allow_html=True)

# Navigation
st.sidebar.title("📚 Enterprise Data Analytics")

# Chapter list for navigation
chapters = [
    "Home",
    "1. Data Fundamentals",
    "2. Distributions",
    "3. Relationships",
    "4. Probability",
    "5. Statistical Distributions",
    "6. Decision Making",
    "7. Sampling",
    "8. Hypothesis Testing"
]

chapter = st.sidebar.radio("Select Chapter", chapters)

# Reset flashcards button
st.sidebar.markdown("---")
if st.sidebar.button("🔄 Reset All Flashcards", use_container_width=True):
    st.session_state.flipped_cards = {}
    st.rerun()

st.sidebar.markdown("---")

# Previous/Next navigation buttons at bottom of content (added later in code)

if "Home" in chapter:
    st.title("Enterprise Data Analytics")
    st.markdown("## Complete Interactive Presentation")

    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Chapters", "8")
    col2.metric("Examples", "32+")
    col3.metric("Flashcards", "80+")
    col4.metric("Research Papers", "24+")

    st.markdown("---")
    st.markdown("""
    ### Real-World Examples
    - **Netflix** - Viewing analytics
    - **Uber** - Ride duration analysis
    - **Amazon** - Product ratings correlation
    - **Tesla** - Insurance risk probability
    - **Twitter** - Engagement distributions
    - **Startup** - Investment decisions
    - **Elections** - Polling and sampling
    - **A/B Testing** - Hypothesis testing

    ### Premium Features
    - 3D Flip Flashcards with interactive learning
    - Concept Connections linking theory to practice
    - Research Papers with academic foundations
    - Enhanced UI with gradient animations

    **Select a chapter to begin**
    """)

    # Navigation buttons
    st.markdown("---")
    render_navigation(chapter, chapters)

elif "1." in chapter:
    st.title("1. Data Analysis Fundamentals")
    tab1, tab2, tab3, tab4 = st.tabs(["Concepts", "Netflix Example", "Flashcards",  "Research Papers"])

    with tab1:
        col1, col2 = st.columns(2)
        with col1:
            st.markdown("""
            ### Quantitative Data
            **Discrete** (countable)
            - Customers: 1, 2, 3
            - Items sold: 47, 103

            **Continuous** (measurable)
            - Revenue: $1,547.92
            - Time: 3.7 seconds
            """)
        with col2:
            st.markdown("""
            ### Qualitative Data
            **Nominal** (no order)
            - Colors, Gender, Types

            **Ordinal** (ordered)
            - Ratings: 1 star to 5 stars
            - Education levels
            """)

        st.markdown("""
        ### Exploratory Data Analysis
        **KDD Process** (Fayyad et al., 1996):
        1. Selection - Choose data
        2. Preprocessing - Clean data
        3. Transformation - Format data
        4. Data Mining - Find patterns
        5. Interpretation - Extract insights

        ### Measures of Central Tendency
        - **Mean**: Average value (sensitive to outliers)
        - **Median**: Middle value (robust to outliers)
        - **Mode**: Most frequent value

        ### Measures of Spread
        - **Range**: Max - Min
        - **Variance**: Average squared deviation from mean
        - **Standard Deviation**: Square root of variance
        - **IQR**: Q3 - Q1 (middle 50%)
        """)

    with tab2:
        st.markdown('<div class="example-box"><h3>Netflix Viewing Analytics</h3><p>Analyzing 230M+ subscribers to optimize content recommendations</p></div>', unsafe_allow_html=True)

        concept_connection_box(
            "Concept Connection: Data Types and Summary Statistics",
            "Netflix uses <strong>continuous quantitative data</strong> (watch time in hours) and <strong>nominal qualitative data</strong> (content type, device). The <strong>right-skewed distribution</strong> of watch time means they use <strong>median</strong> instead of mean for fair subscriber segmentation."
        )

        st.markdown("### Interactive Controls")
        col1, col2 = st.columns(2)
        with col1:
            num_users = st.slider("Number of Users", 100, 5000, 1000, 100)
        with col2:
            skew_factor = st.slider("Skewness Factor", 1.0, 5.0, 2.0, 0.5)

        np.random.seed(42)
        netflix = pd.DataFrame({
            'Hours': np.random.gamma(skew_factor, 3, num_users),
            'Type': np.random.choice(['Series', 'Movie', 'Doc'], num_users, p=[0.6, 0.3, 0.1]),
            'Device': np.random.choice(['TV', 'Mobile', 'Desktop'], num_users, p=[0.5, 0.35, 0.15]),
            'Rating': np.random.choice([1,2,3,4,5], num_users, p=[0.05,0.1,0.2,0.35,0.3])
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

        st.markdown('<div class="insight">Mean > Median indicates right skew. Netflix uses MEDIAN for subscriber metrics to avoid bias from binge-watchers.</div>', unsafe_allow_html=True)

        st.markdown("### Interactive Data Type Explorer")
        selected_type = st.selectbox("Select Content Type", ['All'] + list(netflix['Type'].unique()))

        if selected_type != 'All':
            filtered = netflix[netflix['Type'] == selected_type]
            col1, col2, col3 = st.columns(3)
            col1.metric(f"{selected_type} Mean", f"{filtered['Hours'].mean():.2f}h")
            col2.metric(f"{selected_type} Median", f"{filtered['Hours'].median():.2f}h")
            col3.metric(f"{selected_type} Count", len(filtered))

        # Dataset View/Download
        st.markdown("### Dataset")
        col1, col2 = st.columns([1, 1])
        with col1:
            if st.checkbox("View Dataset", key="view_ch1_netflix"):
                st.dataframe(netflix.head(10))
        with col2:
            csv = netflix.to_csv(index=False).encode('utf-8')
            st.download_button(
                label="Download CSV",
                data=csv,
                file_name="netflix_data.csv",
                mime="text/csv",
                key="download_ch1_netflix"
            )

    with tab3:
        st.markdown("### Flashcards")

        cards = [
            ("Daily downloads - What type of data?",
             "<strong>Discrete Quantitative</strong><br><br>Countable whole numbers. Cannot have 47.5 downloads."),
            ("5-star rating - Ordinal or Nominal?",
             "<strong>Ordinal</strong><br><br>5 > 4 > 3 > 2 > 1 has a meaningful order"),
            ("When to use Mean vs Median for salaries?",
             "<strong>Use Median</strong><br><br>Salary data is right-skewed. Ultra-high earners inflate the mean."),
            ("When should you use Mode?",
             "<strong>Categorical data</strong><br><br>Mode identifies the most common category."),
            ("What does Standard Deviation measure?",
             "<strong>Measures spread/variability</strong><br><br>68% of data falls within ±1 SD in normal distribution."),
            ("Why apply log transformation?",
             "<strong>Handle skewed data</strong><br><br>Compresses large values, making relationships more linear."),
            ("What is the IQR?",
             "<strong>Interquartile Range</strong><br><br>Q3 - Q1. Contains the middle 50% of the data."),
            ("Difference between variance and standard deviation?",
             "<strong>SD = √Variance</strong><br><br>Both measure spread, but SD is in original units."),
            ("Temperature in Celsius - What data type?",
             "<strong>Continuous Quantitative</strong><br><br>Can take any value within a range."),
            ("What are the 5 steps of KDD?",
             "<strong>Selection → Preprocessing → Transformation → Data Mining → Interpretation</strong><br><br>Framework by Fayyad et al., 1996"),
            ("Nominal vs Ordinal data?",
             "<strong>Nominal has no order (colors, types)</strong><br><br>Ordinal has meaningful order (ratings, education level)"),
            ("Why use quartiles?",
             "<strong>Robust to outliers</strong><br><br>Q1, Q2 (median), Q3 divide data into 4 equal parts")
        ]

        # Grid layout: 3 columns
        num_cols = 3
        for i in range(0, len(cards), num_cols):
            cols = st.columns(num_cols)
            for j in range(num_cols):
                if i + j < len(cards):
                    with cols[j]:
                        q, a = cards[i + j]
                        render_flashcard(f"ch1_card{i+j+1}", q, a)

    with tab4:
        st.markdown("### Foundational Research Papers")

        research_paper_card(
            "Exploratory Data Analysis",
            "John W. Tukey",
            "1977",
            "Addison-Wesley Publishing Company",
            "Tukey pioneered EDA as a philosophy emphasizing visual methods and iterative data exploration before formal modeling. He introduced box plots, stem-and-leaf plots, and emphasized the importance of understanding data structure through visualization.",
            "Tukey, J. W. (1977). Exploratory Data Analysis. Addison-Wesley.",
            link="https://archive.org/details/exploratorydataa00tuke_0"
        )

        research_paper_card(
            "Knowledge Discovery in Databases",
            "Fayyad, U., Piatetsky-Shapiro, G., & Smyth, P.",
            "1996",
            "AI Magazine, 17(3), 37-54",
            "Formalized the KDD process that became the standard framework for extracting knowledge from large datasets. Defined data mining as a step within the broader KDD process.",
            "Fayyad, U., Piatetsky-Shapiro, G., & Smyth, P. (1996). From data mining to knowledge discovery in databases. AI magazine, 17(3), 37-37.",
            link="https://doi.org/10.1609/aimag.v17i3.1230"
        )

        research_paper_card(
            "The Future of Data Analysis",
            "John W. Tukey",
            "1962",
            "The Annals of Mathematical Statistics, 33(1), 1-67",
            "Argued that data analysis should be recognized as a legitimate science distinct from mathematics. This paper laid the philosophical foundation for modern data science.",
            "Tukey, J. W. (1962). The future of data analysis. The annals of mathematical statistics, 33(1), 1-67.",
            link="https://doi.org/10.1214/aoms/1177704711"
        )

    # Navigation buttons
    st.markdown("---")
    render_navigation(chapter, chapters)

elif "2." in chapter:
    st.title("2. Distributions")
    tab1, tab3, tab2, tab4 = st.tabs(["Concepts", "Flashcards", "Uber Example", "Research Papers"])

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

        st.markdown("### Interactive Distribution Explorer")
        dist_type = st.selectbox("Explore Distribution", ["Normal", "Right-Skewed", "Left-Skewed", "Bimodal"])

        sample_size = st.slider("Sample Size", 100, 5000, 1000, 100)

        if dist_type == "Normal":
            data = np.random.normal(50, 15, sample_size)
        elif dist_type == "Right-Skewed":
            data = np.random.gamma(2, 10, sample_size)
        elif dist_type == "Left-Skewed":
            data = 100 - np.random.gamma(2, 10, sample_size)
        else:  # Bimodal
            data = np.concatenate([np.random.normal(30, 5, sample_size//2),
                                  np.random.normal(70, 5, sample_size//2)])

        col1, col2 = st.columns(2)
        with col1:
            fig = px.histogram(data, nbins=30, title=f'{dist_type} Distribution')
            fig.add_vline(x=np.mean(data), line_dash="dash", line_color="red", annotation_text="Mean")
            fig.add_vline(x=np.median(data), line_dash="dash", line_color="green", annotation_text="Median")
            st.plotly_chart(fig, use_container_width=True)
        with col2:
            fig = px.box(y=data, title='Box Plot with Outliers')
            st.plotly_chart(fig, use_container_width=True)

        col1, col2, col3, col4 = st.columns(4)
        col1.metric("Mean", f"{np.mean(data):.2f}")
        col2.metric("Median", f"{np.median(data):.2f}")
        col3.metric("Skewness", f"{stats.skew(data):.2f}")
        col4.metric("Kurtosis", f"{stats.kurtosis(data):.2f}")

    with tab3:
        st.markdown('<div class="example-box"><h3>Uber Ride Duration Analysis</h3><p>Analyzing millions of rides to optimize driver allocation and pricing</p></div>', unsafe_allow_html=True)

        concept_connection_box(
            "Concept Connection: Distribution Analysis and Outlier Detection",
            "Uber analyzes ride duration distributions to identify typical patterns and detect anomalies. <strong>Right-skewed distributions</strong> in ride times indicate most trips are short, with occasional long trips. <strong>Outlier detection using IQR</strong> helps identify fraudulent rides or data errors."
        )

        st.markdown("### Interactive Ride Analysis")
        col1, col2, col3 = st.columns(3)
        with col1:
            num_rides = st.slider("Number of Rides", 500, 10000, 2000, 500)
        with col2:
            mean_duration = st.slider("Average Duration (min)", 10, 40, 20, 5)
        with col3:
            skew_level = st.slider("Skewness Level", 1, 5, 2, 1)

        np.random.seed(42)
        uber = pd.DataFrame({
            'Duration': np.random.gamma(skew_level, mean_duration/skew_level, num_rides),
            'Distance': np.random.gamma(2, 5, num_rides),
            'Time_of_Day': np.random.choice(['Morning', 'Afternoon', 'Evening', 'Night'], num_rides)
        })

        # Calculate outliers
        Q1 = uber['Duration'].quantile(0.25)
        Q3 = uber['Duration'].quantile(0.75)
        IQR = Q3 - Q1
        lower_bound = Q1 - 1.5 * IQR
        upper_bound = Q3 + 1.5 * IQR
        outliers = uber[(uber['Duration'] < lower_bound) | (uber['Duration'] > upper_bound)]

        col1, col2 = st.columns(2)
        with col1:
            fig = px.histogram(uber, x='Duration', nbins=40, title='Ride Duration Distribution')
            fig.add_vline(x=uber['Duration'].mean(), line_dash="dash", line_color="red", annotation_text="Mean")
            fig.add_vline(x=uber['Duration'].median(), line_dash="dash", line_color="green", annotation_text="Median")
            fig.add_vline(x=upper_bound, line_dash="dot", line_color="orange", annotation_text="Outlier Threshold")
            st.plotly_chart(fig, use_container_width=True)
        with col2:
            fig = px.box(uber, x='Time_of_Day', y='Duration', title='Duration by Time of Day', color='Time_of_Day')
            st.plotly_chart(fig, use_container_width=True)

        col1, col2, col3, col4 = st.columns(4)
        col1.metric("Mean Duration", f"{uber['Duration'].mean():.1f} min")
        col2.metric("Median Duration", f"{uber['Duration'].median():.1f} min")
        col3.metric("Skewness", f"{stats.skew(uber['Duration']):.2f}")
        col4.metric("Outliers Detected", f"{len(outliers)}")

        st.markdown(f'<div class="insight">IQR Method detected {len(outliers)} outlier rides ({len(outliers)/len(uber)*100:.1f}%). These could be long-distance trips or data errors requiring investigation.</div>', unsafe_allow_html=True)

        if st.checkbox("Show Outlier Details"):
            st.dataframe(outliers[['Duration', 'Distance', 'Time_of_Day']].head(10))

        # Dataset View/Download
        st.markdown("### Dataset")
        col1, col2 = st.columns([1, 1])
        with col1:
            if st.checkbox("View Dataset", key="view_ch2_uber"):
                st.dataframe(uber.head(10))
        with col2:
            csv = uber.to_csv(index=False).encode('utf-8')
            st.download_button(
                label="Download CSV",
                data=csv,
                file_name="uber_data.csv",
                mime="text/csv",
                key="download_ch2_uber"
            )

    with tab2:
        st.markdown("### Flashcards")

        cards = [
            ("What does positive skewness indicate?",
             "<strong>Right-skewed (long right tail)</strong><br><br>Mean > Median. Example: Income data"),
            ("How to detect outliers using IQR?",
             "<strong>Below Q1-1.5×IQR or Above Q3+1.5×IQR</strong><br><br>IQR = Q3 - Q1"),
            ("What does kurtosis measure?",
             "<strong>Tail heaviness</strong><br><br>High kurtosis = more extreme outliers"),
            ("Histogram vs Box Plot?",
             "<strong>Histogram shows distribution shape</strong><br><br>Box plot shows quartiles and outliers"),
            ("When is mean a poor measure?",
             "<strong>When data is skewed</strong><br><br>Outliers pull the mean away from typical values"),
            ("What is a Z-score?",
             "<strong>Number of standard deviations from mean</strong><br><br>Z = (X - μ) / σ"),
            ("What does IQR represent?",
             "<strong>Middle 50% of data</strong><br><br>Range from Q1 to Q3"),
            ("Difference between variance and IQR?",
             "<strong>Variance uses all data, IQR only middle 50%</strong><br><br>IQR is robust to outliers"),
            ("What is negative skewness?",
             "<strong>Left-skewed (long left tail)</strong><br><br>Mean < Median. Example: Age at retirement"),
            ("When is Z-score > 3 significant?",
             "<strong>Indicates potential outlier</strong><br><br>Only 0.3% of normal data exceeds ±3σ"),
            ("What does high kurtosis mean?",
             "<strong>Heavy tails, more outliers</strong><br><br>Leptokurtic distribution (kurtosis > 3)"),
            ("What does low kurtosis mean?",
             "<strong>Light tails, fewer outliers</strong><br><br>Platykurtic distribution (kurtosis < 3)"),
            ("Why is median robust?",
             "<strong>Not affected by extreme values</strong><br><br>Changes only when middle values change"),
            ("What is Tukey's fence rule?",
             "<strong>Q1 - 1.5×IQR and Q3 + 1.5×IQR</strong><br><br>Standard outlier detection method")
        ]

        # Grid layout: 3 columns
        num_cols = 3
        for i in range(0, len(cards), num_cols):
            cols = st.columns(num_cols)
            for j in range(num_cols):
                if i + j < len(cards):
                    with cols[j]:
                        q, a = cards[i + j]
                        render_flashcard(f"ch2_card{i+j+1}", q, a)

    with tab4:
        st.markdown("### Foundational Research Papers")

        research_paper_card(
            "Exploratory Data Analysis",
            "John W. Tukey",
            "1977",
            "Addison-Wesley",
            "Introduced the box plot (box-and-whisker plot) as a standardized way to display distribution through quartiles. The box plot revolutionized outlier detection and distribution comparison.",
            "Tukey, J. W. (1977). Exploratory Data Analysis. Addison-Wesley.",
            link="https://archive.org/details/exploratorydataa00tuke_0"
        )

        research_paper_card(
            "Contributions to the Mathematical Theory of Evolution",
            "Karl Pearson",
            "1894",
            "Philosophical Transactions of the Royal Society of London, 185, 71-110",
            "Developed the concept of skewness and kurtosis as moments of distribution. Introduced systematic methods for describing distribution shape mathematically.",
            "Pearson, K. (1894). Contributions to the mathematical theory of evolution. Philosophical Transactions of the Royal Society of London. A, 185, 71-110.",
            link="https://doi.org/10.1098/rsta.1894.0003"
        )

        research_paper_card(
            "The Influence Function and Its Role in Robust Estimation",
            "Frank Hampel",
            "1974",
            "Journal of the American Statistical Association, 69(346), 383-393",
            "Formalized robust statistics and the influence of outliers on statistical estimates. Showed why median and IQR are more robust than mean and standard deviation.",
            "Hampel, F. R. (1974). The influence curve and its role in robust estimation. JASA, 69(346), 383-393.",
            link="https://doi.org/10.1080/01621459.1974.10482962"
        )

    # Navigation buttons
    st.markdown("---")
    render_navigation(chapter, chapters)

elif "3." in chapter:
    st.title("3. Relationships")
    tab1, tab3, tab2, tab4 = st.tabs(["Concepts", "Flashcards", "Amazon Example", "Research Papers"])

    with tab1:
        st.markdown("""
        ### Correlation
        Measures strength and direction of linear relationship between two variables

        **Pearson Correlation (r)**
        - Range: -1 to +1
        - -1: Perfect negative correlation
        - 0: No correlation
        - +1: Perfect positive correlation
        - Assumes: Linear relationship, no outliers

        **Spearman Correlation (ρ)**
        - Rank-based, robust to outliers
        - Detects monotonic relationships
        - Better for ordinal data

        ### Regression
        Models relationship between variables

        **Linear Regression**
        - Y = β₀ + β₁X + ε
        - β₀: Intercept
        - β₁: Slope (change in Y per unit X)
        - R²: Proportion of variance explained (0 to 1)

        ### Interpretation Guidelines
        - |r| < 0.3: Weak
        - 0.3 ≤ |r| < 0.7: Moderate
        - |r| ≥ 0.7: Strong
        """)

        st.markdown("### Interactive Correlation Explorer")
        col1, col2 = st.columns(2)
        with col1:
            correlation_strength = st.slider("Correlation Strength", -1.0, 1.0, 0.7, 0.1)
        with col2:
            sample_size = st.slider("Number of Points", 50, 500, 200, 50)

        noise_level = st.slider("Noise Level", 0.0, 2.0, 0.5, 0.1)

        np.random.seed(42)
        x = np.random.normal(0, 1, sample_size)
        y = correlation_strength * x + np.random.normal(0, noise_level, sample_size)

        df = pd.DataFrame({'X': x, 'Y': y})

        # Calculate actual correlation
        actual_corr = np.corrcoef(x, y)[0, 1]

        # Linear regression
        from numpy.polynomial import Polynomial
        p = Polynomial.fit(df['X'], df['Y'], 1)
        line_x = np.array([df['X'].min(), df['X'].max()])
        line_y = p(line_x)

        fig = px.scatter(df, x='X', y='Y', title=f'Interactive Correlation (r = {actual_corr:.3f})')
        fig.add_scatter(x=line_x, y=line_y, mode='lines', name='Regression Line',
                       line=dict(color='red', width=2))
        st.plotly_chart(fig, use_container_width=True)

        col1, col2, col3 = st.columns(3)
        col1.metric("Pearson r", f"{actual_corr:.3f}")
        col2.metric("R² (variance explained)", f"{actual_corr**2:.3f}")

        if abs(actual_corr) < 0.3:
            strength_label = "Weak"
        elif abs(actual_corr) < 0.7:
            strength_label = "Moderate"
        else:
            strength_label = "Strong"
        col3.metric("Strength", strength_label)

    with tab3:
        st.markdown('<div class="example-box"><h3>Amazon Product Rating Analysis</h3><p>Analyzing correlation between price, ratings, and reviews for millions of products</p></div>', unsafe_allow_html=True)

        concept_connection_box(
            "Concept Connection: Correlation and Regression Analysis",
            "Amazon uses <strong>correlation analysis</strong> to understand relationships between product price, star ratings, and number of reviews. <strong>Regression models</strong> help predict product success and optimize pricing strategies. Understanding these relationships is crucial for recommendation algorithms."
        )

        st.markdown("### Interactive Product Analysis")
        col1, col2 = st.columns(2)
        with col1:
            num_products = st.slider("Number of Products", 100, 2000, 500, 100)
        with col2:
            price_rating_corr = st.slider("Price-Rating Correlation", -0.8, 0.8, -0.3, 0.1)

        np.random.seed(42)
        price = np.random.uniform(10, 200, num_products)
        rating = 5 - (price_rating_corr * (price - price.mean()) / price.std() +
                     np.random.normal(0, 0.5, num_products))
        rating = np.clip(rating, 1, 5)
        reviews = np.random.poisson(50, num_products) + (rating - 3) * 20

        amazon = pd.DataFrame({
            'Price': price,
            'Rating': rating,
            'Reviews': reviews,
            'Category': np.random.choice(['Electronics', 'Books', 'Home', 'Clothing'], num_products)
        })

        # Calculate correlations
        corr_price_rating = amazon['Price'].corr(amazon['Rating'])
        corr_rating_reviews = amazon['Rating'].corr(amazon['Reviews'])

        col1, col2 = st.columns(2)
        with col1:
            from numpy.polynomial import Polynomial
            p = Polynomial.fit(amazon['Price'], amazon['Rating'], 1)
            line_x = np.array([amazon['Price'].min(), amazon['Price'].max()])
            line_y = p(line_x)

            fig = px.scatter(amazon, x='Price', y='Rating', title='Price vs Rating',
                           color='Category', opacity=0.6)
            fig.add_scatter(x=line_x, y=line_y, mode='lines', name='Trend Line',
                          line=dict(color='red', width=2))
            st.plotly_chart(fig, use_container_width=True)
        with col2:
            p2 = Polynomial.fit(amazon['Rating'], amazon['Reviews'], 1)
            line_x2 = np.array([amazon['Rating'].min(), amazon['Rating'].max()])
            line_y2 = p2(line_x2)

            fig = px.scatter(amazon, x='Rating', y='Reviews', title='Rating vs Reviews',
                           color='Category', opacity=0.6)
            fig.add_scatter(x=line_x2, y=line_y2, mode='lines', name='Trend Line',
                          line=dict(color='red', width=2))
            st.plotly_chart(fig, use_container_width=True)

        col1, col2, col3 = st.columns(3)
        col1.metric("Price-Rating Correlation", f"{corr_price_rating:.3f}")
        col2.metric("Rating-Reviews Correlation", f"{corr_rating_reviews:.3f}")
        col3.metric("Average Rating", f"{amazon['Rating'].mean():.2f}")

        st.markdown(f'<div class="insight">Price and rating show {"negative" if corr_price_rating < 0 else "positive"} correlation (r = {corr_price_rating:.3f}). Higher-rated products tend to attract more reviews (r = {corr_rating_reviews:.3f}).</div>', unsafe_allow_html=True)

        st.markdown("### Category Breakdown")
        selected_category = st.selectbox("Select Category", ['All'] + list(amazon['Category'].unique()))

        if selected_category != 'All':
            cat_data = amazon[amazon['Category'] == selected_category]
            col1, col2, col3 = st.columns(3)
            col1.metric(f"{selected_category} Avg Price", f"${cat_data['Price'].mean():.2f}")
            col2.metric(f"{selected_category} Avg Rating", f"{cat_data['Rating'].mean():.2f}")
            col3.metric(f"{selected_category} Products", len(cat_data))

        # Dataset View/Download
        st.markdown("### Dataset")
        col1, col2 = st.columns([1, 1])
        with col1:
            if st.checkbox("View Dataset", key="view_ch3_amazon"):
                st.dataframe(amazon.head(10))
        with col2:
            csv = amazon.to_csv(index=False).encode('utf-8')
            st.download_button(
                label="Download CSV",
                data=csv,
                file_name="amazon_data.csv",
                mime="text/csv",
                key="download_ch3_amazon"
            )

    with tab2:
        st.markdown("### Flashcards")

        cards = [
            ("What does correlation measure?",
             "<strong>Strength and direction of linear relationship</strong><br><br>Range: -1 to +1"),
            ("Correlation = 0 means what?",
             "<strong>No linear relationship</strong><br><br>But there could be non-linear relationships"),
            ("Difference between Pearson and Spearman?",
             "<strong>Pearson = linear, Spearman = monotonic</strong><br><br>Spearman is robust to outliers"),
            ("What does R² tell you?",
             "<strong>Proportion of variance explained</strong><br><br>R² = 0.64 means 64% of variance explained"),
            ("Does correlation imply causation?",
             "<strong>NO!</strong><br><br>Correlation does not prove one variable causes another"),
            ("What is a strong correlation?",
             "<strong>|r| ≥ 0.7</strong><br><br>Values close to -1 or +1"),
            ("When to use Spearman over Pearson?",
             "<strong>Ordinal data or outliers present</strong><br><br>Spearman uses ranks, not raw values"),
            ("What is the slope in regression?",
             "<strong>Change in Y per unit change in X</strong><br><br>β₁ in Y = β₀ + β₁X"),
            ("What is the intercept in regression?",
             "<strong>Value of Y when X = 0</strong><br><br>β₀ in Y = β₀ + β₁X"),
            ("What is a scatter plot used for?",
             "<strong>Visualize relationship between two variables</strong><br><br>Shows pattern, strength, direction"),
            ("What is negative correlation?",
             "<strong>As X increases, Y decreases</strong><br><br>r is negative (-1 to 0)"),
            ("What is Anscombe's Quartet?",
             "<strong>4 datasets with same stats, different patterns</strong><br><br>Shows importance of visualization"),
            ("What does covariance measure?",
             "<strong>Joint variability of two variables</strong><br><br>Cov(X,Y) = E[(X-μₓ)(Y-μᵧ)]"),
            ("How is Pearson's r calculated?",
             "<strong>r = Cov(X,Y) / (σₓ × σᵧ)</strong><br><br>Standardized covariance")
        ]

        # Grid layout: 3 columns
        num_cols = 3
        for i in range(0, len(cards), num_cols):
            cols = st.columns(num_cols)
            for j in range(num_cols):
                if i + j < len(cards):
                    with cols[j]:
                        q, a = cards[i + j]
                        render_flashcard(f"ch3_card{i+j+1}", q, a)

    with tab4:
        st.markdown("### Foundational Research Papers")

        research_paper_card(
            "Graphs in Statistical Analysis",
            "Francis J. Anscombe",
            "1973",
            "The American Statistician, 27(1), 17-21",
            "Created Anscombe's Quartet demonstrating that datasets with identical statistical properties can have vastly different distributions. Emphasized the importance of visualizing data before analyzing correlations.",
            "Anscombe, F. J. (1973). Graphs in statistical analysis. The American Statistician, 27(1), 17-21.",
            link="https://doi.org/10.1080/00031305.1973.10478966"
        )

        research_paper_card(
            "Regression Towards Mediocrity in Hereditary Stature",
            "Francis Galton",
            "1886",
            "The Journal of the Anthropological Institute of Great Britain and Ireland, 15, 246-263",
            "Discovered the phenomenon of regression to the mean and developed the fundamental concepts of correlation and regression analysis that form the basis of modern statistics.",
            "Galton, F. (1886). Regression towards mediocrity in hereditary stature. JRSS, 15, 246-263.",
            link="https://doi.org/10.2307/2841583"
        )

        research_paper_card(
            "The Probable Error of a Mean",
            "Student (W. S. Gosset)",
            "1908",
            "Biometrika, 6(1), 1-25",
            "Developed the t-distribution and t-test for small samples, enabling statistical inference about correlation and regression coefficients with limited data.",
            "Student. (1908). The probable error of a mean. Biometrika, 6(1), 1-25.",
            link="https://doi.org/10.1093/biomet/6.1.1"
        )

    # Navigation buttons
    st.markdown("---")
    render_navigation(chapter, chapters)

elif "4." in chapter:
    st.title("4. Probability")
    tab1, tab3, tab2, tab4 = st.tabs(["Concepts", "Flashcards", "Tesla Example", "Research Papers"])

    with tab1:
        st.markdown("""
        ### Basic Probability
        - P(A) = Number of favorable outcomes / Total outcomes
        - Range: 0 to 1
        - P(not A) = 1 - P(A)

        ### Conditional Probability
        P(A|B) = P(A and B) / P(B)

        Probability of A given B has occurred

        ### Bayes' Theorem
        P(A|B) = [P(B|A) × P(A)] / P(B)

        Updates probabilities based on new evidence

        ### Independence
        Two events A and B are independent if:
        - P(A and B) = P(A) × P(B)
        - P(A|B) = P(A)

        ### Expected Value
        E(X) = Σ [x × P(x)]

        Weighted average of all possible outcomes
        """)

        st.markdown("### Interactive Probability Calculator")

        st.markdown("**Conditional Probability: P(A|B)**")
        col1, col2 = st.columns(2)
        with col1:
            p_a = st.slider("P(A)", 0.0, 1.0, 0.3, 0.05)
            p_b = st.slider("P(B)", 0.0, 1.0, 0.4, 0.05)
        with col2:
            p_a_and_b = st.slider("P(A and B)", 0.0, min(p_a, p_b), min(p_a, p_b) * 0.8, 0.01)

        if p_b > 0:
            p_a_given_b = p_a_and_b / p_b
            p_b_given_a = p_a_and_b / p_a if p_a > 0 else 0

            col1, col2 = st.columns(2)
            col1.metric("P(A|B)", f"{p_a_given_b:.3f}")
            col2.metric("P(B|A)", f"{p_b_given_a:.3f}")

            st.markdown(f'<div class="insight">Given B occurred, the probability of A is {p_a_given_b:.1%}. Events are {"independent" if abs(p_a_given_b - p_a) < 0.01 else "dependent"}.</div>', unsafe_allow_html=True)

    with tab3:
        st.markdown('<div class="example-box"><h3>Tesla Insurance Risk Assessment</h3><p>Using probability to calculate insurance premiums based on driver behavior</p></div>', unsafe_allow_html=True)

        concept_connection_box(
            "Concept Connection: Conditional Probability and Bayes Theorem",
            "Tesla uses <strong>conditional probability</strong> to assess accident risk given driver behavior (speeding, hard braking). <strong>Bayes' Theorem</strong> updates risk assessments as new driving data is collected, enabling personalized insurance pricing."
        )

        st.markdown("### Interactive Risk Calculator")

        col1, col2 = st.columns(2)
        with col1:
            st.markdown("**Driver Characteristics**")
            age_group = st.selectbox("Age Group", ["16-25", "26-40", "41-60", "60+"])
            driving_score = st.slider("Driving Score (0-100)", 0, 100, 75, 5)
        with col2:
            st.markdown("**Behavior Factors**")
            speeding_freq = st.slider("Speeding Events/Month", 0, 20, 5, 1)
            hard_brake_freq = st.slider("Hard Braking Events/Month", 0, 30, 10, 1)

        # Calculate risk probabilities
        age_risk = {"16-25": 0.15, "26-40": 0.08, "41-60": 0.06, "60+": 0.10}
        base_risk = age_risk[age_group]

        behavior_factor = 1 + (speeding_freq * 0.02) + (hard_brake_freq * 0.01)
        score_factor = (100 - driving_score) / 100

        accident_risk = base_risk * behavior_factor * (1 + score_factor)
        accident_risk = min(accident_risk, 0.95)

        # Bayes' update simulation
        prior_risk = base_risk
        evidence_factor = behavior_factor * (1 + score_factor)
        posterior_risk = accident_risk

        col1, col2, col3 = st.columns(3)
        col1.metric("Base Risk (Age)", f"{prior_risk:.1%}")
        col2.metric("Updated Risk (Behavior)", f"{posterior_risk:.1%}")
        risk_increase = ((posterior_risk - prior_risk) / prior_risk * 100) if prior_risk > 0 else 0
        col3.metric("Risk Change", f"{risk_increase:+.0f}%")

        # Calculate premium
        base_premium = 1200
        premium = base_premium * (posterior_risk / 0.08)

        st.markdown(f'<div class="insight">Your estimated annual premium: <strong>${premium:.2f}</strong>. This is based on conditional probability P(Accident|Behavior) using Bayes theorem to update from base risk.</div>', unsafe_allow_html=True)

        # Probability tree visualization
        st.markdown("### Probability Tree")

        # Tree now updates dynamically based on slider inputs
        fig = go.Figure()

        # Level 1: Age
        fig.add_trace(go.Scatter(
            x=[0, 1], y=[1, 1],
            mode='lines+text',
            text=['', f'Age ({age_group}): {prior_risk:.1%}'],
            textposition='middle right',
            line=dict(color='blue', width=2)
        ))

        # Level 2: With risky behavior (uses actual calculated posterior_risk)
        fig.add_trace(go.Scatter(
            x=[1, 2], y=[1, 1.2],
            mode='lines+text',
            text=['', f'+ Risky Behavior: {posterior_risk:.1%}'],
            textposition='middle right',
            line=dict(color='red', width=2)
        ))

        # Level 2: Safe behavior (dynamically calculated)
        safe_risk = prior_risk * 0.5
        fig.add_trace(go.Scatter(
            x=[1, 2], y=[1, 0.8],
            mode='lines+text',
            text=['', f'+ Safe Behavior: {safe_risk:.1%}'],
            textposition='middle right',
            line=dict(color='green', width=2)
        ))

        fig.update_layout(
            title=f'Risk Probability Tree (Score: {driving_score}, Speeding: {speeding_freq}/mo, Braking: {hard_brake_freq}/mo)',
            showlegend=False,
            xaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
            yaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
            height=300
        )

        st.plotly_chart(fig, use_container_width=True)

        # Create sample dataset for Tesla insurance
        np.random.seed(42)
        num_drivers = 100
        tesla_data = pd.DataFrame({
            'Driver_ID': range(1, num_drivers + 1),
            'Age_Group': np.random.choice(['16-25', '26-40', '41-60', '60+'], num_drivers),
            'Driving_Score': np.random.randint(50, 100, num_drivers),
            'Speeding_Events_Per_Month': np.random.randint(0, 20, num_drivers),
            'Hard_Braking_Events_Per_Month': np.random.randint(0, 30, num_drivers)
        })
        # Calculate risk for each driver
        age_risk_map = {"16-25": 0.15, "26-40": 0.08, "41-60": 0.06, "60+": 0.10}
        tesla_data['Base_Risk'] = tesla_data['Age_Group'].map(age_risk_map)
        tesla_data['Behavior_Factor'] = 1 + (tesla_data['Speeding_Events_Per_Month'] * 0.02) + (tesla_data['Hard_Braking_Events_Per_Month'] * 0.01)
        tesla_data['Score_Factor'] = (100 - tesla_data['Driving_Score']) / 100
        tesla_data['Accident_Risk'] = (tesla_data['Base_Risk'] * tesla_data['Behavior_Factor'] * (1 + tesla_data['Score_Factor'])).clip(upper=0.95)
        tesla_data['Annual_Premium'] = (1200 * (tesla_data['Accident_Risk'] / 0.08)).round(2)

        # Dataset View/Download
        st.markdown("### Dataset")
        col1, col2 = st.columns([1, 1])
        with col1:
            if st.checkbox("View Dataset", key="view_ch4_tesla"):
                st.dataframe(tesla_data.head(10))
        with col2:
            csv = tesla_data.to_csv(index=False).encode('utf-8')
            st.download_button(
                label="Download CSV",
                data=csv,
                file_name="tesla_data.csv",
                mime="text/csv",
                key="download_ch4_tesla"
            )

    with tab2:
        st.markdown("### Flashcards")

        cards = [
            ("What is conditional probability?",
             "<strong>Probability of A given B occurred</strong><br><br>P(A|B) = P(A and B) / P(B)"),
            ("What does Bayes' Theorem do?",
             "<strong>Updates probabilities with new evidence</strong><br><br>P(A|B) = P(B|A) × P(A) / P(B)"),
            ("When are events independent?",
             "<strong>When P(A|B) = P(A)</strong><br><br>Also: P(A and B) = P(A) × P(B)"),
            ("What is expected value?",
             "<strong>Weighted average of outcomes</strong><br><br>E(X) = Σ [x × P(x)]"),
            ("Difference between P(A|B) and P(B|A)?",
             "<strong>Opposite conditional probabilities</strong><br><br>Usually NOT equal"),
            ("What is the complement rule?",
             "<strong>P(not A) = 1 - P(A)</strong><br><br>Probabilities sum to 1"),
            ("What does mutually exclusive mean?",
             "<strong>Events cannot both occur</strong><br><br>P(A and B) = 0"),
            ("When to use Bayes' Theorem?",
             "<strong>When updating beliefs with new evidence</strong><br><br>Medical tests, spam filters"),
            ("What is the multiplication rule?",
             "<strong>P(A and B) = P(A) × P(B|A)</strong><br><br>For dependent events"),
            ("What is the addition rule?",
             "<strong>P(A or B) = P(A) + P(B) - P(A and B)</strong><br><br>Avoids double counting"),
            ("What is prior probability?",
             "<strong>Initial belief before new evidence</strong><br><br>P(A) in Bayes' Theorem"),
            ("What is posterior probability?",
             "<strong>Updated belief after new evidence</strong><br><br>P(A|B) in Bayes' Theorem"),
            ("What is the law of total probability?",
             "<strong>P(A) = Σ P(A|Bᵢ) × P(Bᵢ)</strong><br><br>Sum over all partitions"),
            ("What is a probability distribution?",
             "<strong>Function showing all possible outcomes and probabilities</strong><br><br>All probabilities sum to 1")
        ]

        # Grid layout: 3 columns
        num_cols = 3
        for i in range(0, len(cards), num_cols):
            cols = st.columns(num_cols)
            for j in range(num_cols):
                if i + j < len(cards):
                    with cols[j]:
                        q, a = cards[i + j]
                        render_flashcard(f"ch4_card{i+j+1}", q, a)

    with tab4:
        st.markdown("### Foundational Research Papers")

        research_paper_card(
            "An Essay Towards Solving a Problem in the Doctrine of Chances",
            "Thomas Bayes & Richard Price",
            "1763",
            "Philosophical Transactions of the Royal Society of London, 53, 370-418",
            "Introduced Bayes' Theorem, establishing the foundation for updating probabilities based on new evidence. This theorem became fundamental to modern machine learning and AI.",
            "Bayes, T., & Price, R. (1763). An essay towards solving a problem in the doctrine of chances. PTRSL, 53, 370-418.",
            link="https://doi.org/10.1098/rstl.1763.0053"
        )

        research_paper_card(
            "A Philosophical Essay on Probabilities",
            "Pierre-Simon Laplace",
            "1814",
            "Translated from the 6th French edition by F. W. Truscott and F. L. Emory (1951)",
            "Formalized probability theory and developed mathematical foundations for conditional probability. Extended Bayes' work and applied it to scientific inference.",
            "Laplace, P. S. (1814). A philosophical essay on probabilities. Dover Publications.",
            link="https://archive.org/details/philosophicaless00lapliala"
        )

        research_paper_card(
            "Truth and Probability",
            "Bruno de Finetti",
            "1937",
            "Annales de l'Institut Henri Poincaré, 7(1), 1-68",
            "Developed the subjective interpretation of probability and the concept of exchangeability. Showed how probability can represent degree of belief and uncertainty.",
            "de Finetti, B. (1937). La prévision: ses lois logiques, ses sources subjectives. Annales, 7(1), 1-68.",
            link="https://doi.org/10.1214/aoms/1177730491"
        )

    # Navigation buttons
    st.markdown("---")
    render_navigation(chapter, chapters)

elif "5." in chapter:
    st.title("5. Statistical Distributions")
    tab1, tab3, tab2, tab4 = st.tabs(["Concepts", "Flashcards", "Call Center Example", "Research Papers"])

    with tab1:
        st.markdown("""
        ### Normal Distribution
        - Bell-shaped, symmetric
        - Mean = Median = Mode
        - 68% within ±1σ, 95% within ±2σ, 99.7% within ±3σ
        - Many natural phenomena follow normal distribution

        ### Binomial Distribution
        - Fixed number of trials (n)
        - Each trial: success or failure
        - Constant probability of success (p)
        - Discrete distribution
        - Example: Number of heads in 10 coin flips

        ### Poisson Distribution
        - Models count of events in fixed time/space
        - λ (lambda) = average rate
        - Discrete distribution
        - Example: Number of calls per hour

        ### Exponential Distribution
        - Time between events in Poisson process
        - Continuous distribution
        - Memoryless property
        - Example: Time until next customer arrives
        """)

        st.markdown("### Interactive Distribution Comparison")

        dist_choice = st.selectbox("Select Distribution",
                                   ["Normal", "Binomial", "Poisson", "Exponential"])

        if dist_choice == "Normal":
            col1, col2 = st.columns(2)
            with col1:
                mean = st.slider("Mean (μ)", -10.0, 10.0, 0.0, 0.5)
            with col2:
                std = st.slider("Standard Deviation (σ)", 0.5, 5.0, 1.0, 0.5)

            x = np.linspace(mean - 4*std, mean + 4*std, 1000)
            y = stats.norm.pdf(x, mean, std)

            fig = go.Figure()
            fig.add_trace(go.Scatter(x=x, y=y, fill='tozeroy', name='PDF'))
            fig.add_vline(x=mean, line_dash="dash", annotation_text="Mean")
            fig.add_vline(x=mean+std, line_dash="dot", annotation_text="+1σ")
            fig.add_vline(x=mean-std, line_dash="dot", annotation_text="-1σ")
            fig.update_layout(title=f'Normal Distribution (μ={mean}, σ={std})',
                            xaxis_title='Value', yaxis_title='Probability Density')
            st.plotly_chart(fig, use_container_width=True)

            st.markdown(f"""
            **68-95-99.7 Rule:**
            - 68% of data between {mean-std:.1f} and {mean+std:.1f}
            - 95% of data between {mean-2*std:.1f} and {mean+2*std:.1f}
            - 99.7% of data between {mean-3*std:.1f} and {mean+3*std:.1f}
            """)

        elif dist_choice == "Binomial":
            col1, col2 = st.columns(2)
            with col1:
                n_trials = st.slider("Number of Trials (n)", 1, 50, 20, 1)
            with col2:
                prob = st.slider("Success Probability (p)", 0.0, 1.0, 0.5, 0.05)

            x = np.arange(0, n_trials + 1)
            y = stats.binom.pmf(x, n_trials, prob)

            fig = px.bar(x=x, y=y, title=f'Binomial Distribution (n={n_trials}, p={prob})',
                        labels={'x': 'Number of Successes', 'y': 'Probability'})
            st.plotly_chart(fig, use_container_width=True)

            expected_value = n_trials * prob
            variance = n_trials * prob * (1 - prob)

            col1, col2 = st.columns(2)
            col1.metric("Expected Value", f"{expected_value:.2f}")
            col2.metric("Standard Deviation", f"{np.sqrt(variance):.2f}")

        elif dist_choice == "Poisson":
            lambda_val = st.slider("Average Rate (λ)", 0.5, 20.0, 5.0, 0.5)

            x = np.arange(0, int(lambda_val * 3) + 10)
            y = stats.poisson.pmf(x, lambda_val)

            fig = px.bar(x=x, y=y, title=f'Poisson Distribution (λ={lambda_val})',
                        labels={'x': 'Number of Events', 'y': 'Probability'})
            st.plotly_chart(fig, use_container_width=True)

            st.markdown(f"""
            **Distribution Properties:**
            - Mean = {lambda_val}
            - Variance = {lambda_val}
            - Standard Deviation = {np.sqrt(lambda_val):.2f}
            - Most likely value: {int(lambda_val)}
            """)

        else:  # Exponential
            lambda_val = st.slider("Rate Parameter (λ)", 0.1, 5.0, 1.0, 0.1)

            x = np.linspace(0, 10/lambda_val, 1000)
            y = stats.expon.pdf(x, scale=1/lambda_val)

            fig = go.Figure()
            fig.add_trace(go.Scatter(x=x, y=y, fill='tozeroy', name='PDF'))
            fig.update_layout(title=f'Exponential Distribution (λ={lambda_val})',
                            xaxis_title='Time', yaxis_title='Probability Density')
            st.plotly_chart(fig, use_container_width=True)

            mean_time = 1 / lambda_val
            st.markdown(f"""
            **Distribution Properties:**
            - Mean time between events = {mean_time:.2f}
            - Memoryless property: P(X > s+t | X > s) = P(X > t)
            """)

    with tab3:
        st.markdown('<div class="example-box"><h3>Call Center Operations</h3><p>Using statistical distributions to optimize staffing and service levels</p></div>', unsafe_allow_html=True)

        concept_connection_box(
            "Concept Connection: Poisson and Exponential Distributions",
            "Call centers use <strong>Poisson distribution</strong> to model the number of incoming calls per hour, and <strong>Exponential distribution</strong> to model time between calls. This enables optimal staffing decisions and service level predictions."
        )

        st.markdown("### Interactive Call Center Simulator")

        col1, col2 = st.columns(2)
        with col1:
            avg_calls_per_hour = st.slider("Average Calls per Hour (λ)", 10, 200, 60, 10)
        with col2:
            simulation_hours = st.slider("Simulation Duration (hours)", 1, 24, 8, 1)

        # Poisson: Number of calls per hour
        hours = np.arange(simulation_hours)
        calls_per_hour = np.random.poisson(avg_calls_per_hour, simulation_hours)

        # Exponential: Time between calls
        num_calls = int(avg_calls_per_hour * simulation_hours)
        inter_arrival_times = np.random.exponential(60/avg_calls_per_hour, num_calls)  # in minutes

        col1, col2 = st.columns(2)
        with col1:
            fig = px.bar(x=hours, y=calls_per_hour,
                        title=f'Calls per Hour (Poisson Distribution)',
                        labels={'x': 'Hour', 'y': 'Number of Calls'})
            fig.add_hline(y=avg_calls_per_hour, line_dash="dash",
                         annotation_text="Expected Average", line_color="red")
            st.plotly_chart(fig, use_container_width=True)

        with col2:
            fig = px.histogram(inter_arrival_times[:200], nbins=30,
                             title='Time Between Calls (Exponential)',
                             labels={'value': 'Minutes', 'count': 'Frequency'})
            expected_time = 60 / avg_calls_per_hour
            fig.add_vline(x=expected_time, line_dash="dash",
                         annotation_text="Mean Time", line_color="red")
            st.plotly_chart(fig, use_container_width=True)

        col1, col2, col3, col4 = st.columns(4)
        col1.metric("Total Calls", f"{calls_per_hour.sum()}")
        col2.metric("Peak Hour Calls", f"{calls_per_hour.max()}")
        col3.metric("Avg Time Between Calls", f"{inter_arrival_times.mean():.1f} min")
        col4.metric("Std Dev", f"{inter_arrival_times.std():.1f} min")

        st.markdown(f'<div class="insight">Expected calls per hour: {avg_calls_per_hour}. Actual average: {calls_per_hour.mean():.1f}. Mean time between calls: {60/avg_calls_per_hour:.2f} minutes.</div>', unsafe_allow_html=True)

        # Staffing calculator
        st.markdown("### Staffing Calculator")
        service_level_target = st.slider("Target Service Level (%)", 80, 99, 95, 1)

        # Simple staffing formula (Erlang C approximation)
        calls_per_agent = 15  # assumption
        required_agents = int(np.ceil(avg_calls_per_hour / calls_per_agent * (100 / service_level_target)))

        col1, col2 = st.columns(2)
        col1.metric("Recommended Agents", required_agents)
        col2.metric("Calls per Agent", f"{avg_calls_per_hour / required_agents:.1f}")

        # Create sample dataset for Call Center
        call_center_data = pd.DataFrame({
            'Hour': hours,
            'Calls_Received': calls_per_hour,
            'Expected_Calls': avg_calls_per_hour,
            'Variance_From_Expected': calls_per_hour - avg_calls_per_hour
        })

        # Dataset View/Download
        st.markdown("### Dataset")
        col1, col2 = st.columns([1, 1])
        with col1:
            if st.checkbox("View Dataset", key="view_ch5_callcenter"):
                st.dataframe(call_center_data.head(10))
        with col2:
            csv = call_center_data.to_csv(index=False).encode('utf-8')
            st.download_button(
                label="Download CSV",
                data=csv,
                file_name="call_center_data.csv",
                mime="text/csv",
                key="download_ch5_callcenter"
            )

    with tab2:
        st.markdown("### Flashcards")

        cards = [
            ("What is the 68-95-99.7 rule?",
             "<strong>Normal distribution percentages</strong><br><br>68% within ±1σ, 95% within ±2σ, 99.7% within ±3σ"),
            ("When to use Binomial distribution?",
             "<strong>Fixed trials, binary outcomes</strong><br><br>Each trial independent with constant probability"),
            ("When to use Poisson distribution?",
             "<strong>Count events in fixed interval</strong><br><br>Calls per hour, defects per batch"),
            ("What is the memoryless property?",
             "<strong>Past does not affect future waiting time</strong><br><br>Exponential distribution property"),
            ("Difference between Poisson and Exponential?",
             "<strong>Poisson counts events, Exponential measures time</strong><br><br>Related: if events are Poisson, time is Exponential"),
            ("What is lambda (λ) in Poisson?",
             "<strong>Average rate of events</strong><br><br>Mean = Variance = λ"),
            ("When does Binomial approximate Normal?",
             "<strong>Large n and p near 0.5</strong><br><br>Rule of thumb: np > 5 and n(1-p) > 5"),
            ("What does standard deviation tell you?",
             "<strong>Spread of distribution</strong><br><br>Larger σ means more variability"),
            ("What is the Central Limit Theorem?",
             "<strong>Sample means approach normal distribution</strong><br><br>Works for large n, regardless of population distribution"),
            ("What is a Z-score used for?",
             "<strong>Standardize values to standard normal</strong><br><br>Z = (X - μ) / σ"),
            ("What is the mean of standard normal?",
             "<strong>μ = 0, σ = 1</strong><br><br>Z-scores follow this distribution"),
            ("What is a continuous distribution?",
             "<strong>Can take any value in a range</strong><br><br>Normal, Exponential, Uniform"),
            ("What is a discrete distribution?",
             "<strong>Can only take specific values</strong><br><br>Binomial, Poisson, Geometric"),
            ("What is the variance of Binomial?",
             "<strong>Var(X) = n × p × (1-p)</strong><br><br>n = trials, p = success probability")
        ]

        # Grid layout: 3 columns
        num_cols = 3
        for i in range(0, len(cards), num_cols):
            cols = st.columns(num_cols)
            for j in range(num_cols):
                if i + j < len(cards):
                    with cols[j]:
                        q, a = cards[i + j]
                        render_flashcard(f"ch5_card{i+j+1}", q, a)

    with tab4:
        st.markdown("### Foundational Research Papers")

        research_paper_card(
            "The Doctrine of Chances",
            "Abraham de Moivre",
            "1738",
            "3rd Edition, London",
            "First description of the normal distribution (Gaussian curve) and the central limit theorem. Showed that binomial distribution approaches normal distribution for large n.",
            "de Moivre, A. (1738). The Doctrine of Chances. 3rd ed. London.",
            link="https://archive.org/details/doctrineofchance00moiv"
        )

        research_paper_card(
            "Recherches sur la probabilité des jugements",
            "Siméon Denis Poisson",
            "1837",
            "Bachelier, Paris",
            "Introduced the Poisson distribution for modeling rare events. Showed how it emerges as a limit of binomial distribution when n is large and p is small.",
            "Poisson, S. D. (1837). Recherches sur la probabilité des jugements. Bachelier.",
            link="https://gallica.bnf.fr/ark:/12148/bpt6k110193z"
        )

        research_paper_card(
            "Theoria Motus Corporum Coelestium",
            "Carl Friedrich Gauss",
            "1809",
            "Hamburg: Friedrich Perthes and Johann Heinrich Besser",
            "Formalized the normal distribution (Gaussian distribution) and method of least squares. Proved the central limit theorem for errors in astronomical observations.",
            "Gauss, C. F. (1809). Theoria motus corporum coelestium. Hamburg: Perthes et Besser.",
            link="https://archive.org/details/bub_gb_ORUOAAAAQAAJ"
        )

    # Navigation buttons
    st.markdown("---")
    render_navigation(chapter, chapters)

elif "6." in chapter:
    st.title("6. Decision Making")
    tab1, tab3, tab2, tab4 = st.tabs(["Concepts", "Flashcards", "Startup Example", "Research Papers"])

    with tab1:
        st.markdown("""
        ### Expected Monetary Value (EMV)
        EMV = Σ [Probability × Payoff]

        Choose option with highest EMV

        ### Decision Trees
        Visual framework for sequential decisions
        1. Square nodes = Decisions
        2. Circle nodes = Chance events
        3. Calculate EMV backwards from end

        ### Risk vs Uncertainty
        - **Risk**: Known probabilities
        - **Uncertainty**: Unknown probabilities

        ### Decision Criteria
        - **Maximax**: Optimist (best of best)
        - **Maximin**: Pessimist (best of worst)
        - **Minimax Regret**: Minimize maximum regret
        - **EMV**: Expected value (requires probabilities)
        """)

        st.markdown("### Interactive Decision Analyzer")

        st.markdown("**Simple Investment Decision**")

        col1, col2 = st.columns(2)
        with col1:
            investment_amount = st.number_input("Investment Amount ($)", 1000, 1000000, 50000, 1000)
            success_prob = st.slider("Probability of Success", 0.0, 1.0, 0.6, 0.05)
        with col2:
            success_return = st.number_input("Return if Successful ($)", 0, 5000000, 200000, 10000)
            failure_return = st.number_input("Return if Failed ($)", -1000000, 0, -30000, 1000)

        # Calculate EMV
        emv = success_prob * success_return + (1 - success_prob) * failure_return
        net_emv = emv - investment_amount

        # Create decision tree visualization
        fig = go.Figure()

        # Decision node
        fig.add_trace(go.Scatter(
            x=[0], y=[0],
            mode='markers+text',
            marker=dict(size=20, color='blue', symbol='square'),
            text=['Invest?'],
            textposition='top center'
        ))

        # Chance node
        fig.add_trace(go.Scatter(
            x=[1, 1], y=[0.5, -0.5],
            mode='markers',
            marker=dict(size=15, color='orange', symbol='circle')
        ))

        # Outcomes
        fig.add_trace(go.Scatter(
            x=[2, 2], y=[0.5, -0.5],
            mode='markers+text',
            marker=dict(size=10, color='green'),
            text=[f'Success<br>${success_return:,}', f'Failure<br>${failure_return:,}'],
            textposition='middle right'
        ))

        # Lines
        fig.add_trace(go.Scatter(x=[0, 1], y=[0, 0.5], mode='lines', line=dict(color='black')))
        fig.add_trace(go.Scatter(x=[0, 1], y=[0, -0.5], mode='lines', line=dict(color='black')))
        fig.add_trace(go.Scatter(x=[1, 2], y=[0.5, 0.5], mode='lines+text',
                                line=dict(color='black'),
                                text=[f'{success_prob:.0%}', ''],
                                textposition='top center'))
        fig.add_trace(go.Scatter(x=[1, 2], y=[-0.5, -0.5], mode='lines+text',
                                line=dict(color='black'),
                                text=[f'{1-success_prob:.0%}', ''],
                                textposition='bottom center'))

        fig.update_layout(
            title='Decision Tree',
            showlegend=False,
            xaxis=dict(showgrid=False, zeroline=False, showticklabels=False, range=[-0.5, 3]),
            yaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
            height=400
        )

        st.plotly_chart(fig, use_container_width=True)

        col1, col2, col3 = st.columns(3)
        col1.metric("EMV (Gross)", f"${emv:,.0f}")
        col2.metric("Investment", f"-${investment_amount:,}")
        col3.metric("Net EMV", f"${net_emv:,.0f}", delta=f"{'Invest' if net_emv > 0 else 'Do Not Invest'}")

        if net_emv > 0:
            st.markdown(f'<div class="insight">Decision: INVEST. The expected value (${emv:,}) exceeds the investment cost (${investment_amount:,}) by ${net_emv:,}.</div>', unsafe_allow_html=True)
        else:
            st.markdown(f'<div class="insight">Decision: DO NOT INVEST. The expected value (${emv:,}) is less than the investment cost (${investment_amount:,}).</div>', unsafe_allow_html=True)

    with tab3:
        st.markdown('<div class="example-box"><h3>Startup Product Launch Decision</h3><p>Using EMV analysis to decide whether to launch a new product</p></div>', unsafe_allow_html=True)

        concept_connection_box(
            "Concept Connection: Expected Monetary Value and Decision Trees",
            "Startups use <strong>EMV analysis</strong> to evaluate product launch decisions under uncertainty. <strong>Decision trees</strong> help visualize different scenarios (market success, moderate success, failure) and calculate expected returns. This quantitative approach reduces bias in high-stakes decisions."
        )

        st.markdown("### Interactive Product Launch Analyzer")

        col1, col2 = st.columns(2)
        with col1:
            st.markdown("**Development Costs**")
            dev_cost = st.number_input("Development Cost ($)", 10000, 1000000, 200000, 10000)
            marketing_cost = st.number_input("Marketing Cost ($)", 10000, 500000, 100000, 10000)
        with col2:
            st.markdown("**Market Scenarios**")
            prob_success = st.slider("Probability: High Success", 0.0, 1.0, 0.3, 0.05)
            prob_moderate = st.slider("Probability: Moderate Success", 0.0, 1.0, 0.4, 0.05)
            prob_failure = max(0, 1 - prob_success - prob_moderate)
            st.metric("Probability: Failure", f"{prob_failure:.0%}")

        col1, col2, col3 = st.columns(3)
        with col1:
            revenue_high = st.number_input("Revenue: High Success ($)", 100000, 5000000, 1000000, 50000)
        with col2:
            revenue_moderate = st.number_input("Revenue: Moderate ($)", 50000, 2000000, 400000, 25000)
        with col3:
            revenue_low = st.number_input("Revenue: Failure ($)", 0, 500000, 50000, 10000)

        # Calculate EMV
        total_cost = dev_cost + marketing_cost

        profit_high = revenue_high - total_cost
        profit_moderate = revenue_moderate - total_cost
        profit_low = revenue_low - total_cost

        emv_launch = (prob_success * profit_high +
                     prob_moderate * profit_moderate +
                     prob_failure * profit_low)

        emv_no_launch = 0  # No cost, no revenue

        # Visualization
        scenarios = ['High Success', 'Moderate', 'Failure']
        probabilities = [prob_success, prob_moderate, prob_failure]
        revenues = [revenue_high, revenue_moderate, revenue_low]
        profits = [profit_high, profit_moderate, profit_low]

        col1, col2 = st.columns(2)
        with col1:
            fig = px.bar(x=scenarios, y=probabilities, title='Scenario Probabilities',
                        labels={'x': 'Scenario', 'y': 'Probability'},
                        color=probabilities, color_continuous_scale='RdYlGn')
            fig.update_layout(showlegend=False)
            st.plotly_chart(fig, use_container_width=True)
        with col2:
            fig = px.bar(x=scenarios, y=profits, title='Profit by Scenario',
                        labels={'x': 'Scenario', 'y': 'Profit ($)'},
                        color=profits, color_continuous_scale='RdYlGn')
            fig.update_layout(showlegend=False)
            st.plotly_chart(fig, use_container_width=True)

        col1, col2, col3, col4 = st.columns(4)
        col1.metric("Total Investment", f"${total_cost:,}")
        col2.metric("EMV (Launch)", f"${emv_launch:,.0f}")
        col3.metric("EMV (No Launch)", f"${emv_no_launch:,}")
        col4.metric("Decision", "LAUNCH" if emv_launch > emv_no_launch else "DO NOT LAUNCH",
                   delta=f"${abs(emv_launch - emv_no_launch):,.0f}")

        if emv_launch > 0:
            roi = (emv_launch / total_cost) * 100
            st.markdown(f'<div class="insight">Decision: LAUNCH the product. Expected profit: ${emv_launch:,.0f}. Expected ROI: {roi:.1f}%.</div>', unsafe_allow_html=True)
        else:
            st.markdown(f'<div class="insight">Decision: DO NOT LAUNCH. Expected loss: ${abs(emv_launch):,.0f}. The expected value is negative.</div>', unsafe_allow_html=True)

        # Sensitivity analysis
        st.markdown("### Sensitivity Analysis")
        st.markdown("How does changing success probability affect EMV?")

        prob_range = np.linspace(0, 1-prob_failure, 50)
        emv_range = []
        for p in prob_range:
            emv = (p * profit_high +
                  (1 - prob_failure - p) * profit_moderate +
                  prob_failure * profit_low)
            emv_range.append(emv)

        fig = go.Figure()
        fig.add_trace(go.Scatter(x=prob_range, y=emv_range, mode='lines', name='EMV'))
        fig.add_hline(y=0, line_dash="dash", line_color="red", annotation_text="Break-even")
        fig.add_vline(x=prob_success, line_dash="dot", line_color="blue",
                     annotation_text="Current Estimate")
        fig.update_layout(title='EMV Sensitivity to Success Probability',
                         xaxis_title='Probability of High Success',
                         yaxis_title='Expected Profit ($)')
        st.plotly_chart(fig, use_container_width=True)

        # Create sample dataset for Startup decisions
        startup_data = pd.DataFrame({
            'Scenario': scenarios,
            'Probability': probabilities,
            'Revenue': revenues,
            'Total_Cost': [total_cost] * 3,
            'Profit': profits,
            'Weighted_Profit': [p * pr for p, pr in zip(probabilities, profits)]
        })

        # Dataset View/Download
        st.markdown("### Dataset")
        col1, col2 = st.columns([1, 1])
        with col1:
            if st.checkbox("View Dataset", key="view_ch6_startup"):
                st.dataframe(startup_data)
        with col2:
            csv = startup_data.to_csv(index=False).encode('utf-8')
            st.download_button(
                label="Download CSV",
                data=csv,
                file_name="startup_decision_data.csv",
                mime="text/csv",
                key="download_ch6_startup"
            )

    with tab2:
        st.markdown("### Flashcards")

        cards = [
            ("What is EMV?",
             "<strong>Expected Monetary Value</strong><br><br>Sum of (Probability × Payoff) for all outcomes"),
            ("How to use a decision tree?",
             "<strong>Calculate EMV backwards from right to left</strong><br><br>Start at outcomes, work back to decision"),
            ("Difference between risk and uncertainty?",
             "<strong>Risk has known probabilities</strong><br><br>Uncertainty has unknown probabilities"),
            ("What is the Maximax criterion?",
             "<strong>Choose best possible outcome</strong><br><br>Optimistic approach, ignores probabilities"),
            ("What is the Maximin criterion?",
             "<strong>Choose best of worst outcomes</strong><br><br>Pessimistic approach, conservative"),
            ("When to use EMV?",
             "<strong>When probabilities are known</strong><br><br>Quantitative decision making under risk"),
            ("What is opportunity cost?",
             "<strong>Value of next best alternative</strong><br><br>What you give up when making a choice"),
            ("What is regret in decision analysis?",
             "<strong>Difference between payoff and best payoff</strong><br><br>Minimax regret minimizes maximum regret"),
            ("What is sensitivity analysis?",
             "<strong>Test how changes in inputs affect decisions</strong><br><br>Identifies critical variables"),
            ("What is EVPI?",
             "<strong>Expected Value of Perfect Information</strong><br><br>Maximum you should pay for perfect forecast"),
            ("What is a payoff table?",
             "<strong>Matrix of outcomes for each action-state pair</strong><br><br>Rows = actions, Columns = states"),
            ("What is risk aversion?",
             "<strong>Preference for certain outcome over risky one</strong><br><br>Even if risky has higher EMV"),
            ("What is a decision node?",
             "<strong>Square node where decision maker chooses</strong><br><br>Choose path with highest EMV"),
            ("What is a chance node?",
             "<strong>Circle node representing uncertain events</strong><br><br>Calculate weighted average of paths")
        ]

        # Grid layout: 3 columns
        num_cols = 3
        for i in range(0, len(cards), num_cols):
            cols = st.columns(num_cols)
            for j in range(num_cols):
                if i + j < len(cards):
                    with cols[j]:
                        q, a = cards[i + j]
                        render_flashcard(f"ch6_card{i+j+1}", q, a)

    with tab4:
        st.markdown("### Foundational Research Papers")

        research_paper_card(
            "Applied Statistical Decision Theory",
            "Howard Raiffa & Robert Schlaifer",
            "1961",
            "Harvard Business School",
            "Formalized decision analysis combining probability theory with utility theory. Introduced decision trees and EMV analysis as standard business decision-making tools.",
            "Raiffa, H., & Schlaifer, R. (1961). Applied Statistical Decision Theory. Harvard Business School.",
            link="https://mitpress.mit.edu/9780262680134/"
        )

        research_paper_card(
            "Theory of Games and Economic Behavior",
            "John von Neumann & Oskar Morgenstern",
            "1944",
            "Princeton University Press",
            "Established the mathematical foundations of game theory and decision theory. Introduced the concept of expected utility maximization for rational decision making.",
            "von Neumann, J., & Morgenstern, O. (1944). Theory of Games and Economic Behavior. Princeton University Press.",
            link="https://archive.org/details/in.ernet.dli.2015.223148"
        )

        research_paper_card(
            "Prospect Theory: An Analysis of Decision Under Risk",
            "Daniel Kahneman & Amos Tversky",
            "1979",
            "Econometrica, 47(2), 263-291",
            "Showed how people actually make decisions under risk, deviating from expected utility theory. Introduced concepts of loss aversion and reference dependence.",
            "Kahneman, D., & Tversky, A. (1979). Prospect theory: An analysis of decision under risk. Econometrica, 47(2), 263-291.",
            link="https://doi.org/10.2307/1914185"
        )

    # Navigation buttons
    st.markdown("---")
    render_navigation(chapter, chapters)

elif "7." in chapter:
    st.title("7. Sampling")
    tab1, tab3, tab2, tab4 = st.tabs(["Concepts", "Flashcards", "Election Polling Example", "Research Papers"])

    with tab1:
        st.markdown("""
        ### Sampling Methods
        **Random Sampling**
        - Each member has equal probability
        - Eliminates selection bias

        **Stratified Sampling**
        - Divide population into groups (strata)
        - Sample from each group proportionally

        **Cluster Sampling**
        - Divide into clusters, randomly select clusters
        - Sample all within selected clusters

        ### Central Limit Theorem
        For large sample size (n ≥ 30):
        - Sample mean distribution approaches normal
        - Mean of sample means = population mean
        - Standard error = σ / √n

        ### Confidence Intervals
        CI = x̄ ± (z × SE)

        Where:
        - x̄ = sample mean
        - z = z-score (1.96 for 95% confidence)
        - SE = standard error = σ / √n

        ### Sample Size Calculation
        n = (z × σ / E)²

        Where E = desired margin of error
        """)

        st.markdown("### Interactive Sampling Simulator")

        st.markdown("**Central Limit Theorem Demonstration**")

        col1, col2, col3 = st.columns(3)
        with col1:
            pop_dist = st.selectbox("Population Distribution",
                                   ["Normal", "Uniform", "Exponential", "Bimodal"])
        with col2:
            sample_size = st.slider("Sample Size (n)", 5, 200, 30, 5)
        with col3:
            num_samples = st.slider("Number of Samples", 100, 2000, 500, 100)

        # Generate population
        np.random.seed(42)
        if pop_dist == "Normal":
            population = np.random.normal(100, 20, 100000)
        elif pop_dist == "Uniform":
            population = np.random.uniform(60, 140, 100000)
        elif pop_dist == "Exponential":
            population = np.random.exponential(30, 100000) + 70
        else:  # Bimodal
            population = np.concatenate([np.random.normal(80, 10, 50000),
                                        np.random.normal(120, 10, 50000)])

        # Draw samples and calculate means
        sample_means = []
        for _ in range(num_samples):
            sample = np.random.choice(population, sample_size, replace=False)
            sample_means.append(np.mean(sample))

        sample_means = np.array(sample_means)

        col1, col2 = st.columns(2)
        with col1:
            fig = px.histogram(population[:5000], nbins=50, title='Population Distribution')
            fig.add_vline(x=population.mean(), line_dash="dash", line_color="red",
                         annotation_text=f"μ = {population.mean():.1f}")
            st.plotly_chart(fig, use_container_width=True)
        with col2:
            fig = px.histogram(sample_means, nbins=50, title='Distribution of Sample Means')
            fig.add_vline(x=sample_means.mean(), line_dash="dash", line_color="red",
                         annotation_text=f"Mean = {sample_means.mean():.1f}")
            st.plotly_chart(fig, use_container_width=True)

        theoretical_se = population.std() / np.sqrt(sample_size)
        actual_se = sample_means.std()

        col1, col2, col3, col4 = st.columns(4)
        col1.metric("Population Mean", f"{population.mean():.2f}")
        col2.metric("Sample Means Average", f"{sample_means.mean():.2f}")
        col3.metric("Theoretical SE", f"{theoretical_se:.2f}")
        col4.metric("Actual SE", f"{actual_se:.2f}")

        st.markdown(f'<div class="insight">Central Limit Theorem: Even from a {pop_dist.lower()} population, the distribution of sample means is approximately normal for n={sample_size}. The standard error decreases as √n increases.</div>', unsafe_allow_html=True)

        # Confidence Interval Calculator
        st.markdown("### Confidence Interval Calculator")

        col1, col2 = st.columns(2)
        with col1:
            confidence_level = st.selectbox("Confidence Level", ["90%", "95%", "99%"], index=1, key="ci_conf_level")
            ci_sample_size = st.slider("Sample Size", 10, 1000, 100, 10)
        with col2:
            sample_mean = st.number_input("Sample Mean", 0.0, 200.0, 100.0, 1.0)
            pop_std = st.number_input("Population Std Dev", 1.0, 100.0, 20.0, 1.0)

        z_scores = {"90%": 1.645, "95%": 1.96, "99%": 2.576}
        z = z_scores[confidence_level]

        se = pop_std / np.sqrt(ci_sample_size)
        margin_error = z * se
        ci_lower = sample_mean - margin_error
        ci_upper = sample_mean + margin_error

        col1, col2, col3 = st.columns(3)
        col1.metric("Standard Error", f"{se:.2f}")
        col2.metric("Margin of Error", f"±{margin_error:.2f}")
        col3.metric(f"{confidence_level} CI", f"[{ci_lower:.1f}, {ci_upper:.1f}]")

        st.markdown(f'<div class="insight">We are {confidence_level} confident that the true population mean lies between {ci_lower:.1f} and {ci_upper:.1f}.</div>', unsafe_allow_html=True)

    with tab3:
        st.markdown('<div class="example-box"><h3>Election Polling Analysis</h3><p>Using sampling and confidence intervals to predict election outcomes</p></div>', unsafe_allow_html=True)

        concept_connection_box(
            "Concept Connection: Sampling and Confidence Intervals",
            "Election polls use <strong>random sampling</strong> to estimate voter preferences. <strong>Confidence intervals</strong> quantify uncertainty in predictions. <strong>Sample size calculations</strong> determine how many voters to poll for desired accuracy. Understanding margin of error is critical for interpreting poll results."
        )

        st.markdown("### Interactive Election Poll Simulator")

        col1, col2 = st.columns(2)
        with col1:
            st.markdown("**Population Parameters**")
            true_support = st.slider("True Support for Candidate A (%)", 30, 70, 52, 1)
            total_voters = st.number_input("Total Voters (millions)", 1, 200, 150, 10)
        with col2:
            st.markdown("**Poll Design**")
            poll_size = st.slider("Poll Sample Size", 100, 5000, 1000, 100)
            conf_level = st.selectbox("Confidence Level", ["90%", "95%", "99%"], index=1, key="poll_conf_level")

        # Simulate poll
        np.random.seed(42)
        poll_results = np.random.binomial(1, true_support/100, poll_size)
        sample_support = poll_results.mean() * 100

        # Calculate confidence interval
        z_scores = {"90%": 1.645, "95%": 1.96, "99%": 2.576}
        z = z_scores[conf_level]

        # Standard error for proportion
        se_prop = np.sqrt((sample_support/100) * (1 - sample_support/100) / poll_size)
        margin_error = z * se_prop * 100

        ci_lower = sample_support - margin_error
        ci_upper = sample_support + margin_error

        # Visualize results
        fig = go.Figure()

        # Add bar for each candidate
        fig.add_trace(go.Bar(
            x=['Candidate A', 'Candidate B'],
            y=[sample_support, 100 - sample_support],
            error_y=dict(type='data', array=[margin_error, margin_error]),
            marker_color=['blue', 'red']
        ))

        fig.update_layout(
            title=f'Poll Results (n={poll_size}, {conf_level} CI)',
            yaxis_title='Support (%)',
            yaxis_range=[0, 100],
            showlegend=False
        )

        st.plotly_chart(fig, use_container_width=True)

        col1, col2, col3, col4 = st.columns(4)
        col1.metric("True Support", f"{true_support}%")
        col2.metric("Poll Result", f"{sample_support:.1f}%")
        col3.metric("Margin of Error", f"±{margin_error:.1f}%")
        col4.metric(f"{conf_level} CI", f"[{ci_lower:.1f}%, {ci_upper:.1f}%]")

        # Determine if poll accurately captured true value
        poll_accurate = ci_lower <= true_support <= ci_upper

        if poll_accurate:
            st.markdown(f'<div class="insight">The poll accurately captured the true support ({true_support}%) within the {conf_level} confidence interval [{ci_lower:.1f}%, {ci_upper:.1f}%]. Margin of error: ±{margin_error:.1f}%.</div>', unsafe_allow_html=True)
        else:
            st.markdown(f'<div class="insight">This particular poll missed the true value ({true_support}%). This happens {100-int(conf_level[:-1])}% of the time with {conf_level} confidence intervals. The estimated range is [{ci_lower:.1f}%, {ci_upper:.1f}%].</div>', unsafe_allow_html=True)

        # Sample size calculator
        st.markdown("### Required Sample Size Calculator")

        col1, col2 = st.columns(2)
        with col1:
            desired_margin = st.slider("Desired Margin of Error (%)", 1.0, 10.0, 3.0, 0.5)
        with col2:
            calc_conf = st.selectbox("Confidence Level ", ["90%", "95%", "99%"], index=1, key="calc_conf")

        z_calc = z_scores[calc_conf]
        # Worst case: p = 0.5
        required_n = int(np.ceil((z_calc / (desired_margin/100))**2 * 0.25))

        cost_per_survey = 5  # assumption
        total_cost = required_n * cost_per_survey

        col1, col2, col3 = st.columns(3)
        col1.metric("Required Sample Size", f"{required_n:,}")
        col2.metric("Est. Cost ($5/survey)", f"${total_cost:,}")
        col3.metric("% of Population", f"{required_n/(total_voters*1000000)*100:.4f}%")

        st.markdown(f'<div class="insight">To achieve ±{desired_margin}% margin of error with {calc_conf} confidence, you need {required_n:,} respondents. This is only {required_n/(total_voters*1000000)*100:.4f}% of the population!</div>', unsafe_allow_html=True)

        # Create sample dataset for Election polling
        election_data = pd.DataFrame({
            'Voter_ID': range(1, poll_size + 1),
            'Supports_Candidate_A': poll_results,
            'True_Population_Support': true_support,
            'Sample_Support_Pct': sample_support,
            'Confidence_Level': conf_level,
            'Margin_of_Error': margin_error,
            'CI_Lower': ci_lower,
            'CI_Upper': ci_upper
        })

        # Dataset View/Download
        st.markdown("### Dataset")
        col1, col2 = st.columns([1, 1])
        with col1:
            if st.checkbox("View Dataset", key="view_ch7_election"):
                st.dataframe(election_data.head(10))
        with col2:
            csv = election_data.to_csv(index=False).encode('utf-8')
            st.download_button(
                label="Download CSV",
                data=csv,
                file_name="election_poll_data.csv",
                mime="text/csv",
                key="download_ch7_election"
            )

    with tab2:
        st.markdown("### Flashcards")

        cards = [
            ("What is the Central Limit Theorem?",
             "<strong>Sample means approach normal distribution</strong><br><br>For n ≥ 30, regardless of population shape"),
            ("What is standard error?",
             "<strong>Standard deviation of sample means</strong><br><br>SE = σ / √n"),
            ("How to interpret 95% confidence interval?",
             "<strong>95% of intervals contain true mean</strong><br><br>NOT: 95% probability mean is in this specific interval"),
            ("How does sample size affect margin of error?",
             "<strong>Larger n → smaller margin of error</strong><br><br>Margin decreases by √n"),
            ("Difference between random and stratified sampling?",
             "<strong>Random = equal probability</strong><br><br>Stratified = sample from subgroups proportionally"),
            ("When to use cluster sampling?",
             "<strong>When population naturally grouped</strong><br><br>Schools, cities, hospitals"),
            ("What z-score for 95% confidence?",
             "<strong>z = 1.96</strong><br><br>90%: 1.645, 99%: 2.576"),
            ("How to reduce margin of error?",
             "<strong>Increase sample size</strong><br><br>To cut margin in half, quadruple sample size"),
            ("What is sampling bias?",
             "<strong>Non-random sampling creates systematic error</strong><br><br>Sample doesn't represent population"),
            ("What is margin of error formula?",
             "<strong>ME = z × (σ / √n)</strong><br><br>z depends on confidence level"),
            ("What is point estimate?",
             "<strong>Single value estimate of parameter</strong><br><br>Example: sample mean estimates population mean"),
            ("What is confidence level?",
             "<strong>Probability method captures true parameter</strong><br><br>95%, 90%, 99% are common"),
            ("What is systematic sampling?",
             "<strong>Select every kth element</strong><br><br>k = N/n where N is population, n is sample"),
            ("What is convenience sampling?",
             "<strong>Sample easy-to-reach subjects</strong><br><br>Introduces bias, not representative")
        ]

        # Grid layout: 3 columns
        num_cols = 3
        for i in range(0, len(cards), num_cols):
            cols = st.columns(num_cols)
            for j in range(num_cols):
                if i + j < len(cards):
                    with cols[j]:
                        q, a = cards[i + j]
                        render_flashcard(f"ch7_card{i+j+1}", q, a)

    with tab4:
        st.markdown("### Foundational Research Papers")

        research_paper_card(
            "On the Two Different Aspects of the Representative Method",
            "Jerzy Neyman",
            "1934",
            "Journal of the Royal Statistical Society, 97(4), 558-625",
            "Established the mathematical foundations of random sampling and confidence intervals. Proved that random sampling eliminates selection bias and quantified sampling error.",
            "Neyman, J. (1934). On the two different aspects of the representative method. JRSS, 97(4), 558-625.",
            link="https://doi.org/10.2307/2342192"
        )

        research_paper_card(
            "Theorie Analytique des Probabilités",
            "Pierre-Simon Laplace",
            "1812",
            "Courcier, Paris",
            "First statement of the Central Limit Theorem, showing that the sum of many independent random variables tends toward normal distribution regardless of the underlying distribution.",
            "Laplace, P. S. (1812). Théorie analytique des probabilités. Courcier.",
            link="https://gallica.bnf.fr/ark:/12148/bpt6k77596b"
        )

        research_paper_card(
            "Sampling Techniques",
            "William G. Cochran",
            "1977",
            "John Wiley & Sons, 3rd Edition",
            "Comprehensive treatment of sampling methods including stratified, cluster, and systematic sampling. Provided practical formulas for sample size determination and variance estimation.",
            "Cochran, W. G. (1977). Sampling Techniques. 3rd ed. New York: John Wiley & Sons.",
            link="https://archive.org/details/samplingtechniqu0000coch_t4e3"
        )

    # Navigation buttons
    st.markdown("---")
    render_navigation(chapter, chapters)

elif "8." in chapter:
    st.title("8. Hypothesis Testing")
    tab1, tab3, tab2, tab4 = st.tabs(["Concepts", "Flashcards", "A/B Testing Example", "Research Papers"])

    with tab1:
        st.markdown("""
        ### Hypothesis Testing Framework
        1. State hypotheses (H₀ and H₁)
        2. Choose significance level (α)
        3. Calculate test statistic
        4. Determine p-value
        5. Make decision: reject or fail to reject H₀

        ### Hypotheses
        - **H₀** (Null): No effect, no difference
        - **H₁** (Alternative): There is an effect/difference

        ### Significance Level (α)
        - Typically α = 0.05 (5%)
        - Probability of Type I error
        - Rejecting H₀ when it's actually true

        ### P-value
        Probability of observing data this extreme if H₀ is true
        - p < α: Reject H₀ (statistically significant)
        - p ≥ α: Fail to reject H₀ (not significant)

        ### Types of Errors
        - **Type I Error (α)**: Reject true H₀ (false positive)
        - **Type II Error (β)**: Fail to reject false H₀ (false negative)
        - **Power**: 1 - β (probability of detecting true effect)

        ### Common Tests
        - **t-test**: Compare means (small samples)
        - **z-test**: Compare means (large samples)
        - **Chi-square**: Test independence (categorical)
        - **ANOVA**: Compare multiple groups
        """)

        st.markdown("### Interactive Hypothesis Testing")

        st.markdown("**Two-Sample t-test Simulator**")

        col1, col2 = st.columns(2)
        with col1:
            st.markdown("**Group A**")
            mean_a = st.slider("Mean A", 0.0, 100.0, 50.0, 1.0)
            std_a = st.slider("Std Dev A", 5.0, 30.0, 15.0, 1.0)
            n_a = st.slider("Sample Size A", 10, 500, 100, 10)
        with col2:
            st.markdown("**Group B**")
            mean_b = st.slider("Mean B", 0.0, 100.0, 55.0, 1.0)
            std_b = st.slider("Std Dev B", 5.0, 30.0, 15.0, 1.0)
            n_b = st.slider("Sample Size B", 10, 500, 100, 10)

        alpha_level = st.select_slider("Significance Level (α)",
                                      options=[0.01, 0.05, 0.10], value=0.05)

        # Generate samples
        np.random.seed(42)
        sample_a = np.random.normal(mean_a, std_a, n_a)
        sample_b = np.random.normal(mean_b, std_b, n_b)

        # Perform t-test
        t_stat, p_value = stats.ttest_ind(sample_a, sample_b)

        # Visualization
        col1, col2 = st.columns(2)
        with col1:
            fig = go.Figure()
            fig.add_trace(go.Histogram(x=sample_a, name='Group A', opacity=0.7,
                                      marker_color='blue', nbinsx=30))
            fig.add_trace(go.Histogram(x=sample_b, name='Group B', opacity=0.7,
                                      marker_color='red', nbinsx=30))
            fig.update_layout(title='Distribution Comparison', barmode='overlay',
                            xaxis_title='Value', yaxis_title='Frequency')
            st.plotly_chart(fig, use_container_width=True)
        with col2:
            fig = go.Figure()
            fig.add_trace(go.Box(y=sample_a, name='Group A', marker_color='blue'))
            fig.add_trace(go.Box(y=sample_b, name='Group B', marker_color='red'))
            fig.update_layout(title='Box Plot Comparison', yaxis_title='Value')
            st.plotly_chart(fig, use_container_width=True)

        col1, col2, col3, col4 = st.columns(4)
        col1.metric("Sample Mean A", f"{sample_a.mean():.2f}")
        col2.metric("Sample Mean B", f"{sample_b.mean():.2f}")
        col3.metric("t-statistic", f"{t_stat:.3f}")
        col4.metric("p-value", f"{p_value:.4f}")

        # Decision
        reject_null = p_value < alpha_level

        if reject_null:
            st.markdown(f'<div class="insight">Decision: REJECT H₀. The p-value ({p_value:.4f}) is less than α ({alpha_level}). There is statistically significant evidence that Group A and Group B have different means.</div>', unsafe_allow_html=True)
        else:
            st.markdown(f'<div class="insight">Decision: FAIL TO REJECT H₀. The p-value ({p_value:.4f}) is greater than α ({alpha_level}). There is not enough evidence to conclude the groups are different.</div>', unsafe_allow_html=True)

        # Effect size (Cohen's d)
        pooled_std = np.sqrt(((n_a-1)*std_a**2 + (n_b-1)*std_b**2) / (n_a + n_b - 2))
        cohens_d = abs(sample_a.mean() - sample_b.mean()) / pooled_std

        if cohens_d < 0.2:
            effect_label = "Negligible"
        elif cohens_d < 0.5:
            effect_label = "Small"
        elif cohens_d < 0.8:
            effect_label = "Medium"
        else:
            effect_label = "Large"

        col1, col2 = st.columns(2)
        col1.metric("Cohen's d (Effect Size)", f"{cohens_d:.3f}")
        col2.metric("Effect Size Interpretation", effect_label)

    with tab3:
        st.markdown('<div class="example-box"><h3>Website A/B Testing</h3><p>Testing whether a new website design improves conversion rate</p></div>', unsafe_allow_html=True)

        concept_connection_box(
            "Concept Connection: Hypothesis Testing and Statistical Significance",
            "A/B testing uses <strong>hypothesis testing</strong> to determine if design changes significantly improve metrics. <strong>P-values</strong> quantify whether observed differences are due to the change or random chance. Understanding <strong>Type I and Type II errors</strong> helps balance sensitivity and specificity in decision making."
        )

        st.markdown("### Interactive A/B Test Analyzer")

        col1, col2 = st.columns(2)
        with col1:
            st.markdown("**Version A (Control)**")
            visitors_a = st.number_input("Visitors A", 100, 100000, 10000, 1000)
            conv_rate_a = st.slider("Conversion Rate A (%)", 1.0, 20.0, 5.0, 0.1)
        with col2:
            st.markdown("**Version B (Treatment)**")
            visitors_b = st.number_input("Visitors B", 100, 100000, 10000, 1000)
            conv_rate_b = st.slider("Conversion Rate B (%)", 1.0, 20.0, 6.0, 0.1)

        sig_level = st.select_slider("Significance Level",
                                     options=[0.01, 0.05, 0.10], value=0.05)

        # Calculate conversions
        conversions_a = int(visitors_a * conv_rate_a / 100)
        conversions_b = int(visitors_b * conv_rate_b / 100)

        # Calculate sample proportions
        p_a = conversions_a / visitors_a
        p_b = conversions_b / visitors_b

        # Pooled proportion for z-test
        p_pooled = (conversions_a + conversions_b) / (visitors_a + visitors_b)

        # Standard error
        se = np.sqrt(p_pooled * (1 - p_pooled) * (1/visitors_a + 1/visitors_b))

        # Z-statistic
        z_stat = (p_b - p_a) / se if se > 0 else 0

        # P-value (two-tailed)
        p_value = 2 * (1 - stats.norm.cdf(abs(z_stat)))

        # Visualize results
        fig = go.Figure()

        versions = ['Version A<br>(Control)', 'Version B<br>(Treatment)']
        rates = [p_a * 100, p_b * 100]
        colors = ['blue', 'red']

        fig.add_trace(go.Bar(
            x=versions,
            y=rates,
            marker_color=colors,
            text=[f'{r:.2f}%' for r in rates],
            textposition='outside'
        ))

        fig.update_layout(
            title=f'Conversion Rate Comparison',
            yaxis_title='Conversion Rate (%)',
            yaxis_range=[0, max(rates) * 1.2],
            showlegend=False
        )

        st.plotly_chart(fig, use_container_width=True)

        col1, col2, col3, col4 = st.columns(4)
        col1.metric("Conversion A", f"{p_a*100:.2f}%", f"{conversions_a:,} / {visitors_a:,}")
        col2.metric("Conversion B", f"{p_b*100:.2f}%", f"{conversions_b:,} / {visitors_b:,}")
        col3.metric("z-statistic", f"{z_stat:.3f}")
        col4.metric("p-value", f"{p_value:.4f}")

        # Decision
        is_significant = p_value < sig_level
        lift = ((p_b - p_a) / p_a * 100) if p_a > 0 else 0

        if is_significant:
            if p_b > p_a:
                st.markdown(f'<div class="insight">Decision: Version B WINS. The improvement is statistically significant (p = {p_value:.4f} < {sig_level}). Relative lift: {lift:+.1f}%. Implement Version B.</div>', unsafe_allow_html=True)
            else:
                st.markdown(f'<div class="insight">Decision: Version A WINS. Version B performs significantly worse (p = {p_value:.4f} < {sig_level}). Relative change: {lift:+.1f}%. Keep Version A.</div>', unsafe_allow_html=True)
        else:
            st.markdown(f'<div class="insight">Decision: NO CLEAR WINNER. The difference is not statistically significant (p = {p_value:.4f} ≥ {sig_level}). Need more data or the difference may not be meaningful. Observed lift: {lift:+.1f}%.</div>', unsafe_allow_html=True)

        # Additional metrics
        st.markdown("### Test Metrics")

        # Confidence interval for difference
        ci_z = 1.96  # 95% CI
        se_diff = np.sqrt(p_a*(1-p_a)/visitors_a + p_b*(1-p_b)/visitors_b)
        diff = p_b - p_a
        ci_lower = (diff - ci_z * se_diff) * 100
        ci_upper = (diff + ci_z * se_diff) * 100

        col1, col2, col3 = st.columns(3)
        col1.metric("Absolute Difference", f"{diff*100:+.2f}%")
        col2.metric("Relative Lift", f"{lift:+.1f}%")
        col3.metric("95% CI for Difference", f"[{ci_lower:.2f}%, {ci_upper:.2f}%]")

        # Revenue impact (example)
        avg_order_value = st.number_input("Average Order Value ($)", 10, 1000, 100, 10)

        revenue_a = conversions_a * avg_order_value
        revenue_b = conversions_b * avg_order_value
        revenue_diff = revenue_b - revenue_a

        annual_visitors = st.number_input("Annual Visitors", 10000, 10000000, 1000000, 100000)
        annual_impact = (p_b - p_a) * annual_visitors * avg_order_value

        col1, col2 = st.columns(2)
        col1.metric("Revenue Impact (Test Period)", f"${revenue_diff:,.0f}")
        col2.metric("Projected Annual Impact", f"${annual_impact:,.0f}")

        st.markdown(f'<div class="insight">If implemented, Version B could generate an additional ${annual_impact:,.0f} annually based on {annual_visitors:,} visitors and ${avg_order_value} average order value.</div>', unsafe_allow_html=True)

        # Create sample dataset for A/B testing
        ab_test_data = pd.DataFrame({
            'Version': ['A (Control)', 'B (Treatment)'],
            'Visitors': [visitors_a, visitors_b],
            'Conversions': [conversions_a, conversions_b],
            'Conversion_Rate_Pct': [p_a * 100, p_b * 100],
            'Revenue': [revenue_a, revenue_b],
            'Z_Statistic': [z_stat, z_stat],
            'P_Value': [p_value, p_value],
            'Significant': [is_significant, is_significant],
            'Relative_Lift_Pct': [0, lift]
        })

        # Dataset View/Download
        st.markdown("### Dataset")
        col1, col2 = st.columns([1, 1])
        with col1:
            if st.checkbox("View Dataset", key="view_ch8_abtest"):
                st.dataframe(ab_test_data)
        with col2:
            csv = ab_test_data.to_csv(index=False).encode('utf-8')
            st.download_button(
                label="Download CSV",
                data=csv,
                file_name="ab_test_data.csv",
                mime="text/csv",
                key="download_ch8_abtest"
            )

    with tab2:
        st.markdown("### Flashcards")

        cards = [
            ("What is the null hypothesis (H₀)?",
             "<strong>Assumption of no effect or no difference</strong><br><br>We try to find evidence against it"),
            ("What does p-value tell you?",
             "<strong>Probability of data if H₀ is true</strong><br><br>Low p-value = evidence against H₀"),
            ("What is α (alpha)?",
             "<strong>Significance level / Type I error rate</strong><br><br>Typically 0.05 (5%)"),
            ("Difference between p-value and α?",
             "<strong>α is chosen, p-value is calculated</strong><br><br>Compare p to α to decide"),
            ("What is Type I error?",
             "<strong>Rejecting true H₀ (false positive)</strong><br><br>Finding effect that doesn't exist"),
            ("What is Type II error?",
             "<strong>Failing to reject false H₀ (false negative)</strong><br><br>Missing real effect"),
            ("What is statistical power?",
             "<strong>Probability of detecting true effect</strong><br><br>Power = 1 - β"),
            ("When to use t-test vs z-test?",
             "<strong>t-test for small samples (n < 30)</strong><br><br>z-test for large samples"),
            ("What is effect size?",
             "<strong>Magnitude of difference</strong><br><br>Statistical vs practical significance"),
            ("Can you prove H₀ is true?",
             "<strong>No, only fail to reject it</strong><br><br>Absence of evidence ≠ evidence of absence"),
            ("What is the alternative hypothesis (H₁)?",
             "<strong>What we want to prove</strong><br><br>Opposite of H₀, represents effect or difference"),
            ("What is a one-tailed vs two-tailed test?",
             "<strong>One-tailed tests direction, two-tailed tests difference</strong><br><br>Two-tailed is more conservative"),
            ("What is β (beta)?",
             "<strong>Type II error rate</strong><br><br>Probability of missing true effect"),
            ("What is multiple testing problem?",
             "<strong>More tests increase false positive rate</strong><br><br>Use Bonferroni correction")
        ]

        # Grid layout: 3 columns
        num_cols = 3
        for i in range(0, len(cards), num_cols):
            cols = st.columns(num_cols)
            for j in range(num_cols):
                if i + j < len(cards):
                    with cols[j]:
                        q, a = cards[i + j]
                        render_flashcard(f"ch8_card{i+j+1}", q, a)

    with tab4:
        st.markdown("### Foundational Research Papers")

        research_paper_card(
            "The Design of Experiments",
            "Ronald A. Fisher",
            "1935",
            "Oliver and Boyd, Edinburgh",
            "Established the foundations of experimental design and hypothesis testing. Introduced concepts of randomization, replication, and the null hypothesis testing framework used in modern A/B testing.",
            "Fisher, R. A. (1935). The Design of Experiments. Edinburgh: Oliver and Boyd.",
            link="https://archive.org/details/in.ernet.dli.2015.502684"
        )

        research_paper_card(
            "Statistical Methods for Research Workers",
            "Ronald A. Fisher",
            "1925",
            "Oliver and Boyd, Edinburgh",
            "Introduced the p-value and significance testing. This work revolutionized scientific inference and established the α = 0.05 convention still widely used today.",
            "Fisher, R. A. (1925). Statistical Methods for Research Workers. Edinburgh: Oliver and Boyd.",
            link="https://archive.org/details/statisticalmetho0000fish_e5t0"
        )

        research_paper_card(
            "On the Problem of the Most Efficient Tests of Statistical Hypotheses",
            "Jerzy Neyman & Egon Pearson",
            "1933",
            "Philosophical Transactions of the Royal Society A, 231, 289-337",
            "Formalized the framework of Type I and Type II errors, power analysis, and the Neyman-Pearson lemma for optimal hypothesis testing. Complemented Fisher's approach with decision-theoretic perspective.",
            "Neyman, J., & Pearson, E. S. (1933). On the problem of the most efficient tests of statistical hypotheses. PTRSA, 231, 289-337.",
            link="https://doi.org/10.1098/rsta.1933.0009"
        )
