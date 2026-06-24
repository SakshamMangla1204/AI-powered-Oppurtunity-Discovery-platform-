from services.sheets_writer import write_company

write_company({
    "company_name": "TEST COMPANY",
    "website": "https://test.com",
    "linkedin": "https://linkedin.com/company/test",
    "description": "Google Sheets integration test",
    "hr_email": "hr@test.com",
    "founder_email": "founder@test.com",
    "careers_email": "careers@test.com",
    "apply_email": "apply@test.com",
    "apply_link": "https://test.com/careers",
    "lead_score": 100,
    "status": "TEST"
})

print("SUCCESS: Row added to Google Sheet")
