from src.domain.entities.workflow_context import WorkflowContext


def build_summary_churn_analysis_prompt(
    context: WorkflowContext
) -> str:
    """
    Build the prompt for summary/update-based churn analysis.

    The model will analyze:
    - current client update/summary text
    - top 5 similar historical client summaries

    The model must return strict JSON only.
    """

    current_summary = (
        context.updated_summary
        or context.final_client_summary
        or context.summary
        or context.formatted_update_history
        or "No current summary available."
    )

    historical_matches = []

    for index, match in enumerate(context.summary_matches, start=1):
        historical_matches.append(
            f"""
Historical Match {index}
Client ID: {match.get('client_id', 'N/A')}
Client Name: {match.get('client_name', 'N/A')}
Similarity: {match.get('similarity', 'N/A')}
Summary:
{match.get('summary', 'N/A')}
""".strip()
        )

    historical_matches_block = (
        "\n\n".join(historical_matches)
        if historical_matches
        else "No historical matches available."
    )

    return f"""
You are an expert churn-risk analyst.

Analyze churn risk for the current client using ONLY:
1. The current client summary/update information
2. The retrieved top similar historical client summaries

Your job:
- Compare the current client with historical clients
- Identify red flags
- Identify operational bottlenecks
- Extract historical insights
- Estimate churn probability as an integer from 0 to 100
- Provide a concise analysis

Important rules:
- Use only the provided information
- Do not invent facts
- Return STRICT JSON only
- Do not return markdown
- Do not return code fences
- Do not return any explanation outside JSON

Current Client
Client ID: {context.client_id or 'N/A'}
Client Name: {context.client_name or 'N/A'}

Current Summary
{current_summary}

Historical Similar Clients
{historical_matches_block}

Return JSON with exactly this structure:
{{
  "probability": 0,
  "analysis": "string",
  "red_flags": ["string"],
  "bottlenecks": ["string"],
  "historical_insights": ["string"]
}}

Additional rules:
- probability must be an integer between 0 and 100
- analysis must be a concise business explanation
- red_flags must contain short actionable observations
- bottlenecks must contain short operational issues
- historical_insights must compare current client with historical patterns
""".strip()