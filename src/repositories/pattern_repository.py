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
        result = self.provider.execute(
            operation="select",
            table=self.table_name
        )

        return getattr(result, "data", result)

    # -------------------------------------------------
    # Business Methods
    # -------------------------------------------------

    def find_by_pattern_name(self, pattern_name: str):
        """
        Retrieve the interpretation
        for a KPI pattern.
        """
        result = self.provider.execute(
            operation="select",
            table=self.table_name,
            filters={
                "pattern_name": pattern_name
            }
        )

        data = getattr(result, "data", result)

        if data and len(data) > 0:
            return data[0]

        return None