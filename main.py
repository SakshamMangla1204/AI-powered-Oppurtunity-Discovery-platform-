from agents.discovery import discover_companies
from services.sheets_writer import enqueue_companies
from worker import run_worker

query = "AI startups India"
companies = discover_companies(query)

print(f"\nTOTAL COMPANIES FOUND: {len(companies)}")
print(companies)
added_count = enqueue_companies(companies)

print(f"\nNEW COMPANIES ADDED TO SHEET: {added_count}")

run_worker()
