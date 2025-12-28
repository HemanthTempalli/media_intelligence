from crewai import Agent
from langchain_openai import ChatOpenAI
from dotenv import load_dotenv
import os

from tools import serper_tool


# Load environment variables
load_dotenv()

# =========================
# OPENROUTER LLM CONFIG
# =========================
llm = ChatOpenAI(
    model="openai/gpt-4o-mini",
    openai_api_key=os.getenv("OPENROUTER_API_KEY"),
    base_url="https://openrouter.ai/api/v1",
    temperature=0.2
)

# =========================
# AGENT 1: NEWS FETCH AGENT
# =========================
news_fetch_agent = Agent(
    role="News Fetch Agent",
    goal="Fetch latest news articles from Google News using SERP API based on a given query",
    verbose=True,
    memory=False,
    backstory=(
        "You are a professional news aggregator. "
        "You specialize in collecting real-time news from trusted sources "
        "and presenting it in a clean, structured format for further analysis."
    ),
    tools=[serper_tool],
    llm=llm,
    allow_delegation=False,
    max_iter=1
)

# =========================
# AGENT 2: NEWS CLASSIFICATION AGENT (STRICT)
# =========================
news_classification_agent = Agent(
    role="News Classification Agent",
    goal=(
        "Analyze the news article text and classify it into EXACTLY ONE category.\n\n"
        "Allowed categories ONLY:\n"
        "- Politics\n"
        "- Sports\n"
        "- Business\n"
        "- Technology\n"
        "- Health\n"
        "- Entertainment\n\n"
        "IMPORTANT RULES:\n"
        "- Do NOT invent new categories\n"
        "- If the article is economic or financial, choose Business\n"
        "- Always return STRICT JSON with fields: category, confidence (0-100), reason"
    ),
    verbose=True,
    memory=False,
    backstory="You are an expert news analyst with deep domain knowledge.",
    tools=[],
    llm=llm,
    allow_delegation=False
)

# =========================
# AGENT 3: SENTIMENT ANALYSIS AGENT
# =========================
news_sentiment_agent = Agent(
    role="News Sentiment Analyst",
    goal=(
        "Analyze the sentiment of each news article.\n"
        "Sentiment must be one of: Positive, Negative, Neutral.\n"
        "Return STRICT JSON with sentiment, confidence (0-100), and reason."
    ),
    verbose=True,
    memory=False,
    backstory="You are an expert in sentiment analysis.",
    tools=[],
    llm=llm,
    allow_delegation=False
)

# =========================
# AGENT 4: BREAKING NEWS PRIORITIZATION AGENT
# =========================
news_priority_agent = Agent(
    role="Breaking News Prioritization Agent",
    goal=(
        "Assign a priority level to each news article: HIGH, MEDIUM, or LOW.\n"
        "Consider urgency, public impact, category, sentiment, and keywords.\n"
        "Return STRICT JSON with priority, score (0-100), and reason."
    ),
    verbose=True,
    memory=False,
    backstory="You are a senior newsroom editor.",
    tools=[],
    llm=llm,
    allow_delegation=False
)

# =========================
# AGENT 5: MERGE FINAL OUTPUT
# =========================
news_merge_agent = Agent(
    role="News Output Merger",
    goal=(
        "Merge classification, sentiment, and priority outputs into "
        "one final unified JSON object per news article.\n\n"
        "RULES:\n"
        "- Convert ALL confidence values to integers between 0 and 100\n"
        "- Ensure category is valid\n"
        "- Generate a short description (1–2 sentences)\n"
        "- Output ONLY valid JSON"
    ),
    backstory="You are a data unification specialist.",
    llm=llm,
    verbose=True,
    memory=False,
    allow_delegation=False
)
