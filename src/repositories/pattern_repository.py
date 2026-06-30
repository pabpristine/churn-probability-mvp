from src.base.base_repository import BaseRepository


class PatternRepository(BaseRepository):
    """
    Repository responsible for reading KPI
    patterns and their interpretations.
    """

    def __init__(self):

        super().__init__(
            repository_name="Pattern Repository",
            table_name="kpi_patterns"
        )

    # -------------------------------------------------
    # Read
    # -------------------------------------------------

    def find_all(self):
        """
        Retrieve all KPI patterns.
        """

        return self.provider.execute(
            operation="select",
            table=self.table_name
        )

    # -------------------------------------------------
    # Business Methods
    # -------------------------------------------------

    def find_by_pattern_name(
        self,
        pattern_name
    ):
        """
        Retrieve the interpretation
        for a KPI pattern.
        """

        return self.provider.execute(
            operation="select",
            table=self.table_name,
            filters={
                "pattern_name": pattern_name
            }
        )