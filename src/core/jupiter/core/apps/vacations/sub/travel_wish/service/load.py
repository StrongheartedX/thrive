"""Shared service for loading a travel wish and its dependent entities."""

from jupiter.core.apps.vacations.sub.travel_wish.root import TravelWish
from jupiter.core.common.sub.access.sub.grant.service.get_access_level_for_entity import (
    GetAccessLevelForEntityService,
)
from jupiter.core.common.sub.access.sub.grant.service.load_user_that_owns_entity import (
    LoadUserThatOwnsEntityService,
)
from jupiter.core.common.sub.access.sub.status.root import AccessStatus
from jupiter.core.common.sub.contacts.sub.contact.root import Contact
from jupiter.core.common.sub.contacts.sub.link.root import ContactLinkRepository
from jupiter.core.common.sub.locations.sub.link.root import LocationLinkRepository
from jupiter.core.common.sub.locations.sub.link.service.load import (
    LoadLocationsForLinkService,
)
from jupiter.core.common.sub.locations.sub.location.root import Location
from jupiter.core.common.sub.tags.sub.link.root import TagLinkRepository
from jupiter.core.common.sub.tags.sub.tag.root import Tag, TagRepository
from jupiter.core.named_entity_tag import NamedEntityTag
from jupiter.core.users.user_light import UserLight
from jupiter.framework.base.entity_id import EntityId
from jupiter.framework.base.entity_link import EntityLink
from jupiter.framework.storage.repository import DomainUnitOfWork
from jupiter.framework.use_case_io import UseCaseResultBase, use_case_result


@use_case_result
class TravelWishLoadResult(UseCaseResultBase):
    """TravelWishLoadResult."""

    travel_wish: TravelWish
    tags: list[Tag]
    contacts: list[Contact]
    locations: list[Location]
    owner: UserLight
    access_status: AccessStatus | None


class TravelWishLoadService:
    """Shared service for loading a travel wish and its dependent entities."""

    async def do_it(
        self,
        uow: DomainUnitOfWork,
        travel_wish: TravelWish,
        *,
        user_ref_id: EntityId | None = None,
        allow_archived: bool = False,
    ) -> TravelWishLoadResult:
        """Load a travel wish together with the entities that hang off it."""
        travel_wish = await uow.get_for(TravelWish).load_by_id(
            travel_wish.ref_id, allow_archived=allow_archived
        )
        owner_link = EntityLink.std(
            NamedEntityTag.TRAVEL_WISH.value, travel_wish.ref_id
        )

        tag_link = await uow.get(TagLinkRepository).load_optional_for_owner(
            owner=owner_link,
        )
        if tag_link is not None:
            tags = await uow.get(TagRepository).find_all_generic(
                allow_archived=False,
                ref_id=tag_link.ref_ids,
            )
        else:
            tags = []

        contact_link = await uow.get(ContactLinkRepository).load_optional_for_owner(
            owner_link,
        )
        if contact_link is not None:
            contacts = await uow.get_for(Contact).find_all_generic(
                allow_archived=False,
                ref_id=contact_link.contacts_ref_ids,
            )
        else:
            contacts = []

        location_link = await uow.get(LocationLinkRepository).load_optional_for_owner(
            owner_link,
        )
        locations = await LoadLocationsForLinkService().do_it(uow, location_link)

        owner = await LoadUserThatOwnsEntityService().do_it(uow, owner_link)
        access_status = (
            await GetAccessLevelForEntityService().do_it(uow, owner_link, user_ref_id)
            if user_ref_id is not None
            else None
        )

        return TravelWishLoadResult(
            travel_wish=travel_wish,
            tags=tags,
            contacts=contacts,
            locations=locations,
            owner=owner,
            access_status=access_status,
        )
