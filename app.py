import streamlit as st
import ssl
import certifi
import httpx
import plotly.graph_objects as go

from openai import OpenAI

from finance_agent import FinanceAgent
from market_agent import MarketAgent
from legal_agent import LegalAgent
from aggregator import SharkAggregator

# ==================================================
# PAGE CONFIG
# ==================================================

st.set_page_config(
    page_title="AI Shark Tank",
    page_icon="🦈",
    layout="wide"
)

# ==================================================
# PREMIUM STYLING
# ==================================================

st.markdown("""
<style>

.stApp {
    background: linear-gradient(
        135deg,
        #020617,
        #0f172a,
        #111827
    );
}

.block-container {
    padding-top: 2rem;
}

div[data-testid="stMetric"] {
    background-color: rgba(255,255,255,0.05);
    padding: 20px;
    border-radius: 15px;
}

</style>
""", unsafe_allow_html=True)

# ==================================================
# OPENAI CLIENT
# ==================================================

API_KEY = "wHzWj2P0vy3cCINHg1kDL3PaVRP0osAq5t6c2G1c"

ssl_context = ssl.create_default_context(
    cafile=certifi.where()
)

http_client = httpx.Client(
    verify=ssl_context,
    timeout=60.0
)

client = OpenAI(
    api_key=API_KEY,
    base_url="https://openai.generative.engine.capgemini.com/v1",
    http_client=http_client
)

# ==================================================
# HEADER
# ==================================================

st.markdown("""
# 🦈 AI Shark Tank

### Let Finance, Market and Legal Sharks Evaluate Your Startup
""")

st.divider()

# ==================================================
# FORM SECTION
# ==================================================

col1, col2 = st.columns(2)

with col1:

    startup_name = st.text_input(
        "🚀 Startup Name",
        placeholder="HireAI"
    )

    industry = st.selectbox(
        "🏭 Industry",
        [
            "AI",
            "FinTech",
            "HR Tech",
            "HealthTech",
            "EdTech",
            "SaaS",
            "E-Commerce",
            "Other"
        ]
    )

    customers = st.text_input(
        "🎯 Target Customers",
        placeholder="Recruiters and HR Teams"
    )

with col2:

    business_model = st.selectbox(
        "💰 Business Model",
        [
            "SaaS Subscription",
            "Marketplace",
            "Freemium",
            "Advertising",
            "Commission",
            "Enterprise Licensing"
        ]
    )

problem = st.text_area(
    "⚠️ Problem Statement",
    placeholder="What problem are you solving?"
)

solution = st.text_area(
    "✅ Your Solution",
    placeholder="How does your startup solve it?"
)

startup_idea = f"""
Startup Name:
{startup_name}

Industry:
{industry}

Target Customers:
{customers}

Business Model:
{business_model}

Problem Statement:
{problem}

Solution:
{solution}
"""

# ==================================================
# BUTTON
# ==================================================

if st.button("🦈 Summon The Sharks"):

    if startup_name.strip() == "":
        st.warning("Please enter a Startup Name")
        st.stop()

    try:

        with st.status(
            "🦈 Sharks are discussing your startup...",
            expanded=True
        ) as status:

            st.write("💰 Finance Shark analyzing...")

            finance_agent = FinanceAgent(client)

            finance_result = finance_agent.evaluate(
                startup_idea
            )

            st.write("📈 Market Shark analyzing...")

            market_agent = MarketAgent(client)

            market_result = market_agent.evaluate(
                startup_idea
            )

            st.write("⚖️ Legal Shark analyzing...")

            legal_agent = LegalAgent(client)

            legal_result = legal_agent.evaluate(
                startup_idea
            )

            status.update(
                label="✅ Analysis Complete",
                state="complete"
            )

        # ==========================================
        # AGGREGATION
        # ==========================================

        aggregator = SharkAggregator()

        final_result = aggregator.aggregate(
            finance_result,
            market_result,
            legal_result
        )

        # ==========================================
        # VERDICT
        # ==========================================

        st.markdown(
            f"""
            <div style="
                padding:25px;
                border-radius:20px;
                background:linear-gradient(
                    135deg,
                    #0ea5e9,
                    #2563eb
                );
                text-align:center;
                margin-bottom:20px;
            ">
                <h1>🦈 FINAL VERDICT</h1>
                <h2>{final_result['verdict']}</h2>
                <h1>{final_result['overall_score']}</h1>
            </div>
            """,
            unsafe_allow_html=True
        )

        # ==========================================
        # GAUGE CHART
        # ==========================================

        score = float(final_result["overall_score"])

        fig = go.Figure(
            go.Indicator(
                mode="gauge+number",
                value=score,
                title={
                    "text": "Investment Score"
                },
                gauge={
                    "axis": {
                        "range": [0, 100]
                    },
                    "bar": {
                        "color": "cyan"
                    }
                }
            )
        )

        st.plotly_chart(
            fig,
            use_container_width=True
        )

        # ==========================================
        # SHARKS
        # ==========================================

        col1, col2, col3 = st.columns(3)

        with col1:

            st.subheader("💰 Finance Shark")

            st.metric(
                "Score",
                finance_result["overall_score"]
            )

            st.write("### Strengths")

            for item in finance_result["strengths"]:
                st.write("✅", item)

            st.write("### Weaknesses")

            for item in finance_result["weaknesses"]:
                st.write("⚠️", item)

        with col2:

            st.subheader("📈 Market Shark")

            st.metric(
                "Score",
                market_result["overall_score"]
            )

            st.write("### Strengths")

            for item in market_result["strengths"]:
                st.write("✅", item)

            st.write("### Weaknesses")

            for item in market_result["weaknesses"]:
                st.write("⚠️", item)

        with col3:

            st.subheader("⚖️ Legal Shark")

            st.metric(
                "Score",
                legal_result["overall_score"]
            )

            st.write("### Strengths")

            for item in legal_result["strengths"]:
                st.write("✅", item)

            st.write("### Weaknesses")

            for item in legal_result["weaknesses"]:
                st.write("⚠️", item)

        st.divider()

        st.header("📊 Detailed Results")

        st.json({
            "finance": finance_result,
            "market": market_result,
            "legal": legal_result,
            "final": final_result
        })

        st.download_button(
            "📄 Download Investor Report",
            str(final_result),
            file_name="shark_tank_report.txt"
        )

    except Exception as e:

        st.error("Analysis Failed")

        st.exception(e)