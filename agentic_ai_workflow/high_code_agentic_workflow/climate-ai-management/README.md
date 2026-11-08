```sh
                CLIENT / FRONTEND
                        │
                        ▼
                 FastAPI (main.py)
                        │
                        ▼
                  api/routes.py
                        │
                        ▼
              Google ADK Runner
                        │
                        ▼
              agents/workflow.py
                        │
                 SequentialAgent
                        │
            ┌───────────┴───────────┐
            │                       │
            ▼                       │
     ExtractionAgent                │
            │                       │
            ▼                       │
     Vertex AI / Gemini             │
            │                       │
            ▼                       │
     ADK Session State              │
            │                       │
            ▼                       │
      AnalysisAgent ◄───────────────┘
            │
            ▼
     Vertex AI / Gemini
            │
            ▼
       Final Report
            │
            ▼
      FastAPI Response

```
# prima passo
```sh
              DOCUMENTO PDF
                    │
                    ▼
              PDF PARSER
                    │
                    ▼
           GOOGLE ADK RUNNER
                    │
                    ▼
            SEQUENTIAL AGENT
                    │
                    ▼
          1. EXTRACTION AGENT
             Vertex AI / Gemini
                    │
                    ▼
             extracted_data
                    │
                    ▼
          2. ANALYSIS AGENT
             Vertex AI / Gemini
                    │
                    ▼
             analysis_result
                    │
                    ▼
           3. REPORT AGENT
             Vertex AI / Gemini
                    │
                    ▼
               final_report
                    │
                    ▼
           RAPPORTO STRUTTURATO
```
## Google ADK: Sequential Carbon footprint analysis workflow
```sh
             DOCUMENTO
                 │
                 ▼
          ExtractionAgent
                 │
                 ▼
         ExtractionSchema
                 │
                 ▼
       state["extracted_data"]
                 │
                 ▼
           AnalysisAgent
                 │
                 ▼
          AnalysisSchema
                 │
                 ▼
       state["analysis_result"]
                 │
                 ▼
            ReportAgent
                 │
                 ▼
           ReportSchema
                 │
                 ▼
        state["final_report"]

```
