from agents.discovery import discover_companies
from graph.research_graph import graph
from services.sheets_writer import write_company

query = "AI startups India"
companies = discover_companies(query)

print(f"\nTOTAL COMPANIES FOUND: {len(companies)}")
print(companies)

results = []

for company in companies:

    print(f"\n{'=' * 60}")
    print(f"PROCESSING: {company}")
    print(f"{'=' * 60}\n")

    state = {
        "query": query,
        "companies": companies,

        "company_name": company,

        "website": "",
        "linkedin": "",
        "description": "",

        "hr_email": "",
        "founder_email": "",
        "careers_email": "",

        "apply_email": "",
        "apply_link": "",

        "lead_score": 0,
        "status": "NEW"
    }

    result = graph.invoke(state)
    write_company(result)

    results.append(result)

print("\n\nFINAL RESULTS:\n")

for result in results:
    print(result)
