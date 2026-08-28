from src.workflows.ai_workflow_orchestrator import AIWorkflowOrchestrator
from src.api.schemas.client_analysis_response import (
    ClientAnalysisResponse,
    ClientInfo,
    SummaryResult,
    KPIResult,
    HistoricalContext,
    ChurnResult,
)


class ClientAnalysisController:

    def __init__(self):
        self.orchestrator = AIWorkflowOrchestrator()

    def analyze(self, user_query: str) -> ClientAnalysisResponse:

        # Run the complete existing workflow
        context = self.orchestrator.run(user_query)

        # Convert WorkflowContext into API response
        response = ClientAnalysisResponse(

            client=ClientInfo(
                id=context.client_id,
                name=context.client_name,
                program_type=context.program_type,
                program_duration=context.program_duration,
                program_stage=context.program_stage,
                campaign_status=context.campaign_status,
            ),

            summary=SummaryResult(
                text=context.updated_summary,
                satisfaction_score=context.updated_satisfaction_score,
            ),

            kpi=KPIResult(
                interpretation=context.kpi_interpretation,
            ),

            historical_context=HistoricalContext(
                historical_matches=context.historical_matches,
                summary_matches=context.summary_matches,
                kpi_matches=context.kpi_matches,
            ),

            churn=ChurnResult(
                probability=context.final_probability,
                risk_level=context.risk_level,
                analysis=context.final_analysis,
                red_flags=context.final_red_flags,
                bottlenecks=context.final_bottlenecks,
                historical_insights=context.final_historical_insights,
            ),

            recommendations=context.recommendations,

            status=context.workflow_status,
        )

        return response