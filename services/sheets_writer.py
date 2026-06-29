import gspread
from google.oauth2.service_account import Credentials

SCOPES = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive"
]

HEADERS = [
    "company_name",
    "website",
    "linkedin",
    "description",
    "hr_email",
    "founder_email",
    "careers_email",
    "apply_email",
    "apply_link",
    "lead_score",
    "status"
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


def ensure_headers():
    worksheet = get_sheet()
    first_row = worksheet.row_values(1)

    if not first_row:
        worksheet.append_row(HEADERS)


def build_row(data):
    return [data.get(header, "") for header in HEADERS]


def row_to_data(row):
    padded_row = list(row[:len(HEADERS)])

    while len(padded_row) < len(HEADERS):
        padded_row.append("")

    return dict(zip(HEADERS, padded_row))


def write_company(data):
    worksheet = get_sheet()
    ensure_headers()
    worksheet.append_row(build_row(data))


def enqueue_companies(companies):
    worksheet = get_sheet()
    ensure_headers()

    existing_rows = worksheet.get_all_values()[1:]
    existing_names = {
        row[0].strip().lower()
        for row in existing_rows
        if row and row[0].strip()
    }

    new_rows = []

    for company in companies:
        name = company.strip()

        if not name or name.lower() in existing_names:
            continue

        existing_names.add(name.lower())
        new_rows.append(build_row({
            "company_name": name,
            "status": "NEW"
        }))

    if new_rows:
        worksheet.append_rows(new_rows)

    return len(new_rows)


def get_next_new_row():
    worksheet = get_sheet()
    ensure_headers()

    rows = worksheet.get_all_values()

    for index, row in enumerate(rows[1:], start=2):
        data = row_to_data(row)

        if data["status"] == "NEW" and data["company_name"]:
            return {
                "row_number": index,
                "data": data
            }

    return None


def update_company_row(row_number, data):
    worksheet = get_sheet()
    ensure_headers()
    worksheet.update(f"A{row_number}:K{row_number}", [build_row(data)])

