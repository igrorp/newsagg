# 📰 newsagg – Multi-Source News Aggregator API

`newsagg` is a pluggable, API-driven platform for aggregating, ranking, and serving news from multiple sources (RSS, APIs, JSON feeds).

---

## 🚀 Features

- 🧩 **Modular Adapter System** for fetching news from:
  - RSS feeds (G1, Folha, BBC, etc.)
  - APIs (NewsAPI.org, Reddit, HackerNews)
- 📊 **Pluggable Ranking Strategies** (recency, popularity, sentiment, etc.)
- 🧠 Group articles by topics or source
- 🌐 RESTful API (FastAPI) to expose article data
- ☁️ Deployable to AWS (Lambda or EC2)

---

## 🛠️ Tech Stack

- **Python 3.10+**
- **FastAPI** for REST API
- **Pydantic** for data validation
- **Feedparser** for RSS ingestion
- **Uvicorn** for local dev server
- **Docker** for containerized deployment
- **AWS** (Lambda, API Gateway, S3, etc. planned)

---

## 🧠 Design Patterns Used

- **Adapter**: Standardize news input formats
- **Strategy**: Switchable article ranking logic
- **Facade**: Simple interface for consuming articles
- **Composite**: Group articles by source, topic, etc.
- *(Optional)* **Observer**: Trigger actions on new article ingestion

---

## 📦 Example API Endpoints

| Method | Route | Description |
|--------|-------|-------------|
| GET    | `/articles` | Get all aggregated articles |
| GET    | `/articles?source=g1` | Filter by source |
| GET    | `/topics/trending` | Group articles by topic |
| POST   | `/rankings/strategy` | Set current ranking strategy |
