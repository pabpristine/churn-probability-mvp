from src.repositories.llm_usage_repository import (
    LLMUsageRepository
)

repository = LLMUsageRepository()

print(repository.find_all())