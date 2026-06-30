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

    def find_by_status(
        self,
        status
    ):
        """
        Retrieve KPI and summary weights
        for a campaign stage.
        """

        return self.provider.execute(
            operation="select",
            table=self.table_name,
            filters={
                "status": status
            }
        )