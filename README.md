# News Intelligence Crew - Project Documentation

## 📋 Overview

This project is a **CrewAI-based News Intelligence Pipeline** that automates the process of fetching, classifying, analyzing sentiment, prioritizing, and merging news articles. It uses a multi-agent architecture where each agent is responsible for a specific task in the news processing workflow.

---

## 🏗️ Project Structure

```
crew/
├── agents.py         # Defines all AI agents
├── crew.py           # Orchestrates the crew and execution
├── tasks.py          # Defines tasks for each agent
├── tools.py          # External tools (Serper API, validation)
├── requirements.txt  # Python dependencies
└── __pycache__/      # Python cache
```

---

## 📦 Dependencies

| Package               | Purpose                                      |
|-----------------------|----------------------------------------------|
| `crewai`              | Multi-agent orchestration framework          |
| `crewai-tools`        | Pre-built tools for CrewAI (SerperDevTool)   |
| `langchain-openai`    | OpenAI/OpenRouter LLM integration            |
| `langchain-google-genai` | Google Generative AI integration          |
| `python-dotenv`       | Environment variable management              |

### Installation

```bash
pip install -r requirements.txt
```

---

## 🔑 Environment Variables

Create a `.env` file in the project root with the following keys:

```env
OPENROUTER_API_KEY=your_openrouter_api_key
SERPER_API_KEY=your_serper_api_key
```

| Variable             | Description                                  |
|----------------------|----------------------------------------------|
| `OPENROUTER_API_KEY` | API key for OpenRouter (LLM provider)        |
| `SERPER_API_KEY`     | API key for Serper (Google News search)      |

---

## 🤖 Agents

The project uses **5 specialized agents**, each with a distinct role:

### 1. News Fetch Agent
- **Role**: News Fetch Agent
- **Goal**: Fetch latest news articles from Google News using SERP API
- **Tools**: `SerperDevTool` (news search)
- **Backstory**: Professional news aggregator specializing in real-time news collection

### 2. News Classification Agent
- **Role**: News Classification Agent
- **Goal**: Classify news into one of 6 categories:
  - Politics
  - Sports
  - Business
  - Technology
  - Health
  - Entertainment
- **Output**: JSON with `category`, `confidence`, and `reason`

### 3. News Sentiment Agent
- **Role**: News Sentiment Analyst
- **Goal**: Analyze sentiment of each article
- **Sentiment Values**: Positive, Negative, Neutral
- **Output**: JSON with `sentiment`, `confidence`, and `reason`

### 4. News Priority Agent
- **Role**: Breaking News Prioritization Agent
- **Goal**: Assign priority levels (HIGH, MEDIUM, LOW)
- **Criteria**: Urgency, public impact, category, sentiment, keywords (breaking, emergency, crisis, etc.)
- **Output**: JSON with `priority`, `score`, and `reason`

### 5. News Merge Agent
- **Role**: News Output Merger
- **Goal**: Merge all analysis results into unified JSON objects
- **Output**: Final structured JSON with all fields

---

## 📝 Tasks

### Task 1: Fetch News
```
Input: {topic}, {num_articles}
Output: JSON array with title, snippet, clean_text
```

### Task 2: Classify News
```
Input: News articles from Task 1
Output: JSON classification per article (category, confidence, reason)
```

### Task 3: Sentiment Analysis
```
Input: Classified news articles
Output: JSON with sentiment, confidence, reason per article
```

### Task 4: Breaking News Prioritization
```
Input: News articles with sentiment
Output: JSON with priority, score, reason per article
```

### Task 5: Merge Final Output
```
Input: All previous analysis results
Output: Unified JSON objects with all fields merged
```

---

## 🔧 Tools

### SerperDevTool
- **Type**: External API tool
- **Purpose**: Search Google News via Serper API
- **Configuration**: `search_type="news"`

### Validation Tool
- **Type**: Custom tool
- **Purpose**: Validate final merged output
- **Required Fields**:
  - `title`
  - `description`
  - `category`
  - `category_confidence`
  - `sentiment`
  - `sentiment_confidence`
  - `priority`
  - `priority_score`

---

## 🔄 Pipeline Flow

```
┌─────────────────┐
│  User Input     │
│  (topic, count) │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│ 1. Fetch News   │ ◄─── SerperDevTool (Google News)
│    Agent        │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│ 2. Classify     │
│    Agent        │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│ 3. Sentiment    │
│    Agent        │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│ 4. Priority     │
│    Agent        │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│ 5. Merge        │
│    Agent        │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│  Final JSON     │
│  Output         │
└─────────────────┘
```

---

## 🚀 Usage

### Running the Pipeline

```bash
python crew.py
```

### Default Configuration
- **Topic**: "latest news"
- **Number of Articles**: 3

### Custom Execution
Modify the `inputs` in `crew.py`:

```python
result = news_crew.kickoff(
    inputs={
        "topic": "artificial intelligence",
        "num_articles": 5
    }
)
```

---

## 📤 Output Format

The final output is a JSON array where each article contains:

```json
[
  {
    "title": "Article Title",
    "description": "1-2 sentence summary",
    "category": "Technology",
    "category_confidence": 85,
    "sentiment": "Positive",
    "sentiment_confidence": 90,
    "priority": "HIGH",
    "priority_score": 75
  }
]
```

---

## ⚙️ LLM Configuration

| Setting        | Value                              |
|----------------|------------------------------------|
| **Provider**   | OpenRouter                         |
| **Model**      | `openai/gpt-4o-mini`               |
| **Base URL**   | `https://openrouter.ai/api/v1`     |
| **Temperature**| 0.2 (for consistent outputs)       |

---

## 📊 Process Type

The crew uses **Sequential Process** (`Process.sequential`), meaning:
- Tasks execute one after another
- Each task receives output from the previous task
- Ensures strict pipeline execution order

---

## 🛠️ Key Features

| Feature                  | Description                                      |
|--------------------------|--------------------------------------------------|
| Multi-Agent Architecture | 5 specialized agents with distinct roles         |
| Sequential Pipeline      | Strict task execution order                      |
| Strict JSON Output       | All outputs in structured JSON format            |
| Configurable Categories  | 6 predefined news categories                     |
| Sentiment Analysis       | 3-tier sentiment classification                  |
| Priority Scoring         | 3-level priority with 0-100 scoring              |
| Validation Tool          | Built-in output validation                       |

---

## 📁 File Descriptions

| File              | Description                                                  |
|-------------------|--------------------------------------------------------------|
| `agents.py`       | Defines 5 AI agents with roles, goals, and configurations    |
| `tasks.py`        | Defines 5 tasks assigned to respective agents                |
| `tools.py`        | Serper search tool and validation tool                       |
| `crew.py`         | Main entry point; creates and executes the crew              |
| `requirements.txt`| Python package dependencies                                  |

---

## 🔒 Error Handling

- **Missing `SERPER_API_KEY`**: Raises `RuntimeError` with clear message
- **Invalid Output Structure**: Validation tool reports missing keys
- **Non-list Output**: Validation tool rejects with failure status

---

## 📝 Notes

1. **Memory is disabled** for all agents (`memory=False`)
2. **Delegation is disabled** for all agents (`allow_delegation=False`)
3. **Verbose mode is enabled** for debugging and monitoring
4. The News Fetch Agent has `max_iter=1` to limit iterations

---

## 🎯 Use Cases

- Real-time news monitoring dashboards
- Automated news categorization systems
- Sentiment tracking for news topics
- Breaking news alert systems
- News aggregation platforms

---

*Generated for the News Intelligence Crew project*
