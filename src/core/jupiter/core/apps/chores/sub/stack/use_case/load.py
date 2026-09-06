"""Use case for loading a particular chore stack."""

from jupiter.core.apps.chores.sub.stack.root import ChoreStack
from jupiter.core.apps.chores.sub.stack.service.load import (
    ChoreStackLoadResult,
    ChoreStackLoadService,
)
from jupiter.core.config import (
    JupiterLoggedInReadonlyContext,
)
from jupiter.core.crown_entity_support import (
    JupiterLoadCrownEntityArgs,
    JupiterLoadCrownEntityUseCase,
)
from jupiter.core.features import WorkspaceFeature
from jupiter.framework.base.entity_id import EntityId
from jupiter.framework.storage.repository import DomainUnitOfWork
from jupiter.framework.use_case import (
    readonly_use_case,
)
from jupiter.framework.use_case_io import (
    use_case_args,
)

__all__ = [
    "ChoreStackLoadArgs",
    "ChoreStackLoadResult",
    "ChoreStackLoadUseCase",
]


@use_case_args
class ChoreStackLoadArgs(JupiterLoadCrownEntityArgs):
    """ChoreStackLoadArgs."""

    ref_id: EntityId
    allow_archived: bool | None


@readonly_use_case(WorkspaceFeature.CHORES)
class ChoreStackLoadUseCase(
    JupiterLoadCrownEntityUseCase[ChoreStackLoadArgs, ChoreStackLoadResult]
):
    """Use case for loading a particular chore stack."""

    async def _perform_transactional_read(
        self,
        uow: DomainUnitOfWork,
        context: JupiterLoggedInReadonlyContext,
        args: ChoreStackLoadArgs,
    ) -> ChoreStackLoadResult:
        """Execute the command's action."""
        allow_archived = args.allow_archived or False

        chore_stack = await self.load_entity(
            uow,
            context.user.ref_id,
            ChoreStack,
            args.ref_id,
            allow_archived,
        )

        return await ChoreStackLoadService().do_it(
            uow,
            chore_stack,
            user_ref_id=context.user.ref_id,
            allow_archived=allow_archived,
        )
