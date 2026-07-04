import json
from difflib import get_close_matches

from src.base.base_service import BaseService
from src.providers.external.google_sheet_provider import (
    GoogleSheetsProvider
)


class ClientDataRetrievalService(BaseService):
    """
    Retrieves client information from Google Sheets.

    Responsibilities
    ----------------
    1. Validate client exists.
    2. Suggest similar client names.
    3. Parse JSON stored inside Updates column.
    4. Populate WorkflowContext.
    """

    def __init__(self):

        super().__init__(
            service_name="Client Data Retrieval Service",
            service_type="CLIENT_DATA_RETRIEVAL"
        )

        self.google_provider = GoogleSheetsProvider()

    # -------------------------------------------------
    # Validation
    # -------------------------------------------------

    def validate(self, context):

        if context is None:
            raise ValueError(
                "WorkflowContext cannot be None."
            )

        if not context.client_name:
            raise ValueError(
                "Client name is missing."
            )

        return True

    # -------------------------------------------------
    # Utility
    # -------------------------------------------------

    @staticmethod
    def to_float(value):
        """
        Convert KPI values to float.

        Returns None for invalid values.
        """

        if value in (
            None,
            "",
            "null",
            "None"
        ):
            return None

        try:
            return float(value)

        except Exception:
            return None

    # -------------------------------------------------
    # Business Logic
    # -------------------------------------------------

    def process(self, context):

        # ---------------------------------------------
        # Retrieve Client
        # ---------------------------------------------

        client = self.google_provider.get_client(
            context.client_name
        )

        # ---------------------------------------------
        # Client Not Found
        # ---------------------------------------------

        if client is None:

            all_clients = [

                row["Client_name"]

                for row in self.google_provider.get_all_records()

            ]

            suggestions = get_close_matches(
                context.client_name,
                all_clients,
                n=3,
                cutoff=0.60
            )

            if suggestions:

                raise ValueError(
                    f"""
Client '{context.client_name}' does not exist.

Did you mean:

{chr(10).join(suggestions)}
"""
                )

            raise ValueError(
                f"Client '{context.client_name}' does not exist."
            )

        # ---------------------------------------------
        # Parse Updates JSON
        # ---------------------------------------------

        try:

            client_json = json.loads(
                client["Updates"]
            )

        except Exception as error:

            raise ValueError(
                f"Unable to parse Updates JSON : {error}"
            )

        if not client_json:

            raise ValueError(
                "Updates JSON is empty."
            )

        # Google Sheet stores JSON as a list
        client_data = client_json[0]
        print(len(client_data["updates"]))

        # ---------------------------------------------
        # Client Information
        # ---------------------------------------------

        context.client_id = client_data.get(
            "clientId"
        )

        context.client_name = client_data.get(
            "clientName"
        )

        context.program_type = client_data.get(
            "programType"
        )

        context.program_duration = client_data.get(
            "programDuration"
        )

        context.program_stage = client_data.get(
            "programStage"
        )

        context.current_satisfaction = client_data.get(
            "currentSatisfaction"
        )

        context.campaign_status = client_data.get(
            "campaignStatus"
        )

        # ---------------------------------------------
        # KPI Information
        # ---------------------------------------------

        context.current_kpis = {

            "adSpend7D":
                self.to_float(
                    client_data.get("adSpend7D")
                ),

            "adSpendMTD":
                self.to_float(
                    client_data.get("adSpendMTD")
                ),

            "adSpend30D":
                self.to_float(
                    client_data.get("adSpend30D")
                ),

            "leadCost7D":
                self.to_float(
                    client_data.get("leadCost7D")
                ),

            "leadCostMTD":
                self.to_float(
                    client_data.get("leadCostMTD")
                ),

            "leadCost30D":
                self.to_float(
                    client_data.get("leadCost30D")
                ),

            "apptCost7D":
                self.to_float(
                    client_data.get("apptCost7D")
                ),

            "apptCostMTD":
                self.to_float(
                    client_data.get("apptCostMTD")
                ),

            "apptCost30D":
                self.to_float(
                    client_data.get("apptCost30D")
                )

        }

        # ---------------------------------------------
        # Client Updates
        # ---------------------------------------------

        updates = client_data.get(
            "updates",
            []
        )

        updates = sorted(
            updates,
            key=lambda x: x.get(
                "created_at",
                ""
            ),
            reverse=True
        )

        context.client_updates = updates

        context.total_updates = len(
            updates
        )

        context.latest_update = (

            updates[0]

            if updates

            else None

        )

        # ---------------------------------------------
        # Store Raw JSON
        # ---------------------------------------------

        context.google_sheet_data = client_data

        return context