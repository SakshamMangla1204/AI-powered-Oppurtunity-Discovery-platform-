# AI-powered Opportunity Discovery Platform

A Python-based agentic research pipeline that discovers companies from a user query, researches each company, extracts hiring/contact information, and stores the results in Google Sheets.

## What This Project Does

Given a search query such as:

```text
AI startups India
```

the project:

1. discovers relevant companies from the web
2. researches each company
3. extracts career and HR contact information
4. writes the final result to a Google Sheet

This turns ad-hoc research into a repeatable pipeline.

## Current Architecture

```text
User Query
↓
Discovery Agent
    Tavily + Groq
↓
Companies List
↓
For each company
    Research Agent
        Tavily + Ollama (Qwen3:8B)
    Contact Agent
        Tavily + Groq
↓
Google Sheets
```

## Active Flow

The main runtime entry point is [main.py](./main.py).

It currently:

1. sets a query
2. runs discovery before LangGraph starts
3. loops through discovered companies
4. invokes the LangGraph research pipeline for each company
5. writes every final result to Google Sheets

## LangGraph Pipeline

The active graph is defined in [graph/research_graph.py](./graph/research_graph.py).

Current graph:

```text
Research → Contact → END
```

The scoring agent file still exists in the repo, but it is not part of the active graph right now.

## Agents

### 1. Discovery Agent

File: [agents/discovery.py](./agents/discovery.py)

Responsibilities:

- take a query string
- search Tavily for relevant web results
- send the combined search content to Groq
- extract a clean JSON array of company names
- return up to 10 companies

Current model:

- `ChatGroq`
- model: `llama-3.3-70b-versatile`

### 2. Research Agent

File: [agents/research.py](./agents/research.py)

Responsibilities:

- search for the official website
- search for the LinkedIn page
- generate a short company description

Fields filled:

- `company_name`
- `website`
- `linkedin`
- `description`

Current model:

- `ChatOllama`
- model: `qwen3:8b`

### 3. Contact Agent

File: [agents/contact.py](./agents/contact.py)

Responsibilities:

- search for careers and job links
- extract HR-related contact details
- return structured JSON

Fields filled:

- `apply_link`
- `careers_email`
- `hr_email`

Current model:

- `ChatGroq`
- model: `llama-3.3-70b-versatile`

Status logic:

- sets `status = "CONTACT_FOUND"` if `apply_link` exists
- otherwise sets `status = "RESEARCHED"`

## State Object

The shared state is defined in [state/research_state.py](./state/research_state.py).

Main fields:

- `query`
- `companies`
- `company_name`
- `website`
- `linkedin`
- `description`
- `hr_email`
- `founder_email`
- `careers_email`
- `apply_email`
- `apply_link`
- `lead_score`
- `status`

Not every field is actively populated by the current pipeline. Some are placeholders for future expansion.

## Google Sheets Integration

File: [services/sheets_writer.py](./services/sheets_writer.py)

The project writes one row per company into a Google Sheet named:

```text
company-research-agent
```

The writer uses:

- `gspread`
- a Google service account
- a local `credentials.json` file

Each row currently includes:

- company name
- website
- LinkedIn
- description
- HR email
- founder email
- careers email
- apply email
- apply link
- lead score
- status

## Project Structure

```text
.
├── agents/
│   ├── contact.py
│   ├── discovery.py
│   ├── enrichment.py
│   ├── memory.py
│   ├── qc.py
│   ├── research.py
│   ├── scoring.py
│   └── verification.py
├── graph/
│   ├── discovery_graph.py
│   └── research_graph.py
├── services/
│   └── sheets_writer.py
├── state/
│   ├── discovery_state.py
│   └── research_state.py
├── main.py
├── test_contact.py
├── test_discovery.py
├── test_ollama.py
├── test_research.py
├── test_sheet.py
└── test_tavily.py
```

## Setup

### 1. Create and activate a virtual environment

```bash
python3 -m venv venv
source venv/bin/activate
```

### 2. Install dependencies

Because `requirements.txt` is currently empty, install the libraries used by the project directly:

```bash
pip install langgraph tavily-python python-dotenv langchain-groq langchain-ollama gspread google-auth
```

### 3. Create `.env`

Example:

```env
TAVILY_API_KEY=your_tavily_key
GROQ_API_KEY=your_groq_key
```

### 4. Add Google Sheets credentials

Place your Google service account JSON file in the project root as:

```text
credentials.json
```

### 5. Make sure Ollama is running locally

You need Ollama available for the Research Agent:

```bash
ollama serve
ollama pull qwen3:8b
```

## How To Run

Run the full pipeline:

```bash
python3 main.py
```

Expected flow:

1. discovery runs for the query
2. company count is printed
3. each company is processed through the research graph
4. each final result is appended to Google Sheets
5. final results are printed in the terminal

## Test Scripts

The repo includes small manual test files:

- [test_discovery.py](./test_discovery.py)
- [test_research.py](./test_research.py)
- [test_contact.py](./test_contact.py)
- [test_tavily.py](./test_tavily.py)
- [test_sheet.py](./test_sheet.py)
- [test_ollama.py](./test_ollama.py)

These are simple runnable scripts for checking individual parts of the system.

## Current Strengths

- clear agent separation
- query-to-sheet automation
- practical use of Tavily for web search
- LangGraph orchestration for multi-step research
- mixed-model architecture to balance cost and capability

## Current Limitations

- `requirements.txt` is not yet maintained
- some files in the repo are placeholders or not part of the active runtime
- model/provider usage is mixed by design and depends on both cloud and local services
- discovery and contact quality still depend heavily on search result quality
- the Google Sheet schema still includes some fields that the current pipeline does not fully use

## Future Improvements

- maintain a proper `requirements.txt`
- add better parsing validation for model outputs
- add structured logging
- improve contact extraction accuracy
- clean unused placeholder files
- add real automated tests
- support configurable queries from CLI or UI

## Summary

This project is an agentic company research pipeline for opportunity discovery.

It combines:

- Tavily for web search
- Groq for high-quality company discovery and contact extraction
- Ollama/Qwen3:8B for local company research
- LangGraph for orchestration
- Google Sheets for persistent storage

The result is a practical workflow for finding companies, researching them, and storing structured opportunity data automatically.
