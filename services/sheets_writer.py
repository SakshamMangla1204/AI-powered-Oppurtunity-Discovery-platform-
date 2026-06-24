import gspread
from google.oauth2.service_account import Credentials

SCOPES = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive"
]

creds = Credentials.from_service_account_file(
    "credentials.json",
    scopes=SCOPES
)

client = gspread.authorize(creds)
sheet = None


def get_sheet():
    global sheet

    if sheet is None:
        sheet = client.open(
            "company-research-agent"
        ).sheet1

    return sheet


def write_company(data):
    worksheet = get_sheet()
    row = [
        data.get("company_name", ""),
        data.get("website", ""),
        data.get("linkedin", ""),
        data.get("description", ""),
        data.get("hr_email", ""),
        data.get("founder_email", ""),
        data.get("careers_email", ""),
        data.get("apply_email", ""),
        data.get("apply_link", ""),
        data.get("lead_score", ""),
        data.get("status", "")
    ]

    worksheet.append_row(row)
