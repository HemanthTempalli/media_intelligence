from crewai import Crew, Process

import json

# =========================
# IMPORT TASKS
# =========================
from tasks import (
    fetch_news_task,
    classify_news_task,
    sentiment_analysis_task,
    breaking_news_task,
    merge_output_task
)

# =========================
# IMPORT AGENTS
# =========================
from agents import (
    news_fetch_agent,
    news_classification_agent,
    news_sentiment_agent,
    news_priority_agent,
    news_merge_agent
)

# =================================================
# FORM THE NEWS INTELLIGENCE CREW
# =================================================
news_crew = Crew(
    agents=[
        news_fetch_agent,
        news_classification_agent,
        news_sentiment_agent,
        news_priority_agent,
        news_merge_agent
    ],
    tasks=[
        fetch_news_task,
        classify_news_task,
        sentiment_analysis_task,
        breaking_news_task,
        merge_output_task
    ],
    process=Process.sequential,  # STRICT PIPELINE EXECUTION
    verbose=True
)

# =================================================
# START EXECUTION
# =================================================
if __name__ == "__main__":
    result = news_crew.kickoff(
        inputs={
            "topic": "latest news",
            "num_articles": 3
        }
    )

    print("\n==============================")
    print("FINAL NEWS INTELLIGENCE OUTPUT")
    print("==============================\n")
    print(result)


# after print(result)
with open("output.json", "w", encoding="utf-8") as f:
    json.dump(result, f, indent=2)
