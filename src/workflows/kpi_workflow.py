from src.base.base_workflow import BaseWorkflow
from src.services.kpi_analysis_service import KPIAnalysisService
from src.services.kpi_data_service import KPIDataService
from src.services.kpi_embedding_service import KPIEmbeddingService


# Workflow responsible for running KPI-related services
# in the required sequence.
class KPIWorkflow(BaseWorkflow):
    """
    Workflow that fetches KPI data, performs KPI analysis,
    and creates KPI embeddings.
    """

    def __init__(self):
        # Initialize the workflow with a readable workflow name.
        super().__init__("KPI Workflow")

    def build_workflow(self):
        # First step: fetch and prepare KPI data.
        self.add_service(KPIDataService())

        # Second step: analyze the prepared KPI data.
        self.add_service(KPIAnalysisService())

        # Third step: generate and persist KPI embeddings.
        self.add_service(KPIEmbeddingService())