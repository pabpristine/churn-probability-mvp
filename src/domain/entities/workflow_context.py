from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional


@dataclass
class WorkflowContext:
    """
    Shared object passed across the workflow.

    Every service reads from it and writes back
    to it. This serves as the single source of
    truth during workflow execution.
    """

    # -------------------------------------------------
    # Request Information
    # -------------------------------------------------

    request_id: Optional[str] = None

    # -------------------------------------------------
    # Client Information
    # -------------------------------------------------

    client_id: Optional[str] = None
    client_name: Optional[str] = None

    google_sheet_data: Dict[str, Any] = field(default_factory=dict)
    client_updates: List[Dict[str, Any]] = field(default_factory=list)
    latest_client_update: Optional[Dict[str, Any]] = None

        # Program Information
    program_type: Optional[str] = None

    program_duration: Optional[str] = None

    program_stage: Optional[str] = None

    campaign_status: Optional[str] = None


    # -------------------------------------------------
    # KPI Information
    # -------------------------------------------------

    current_kpis: Dict[str, Any] = field(default_factory=dict)

    campaign_weights: Dict[str, Any] = field(default_factory=dict)

    current_satisfaction: Optional[str] = None

    # -------------------------------------------------
    # KPI Pipeline
    # -------------------------------------------------

    kpi_dataset: Dict[str, Any] = field(default_factory=dict)

    kpi_interpretation: Dict[str, Any] = field(default_factory=dict)
    # -------------------------------------------------
    # AI Summary
    # -------------------------------------------------

    summary: Optional[str] = None
    final_client_summary: Optional[str] = None

    recommendations: List[str] = field(default_factory=list)

    # -------------------------------------------------
    # Embeddings
    # -------------------------------------------------

    summary_embedding: Optional[List[float]] = None
    kpi_embedding: Optional[List[float]] = None

    # -------------------------------------------------
    # RAG Retrieval
    # -------------------------------------------------

    historical_matches: List[Dict[str, Any]] = field(default_factory=list)

    # -------------------------------------------------
    # Churn Prediction
    # -------------------------------------------------

    summary_probability: Optional[float] = None
    kpi_probability: Optional[float] = None
    final_probability: Optional[float] = None
    risk_level: Optional[str] = None

    # -------------------------------------------------
    # Workflow Status
    # -------------------------------------------------

    workflow_status: Optional[str] = None

    # -------------------------------------------------
    # Previous Summary
    # -------------------------------------------------

    previous_summary: Optional[str] = None

    previous_summary_timestamp: Optional[str] = None

    previous_satisfaction_score: Optional[int] = None

    is_new_client: bool = False
    
    previous_record: Optional[Dict] = None

    # ------------------------------------------
    # Summary Batches
    # ------------------------------------------

    # Summary Batches
    summary_batches: List[Dict] = field(
        default_factory=list
    )

    formatted_update_history: Optional[str] = None

    updated_summary: Optional[str] = None

    updated_satisfaction_score: Optional[int] = None

    # -------------------------------------------------
    # Generated Summary
    # -------------------------------------------------

    updated_summary: Optional[str] = None

    updated_satisfaction_score: Optional[int] = None

    # -------------------------------------------------
    # LLM Output
    # -------------------------------------------------

    llm_output: Optional[Dict[str, Any]] = None

    # -------------------------------------------------
    # Token Usage
    # -------------------------------------------------

    llm_usage: Dict[str, int] = field(
        default_factory=dict
    )

    # -------------------------------------------------
    # Metadata
    # -------------------------------------------------

    metadata: Dict[str, Any] = field(default_factory=dict)