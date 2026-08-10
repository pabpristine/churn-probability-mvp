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

    def find_by_pattern_key(
        self,
        pattern_key: str
    ):
        """
        Retrieve a KPI pattern by its pattern name.

        The method keeps its existing name for compatibility,
        while the database filter uses the actual column
        `pattern_name`.
        """

        result = self.provider.execute(
            operation="select",
            table=self.table_name,
            filters={
                "pattern_name": pattern_key
            }
        )

        if result and len(result) > 0:
            return result[0]

        return None