"""Use case for loading a particular habit stack."""

from jupiter.core.apps.habits.sub.stack.root import HabitStack
from jupiter.core.apps.habits.sub.stack.service.load import (
    HabitStackLoadResult,
    HabitStackLoadService,
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
    "HabitStackLoadArgs",
    "HabitStackLoadResult",
    "HabitStackLoadUseCase",
]


@use_case_args
class HabitStackLoadArgs(JupiterLoadCrownEntityArgs):
    """HabitStackLoadArgs."""

    ref_id: EntityId
    allow_archived: bool | None


@readonly_use_case(WorkspaceFeature.HABITS)
class HabitStackLoadUseCase(
    JupiterLoadCrownEntityUseCase[HabitStackLoadArgs, HabitStackLoadResult]
):
    """Use case for loading a particular habit stack."""

    async def _perform_transactional_read(
        self,
        uow: DomainUnitOfWork,
        context: JupiterLoggedInReadonlyContext,
        args: HabitStackLoadArgs,
    ) -> HabitStackLoadResult:
        """Execute the command's action."""
        allow_archived = args.allow_archived or False

        habit_stack = await self.load_entity(
            uow,
            context.user.ref_id,
            HabitStack,
            args.ref_id,
            allow_archived,
        )

        return await HabitStackLoadService().do_it(
            uow,
            habit_stack,
            user_ref_id=context.user.ref_id,
            allow_archived=allow_archived,
        )
