from src.api.schemas.tests_schema import (
    AvailableTestsResponse,
    AvailableTestItem,
    ClientExtractionTestResponse,
    ClientExtractionTestCase,
    ClientDataRetrievalTestResponse,
    AllTestsResponse,
)

from src.tests.unit.nodes.client_name_extraction import (
    run_client_name_extraction_test
)
from src.tests.unit.nodes.client_data_retrieval import (
    run_client_data_retrieval_test
)


class TestsController:

    def get_available_tests(self) -> AvailableTestsResponse:
        return AvailableTestsResponse(
            available_tests=[
                AvailableTestItem(
                    name="client-name-extraction",
                    endpoint="/api/v1/tests/client-name-extraction",
                    description="Runs existing hardcoded client name extraction test cases (9 queries)"
                ),
                AvailableTestItem(
                    name="client-data-retrieval",
                    endpoint="/api/v1/tests/client-data-retrieval",
                    description="Runs existing hardcoded client data retrieval test for Yardworx Land Management"
                ),
                AvailableTestItem(
                    name="run-all",
                    endpoint="/api/v1/tests/run-all",
                    description="Runs all existing node test suites and returns individual test outputs"
                )
            ]
        )

    def run_client_name_extraction(self) -> ClientExtractionTestResponse:
        results_data = run_client_name_extraction_test()
        test_cases = [
            ClientExtractionTestCase(**item) for item in results_data
        ]
        return ClientExtractionTestResponse(
            total_cases=len(test_cases),
            results=test_cases
        )

    def run_client_data_retrieval(self) -> ClientDataRetrievalTestResponse:
        res = run_client_data_retrieval_test()
        return ClientDataRetrievalTestResponse(
            client_id=res.get("client_id"),
            client_name=res.get("client_name"),
            program_type=res.get("program_type"),
            program_stage=res.get("program_stage"),
            campaign_status=res.get("campaign_status"),
            current_satisfaction=res.get("current_satisfaction"),
            current_kpis=res.get("current_kpis", {}),
            total_updates=res.get("total_updates", 0),
            latest_update=res.get("latest_update")
        )

    def run_all_tests(self) -> AllTestsResponse:
        extraction_res = self.run_client_name_extraction()
        retrieval_res = self.run_client_data_retrieval()

        return AllTestsResponse(
            status="completed",
            test_suites={
                "client_name_extraction": extraction_res.model_dump(),
                "client_data_retrieval": retrieval_res.model_dump()
            }
        )
