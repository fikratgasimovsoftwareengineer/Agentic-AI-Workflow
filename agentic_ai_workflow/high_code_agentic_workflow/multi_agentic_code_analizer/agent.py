from google.adk.agents.llm_agent import Agent
from google.adk.agents.sequential_agent import SequentialAgent
from google.adk.agents.parallel_agent import ParallelAgent
from google.adk.agents.llm_agent import LlmAgent
from google.adk.models.lite_llm import LiteLlm

from .agents.code_syntax_analizer import CodeSyntaxAnalyzerAgent
from .agents.code_logical_analizer import CodeLogicAnalyzerAgent
from .agents.code_report_generator import CodeReportGeneratorAgent
from .agents.optimizazione_del_codice import OptimizationAgent
from .config import CODICE_OLLAMA_MODEL, REPORT_OLLAMA_MODEL


### report generator

root_agent = SequentialAgent(
    name="CodePipelineAgent",
    sub_agents=[
        # Step 1 — Syntax e Logic in parallelo
        ParallelAgent(
            name="ParallelAnalysis",
            description="Analizza sintassi e logica del codice in parallelo.",
            sub_agents=[
                CodeSyntaxAnalyzerAgent(),
                CodeLogicAnalyzerAgent()
            ],
        ),
        #Step 2.  Report basato sui risultati del parallelo
        CodeReportGeneratorAgent(),
        OptimizationAgent(),
    ],
)