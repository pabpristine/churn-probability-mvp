from abc import abstractmethod
from typing import List

from src.base.base_node import BaseNode
from src.base.base_service import BaseService
from src.domain.entities.workflow_context import WorkflowContext
from src.domain.enums.status_enum import WorkflowStatus


class BaseWorkflow(BaseNode):
    """
    Base class for all workflows.

    A workflow is responsible for orchestrating the
    execution of multiple services while maintaining
    a shared WorkflowContext throughout execution.
    """

    def __init__(
        self,
        workflow_name: str
    ):
        super().__init__(
            node_name=workflow_name,
            node_type="WORKFLOW"
        )

        # Unique workflow identifier
        self.workflow_id = self.node_id

        self.workflow_name = workflow_name

        # Current workflow execution status
        self.workflow_status = (
            WorkflowStatus.PENDING
        )

        # Shared context passed between services
        self.context: WorkflowContext | None = None

        # Ordered list of services
        self.services: List[
            BaseService
        ] = []

    # -------------------------------------------------
    # Workflow Construction
    # -------------------------------------------------

    @abstractmethod
    def build_workflow(self):
        """
        Register all services required
        for the workflow.

        Must be implemented by child workflows.
        """
        pass

    def add_service(
        self,
        service: BaseService
    ):
        """
        Register a service in the workflow.
        """

        if service not in self.services:

            self.services.append(
                service
            )

    # -------------------------------------------------
    # Workflow Lifecycle
    # -------------------------------------------------

    def start(
        self,
        context: WorkflowContext
    ):
        """
        Initialize workflow execution.
        """

        self.initialize()

        self.context = context

        self.workflow_status = (
            WorkflowStatus.RUNNING
        )

        self.logger.info(
            f"{self.workflow_name} started."
        )

    def update_context(
        self,
        context: WorkflowContext
    ):
        """
        Update the shared workflow context.
        """

        self.context = context

    def execute(
        self,
        context: WorkflowContext
    ) -> WorkflowContext:
        """
        Execute all registered services
        sequentially.
        """

        try:

            self.start(context)

            # Prevent duplicate services
            self.services.clear()

            self.build_workflow()

            for service in self.services:

                context = service.execute(
                    context
                )

                self.update_context(
                    context
                )

            self.stop()

            return self.context

        except Exception as error:

            self.rollback()

            self.handle_error(
                error
            )

            raise error

    def stop(self):
        """
        Mark workflow execution as completed.
        """

        self.workflow_status = (
            WorkflowStatus.COMPLETED
        )

        self.complete()

        self.logger.info(
            f"{self.workflow_name} completed."
        )

    def rollback(self):
        """
        Roll back workflow after failure.
        """

        self.workflow_status = (
            WorkflowStatus.ROLLED_BACK
        )

        self.logger.warning(
            f"{self.workflow_name} rolled back."
        )