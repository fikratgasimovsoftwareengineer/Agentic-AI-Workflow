from climate_ai_management.services.document_parser import parse_pdf


document = parse_pdf("/home/fikrat/Agentic-AI-Workflow/agentic_ai_workflow/high_code_agentic_workflow/climate-ai-management/tests/files/carbon_footprint_sample_2025.pdf")

print(document.document_id)
print(document.filename)

for page in document.page_block:
    print(f"\n--- PAGE {page.page_number} ---")
    print(page.page_text)
