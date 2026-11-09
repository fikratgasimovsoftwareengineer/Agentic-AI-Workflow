from climate_ai_management.schemas.extration_schema import ExtractionSchema


data = ExtractionSchema(
    company="Demo Company",
    year= 2025,
    scope_1_tco2e=120.0,
    scope_2_tco2e=80.0,
    scope_3_tco2e=None,
    declared_total_tco2=250.0,
    evidence=["Scope 1: 120 tCO2e", "Scope 2: 80 tCO2e"],
    missing_fields=["Scope 3 emissions"]
)

print(data.model_dump_json(indent=2))