# Used to create mock objects and replace real dependencies in tests
from unittest.mock import Mock, patch

# Import the shared workflow context object
from src.domain.entities.workflow_context import WorkflowContext

# Import the service that we want to test
from src.services.client_name_extraction_service import (
    ClientNameExtractionService,
)


def test_extract_client_name_with_code_logic():
    # Create an instance of the service
    service = ClientNameExtractionService()

    # Create a fresh workflow context for this test
    context = WorkflowContext()

    # Add the user query in metadata
    context.metadata["user_query"] = (
        "Give me the churn summary for Acme Corp"
    )

    # Execute the service
    result = service.execute(context)

    # Check that the client name was extracted correctly
    assert result.client_name == "Acme Corp"

    # Check that the extraction method used was code-based logic
    assert (
        result.metadata["client_name_extraction_method"]
        == "code"
    )


# Patch the GroqProvider so that no real API call is made
@patch(
    "src.services.client_name_extraction_service.GroqProvider"
)
def test_extract_client_name_with_ai_fallback(mock_groq_provider):
    # Create a fake provider instance
    mock_provider_instance = Mock()

    # Mock the AI response returned by generate_response()
    mock_provider_instance.generate_response.return_value = {
        "content": "Bright Smile Dental"
    }

    # Tell the patched GroqProvider to return our fake provider
    mock_groq_provider.return_value = mock_provider_instance

    # Create the service instance
    service = ClientNameExtractionService()

    # Replace the real groq provider inside the service with mocked one
    service.groq_provider = mock_provider_instance

    # Create a fresh workflow context
    context = WorkflowContext()

    # Add a query where code-based logic is expected to fail
    # and AI fallback should be used
    context.metadata["user_query"] = (
        "Can you check how that dental client is doing this month?"
    )

    # Execute the service
    result = service.execute(context)

    # Check that the AI fallback returned the expected client name
    assert result.client_name == "Bright Smile Dental"

    # Check that the extraction method used was AI fallback
    assert (
        result.metadata["client_name_extraction_method"]
        == "ai"
    )


# Patch the GroqProvider so that no real API call is made
@patch(
    "src.services.client_name_extraction_service.GroqProvider"
)
def test_extract_client_name_not_found(mock_groq_provider):
    # Create a fake provider instance
    mock_provider_instance = Mock()

    # Mock the AI response as UNKNOWN when no client name is found
    mock_provider_instance.generate_response.return_value = {
        "content": "UNKNOWN"
    }

    # Tell the patched GroqProvider to return our fake provider
    mock_groq_provider.return_value = mock_provider_instance

    # Create the service instance
    service = ClientNameExtractionService()

    # Replace the real groq provider with mocked one
    service.groq_provider = mock_provider_instance

    # Create a fresh workflow context
    context = WorkflowContext()

    # Add a query that does not contain any identifiable client name
    context.metadata["user_query"] = "Show me the latest report"

    # Execute the service
    result = service.execute(context)

    # Check that no client name was extracted
    assert result.client_name is None

    # Check that the method is marked as not_found
    assert (
        result.metadata["client_name_extraction_method"]
        == "not_found"
    )