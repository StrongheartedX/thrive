"""The command for removing a habit stack."""

from jupiter.core.apps.habits.sub.stack.root import HabitStack
from jupiter.core.apps.habits.sub.stack.service.remove import HabitStackRemoveService
from jupiter.core.config import (
    JupiterLoggedInMutationContext,
)
from jupiter.core.crown_entity_support import (
    JupiterRemoveCrownEntityArgs,
    JupiterRemoveCrownEntityUseCase,
)
from jupiter.core.features import WorkspaceFeature
from jupiter.framework.base.entity_id import EntityId
from jupiter.framework.progress_reporter.reporter import ProgressReporter
from jupiter.framework.storage.repository import DomainUnitOfWork
from jupiter.framework.use_case import (
    mutation_use_case,
)
from jupiter.framework.use_case_io import use_case_args


@use_case_args
class HabitStackRemoveArgs(JupiterRemoveCrownEntityArgs):
    """Habit stack remove parameters."""

    ref_id: EntityId


@mutation_use_case(WorkspaceFeature.HABITS)
class HabitStackRemoveUseCase(
    JupiterRemoveCrownEntityUseCase[HabitStackRemoveArgs, None]
):
    """The command for removing a habit stack."""

    async def _perform_transactional_mutation(
        self,
        uow: DomainUnitOfWork,
        progress_reporter: ProgressReporter,
        context: JupiterLoggedInMutationContext,
        args: HabitStackRemoveArgs,
    ) -> None:
        """Execute the command's action."""
        await self.check_entity(uow, context.user.ref_id, HabitStack, args.ref_id)

        await HabitStackRemoveService().remove(
            context.domain_context, uow, progress_reporter, args.ref_id
        )
