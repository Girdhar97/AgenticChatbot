# Stateful Agentic AI with LangGraph & Llama 3

Production-style **agentic AI system** built with **LangGraph, LangChain, Groq (Llama 3), Tavily, and Streamlit**.

It exposes three agents:

1. **Basic Chatbot** – Stateful LLM chatbot with memory.
2. **Chatbot With Web** – Tool-augmented chatbot using Tavily web search (`ToolNode`).
3. **AI News Summarizer** – Multi-step DAG that fetches AI news, summarizes it, and saves markdown reports.

---

## 1. Architecture Overview

### 1.1 Project Pipeline

```text
[User / Browser]
        ↓
[Streamlit UI]
  - Select LLM, model, use case
  - Enter GROQ & Tavily API keys
        ↓
[Groq LLM Config]
  - ChatGroq (Llama 3)
        ↓
[GraphBuilder (LangGraph StateGraph)]
  - Builds graph based on use case:
    - Basic Chatbot
    - Chatbot With Web (ToolNode + tools_condition)
        - AI News (multi-step DAG)
        ↓
[Graph Execution]
  - Nodes call LLM and tools
  - State (messages, news_data, summary, filename) flows between nodes
        ↓
[Output Rendering]
  - Chat responses in Streamlit
  - AI News markdown from ./AINews/<frequency>_summary.md
```

### 1.2 Folder Structure (Simplified)

```bash
AgenticChatbot/
├── app.py
└── src/
    └── langgraphagenticai/
        ├── LLMS/
        │   └── groqllm.py
        ├── graph/
        │   └── graph_builder.py
        ├── nodes/
        │   ├── basic_chatbot_node.py
        │   ├── chatbot_with_Tool_node.py
        │   └── ai_news_node.py
        ├── state/
        │   └── state.py
        ├── tools/
        │   └── search_tool.py
        ├── ui/
        │   └── streamlitui/
        │       ├── loadui.py
        │       ├── display_result.py
        │       └── uiconfigfile.py
        └── main.py
```

---

## 2. Agents & Workflows

### 2.1 Basic Chatbot

**Graph:** `START → chatbot → END`

**Behavior:** Reads messages, calls Llama 3, appends reply via `add_messages`, Streamlit shows user + assistant chat.

### 2.2 Chatbot With Web (Tavily Tool)

**Tools:** Tavily web search via LangGraph `ToolNode`.

**Graph:**

```text
START → Chatbot (LLM with tools)
          ↓
     tools_condition ?
        ├─→ ToolNode(Tavily) → back to Chatbot
        └─→ END
```

**Behavior:** LLM decides when to call tools; answers are grounded in web search results.

### 2.3 AI News Summarizer (Multi-Step DAG)

**Timeframes:** Daily / Weekly / Monthly.

**Nodes:**

- `fetch_news` → Tavily news search, store `news_data`.
- `summarize_news` → LLM markdown summary, store `summary`.
- `save_result` → write `./AINews/<frequency>_summary.md`.

**Graph:** `fetch_news → summarize_news → save_result → END`

---

## 3. Setup & Installation

### 3.1 Prerequisites

- Python 3.10+
- `GROQ_API_KEY` – https://console.groq.com/keys
- `TAVILY_API_KEY` – https://app.tavily.com/home

### 3.2 Clone Repository

```bash
git clone <your-repo-url>.git
cd Stateful_AgenticAI/code/AgenticChatbot
```

### 3.3 Create & Activate Virtual Environment

```bash
python -m venv .venv

# macOS / Linux
source .venv/bin/activate

# Windows (PowerShell)
.venv\Scripts\Activate.ps1
```

### 3.4 Install Dependencies

```bash
pip install -r requirements.txt
```

**Note:** Ensure `requirements.txt` contains: `streamlit`, `langchain`, `langgraph`, `langchain-groq`, `langchain-community`, `tavily-python`, `typing-extensions`, `pydantic`, `python-dotenv`.

### 3.5 Optional: Set Environment Variables

**macOS / Linux:**

```bash
export GROQ_API_KEY="your_groq_api_key"
export TAVILY_API_KEY="your_tavily_api_key"
```

**Windows (PowerShell):**

```powershell
$env:GROQ_API_KEY="your_groq_api_key"
$env:TAVILY_API_KEY="your_tavily_api_key"
```

---

## 4. Run the Application

From the `AgenticChatbot` root:

```bash
streamlit run app.py
```

Then in the browser:

1. Select **LLM** = `Groq` and a Llama 3 model.
2. Enter `GROQ_API_KEY` (and `TAVILY_API_KEY` for "Chatbot With Web" or "AI News").
3. Choose **Usecase**:
   - **Basic Chatbot** – simple chat.
   - **Chatbot With Web** – chat with web search.
   - **AI News** – pick timeframe, click "Fetch Latest AI News".
