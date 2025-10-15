import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from scipy import stats
from sklearn.linear_model import LinearRegression

st.set_page_config(page_title="Enterprise Data Analytics", page_icon="📊", layout="wide")

# Styling
st.markdown("""
<style>
.main {background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);}
h1, h2, h3 {color: white !important;}
.flashcard {background: white; border-radius: 15px; padding: 25px; margin: 15px 0; box-shadow: 0 10px 30px rgba(0,0,0,0.3);}
.example-box {background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%); color: white; padding: 30px; border-radius: 15px; margin: 20px 0;}
.insight {background: linear-gradient(135deg, #ffd89b 0%, #19547b 100%); color: white; padding: 20px; border-radius: 12px; font-weight: 600; margin: 15px 0;}
</style>
""", unsafe_allow_html=True)

# Navigation
st.sidebar.title("📚 Enterprise Data Analytics")
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
    st.title("🎓 Enterprise Data Analytics")
    st.markdown("## Complete Interactive Presentation")
    
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Chapters", "8")
    col2.metric("Examples", "32+")
    col3.metric("Flashcards", "60+")
    col4.metric("Interactive", "100%")
    
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
    
    👈 **Select a chapter to begin!**
    """)

elif "1️⃣" in chapter:
    st.title("1️⃣ Data Analysis Fundamentals")
    tab1, tab2, tab3 = st.tabs(["📖 Concepts", "🎴 Flashcards", "🎬 Netflix Example"])
    
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
        """)
    
    with tab2:
        cards = [
            ("'Daily downloads' - What type?", "**Discrete Quantitative**\n\nCountable whole numbers!"),
            ("'5-star rating' - Ordinal or Nominal?", "**Ordinal**\n\n5 > 4 > 3 > 2 > 1 has order"),
            ("Mean vs Median for salaries?", "**Median!**\n\nSkewed by ultra-high earners"),
            ("When use Mode?", "**Categorical data**\n\nMost common category"),
            ("What's Standard Deviation?", "**Measures spread**\n\n68% within ±1 SD"),
            ("Why log transform?", "**Handle skewed data**\n\nCompress large values")
        ]
        for i, (q, a) in enumerate(cards, 1):
            with st.expander(f"💳 #{i}: {q}"):
                st.markdown(f"**Question:** {q}")
                st.markdown("---")
                st.markdown(a)
    
    with tab3:
        st.markdown('<div class="example-box"><h3>🎬 Netflix Viewing Analytics</h3><p>Analyzing 230M+ subscribers</p></div>', unsafe_allow_html=True)
        
        np.random.seed(42)
        netflix = pd.DataFrame({
            'Hours': np.random.gamma(2, 3, 1000),
            'Type': np.random.choice(['Series', 'Movie', 'Doc'], 1000, p=[0.6, 0.3, 0.1]),
            'Device': np.random.choice(['TV', 'Mobile', 'Desktop'], 1000, p=[0.5, 0.35, 0.15]),
            'Rating': np.random.choice([1,2,3,4,5], 1000, p=[0.05,0.1,0.2,0.35,0.3])
        })
        
        col1, col2 = st.columns(2)
        with col1:
            fig = px.histogram(netflix, x='Hours', nbins=40, title='Watch Time Distribution', color_discrete_sequence=['#E50914'])
            st.plotly_chart(fig, use_container_width=True)
        with col2:
            fig = px.box(netflix, x='Device', y='Hours', title='Hours by Device', color='Device')
            st.plotly_chart(fig, use_container_width=True)
        
        st.markdown(f'<div class="insight">🔑 Mean={netflix["Hours"].mean():.2f}, Median={netflix["Hours"].median():.2f} → Right-skewed! Netflix uses MEDIAN.</div>', unsafe_allow_html=True)

