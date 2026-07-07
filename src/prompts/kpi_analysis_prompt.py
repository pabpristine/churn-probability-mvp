from typing import Any, Dict, List, Optional


# System prompt used for KPI interpretation generation.
# This defines the role and style the LLM should follow.
KPI_ANALYSIS_SYSTEM_PROMPT = (
    "You are a churn risk analysis assistant. "
    "Summarize KPI pattern signals clearly and concisely."
)


def build_kpi_analysis_prompt(
    client_name: Optional[str],
    summary_text: str,
    current_kpis: Dict[str, Any],
    matched_patterns: List[Dict[str, Any]]
) -> str:
    """
    Build the user prompt for KPI analysis.

    This prompt provides:
    - client identity
    - final summary text
    - current KPI values
    - matched KPI pattern rows

    The LLM is then asked to generate a short business interpretation.
    """

    return f"""
Client Name: {client_name}

Final Client Summary:
{summary_text}

Current KPIs:
{current_kpis}

Matched KPI Patterns:
{matched_patterns}

Write a concise KPI interpretation in 4-6 sentences.
Focus on:
1. performance trend,
2. main risks,
3. most important business takeaway.
""".strip()