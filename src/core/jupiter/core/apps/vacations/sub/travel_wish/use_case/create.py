"""The command for creating a travel wish."""

from jupiter.core.apps.vacations.collection import VacationCollection
from jupiter.core.apps.vacations.sub.travel_wish.name import TravelWishName
from jupiter.core.apps.vacations.sub.travel_wish.root import TravelWish
from jupiter.core.common.sub.locations.root import LocationDomain
from jupiter.core.common.sub.locations.sub.link.root import (
    LocationLink,
    LocationLinkRepository,
)
from jupiter.core.common.sub.locations.sub.location.root import Location
from jupiter.core.config import (
    JupiterLoggedInMutationContext,
)
from jupiter.core.crown_entity_support import (
    JupiterCreateCrownEntityArgs,
    JupiterCreateCrownEntityUseCase,
)
from jupiter.core.features import WorkspaceFeature
from jupiter.core.named_entity_tag import NamedEntityTag
from jupiter.framework.base.entity_id import EntityId
from jupiter.framework.base.entity_link import EntityLink
from jupiter.framework.progress_reporter.reporter import ProgressReporter
from jupiter.framework.storage.repository import DomainUnitOfWork
from jupiter.framework.use_case import (
    mutation_use_case,
)
from jupiter.framework.use_case_io import (
    UseCaseResultBase,
    use_case_args,
    use_case_result,
)


@use_case_args
class TravelWishCreateArgs(JupiterCreateCrownEntityArgs):
    """Travel wish creation parameters."""

    location_ref_id: EntityId


@use_case_result
class TravelWishCreateResult(UseCaseResultBase):
    """Travel wish creation result."""

    new_travel_wish: TravelWish


@mutation_use_case(WorkspaceFeature.VACATIONS)
class TravelWishCreateUseCase(
    JupiterCreateCrownEntityUseCase[TravelWishCreateArgs, TravelWishCreateResult]
):
    """The command for creating a travel wish."""

    async def _perform_transactional_mutation(
        self,
        uow: DomainUnitOfWork,
        progress_reporter: ProgressReporter,
        context: JupiterLoggedInMutationContext,
        args: TravelWishCreateArgs,
    ) -> TravelWishCreateResult:
        """Execute the command's actions."""
        vacation_collection = await uow.get_for(VacationCollection).load_by_parent(
            context.workspace.ref_id,
        )
        location_domain = await uow.get_for(LocationDomain).load_by_parent(
            context.workspace.ref_id,
        )
        location = await uow.get_for(Location).load_by_id(
            args.location_ref_id,
            allow_archived=False,
        )

        new_travel_wish = TravelWish.new_travel_wish(
            context.domain_context,
            vacation_collection_ref_id=vacation_collection.ref_id,
            name=TravelWishName(str(location.name)),
        )

        new_travel_wish = await self.create_entity(
            context.domain_context,
            uow,
            progress_reporter,
            context.user.ref_id,
            new_travel_wish,
        )

        location_link = LocationLink.new_location_link(
            context.domain_context,
            location_domain_ref_id=location_domain.ref_id,
            owner=EntityLink.std(
                NamedEntityTag.TRAVEL_WISH.value, new_travel_wish.ref_id
            ),
            locations_ref_ids=[location.ref_id],
        )
        await uow.get(LocationLinkRepository).upsert(location_link)

        return TravelWishCreateResult(new_travel_wish=new_travel_wish)
