from agents.contact import contact_agent
from agents.research import research_agent
from services.sheets_writer import get_next_new_row, update_company_row


def build_state(row_data):
    return {
        "query": "",
        "companies": [],
        "company_name": row_data.get("company_name", ""),
        "website": row_data.get("website", ""),
        "linkedin": row_data.get("linkedin", ""),
        "description": row_data.get("description", ""),
        "hr_email": row_data.get("hr_email", ""),
        "founder_email": row_data.get("founder_email", ""),
        "careers_email": row_data.get("careers_email", ""),
        "apply_email": row_data.get("apply_email", ""),
        "apply_link": row_data.get("apply_link", ""),
        "lead_score": row_data.get("lead_score", ""),
        "status": row_data.get("status", "NEW")
    }


def run_worker():
    while True:
        next_item = get_next_new_row()

        if next_item is None:
            print("\nNo NEW rows remaining. Worker exiting.")
            break

        row_number = next_item["row_number"]
        state = build_state(next_item["data"])
        company_name = state["company_name"]

        print(f"\n{'=' * 60}")
        print(f"PROCESSING ROW {row_number}: {company_name}")
        print(f"{'=' * 60}\n")

        try:
            state["status"] = "RESEARCHING"
            update_company_row(row_number, state)

            state = research_agent(state)
            update_company_row(row_number, state)

            state["status"] = "CONTACTING"
            update_company_row(row_number, state)

            state = contact_agent(state)
            state["status"] = "COMPLETED"
            update_company_row(row_number, state)

            print(f"Completed: {company_name}")
        except Exception as exc:
            state["status"] = "FAILED"
            update_company_row(row_number, state)
            print(f"Failed: {company_name}")
            print(exc)


if __name__ == "__main__":
    run_worker()
