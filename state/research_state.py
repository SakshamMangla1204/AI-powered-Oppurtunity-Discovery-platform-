from typing import TypedDict

class ResearchState(TypedDict):
    query: str
    companies: list

    company_name: str

    website: str
    linkedin: str
    description: str

    hr_email: str
    founder_email: str
    careers_email: str

    apply_email: str
    apply_link: str

    lead_score: int
    status: str
