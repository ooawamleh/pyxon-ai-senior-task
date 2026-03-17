```markdown
# 🛡️ GIL: Multi-Agent Intelligence Swarm (Enterprise Edition)

**Global Intelligence Liaison (GIL)** is a strategic geopolitical intelligence desk powered by a highly orchestrated **Multi-Agent Swarm**. Designed for enterprise-grade performance, GIL dynamically processes ambiguous queries, fetches real-time data, and synthesizes complex intelligence using an **Ephemeral RAG** architecture and **Self-Healing Semantic Caching**.

## 🧠 Swarm Architecture & High-Performance Pipeline

GIL utilizes a **7-Agent Pipeline** built with LangChain (LCEL) to ensure high accuracy and low latency:

1.  **Agent 1: The Clarifier (Time-Aware):** Analyzes intent and auto-corrects queries. [cite_start]It uses **Dynamic Date Injection** to ground relative time (e.g., "last 2 days") into absolute calendar dates[cite: 1, 2].
2.  [cite_start]**Agent 2: The Expander (Search Strategist):** Generates 3 optimized search variations while maintaining a **Context Anchor** to prevent subject drift[cite: 1, 2].
3.  **Agent 3: Multi-Source Fetcher:**
    * [cite_start]*Targeted Search:* Queries verified defense/news domains via SerpAPI[cite: 1, 2].
    * [cite_start]*URL/API Ingestion:* Dynamically scrapes and parses user-provided links using BeautifulSoup[cite: 1, 2].
4.  [cite_start]**Agent 4: The Synthesizer:** Resolves contradictions and highlights multimodal evidence (satellite, video)[cite: 1, 2].
5.  [cite_start]**Agent 5: The Final Responder:** Formats intelligence into a strict **SITREP** or **Strategic Analysis** based on dynamic path routing[cite: 1, 2].
6.  [cite_start]**Agent 6: Background Cache Manager:** A persistent FAISS store that serves identical requests instantly[cite: 1, 2].
7.  **The Quality Gate (Self-Healing):** A background process that inspects cached responses. [cite_start]If a response contains "no data found," it is flagged as "poisoned" and bypassed to ensure only high-quality intelligence is served[cite: 1, 2].

## 🚀 Key Enterprise Features

* [cite_start]**Asynchronous Processing:** Final responses are delivered immediately while caching tasks run in the background via FastAPI `BackgroundTasks`[cite: 1, 2].
* [cite_start]**Model Agnostic (OpenRouter):** Integrated with OpenRouter to allow seamless switching between LLMs (Gemini, Claude, Llama)[cite: 1, 2].
* [cite_start]**Zero-Hallucination Policy:** The system is instructed to admit lack of data rather than fabricating intelligence[cite: 1, 2].

## 🛠️ Tech Stack

* **Orchestration:** LangChain (LCEL)
* **Backend:** FastAPI (Microservice Architecture)
* **LLM:** openrouter/free (via OpenRouter)
* **Vector DB:** FAISS (Local persistent store)
* **Deployment:** Docker & Docker Compose

## 📋 Environment Setup

Create a `.env` file:
```env
OPENROUTER_API_KEY="your_key"
SERPAPI_API_KEY="your_key"
```

## 🚀 Deployment

### Docker (Recommended)
```bash
docker-compose up --build
```
The system is deployed at `https://huggingface.co/spaces/Ounaa2003/gil-intelligence-swarm`.

---
**Author:** Oun Alawamleh
*AI Engineer*
```
