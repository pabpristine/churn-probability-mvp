from src.workflows.input_pipeline_orchestrator import InputPipelineOrchestrator
from src.workflows.summary_workflow import SummaryWorkflow
from src.workflows.kpi_workflow import KPIWorkflow
from src.workflows.rag_workflow import RAGWorkflow
from src.workflows.churn_analysis_and_recommendation_generation_workflow import ChurnWorkflow


class AIWorkflowOrchestrator:

    def __init__(self):

        self.input_pipeline = InputPipelineOrchestrator()

        self.summary_workflow = SummaryWorkflow()

        self.kpi_workflow = KPIWorkflow()

        self.rag_workflow = RAGWorkflow()

        self.churn_workflow = ChurnWorkflow()

    def run(self, user_query):

        context = self.input_pipeline.run(user_query)

        context = self.summary_workflow.execute(context)

        context = self.kpi_workflow.execute(context)

        context = self.rag_workflow.execute(context)

        context = self.churn_workflow.execute(context)

        return context