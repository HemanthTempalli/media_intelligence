import streamlit as st
import json
import pandas as pd

# =================================================
# PAGE CONFIG
# =================================================
st.set_page_config(
    page_title="CrewAI News Intelligence",
    page_icon="📰",
    layout="wide"
)

st.title("📰 News Intelligence Dashboard")
st.caption("Frontend visualization of CrewAI multi-agent pipeline output")

# =================================================
# LOAD OUTPUT.JSON
# =================================================
try:
    with open("output.json", "r", encoding="utf-8") as f:
        raw = f.read()
except FileNotFoundError:
    st.error("❌ output.json not found. Run `python crew.py` first.")
    st.stop()

# =================================================
# SAFE PARSING (LIST OR STRING)
# =================================================
try:
    data = json.loads(raw)
except Exception:
    st.error("❌ output.json is not valid JSON.")
    st.stop()

# Crew may return stringified JSON
if isinstance(data, str):
    try:
        data = json.loads(data)
    except Exception:
        st.error("❌ Crew output is plain text, not JSON.")
        st.stop()

# =================================================
# VALIDATE FORMAT
# =================================================
if not isinstance(data, list):
    st.error("❌ Expected a LIST of merged news articles.")
    st.stop()

if len(data) == 0:
    st.warning("⚠️ No news articles found.")
    st.stop()

df = pd.DataFrame(data)

# =================================================
# SIDEBAR – AGENT PIPELINE
# =================================================
st.sidebar.title("⚙️ Agent Pipeline")

pipeline = [
    "🟢 News Fetch Agent",
    "🟢 News Classification Agent",
    "🟢 Sentiment Analysis Agent",
    "🟢 Breaking News Priority Agent",
    "🟢 News Merge Agent"
]

for step in pipeline:
    st.sidebar.write(step)

st.sidebar.success("Pipeline executed successfully")

# =================================================
# KPI METRICS
# =================================================
st.subheader("📊 Execution Summary")

col1, col2, col3 = st.columns(3)

with col1:
    st.metric("Total Articles", len(df))

with col2:
    st.metric(
        "High Priority News",
        int((df["priority"] == "HIGH").sum())
    )

with col3:
    st.metric(
        "Positive Sentiment",
        int((df["sentiment"] == "Positive").sum())
    )

st.divider()

# =================================================
# FILTERS
# =================================================
st.subheader("🔍 Filter News")

category_filter = st.multiselect(
    "Category",
    options=df["category"].unique(),
    default=list(df["category"].unique())
)

priority_filter = st.multiselect(
    "Priority",
    options=df["priority"].unique(),
    default=list(df["priority"].unique())
)

filtered_df = df[
    (df["category"].isin(category_filter)) &
    (df["priority"].isin(priority_filter))
]

# =================================================
# NEWS DISPLAY
# =================================================
st.subheader("🗞️ News Articles")

for _, row in filtered_df.iterrows():
    with st.expander(f"📰 {row['title']}"):
        st.write(row["description"])
        st.markdown(
            f"""
            **Category:** {row['category']}  
            **Sentiment:** {row['sentiment']}  
            **Priority:** {row['priority']}
            """
        )

# =================================================
# RAW OUTPUT (FOR DEMO / JUDGES)
# =================================================
st.divider()
with st.expander("🧾 View Raw Crew Output"):
    st.json(data)

# =================================================
# FOOTER
# =================================================
st.caption(
    "Built with CrewAI • OpenRouter • Streamlit | "
    "Agent-based News Intelligence System"
)
