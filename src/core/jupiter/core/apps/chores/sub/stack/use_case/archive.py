"""The command for archiving a chore stack."""

from jupiter.core.apps.chores.sub.stack.root import ChoreStack
from jupiter.core.apps.chores.sub.stack.service.archive import (
    ChoreStackArchiveService,
)
from jupiter.core.archival_reason import JupiterArchivalReason
from jupiter.core.config import (
    JupiterLoggedInMutationContext,
)
from jupiter.core.crown_entity_support import (
    JupiterArchiveCrownEntityArgs,
    JupiterArchiveCrownEntityUseCase,
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
class ChoreStackArchiveArgs(JupiterArchiveCrownEntityArgs):
    """Chore stack archive parameters."""

    ref_id: EntityId


@mutation_use_case(WorkspaceFeature.CHORES)
class ChoreStackArchiveUseCase(
    JupiterArchiveCrownEntityUseCase[ChoreStackArchiveArgs, None]
):
    """The command for archiving a chore stack."""

    async def _perform_transactional_mutation(
        self,
        uow: DomainUnitOfWork,
        progress_reporter: ProgressReporter,
        context: JupiterLoggedInMutationContext,
        args: ChoreStackArchiveArgs,
    ) -> None:
        """Execute the command's action."""
        chore_stack = await self.load_entity(
            uow, context.user.ref_id, ChoreStack, args.ref_id
        )

        await ChoreStackArchiveService().do_it(
            context.domain_context,
            uow,
            progress_reporter,
            chore_stack,
            JupiterArchivalReason.USER,
        )
