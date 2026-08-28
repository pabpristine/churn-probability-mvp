from typing import Optional
from pydantic import BaseModel, Field, AliasChoices


class ClientAnalysisRequest(BaseModel):
    user_query: Optional[str] = Field(
        default=None,
        validation_alias=AliasChoices("user_query", "query"),
        description="User query for client analysis",
        json_schema_extra={"example": "Give me churn analysis for Yardworx Land Management"}
    )

    @property
    def text_query(self) -> str:
        return self.user_query or ""



