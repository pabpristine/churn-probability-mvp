from src.base.base_workflow import BaseWorkflow
from src.services.kpi_analysis_service import KPIAnalysisService
from src.services.kpi_data_service import KPIDataService


class KPIWorkflow(BaseWorkflow):
    """
    Workflow that fetches KPI data and then performs KPI analysis.
    """

    def __init__(self):
        super().__init__("KPI Workflow")

    def build_workflow(self):
        self.add_service(KPIDataService())
        self.add_service(KPIAnalysisService())