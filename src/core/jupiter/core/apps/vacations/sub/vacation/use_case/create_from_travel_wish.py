"""The command for creating a vacation from a travel wish."""

from jupiter.core.apps.vacations.collection import VacationCollection
from jupiter.core.apps.vacations.sub.travel_wish.root import TravelWish
from jupiter.core.apps.vacations.sub.vacation.name import VacationName
from jupiter.core.apps.vacations.sub.vacation.root import Vacation
from jupiter.core.archival_reason import JupiterArchivalReason
from jupiter.core.common.sub.contacts.root import ContactDomain
from jupiter.core.common.sub.contacts.sub.link.root import (
    ContactLink,
    ContactLinkRepository,
)
from jupiter.core.common.sub.locations.root import LocationDomain
from jupiter.core.common.sub.locations.sub.link.root import (
    LocationLink,
    LocationLinkRepository,
)
from jupiter.core.common.sub.tags.root import TagDomain
from jupiter.core.common.sub.tags.sub.link.root import TagLink, TagLinkRepository
from jupiter.core.common.sub.time_events.domain import TimeEventDomain
from jupiter.core.common.sub.time_events.sub.full_days_block.root import (
    TimeEventFullDaysBlock,
)
from jupiter.core.config import (
    JupiterLoggedInMutationContext,
)
from jupiter.core.crown_entity_support import (
    JupiterCreateCrownEntityArgs,
    JupiterCreateCrownEntityUseCase,
)
from jupiter.core.features import WorkspaceFeature
from jupiter.core.named_entity_tag import NamedEntityTag
from jupiter.framework.base.adate import ADate
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
from jupiter.framework.utils.generic_crown_archiver import generic_crown_archiver


@use_case_args
class VacationCreateFromTravelWishArgs(JupiterCreateCrownEntityArgs):
    """Vacation creation from a travel wish parameters."""

    travel_wish_ref_id: EntityId
    start_date: ADate
    end_date: ADate


@use_case_result
class VacationCreateFromTravelWishResult(UseCaseResultBase):
    """Vacation creation from a travel wish result."""

    new_vacation: Vacation
    new_time_event_block: TimeEventFullDaysBlock


@mutation_use_case(WorkspaceFeature.VACATIONS)
class VacationCreateFromTravelWishUseCase(
    JupiterCreateCrownEntityUseCase[
        VacationCreateFromTravelWishArgs, VacationCreateFromTravelWishResult
    ]
):
    """The command for creating a vacation from a travel wish."""

    async def _perform_transactional_mutation(
        self,
        uow: DomainUnitOfWork,
        progress_reporter: ProgressReporter,
        context: JupiterLoggedInMutationContext,
        args: VacationCreateFromTravelWishArgs,
    ) -> VacationCreateFromTravelWishResult:
        """Execute the command's actions."""
        travel_wish = await self.load_entity(
            uow, context.user.ref_id, TravelWish, args.travel_wish_ref_id
        )
        travel_wish_link = EntityLink.std(
            NamedEntityTag.TRAVEL_WISH.value, travel_wish.ref_id
        )

        vacation_collection = await uow.get_for(VacationCollection).load_by_id(
            travel_wish.vacation_collection.ref_id,
        )
        time_event_domain = await uow.get_for(TimeEventDomain).load_by_parent(
            vacation_collection.workspace.ref_id,
        )

        new_vacation = Vacation.new_vacation(
            context.domain_context,
            vacation_collection_ref_id=vacation_collection.ref_id,
            name=VacationName(str(travel_wish.name)),
            start_date=args.start_date,
            end_date=args.end_date,
        )
        new_vacation = await self.create_entity(
            context.domain_context,
            uow,
            progress_reporter,
            context.user.ref_id,
            new_vacation,
        )
        vacation_link = EntityLink.std(
            NamedEntityTag.VACATION.value, new_vacation.ref_id
        )

        new_time_event_block = TimeEventFullDaysBlock.new_time_event_for_vacation(
            context.domain_context,
            time_event_domain_ref_id=time_event_domain.ref_id,
            vacation_ref_id=new_vacation.ref_id,
            start_date=args.start_date,
            end_date=args.end_date,
        )
        new_time_event_block = await uow.get_for(TimeEventFullDaysBlock).create(
            new_time_event_block,
        )

        tag_link = await uow.get(TagLinkRepository).load_optional_for_owner(
            travel_wish_link
        )
        if tag_link is not None and tag_link.ref_ids:
            tag_domain = await uow.get_for(TagDomain).load_by_parent(
                vacation_collection.workspace.ref_id
            )
            new_tag_link = TagLink.new_tag_link(
                context.domain_context,
                tag_domain_ref_id=tag_domain.ref_id,
                owner=vacation_link,
                ref_ids=list(tag_link.ref_ids),
            )
            await uow.get(TagLinkRepository).upsert(new_tag_link)

        contact_link = await uow.get(ContactLinkRepository).load_optional_for_owner(
            travel_wish_link
        )
        if contact_link is not None and contact_link.contacts_ref_ids:
            contact_domain = await uow.get_for(ContactDomain).load_by_parent(
                vacation_collection.workspace.ref_id
            )
            new_contact_link = ContactLink.new_contact_link(
                context.domain_context,
                contact_domain_ref_id=contact_domain.ref_id,
                owner=vacation_link,
                contacts_ref_ids=list(contact_link.contacts_ref_ids),
            )
            await uow.get(ContactLinkRepository).upsert(new_contact_link)

        location_link = await uow.get(LocationLinkRepository).load_optional_for_owner(
            travel_wish_link
        )
        if location_link is not None and location_link.locations_ref_ids:
            location_domain = await uow.get_for(LocationDomain).load_by_parent(
                vacation_collection.workspace.ref_id
            )
            new_location_link = LocationLink.new_location_link(
                context.domain_context,
                location_domain_ref_id=location_domain.ref_id,
                owner=vacation_link,
                locations_ref_ids=list(location_link.locations_ref_ids),
            )
            await uow.get(LocationLinkRepository).upsert(new_location_link)

        await generic_crown_archiver(
            context.domain_context,
            uow,
            progress_reporter,
            TravelWish,
            travel_wish.ref_id,
            JupiterArchivalReason.USER,
        )

        return VacationCreateFromTravelWishResult(
            new_vacation=new_vacation,
            new_time_event_block=new_time_event_block,
        )
