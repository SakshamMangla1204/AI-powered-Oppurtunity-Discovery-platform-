import json
import os

from dotenv import load_dotenv
from langchain_groq import ChatGroq
from tavily import TavilyClient

load_dotenv()

tavily = TavilyClient(
    api_key=os.getenv("TAVILY_API_KEY")
)

llm = ChatGroq(
    model="llama-3.3-70b-versatile",
    groq_api_key=os.getenv("GROQ_API_KEY"),
    temperature=0
)


def _extract_json_array(content: str) -> list[str]:
    content = content.strip()

    if content.startswith("```"):
        lines = content.splitlines()
        if lines and lines[0].startswith("```"):
            lines = lines[1:]
        if lines and lines[-1].startswith("```"):
            lines = lines[:-1]
        content = "\n".join(lines).strip()

    start = content.find("[")
    end = content.rfind("]")

    if start == -1 or end == -1 or end < start:
        raise ValueError("Gemini response did not contain a JSON array.")

    companies = json.loads(content[start:end + 1])

    if not isinstance(companies, list):
        raise ValueError("Gemini response was not a list.")

    unique_companies = []
    seen = set()

    for company in companies:
        if not isinstance(company, str):
            continue

        name = company.strip()
        key = name.lower()

        if not name or key in seen:
            continue

        seen.add(key)
        unique_companies.append(name)

        if len(unique_companies) == 10:
            break

    return unique_companies


def discover_companies(query: str) -> list[str]:
    print("\n===== DISCOVERY =====")
    print("Query:", query)

    response = tavily.search(
        query=query,
        max_results=10
    )

    combined_content = ""

    for result in response["results"]:
        combined_content += f"""
TITLE: {result.get('title')}

URL: {result.get('url')}

CONTENT:
{result.get('content')}

----------------------------------
"""

    prompt = f"""
You are a company extraction agent.

Extract only real company or startup names related to the query.

Return ONLY valid JSON.

Format:
[
  "Company 1",
  "Company 2",
  "Company 3"
]

Rules:
- Only company names.
- Remove duplicates.
- No explanations.
- No markdown.
- No numbering.
- Limit the final list to 10 companies.

QUERY:
{query}

TEXT:
{combined_content}
"""

    result = llm.invoke(prompt)
    companies = _extract_json_array(result.content)

    print("Discovered companies:", companies)

    return companies
