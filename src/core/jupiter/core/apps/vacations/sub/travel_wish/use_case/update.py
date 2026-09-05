"""The command for updating a travel wish's properties."""

from jupiter.core.apps.vacations.sub.travel_wish.name import TravelWishName
from jupiter.core.apps.vacations.sub.travel_wish.root import TravelWish
from jupiter.core.config import (
    JupiterLoggedInMutationContext,
)
from jupiter.core.crown_entity_support import (
    JupiterUpdateCrownEntityArgs,
    JupiterUpdateCrownEntityUseCase,
)
from jupiter.core.features import WorkspaceFeature
from jupiter.framework.base.entity_id import EntityId
from jupiter.framework.progress_reporter.reporter import ProgressReporter
from jupiter.framework.storage.repository import DomainUnitOfWork
from jupiter.framework.update_action import UpdateAction
from jupiter.framework.use_case import (
    mutation_use_case,
)
from jupiter.framework.use_case_io import use_case_args


@use_case_args
class TravelWishUpdateArgs(JupiterUpdateCrownEntityArgs):
    """Travel wish update parameters."""

    ref_id: EntityId
    name: UpdateAction[TravelWishName]


@mutation_use_case(WorkspaceFeature.VACATIONS)
class TravelWishUpdateUseCase(
    JupiterUpdateCrownEntityUseCase[TravelWishUpdateArgs, None]
):
    """The command for updating a travel wish's properties."""

    async def _perform_transactional_mutation(
        self,
        uow: DomainUnitOfWork,
        progress_reporter: ProgressReporter,
        context: JupiterLoggedInMutationContext,
        args: TravelWishUpdateArgs,
    ) -> None:
        """Execute the command's action."""
        travel_wish = await self.load_entity(
            uow, context.user.ref_id, TravelWish, args.ref_id
        )

        travel_wish = travel_wish.update(
            context.domain_context,
            name=args.name,
        )

        travel_wish = await uow.get_for(TravelWish).save(travel_wish)
        await progress_reporter.mark_updated(travel_wish)