elif "2️⃣" in chapter:
    st.title("2️⃣ Distributions")
    tab1, tab2, tab3 = st.tabs(["📖 Concepts", "🎴 Flashcards", "🚗 Uber Example"])
    
    with tab1:
        st.markdown("""
        ### Distribution Visualization
        - **Histogram**: Shows frequency distribution
        - **Box Plot**: Shows quartiles and outliers
        - **Skewness**: Measures asymmetry
        - **Kurtosis**: Measures tail heaviness
        
        ### Outlier Detection (IQR Method)
        1. Q1 = 25th percentile, Q3 = 75th percentile
        2. IQR = Q3 - Q1
        3. Outliers: < Q1-1.5×IQR or > Q3+1.5×IQR
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
        
        col1, col2, col3 = st.columns(3)
        col1.metric("Mean", f"{np.mean(data):.1f}")
        col2.metric("Median", f"{np.median(data):.1f}")
        col3.metric("Skewness", f"{stats.skew(data):.2f}")
    
    with tab2:
        cards = [
            ("IQR outlier detection?", "**IQR = Q3 - Q1**\n\nOutliers: < Q1-1.5×IQR or > Q3+1.5×IQR"),
            ("Positive skewness?", "**Right-skewed**\n\nMean > Median, long right tail"),
            ("Box plot vs Histogram?", "**Box**: Compare groups, spot outliers\n**Histogram**: Show exact shape"),
            ("What's kurtosis?", "**Tail heaviness**\n\nHigh = more outliers"),
            ("Z-score for outliers?", "**Z = (X - μ) / σ**\n\nOutliers: |Z| > 3"),
        ]
        for i, (q, a) in enumerate(cards, 1):
            with st.expander(f"💳 #{i}: {q}"):
                st.markdown(a)
    
    with tab3:
        st.markdown('<div class="example-box"><h3>🚗 Uber Ride Durations</h3><p>Optimize driver allocation</p></div>', unsafe_allow_html=True)
        
        np.random.seed(123)
        rides = np.concatenate([np.random.gamma(2, 5, 800), np.random.gamma(4, 8, 150), np.random.gamma(6, 10, 50)])
        uber = pd.DataFrame({'Minutes': rides, 'City': np.random.choice(['NYC', 'SF', 'LA'], 1000)})
        
        col1, col2 = st.columns(2)
        with col1:
            fig = px.histogram(uber, x='Minutes', nbins=40, title='Ride Duration Distribution', color_discrete_sequence=['#000000'])
            st.plotly_chart(fig, use_container_width=True)
        with col2:
            fig = px.box(uber, x='City', y='Minutes', title='Duration by City', color='City')
            st.plotly_chart(fig, use_container_width=True)
        
        Q1, Q3 = uber['Minutes'].quantile([0.25, 0.75])
        IQR = Q3 - Q1
        outliers = uber[(uber['Minutes'] < Q1-1.5*IQR) | (uber['Minutes'] > Q3+1.5*IQR)]
        
        col1, col2, col3 = st.columns(3)
        col1.metric("Total Rides", len(uber))
        col2.metric("Outliers", len(outliers))
        col3.metric("Median", f"{uber['Minutes'].median():.1f} min")
        
        st.markdown('<div class="insight">🔑 Right-skewed with outliers >60min. Flag for fraud detection!</div>', unsafe_allow_html=True)

elif "3️⃣" in chapter:
    st.title("3️⃣ Relationships & Correlation")
    tab1, tab2, tab3 = st.tabs(["📖 Concepts", "🎴 Flashcards", "📦 Amazon Example"])
    
    with tab1:
        st.markdown("""
        ### Correlation Types
        - **Pearson**: Linear relationships (r between -1 and 1)
        - **Spearman**: Monotonic relationships (rank-based)
        
        ### Interpreting r
        - |r| = 0.9-1.0: Very strong
        - |r| = 0.7-0.9: Strong
        - |r| = 0.5-0.7: Moderate
        - |r| = 0.3-0.5: Weak
        - |r| < 0.3: Very weak
        
        ### Linear Regression
        **Y = β₀ + β₁X + ε**
        - β₀: Intercept
        - β₁: Slope
        - R²: % variance explained
        
        ### Correlation ≠ Causation!
        """)
        
        st.markdown("#### Interactive Correlation Demo")
        strength = st.slider("Correlation strength", -1.0, 1.0, 0.8, 0.1)
        np.random.seed(42)
        x = np.random.normal(0, 1, 100)
        y = strength * x + np.random.normal(0, np.sqrt(1-strength**2), 100)
        
        df = pd.DataFrame({'X': x, 'Y': y})
        fig = px.scatter(df, x='X', y='Y', title=f'Correlation = {strength:.2f}')
        # Add manual trendline
        from numpy.polynomial import Polynomial
        p = Polynomial.fit(df['X'], df['Y'], 1)
        line_x = np.array([df['X'].min(), df['X'].max()])
        line_y = p(line_x)
        fig.add_scatter(x=line_x, y=line_y, mode='lines', name='Trendline', line=dict(color='red'))
        st.plotly_chart(fig, use_container_width=True)
        
        st.metric("Actual Correlation", f"{np.corrcoef(x, y)[0,1]:.3f}")
    
    with tab2:
        cards = [
            ("Correlation range?", "**-1 to +1**\n\n-1=perfect negative, 0=none, +1=perfect positive"),
            ("Pearson vs Spearman?", "**Pearson**: Linear only\n**Spearman**: Any monotonic"),
            ("What's R² in regression?", "**% variance explained**\n\nR²=0.81 means 81% explained"),
            ("Correlation = Causation?", "**NO!**\n\nIce cream sales correlate with drownings (both caused by summer)"),
            ("Interpreting slope β₁?", "**Change in Y per unit X**\n\nβ₁=2.5: Y increases 2.5 when X increases 1"),
            ("What's residual?", "**Actual - Predicted**\n\nError in prediction")
        ]
        for i, (q, a) in enumerate(cards, 1):
            with st.expander(f"💳 #{i}: {q}"):
                st.markdown(a)
    
    with tab3:
        st.markdown('<div class="example-box"><h3>📦 Amazon Product Ratings</h3><p>Do higher prices get better reviews?</p></div>', unsafe_allow_html=True)
        
        np.random.seed(42)
        price = np.random.uniform(10, 200, 200)
        rating = 3.5 + 0.005 * price + np.random.normal(0, 0.3, 200)
        rating = np.clip(rating, 1, 5)
        reviews = np.random.poisson(100, 200)
        
        amazon = pd.DataFrame({'Price': price, 'Rating': rating, 'Reviews': reviews})
        
        col1, col2 = st.columns(2)
        with col1:
            fig = px.scatter(amazon, x='Price', y='Rating', size='Reviews', title='Price vs Rating')
            # Add trendline
            model = LinearRegression()
            model.fit(amazon[['Price']], amazon['Rating'])
            line_x = np.array([amazon['Price'].min(), amazon['Price'].max()])
            line_y = model.predict(line_x.reshape(-1, 1))
            fig.add_scatter(x=line_x, y=line_y, mode='lines', name='Trendline', line=dict(color='red'))
            st.plotly_chart(fig, use_container_width=True)
        with col2:
            corr = amazon['Price'].corr(amazon['Rating'])
            st.metric("Correlation", f"{corr:.3f}")
            
            from sklearn.linear_model import LinearRegression
            model = LinearRegression()
            model.fit(amazon[['Price']], amazon['Rating'])
            
            st.metric("Slope (β₁)", f"{model.coef_[0]:.4f}")
            st.metric("R²", f"{model.score(amazon[['Price']], amazon['Rating']):.3f}")
            
            st.markdown(f"""
            **Interpretation:**
            - For every $10 increase in price, rating increases by {model.coef_[0]*10:.3f} stars
            - R² = {model.score(amazon[['Price']], amazon['Rating']):.1%} of rating variance explained by price
            """)
        
        st.markdown('<div class="insight">🔑 Weak positive correlation. Higher prices slightly correlate with better ratings (selection bias: expensive = premium quality)</div>', unsafe_allow_html=True)

elif "4️⃣" in chapter:
    st.title("4️⃣ Probability")
    tab1, tab2, tab3 = st.tabs(["📖 Concepts", "🎴 Flashcards", "🚗 Tesla Example"])
    
    with tab1:
        st.markdown("""
        ### Probability Rules
        1. **Addition Rule**: P(A or B) = P(A) + P(B) - P(A and B)
        2. **Multiplication Rule**: P(A and B) = P(A) × P(B|A)
        3. **Complement Rule**: P(not A) = 1 - P(A)
        
        ### Conditional Probability
        **P(A|B) = P(A and B) / P(B)**
        
        ### Bayes' Theorem
        **P(A|B) = P(B|A) × P(A) / P(B)**
        
        ### Expected Value
        **E(X) = Σ x × P(x)**
        
        Average outcome over many trials
        """)
        
        st.markdown("#### Probability Calculator")
        pa = st.slider("P(A)", 0.0, 1.0, 0.3, 0.05)
        pb = st.slider("P(B)", 0.0, 1.0, 0.4, 0.05)
        pa_and_b = st.slider("P(A and B)", 0.0, min(pa, pb), min(pa, pb)/2, 0.05)
        
        pa_or_b = pa + pb - pa_and_b
        pa_given_b = pa_and_b / pb if pb > 0 else 0
        
        col1, col2, col3 = st.columns(3)
        col1.metric("P(A or B)", f"{pa_or_b:.3f}")
        col2.metric("P(A|B)", f"{pa_given_b:.3f}")
        col3.metric("P(not A)", f"{1-pa:.3f}")
    
    with tab2:
        cards = [
            ("P(A or B) formula?", "**P(A) + P(B) - P(A and B)**\n\nSubtract overlap!"),
            ("P(A and B) independent?", "**P(A) × P(B)**\n\nWhen events don't affect each other"),
            ("What's P(A|B)?", "**Probability of A given B**\n\nP(A|B) = P(A and B) / P(B)"),
            ("Bayes' Theorem use?", "**Update beliefs with new evidence**\n\nMedical diagnosis, spam filters"),
            ("Expected value?", "**E(X) = Σ x×P(x)**\n\nLong-run average"),
            ("Complement rule?", "**P(not A) = 1 - P(A)**\n\nProbabilities sum to 1")
        ]
        for i, (q, a) in enumerate(cards, 1):
            with st.expander(f"💳 #{i}: {q}"):
                st.markdown(a)
    
    with tab3:
        st.markdown('<div class="example-box"><h3>🚗 Tesla Insurance Risk</h3><p>Calculate accident probabilities</p></div>', unsafe_allow_html=True)
        
        st.markdown("""
        **Scenario**: Tesla offers insurance based on driving data
        - P(Accident) = 0.05 (5% of drivers have accident)
        - P(Aggressive Driving) = 0.20 (20% drive aggressively)
        - P(Aggressive | Accident) = 0.60 (60% of accidents involve aggressive driving)
        
        **Question**: If someone drives aggressively, what's probability of accident?
        """)
        
        # Bayes' Theorem
        p_accident = 0.05
        p_aggressive = 0.20
        p_aggressive_given_accident = 0.60
        
        # P(Accident | Aggressive) = P(Aggressive | Accident) × P(Accident) / P(Aggressive)
        p_accident_given_aggressive = (p_aggressive_given_accident * p_accident) / p_aggressive
        
        st.markdown("### Using Bayes' Theorem:")
        st.latex(r"P(Accident|Aggressive) = \frac{P(Aggressive|Accident) \times P(Accident)}{P(Aggressive)}")
        st.latex(rf"= \frac{{0.60 \times 0.05}}{{0.20}} = {p_accident_given_aggressive:.3f}")
        
        col1, col2, col3 = st.columns(3)
        col1.metric("General Risk", f"{p_accident:.1%}")
        col2.metric("Aggressive Driver Risk", f"{p_accident_given_aggressive:.1%}")
        col3.metric("Risk Increase", f"{p_accident_given_aggressive/p_accident:.1f}x")
        
        st.markdown("""
        ### Expected Value: Insurance Pricing
        - P(No Accident) = 0.85, Cost = $0
        - P(Minor) = 0.12, Cost = $5,000
        - P(Major) = 0.03, Cost = $30,000
        """)
        
        expected_cost = 0.85 * 0 + 0.12 * 5000 + 0.03 * 30000
        st.metric("Expected Cost per Driver", f"${expected_cost:,.0f}")
        st.markdown(f"**Premium Calculation**: ${expected_cost:,.0f} + Profit Margin + Admin = ~${expected_cost*1.3:,.0f}/year")
        
        st.markdown('<div class="insight">🔑 Aggressive drivers are 3x more likely to have accidents. Tesla charges them higher premiums!</div>', unsafe_allow_html=True)

elif "5️⃣" in chapter:
    st.title("5️⃣ Statistical Distributions")
    tab1, tab2, tab3 = st.tabs(["📖 Concepts", "🎴 Flashcards", "📞 Call Center Example"])
    
    with tab1:
        st.markdown("""
        ### Key Distributions
        
        **1. Normal (Gaussian)**
        - Bell curve, symmetric
        - Mean = Median = Mode
        - 68-95-99.7 rule
        - Example: Heights, test scores
        
        **2. Binomial**
        - n trials, p success probability
        - Discrete outcomes (success/failure)
        - Example: Coin flips, quality control
        
        **3. Poisson**
        - Count of events in fixed interval
        - λ = average rate
        - Example: Calls per hour, defects per batch
        
        **4. Exponential**
        - Time between events
        - Memoryless property
        - Example: Time between arrivals, system lifetime
        """)
        
        dist_choice = st.selectbox("Explore Distribution", ["Normal", "Binomial", "Poisson", "Exponential"])
        
        if dist_choice == "Normal":
            mu = st.slider("Mean (μ)", 0, 100, 50, 5)
            sigma = st.slider("Std Dev (σ)", 1, 20, 10, 1)
            x = np.linspace(mu-4*sigma, mu+4*sigma, 1000)
            y = stats.norm.pdf(x, mu, sigma)
            fig = px.line(pd.DataFrame({'x': x, 'y': y}), x='x', y='y', title=f'Normal(μ={mu}, σ={sigma})')
            st.plotly_chart(fig, use_container_width=True)
            
        elif dist_choice == "Binomial":
            n = st.slider("Trials (n)", 1, 50, 20, 1)
            p = st.slider("Success prob (p)", 0.0, 1.0, 0.5, 0.05)
            x = np.arange(0, n+1)
            y = stats.binom.pmf(x, n, p)
            fig = px.bar(pd.DataFrame({'x': x, 'y': y}), x='x', y='y', title=f'Binomial(n={n}, p={p})')
            st.plotly_chart(fig, use_container_width=True)
            
        elif dist_choice == "Poisson":
            lam = st.slider("Rate (λ)", 1.0, 20.0, 5.0, 0.5)
            x = np.arange(0, int(lam*3))
            y = stats.poisson.pmf(x, lam)
            fig = px.bar(pd.DataFrame({'x': x, 'y': y}), x='x', y='y', title=f'Poisson(λ={lam})')
            st.plotly_chart(fig, use_container_width=True)
            
        else:  # Exponential
            scale = st.slider("Scale (1/λ)", 0.5, 5.0, 2.0, 0.5)
            x = np.linspace(0, scale*5, 1000)
            y = stats.expon.pdf(x, scale=scale)
            fig = px.line(pd.DataFrame({'x': x, 'y': y}), x='x', y='y', title=f'Exponential(λ={1/scale:.2f})')
            st.plotly_chart(fig, use_container_width=True)
    
    with tab2:
        cards = [
            ("Normal distribution properties?", "**Bell curve, symmetric**\n\n68% within ±1σ, 95% within ±2σ, 99.7% within ±3σ"),
            ("When use Binomial?", "**Fixed trials, binary outcomes**\n\nCoin flips, pass/fail tests"),
            ("Poisson vs Binomial?", "**Poisson**: Count events (calls/hour)\n**Binomial**: Fixed trials (10 coin flips)"),
            ("Exponential distribution?", "**Time between events**\n\nMemoryless property"),
            ("Z-score formula?", "**Z = (X - μ) / σ**\n\nStandardizes to N(0,1)"),
            ("What's λ in Poisson?", "**Average rate**\n\nExpected # events per interval")
        ]
        for i, (q, a) in enumerate(cards, 1):
            with st.expander(f"💳 #{i}: {q}"):
                st.markdown(a)
    
    with tab3:
        st.markdown('<div class="example-box"><h3>📞 Call Center Analytics</h3><p>Optimize staffing with distributions</p></div>', unsafe_allow_html=True)
        
        st.markdown("""
        **Scenario**: Customer support call center
        - Average: 12 calls/hour (λ = 12)
        - Question: How many calls in next hour? How long until next call?
        """)
        
        # Poisson: Number of calls
        lam = 12
        x_calls = np.arange(0, 25)
        y_calls = stats.poisson.pmf(x_calls, lam)
        
        # Exponential: Time between calls
        mean_time = 60/lam  # minutes
        x_time = np.linspace(0, 20, 100)
        y_time = stats.expon.pdf(x_time, scale=mean_time)
        
        col1, col2 = st.columns(2)
        
        with col1:
            fig1 = px.bar(pd.DataFrame({'Calls': x_calls, 'Probability': y_calls}), 
                         x='Calls', y='Probability', title='# Calls in Next Hour (Poisson)')
            st.plotly_chart(fig1, use_container_width=True)
            
            prob_10_to_15 = stats.poisson.cdf(15, lam) - stats.poisson.cdf(9, lam)
            st.metric("P(10-15 calls)", f"{prob_10_to_15:.1%}")
        
        with col2:
            fig2 = px.line(pd.DataFrame({'Minutes': x_time, 'Density': y_time}),
                          x='Minutes', y='Density', title='Time Until Next Call (Exponential)')
            st.plotly_chart(fig2, use_container_width=True)
            
            prob_within_5 = stats.expon.cdf(5, scale=mean_time)
            st.metric("P(call within 5 min)", f"{prob_within_5:.1%}")
        
        st.markdown("""
        ### Staffing Decisions
        - **Expected**: 12 calls/hour
        - **90th percentile**: ~17 calls/hour
        - **Recommendation**: Staff for 17-18 calls/hour to maintain quality
        """)
        
        st.markdown('<div class="insight">🔑 Use Poisson for volume planning, Exponential for response time SLAs!</div>', unsafe_allow_html=True)

elif "6️⃣" in chapter:
    st.title("6️⃣ Decision Making")
    tab1, tab2, tab3 = st.tabs(["📖 Concepts", "🎴 Flashcards", "💰 Startup Example"])
    
    with tab1:
        st.markdown("""
        ### Decision Analysis Tools
        
        **1. Expected Monetary Value (EMV)**
        - EMV = Σ (Probability × Payoff)
        - Choose highest EMV
        
        **2. Decision Criteria**
        - **Maximax**: Choose best of best outcomes (optimistic)
        - **Maximin**: Choose best of worst outcomes (pessimistic)
        - **Minimax Regret**: Minimize maximum regret
        
        **3. Decision Trees**
        - Visual representation of choices
        - Calculate EMV at each node
        - Work backwards from outcomes
        
        **4. Sensitivity Analysis**
        - How robust is decision to changes in probabilities?
        """)
        
        st.markdown("#### Interactive Decision Tree")
        
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
        
        st.markdown(f"""
        ### EMV Calculation
        
        **Launch**:
        - EMV = {p_success:.0%} × (${revenue_success:,} - ${launch_cost:,}) + {1-p_success:.0%} × (${revenue_fail:,} - ${launch_cost:,})
        - EMV = **${emv_launch:,.0f}**
        
        **Don't Launch**:
        - EMV = **$0**
        decision_text = "LAUNCH" if emv_launch > 0 else "Dont launch"
        """)
        
        if emv_launch > 0:
            st.success(f"Expected profit: ${emv_launch:,.0f}")
        else:
            st.error(f"Expected loss: ${abs(emv_launch):,.0f}")
    
    with tab2:
        cards = [
            ("EMV formula?", "**Σ P(outcome) × Value(outcome)**\n\nWeighted average of all outcomes"),
            ("Maximax strategy?", "**Choose best of best**\n\nOptimistic: assume everything goes right"),
            ("Maximin strategy?", "**Choose best of worst**\n\nPessimistic: assume everything goes wrong"),
            ("What's decision tree?", "**Visual map of choices**\n\nSquares = decisions, Circles = chance events"),
            ("Minimax regret?", "**Minimize maximum regret**\n\nRegret = Opportunity cost of wrong choice"),
            ("Why sensitivity analysis?", "**Test robustness**\n\nHow much can probabilities change before decision flips?")
        ]
        for i, (q, a) in enumerate(cards, 1):
            with st.expander(f"💳 #{i}: {q}"):
                st.markdown(a)
    
    with tab3:
        st.markdown('<div class="example-box"><h3>💰 Startup Investment Decision</h3><p>VC firm deciding on Series A investment</p></div>', unsafe_allow_html=True)
        
        st.markdown("""
        **Decision**: Invest $2M in startup or pass?
        
        **Possible Outcomes**:
        1. **Unicorn** (20%): Exit at $100M → Return $15M (7.5x)
        2. **Moderate Success** (30%): Exit at $20M → Return $3M (1.5x)
        3. **Zombie** (35%): Breakeven → Return $2M (1.0x)
        4. **Failure** (15%): Company dies → Return $0 (0x)
        """)
        
        # Calculate EMV
        investment = 2_000_000
        outcomes = [
            (0.20, 15_000_000),  # Unicorn
            (0.30, 3_000_000),   # Moderate
            (0.35, 2_000_000),   # Zombie
            (0.15, 0)            # Failure
        ]
        
        emv_invest = sum(p * (v - investment) for p, v in outcomes)
        emv_pass = 0
        
        # Create decision tree visualization
        df_tree = pd.DataFrame({
            'Outcome': ['Unicorn (20%)', 'Moderate (30%)', 'Zombie (35%)', 'Failure (15%)'],
            'Net Return': [15_000_000 - investment, 3_000_000 - investment, 2_000_000 - investment, -investment],
            'Probability': [0.20, 0.30, 0.35, 0.15]
        })
        
        fig = px.bar(df_tree, x='Outcome', y='Net Return', color='Probability',
                    title='Investment Outcomes', color_continuous_scale='RdYlGn')
        st.plotly_chart(fig, use_container_width=True)
        
        col1, col2, col3 = st.columns(3)
        col1.metric("EMV (Invest)", f"${emv_invest:,.0f}")
        col2.metric("EMV (Pass)", "$0")
        col3.metric("Decision", "✅ INVEST" if emv_invest > 0 else "❌ PASS")
        
        st.markdown(f"""
        ### Analysis
        - **Expected Return**: ${emv_invest:,.0f} per $2M invested
        - **ROI**: {emv_invest/investment:.1%}
        - **Risk**: 50% chance of loss or breakeven
        - **Upside**: 20% chance of 7.5x return
        
        ### Sensitivity Analysis
        What if unicorn probability changes?
        """)
        
        p_unicorns = np.linspace(0.05, 0.40, 50)
        emvs = []
        for p in p_unicorns:
            outcomes_adjusted = [
                (p, 15_000_000),
                (0.30, 3_000_000),
                ((1-p-0.30-0.15), 2_000_000),
                (0.15, 0)
            ]
            emv = sum(prob * (val - investment) for prob, val in outcomes_adjusted)
            emvs.append(emv)
        
        fig_sens = px.line(pd.DataFrame({'P(Unicorn)': p_unicorns, 'EMV': emvs}),
                          x='P(Unicorn)', y='EMV', title='Sensitivity: Unicorn Probability')
        fig_sens.add_hline(y=0, line_dash="dash", line_color="red")
        st.plotly_chart(fig_sens, use_container_width=True)
        
        st.markdown('<div class="insight">🔑 Investment is positive EMV even with lower unicorn probability. Diversify across 10 startups to reduce variance!</div>', unsafe_allow_html=True)

elif "7️⃣" in chapter:
    st.title("7️⃣ Sampling & Central Limit Theorem")
    tab1, tab2, tab3 = st.tabs(["📖 Concepts", "🎴 Flashcards", "🗳️ Polling Example"])
    
    with tab1:
        st.markdown("""
        ### Central Limit Theorem (CLT)
        
        **The most important theorem in statistics!**
        
        For sample means from ANY distribution:
        - Distribution of x̄ approaches Normal as n increases
        - Mean of x̄ = population mean (μ)
        - Standard error = σ / √n
        
        **Rule of thumb**: n ≥ 30 for CLT
        
        ### Sampling Methods
        
        **1. Simple Random Sample (SRS)**
        - Every element has equal probability
        - Gold standard but expensive
        
        **2. Stratified Sampling**
        - Divide into strata, sample from each
        - Ensures representation
        
        **3. Cluster Sampling**
        - Randomly select groups, sample all in group
        - Cost-effective
        
        **4. Systematic Sampling**
        - Every kth element
        - Simple but risk of patterns
        
        ### Confidence Intervals
        **x̄ ± z × (σ/√n)**
        - 90% CI: z = 1.645
        - 95% CI: z = 1.96
        - 99% CI: z = 2.576
        """)
        
        st.markdown("#### Interactive CLT Demo")
        
        pop_dist = st.selectbox("Population Distribution", ["Uniform", "Exponential", "Bimodal"])
        sample_size = st.slider("Sample Size (n)", 5, 100, 30, 5)
        num_samples = st.slider("Number of Samples", 100, 2000, 500, 100)
        
        np.random.seed(42)
        if pop_dist == "Uniform":
            population = np.random.uniform(0, 10, 10000)
        elif pop_dist == "Exponential":
            population = np.random.exponential(2, 10000)
        else:
            population = np.concatenate([np.random.normal(3, 1, 5000), np.random.normal(7, 1, 5000)])
        
        # Draw many samples and calculate means
        sample_means = [np.random.choice(population, sample_size).mean() for _ in range(num_samples)]
        
        col1, col2 = st.columns(2)
        
        with col1:
            fig1 = px.histogram(pd.DataFrame({'Value': population}), x='Value', nbins=50,
                               title='Population Distribution')
            st.plotly_chart(fig1, use_container_width=True)
        
        with col2:
            fig2 = px.histogram(pd.DataFrame({'Sample Mean': sample_means}), x='Sample Mean', nbins=40,
                               title=f'Distribution of Sample Means (n={sample_size})')
            st.plotly_chart(fig2, use_container_width=True)
        
        st.markdown(f"""
        ### CLT in Action!
        - Population mean: {np.mean(population):.2f}
        - Mean of sample means: {np.mean(sample_means):.2f} ✓
        - Population std: {np.std(population):.2f}
        - Std of sample means: {np.std(sample_means):.2f}
        - Predicted SE (σ/√n): {np.std(population)/np.sqrt(sample_size):.2f} ✓
        
        Notice: Sample means form a **normal distribution** even though population may not be!
        """)
    
    with tab2:
        cards = [
            ("Central Limit Theorem?", "**Sample means → Normal**\n\nRegardless of population shape (if n ≥ 30)"),
            ("Standard Error formula?", "**SE = σ / √n**\n\nDecreases as sample size increases"),
            ("95% Confidence Interval?", "**x̄ ± 1.96 × SE**\n\n95% of intervals contain true μ"),
            ("Stratified vs Cluster?", "**Stratified**: Sample from each group\n**Cluster**: Sample entire groups"),
            ("Margin of Error?", "**MOE = z × SE**\n\nHalf-width of confidence interval"),
            ("Why n=30 rule?", "**CLT kicks in**\n\nSample means become approximately normal")
        ]
        for i, (q, a) in enumerate(cards, 1):
            with st.expander(f"💳 #{i}: {q}"):
                st.markdown(a)
    
    with tab3:
        st.markdown('<div class="example-box"><h3>🗳️ Election Polling</h3><p>Predicting election results with confidence intervals</p></div>', unsafe_allow_html=True)
        
        st.markdown("""
        **Scenario**: Presidential election poll
        - Population: 150M voters
        - Sample: 1,200 likely voters
        - Candidate A: 52% support in sample
        
        **Question**: What's the 95% confidence interval for true support?
        """)
        
        # Poll parameters
        n = 1200
        p_hat = 0.52
        
        # Standard error for proportion
        se = np.sqrt(p_hat * (1 - p_hat) / n)
        
        # 95% CI
        z = 1.96
        moe = z * se
        ci_lower = p_hat - moe
        ci_upper = p_hat + moe
        
        col1, col2, col3 = st.columns(3)
        col1.metric("Sample Proportion", f"{p_hat:.1%}")
        col2.metric("Margin of Error", f"±{moe:.1%}")
        col3.metric("95% CI", f"[{ci_lower:.1%}, {ci_upper:.1%}]")
        
        st.markdown(f"""
        ### Interpretation
        - We are **95% confident** true support is between {ci_lower:.1%} and {ci_upper:.1%}
        - Margin of error: ±{moe:.1%}
        - Since entire CI is above 50%, **Candidate A is likely to win!**
        
        ### Sample Size Effect
        What if we polled more people?
        """)
        
        sample_sizes = [300, 600, 1200, 2400, 4800]
        moes = [1.96 * np.sqrt(0.52 * 0.48 / n) for n in sample_sizes]
        
        fig = px.line(pd.DataFrame({'Sample Size': sample_sizes, 'MOE': [m*100 for m in moes]}),
                     x='Sample Size', y='MOE', title='Margin of Error vs Sample Size',
                     labels={'MOE': 'Margin of Error (%)'})
        st.plotly_chart(fig, use_container_width=True)
        
        st.markdown("""
        ### Key Insights
        - Doubling sample size doesn't double precision (√n effect)
        - n=1,200 gives ±2.8% MOE (industry standard)
        - Diminishing returns beyond 2,000-3,000
        """)
        
        st.markdown('<div class="insight">🔑 Polls work because of CLT! Even 1,200 people can predict 150M voters within ±3%</div>', unsafe_allow_html=True)

elif "8️⃣" in chapter:
    st.title("8️⃣ Hypothesis Testing")
    tab1, tab2, tab3 = st.tabs(["📖 Concepts", "🎴 Flashcards", "🧪 A/B Test Example"])
    
    with tab1:
        st.markdown("""
        ### Hypothesis Testing Framework
        
        **1. State Hypotheses**
        - **H₀** (Null): Status quo, no effect
        - **H₁** (Alternative): What we want to prove
        
        **2. Choose Significance Level (α)**
        - α = 0.05 (5%) most common
        - α = probability of Type I error
        
        **3. Calculate Test Statistic**
        - z-test, t-test, chi-square, etc.
        
        **4. Find p-value**
        - p = probability of observing data if H₀ true
        
        **5. Make Decision**
        - If p < α: Reject H₀ (statistically significant)
        - If p ≥ α: Fail to reject H₀
        
        ### Types of Errors
        - **Type I (α)**: Reject H₀ when it's true (false positive)
        - **Type II (β)**: Fail to reject H₀ when it's false (false negative)
        - **Power**: 1 - β (probability of correctly rejecting H₀)
        
        ### Common Tests
        - **One-sample t-test**: Compare mean to value
        - **Two-sample t-test**: Compare two means
        - **Paired t-test**: Compare before/after
        - **Chi-square**: Test independence of categories
        """)
        
        st.markdown("#### Interactive Hypothesis Test")
        
        st.markdown("**Scenario**: Does new drug lower blood pressure?")
        
        # Generate data
        np.random.seed(42)
        before = np.random.normal(140, 15, 100)
        effect_size = st.slider("True Effect Size (mm Hg)", 0, 15, 8, 1)
        after = before - effect_size + np.random.normal(0, 10, 100)
        
        # Paired t-test
        t_stat, p_value = stats.ttest_rel(before, after)
        
        col1, col2 = st.columns(2)
        
        with col1:
            fig = go.Figure()
            fig.add_trace(go.Box(y=before, name='Before', marker_color='lightblue'))
            fig.add_trace(go.Box(y=after, name='After', marker_color='lightgreen'))
            fig.update_layout(title='Blood Pressure Before vs After', yaxis_title='BP (mm Hg)')
            st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            st.markdown(f"""
            ### Test Results
            - **H₀**: No difference (μ_diff = 0)
            - **H₁**: BP decreases (μ_diff > 0)
            
            **Statistics:**
            - Mean Before: {np.mean(before):.1f}
            - Mean After: {np.mean(after):.1f}
            - Difference: {np.mean(before - after):.1f}
            - t-statistic: {t_stat:.3f}
            - p-value: {p_value:.4f}
            
            **Decision (α=0.05):**
            """)
            
            if p_value < 0.05:
                st.success(f"✅ REJECT H₀ (p={p_value:.4f} < 0.05)")
                st.markdown("Drug **significantly lowers** blood pressure!")
            else:
                st.error(f"❌ Fail to reject H₀ (p={p_value:.4f} ≥ 0.05)")
                st.markdown("Insufficient evidence of effect")
    
    with tab2:
        cards = [
            ("What's null hypothesis?", "**H₀: No effect/difference**\n\nStatus quo assumption"),
            ("What's p-value?", "**P(data | H₀ true)**\n\nProbability of seeing data if no real effect"),
            ("p < 0.05 means?", "**Reject H₀**\n\nResult is statistically significant"),
            ("Type I vs Type II error?", "**Type I**: False positive (reject true H₀)\n**Type II**: False negative (miss real effect)"),
            ("Statistical vs Practical significance?", "**Statistical**: p < α\n**Practical**: Effect is large enough to matter"),
            ("What's confidence interval?", "**Range of plausible values**\n\n95% CI: 95% chance contains true parameter")
        ]
        for i, (q, a) in enumerate(cards, 1):
            with st.expander(f"💳 #{i}: {q}"):
                st.markdown(a)
    
    with tab3:
        st.markdown('<div class="example-box"><h3>🧪 A/B Test: Mobile App Redesign</h3><p>Does new UI increase purchases?</p></div>', unsafe_allow_html=True)
        
        st.markdown("""
        **Scenario**: E-commerce app tests new checkout flow
        - **Control (A)**: Current design
        - **Treatment (B)**: New streamlined design
        - **Metric**: Conversion rate (% who purchase)
        - **Users**: 10,000 per group
        """)
        
        # Simulate A/B test data
        np.random.seed(42)
        n_a = 10000
        n_b = 10000
        p_a = 0.045  # 4.5% conversion
        p_b = 0.052  # 5.2% conversion (15% relative lift)
        
        conv_a = np.random.binomial(1, p_a, n_a).sum()
        conv_b = np.random.binomial(1, p_b, n_b).sum()
        
        rate_a = conv_a / n_a
        rate_b = conv_b / n_b
        
        # Two-proportion z-test
        p_pool = (conv_a + conv_b) / (n_a + n_b)
        se = np.sqrt(p_pool * (1 - p_pool) * (1/n_a + 1/n_b))
        z_stat = (rate_b - rate_a) / se
        p_value = 1 - stats.norm.cdf(z_stat)
        
        # Confidence interval for difference
        se_diff = np.sqrt(rate_a*(1-rate_a)/n_a + rate_b*(1-rate_b)/n_b)
        ci_lower = (rate_b - rate_a) - 1.96 * se_diff
        ci_upper = (rate_b - rate_a) + 1.96 * se_diff
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("### Results")
            results_df = pd.DataFrame({
                'Group': ['Control (A)', 'Treatment (B)'],
                'Users': [n_a, n_b],
                'Conversions': [conv_a, conv_b],
                'Rate': [f'{rate_a:.2%}', f'{rate_b:.2%}']
            })
            st.dataframe(results_df, hide_index=True)
            
            lift = (rate_b - rate_a) / rate_a
            st.metric("Absolute Lift", f"+{(rate_b - rate_a)*100:.2f}pp")
            st.metric("Relative Lift", f"+{lift:.1%}")
        
        with col2:
            st.markdown("### Statistical Test")
            st.markdown(f"""
            **Hypotheses:**
            - H₀: p_B = p_A (no difference)
            - H₁: p_B > p_A (B is better)
            
            **Statistics:**
            - z-statistic: {z_stat:.3f}
            - p-value: {p_value:.4f}
            - 95% CI: [{ci_lower*100:.2f}pp, {ci_upper*100:.2f}pp]
            """)
            
            if p_value < 0.05:
                st.success(f"✅ SIGNIFICANT (p={p_value:.4f})")
                st.markdown("**Recommendation: SHIP NEW DESIGN!**")
            else:
                st.warning(f"❌ Not significant (p={p_value:.4f})")
                st.markdown("Need more data or larger effect")
        
        # Visualize
        fig = go.Figure()
        fig.add_trace(go.Bar(x=['Control', 'Treatment'], y=[rate_a*100, rate_b*100],
                            marker_color=['lightblue', 'lightgreen'],
                            text=[f'{rate_a:.2%}', f'{rate_b:.2%}'],
                            textposition='auto'))
        fig.update_layout(title='Conversion Rates', yaxis_title='Conversion Rate (%)',
                         showlegend=False)
        st.plotly_chart(fig, use_container_width=True)
        
        st.markdown("""
        ### Business Impact
        - **Additional conversions**: {:.0f} per 10,000 users
        - **Revenue per conversion**: $50 (average)
        - **Additional revenue**: ${:,.0f} per 10,000 users
        - **Annual impact** (1M users): ${:,.0f}
        """.format((rate_b - rate_a) * 10000, 
                   (rate_b - rate_a) * 10000 * 50,
                   (rate_b - rate_a) * 1000000 * 50))
        
        st.markdown('<div class="insight">🔑 Even small % lifts = big $$ at scale. A/B testing drives data-driven product decisions!</div>', unsafe_allow_html=True)

# Footer
st.sidebar.markdown("---")
st.sidebar.info("💡 Use tabs to explore: Concepts → Flashcards → Examples")
st.sidebar.success(f"🎓 Complete coverage of Enterprise Data Analytics")

