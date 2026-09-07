from src.base.base_repository import BaseRepository


class CampaignStageRepository(BaseRepository):
    """
    Repository responsible for reading
    campaign stage weights.
    """

    def __init__(self):
        super().__init__(
            repository_name="Campaign Stage Repository",
            table_name="campaign_stage_weights"
        )

    # -------------------------------------------------
    # Read
    # -------------------------------------------------

    def find_all(self):
        """
        Retrieve all campaign stages.
        """

        return self.provider.execute(
            operation="select",
            table=self.table_name
        )

    # -------------------------------------------------
    # Business Methods
    # -------------------------------------------------

    def find_by_campaign_stage(
        self,
        campaign_stage: str
    ):
        """
        Retrieve KPI and summary weights
        for a campaign stage.
        """

        result = self.provider.execute(
            operation="select",
            table=self.table_name,
            filters={
                "status": campaign_stage
            }
        )

        if result and len(result) > 0:
            return result[0]

        return None

    def find_by_status(
        self,
        status: str
    ):
        """
        Backward-compatible method.

        The old method name is retained so existing callers
        do not immediately fail. The value is treated as a
        campaign stage and filtered against campaign_stage.
        """

        return self.find_by_campaign_stage(status)