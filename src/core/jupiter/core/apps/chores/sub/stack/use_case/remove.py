"""The command for removing a chore stack."""

from jupiter.core.apps.chores.sub.stack.root import ChoreStack
from jupiter.core.apps.chores.sub.stack.service.remove import ChoreStackRemoveService
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
class ChoreStackRemoveArgs(JupiterRemoveCrownEntityArgs):
    """Chore stack remove parameters."""

    ref_id: EntityId


@mutation_use_case(WorkspaceFeature.CHORES)
class ChoreStackRemoveUseCase(
    JupiterRemoveCrownEntityUseCase[ChoreStackRemoveArgs, None]
):
    """The command for removing a chore stack."""

    async def _perform_transactional_mutation(
        self,
        uow: DomainUnitOfWork,
        progress_reporter: ProgressReporter,
        context: JupiterLoggedInMutationContext,
        args: ChoreStackRemoveArgs,
    ) -> None:
        """Execute the command's action."""
        await self.check_entity(uow, context.user.ref_id, ChoreStack, args.ref_id)

        await ChoreStackRemoveService().remove(
            context.domain_context, uow, progress_reporter, args.ref_id
        )
