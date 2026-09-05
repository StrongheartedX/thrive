"""Use case for loading a particular travel wish."""

from jupiter.core.apps.vacations.sub.travel_wish.root import TravelWish
from jupiter.core.apps.vacations.sub.travel_wish.service.load import (
    TravelWishLoadResult,
    TravelWishLoadService,
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

__all__ = ["TravelWishLoadArgs", "TravelWishLoadResult", "TravelWishLoadUseCase"]


@use_case_args
class TravelWishLoadArgs(JupiterLoadCrownEntityArgs):
    """TravelWishLoadArgs."""

    ref_id: EntityId
    allow_archived: bool | None


@readonly_use_case(WorkspaceFeature.VACATIONS)
class TravelWishLoadUseCase(
    JupiterLoadCrownEntityUseCase[TravelWishLoadArgs, TravelWishLoadResult]
):
    """Use case for loading a particular travel wish."""

    async def _perform_transactional_read(
        self,
        uow: DomainUnitOfWork,
        context: JupiterLoggedInReadonlyContext,
        args: TravelWishLoadArgs,
    ) -> TravelWishLoadResult:
        """Execute the command's action."""
        allow_archived = args.allow_archived or False

        travel_wish = await self.load_entity(
            uow,
            context.user.ref_id,
            TravelWish,
            args.ref_id,
            allow_archived,
        )

        return await TravelWishLoadService().do_it(
            uow,
            travel_wish,
            user_ref_id=context.user.ref_id,
            allow_archived=allow_archived,
        )
