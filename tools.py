"""
tools.py
---------
Tools for fetching and validating news articles.
"""

import os
from dotenv import load_dotenv
from crewai_tools import SerperDevTool, tool

# =================================================
# LOAD ENV VARIABLES
# =================================================
load_dotenv()

"""
tools.py
---------
CrewAI tools (Serper only).
"""

import os
from dotenv import load_dotenv
from crewai_tools import SerperDevTool

# =================================================
# LOAD ENV VARIABLES
# =================================================
load_dotenv()

# =================================================
# SERPER API CHECK
# =================================================
if not os.getenv("SERPER_API_KEY"):
    raise RuntimeError("❌ SERPER_API_KEY not found in environment")

# =================================================
# EXPOSE SERPER TOOL DIRECTLY (NO WRAPPER!)
# =================================================
serper_tool = SerperDevTool(search_type="news")



# =================================================
# TOOL 2: VALIDATION TOOL
# =================================================
@tool("validation_tool")
def validation_tool(final_output):
    """
    Validate final merged news intelligence output.
    """
    required_keys = {
        "title",
        "description",
        "category",
        "category_confidence",
        "sentiment",
        "sentiment_confidence",
        "priority",
        "priority_score"
    }

    if not isinstance(final_output, list):
        return {"status": "fail", "reason": "Final output must be a list"}

    results = []

    for item in final_output:
        if not isinstance(item, dict):
            results.append({"status": "fail", "reason": "Item not a dictionary"})
            continue

        missing = required_keys - item.keys()
        if missing:
            results.append({
                "status": "fail",
                "reason": f"Missing keys: {list(missing)}"
            })
            continue

        results.append({"status": "pass", "result": item})

    return results
