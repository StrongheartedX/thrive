"""The command for removing a travel wish."""

from jupiter.core.apps.vacations.sub.travel_wish.root import TravelWish
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
from jupiter.framework.utils.generic_crown_remover import generic_crown_remover


@use_case_args
class TravelWishRemoveArgs(JupiterRemoveCrownEntityArgs):
    """Travel wish remove parameters."""

    ref_id: EntityId


@mutation_use_case(WorkspaceFeature.VACATIONS)
class TravelWishRemoveUseCase(
    JupiterRemoveCrownEntityUseCase[TravelWishRemoveArgs, None]
):
    """The command for removing a travel wish."""

    async def _perform_transactional_mutation(
        self,
        uow: DomainUnitOfWork,
        progress_reporter: ProgressReporter,
        context: JupiterLoggedInMutationContext,
        args: TravelWishRemoveArgs,
    ) -> None:
        """Execute the command's action."""
        await self.check_entity(uow, context.user.ref_id, TravelWish, args.ref_id)

        await generic_crown_remover(
            context.domain_context, uow, progress_reporter, TravelWish, args.ref_id
        )
