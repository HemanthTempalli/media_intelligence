from crewai import Task
from agents import (
    news_fetch_agent,
    news_classification_agent,
    news_sentiment_agent,
    news_priority_agent,
    news_merge_agent
)

# =========================
# TASK 1: FETCH NEWS
# =========================
fetch_news_task = Task(
    description=(
        "Use the Serper tool to search Google News for query: {topic}. "
        "From the search results, extract EXACTLY {num_articles} news items. "
        "Return a JSON array where each item has:\n"
        "- title\n"
        "- snippet\n"
        "- clean_text (combine title + snippet)"
    ),
    expected_output=(
        "A JSON array of news articles with title, snippet, and clean_text."
    ),
    agent=news_fetch_agent
)



# =========================
# TASK 2: CLASSIFY NEWS
# =========================
classify_news_task = Task(
    description=(
        "Given the list of news articles from the previous task, "
        "analyze each article's clean_text and classify it into exactly ONE category: "
        "Politics, Sports, Business, Technology, Health, or Entertainment. "
        "Return STRICT JSON."
    ),
    expected_output="JSON classification per article.",
    agent=news_classification_agent
)

# =========================
# TASK 3: SENTIMENT ANALYSIS
# =========================
sentiment_analysis_task = Task(
    description=(
        "For EACH classified news article, analyze the clean_text and determine its sentiment. "
        "Sentiment must be one of: Positive, Negative, Neutral. "
        "Return STRICT JSON with fields: sentiment, confidence (0-100), and reason."
    ),
    expected_output=(
        "A list of JSON objects, one per article, each containing: "
        "sentiment, confidence, and reason."
    ),
    agent=news_sentiment_agent
)

# =========================
# TASK 4: BREAKING NEWS PRIORITIZATION
# =========================
breaking_news_task = Task(
    description=(
        "For EACH news article, determine its priority level. "
        "Priority must be one of: HIGH, MEDIUM, LOW. "
        "Use category, sentiment, and urgency indicators such as "
        "breaking, emergency, crisis, attack, disaster, collapse. "
        "Return STRICT JSON with priority, score (0-100), and reason."
    ),
    expected_output=(
        "A list of JSON objects, one per article, each containing: "
        "priority, score, and reason."
    ),
    agent=news_priority_agent
)

# =========================
# TASK 5: MERGE FINAL OUTPUT
# =========================
merge_output_task = Task(
    description=(
        "For EACH news article, merge all analysis results into ONE final JSON object.\n\n"
        "While merging, ALSO generate a short, clear description (1–2 sentences) "
        "that explains what the news article is about using the title and clean_text.\n\n"
        "The final JSON for each article MUST include:\n"
        "- title\n"
        "- description\n"
        "- category\n"
        "- category_confidence\n"
        "- sentiment\n"
        "- sentiment_confidence\n"
        "- priority\n"
        "- priority_score\n\n"
        "Convert all confidence values to integers between 0 and 100.\n"
        "Return a list of FINAL unified JSON objects, one per article. "
        "Do NOT return anything outside JSON."
    ),
    expected_output=(
        "A list of unified JSON objects with title, description, category, sentiment, "
        "priority, and confidence scores."
    ),
    agent=news_merge_agent
)
