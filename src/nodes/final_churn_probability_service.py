from src.base.base_service import BaseService
from src.domain.entities.workflow_context import WorkflowContext
from src.repositories.campaign_stage_repository import (
    CampaignStageRepository
)


class FinalChurnProbabilityService(BaseService):
    """
    Calculates the final churn probability
    using the predefined business rules.

    Business Rules

    Case 1
    --------
    Summary >= 70 and KPI >= 70

        Final Probability = Average
        Risk = High

    Case 2
    --------
    Summary >= 70

        Summary dominates
        Final Probability = Summary Probability
        Risk = High

    Case 3
    --------
    Summary < 70 and KPI < 70

        Fetch campaign weights

        Final Probability =
            Summary × Updates Weight +
            KPI × KPI Weight
    """

    def __init__(self):

        super().__init__(
            service_name="Final Churn Probability Service",
            service_type="BUSINESS"
        )

        self.campaign_stage_repository = (
            CampaignStageRepository()
        )

    # -------------------------------------------------
    # Validation
    # -------------------------------------------------

    def validate(
        self,
        context: WorkflowContext
    ):

        if context.summary_probability is None:

            raise ValueError(
                "Summary probability is required."
            )

        if context.kpi_probability is None:

            raise ValueError(
                "KPI probability is required."
            )

        return True

    # -------------------------------------------------
    # Business Logic
    # -------------------------------------------------

    def process(
        self,
        context: WorkflowContext
    ) -> WorkflowContext:

        summary = context.summary_probability

        kpi = context.kpi_probability

        # ---------------------------------------------
        # Case 1
        # Both probabilities are High
        # ---------------------------------------------

        if summary >= 70 and kpi >= 70:

            context.final_probability = round(
                (
                    summary + kpi
                ) / 2,
                2
            )

            context.risk_level = "High"

        # ---------------------------------------------
        # Case 2
        # Summary dominates
        # ---------------------------------------------

        elif summary >= 70:

            context.final_probability = summary

            context.risk_level = "High"

        # ---------------------------------------------
        # Case 3
        # Weighted Average
        # ---------------------------------------------

        else:

            response = (
                self.campaign_stage_repository.find_by_status(
                    context.campaign_status
                )
            )

            if not response:

                raise Exception(
                    f"No campaign weights found "
                    f"for {context.campaign_status}"
                )

            weights = response[0]

            updates_weight = weights[
                "updates_weight"
            ]

            kpi_weight = weights[
                "kpi_weight"
            ]

            context.final_probability = round(

                (
                    summary * updates_weight
                )
                +
                (
                    kpi * kpi_weight
                ),

                2

            )

            # -----------------------------------------
            # Risk Level
            # -----------------------------------------

            if context.final_probability >= 70:

                context.risk_level = "High"

            elif context.final_probability >= 40:

                context.risk_level = "Medium"

            else:

                context.risk_level = "Low"

        # -------------------------------------------------
        # Merge Summary & KPI Analysis
        # -------------------------------------------------

        analysis = []

        if context.summary_analysis:

            analysis.append(

                f"Summary Analysis\n"
                f"-----------------\n"
                f"{context.summary_analysis}"

            )

        if context.kpi_analysis:

            analysis.append(

                f"KPI Analysis\n"
                f"-------------\n"
                f"{context.kpi_analysis}"

            )

        context.final_analysis = (

            "\n\n"
            "========================================"
            "\n\n"

        ).join(analysis)

        # -------------------------------------------------
        # Merge Red Flags
        # -------------------------------------------------

        context.final_red_flags = list(

            dict.fromkeys(

                context.summary_red_flags
                +

                context.kpi_red_flags

            )

        )

        # -------------------------------------------------
        # Merge Bottlenecks
        # -------------------------------------------------

        context.final_bottlenecks = list(

            dict.fromkeys(

                context.summary_bottlenecks
                +

                context.kpi_bottlenecks

            )

        )

        # -------------------------------------------------
        # Merge Historical Insights
        # -------------------------------------------------

        context.final_historical_insights = list(

            dict.fromkeys(

                context.summary_historical_insights
                +

                context.kpi_historical_insights

            )

        )

        return context