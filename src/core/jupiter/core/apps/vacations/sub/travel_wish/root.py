"""A travel wish — a place someone would like to visit."""

from jupiter.core.apps.vacations.sub.travel_wish.name import TravelWishName
from jupiter.core.common.sub.contacts.sub.link.root import ContactLink
from jupiter.core.common.sub.locations.sub.link.root import LocationLink
from jupiter.core.common.sub.tags.sub.link.root import TagLink
from jupiter.core.named_entity_tag import NamedEntityTag
from jupiter.framework.base.entity_id import EntityId
from jupiter.framework.context import DomainContext
from jupiter.framework.entity import (
    IsEntityLinkStd,
    LeafEntity,
    OwnsAtMostOne,
    ParentLink,
    create_entity_action,
    entity,
    update_entity_action,
)
from jupiter.framework.update_action import UpdateAction


@entity("VacationCollection")
class TravelWish(LeafEntity):
    """A travel wish."""

    vacation_collection: ParentLink
    name: TravelWishName

    tag_link = OwnsAtMostOne(
        TagLink, owner=IsEntityLinkStd(NamedEntityTag.TRAVEL_WISH.value)
    )
    contact_link = OwnsAtMostOne(
        ContactLink, owner=IsEntityLinkStd(NamedEntityTag.TRAVEL_WISH.value)
    )
    location_link = OwnsAtMostOne(
        LocationLink, owner=IsEntityLinkStd(NamedEntityTag.TRAVEL_WISH.value)
    )

    @staticmethod
    @create_entity_action
    def new_travel_wish(
        ctx: DomainContext,
        vacation_collection_ref_id: EntityId,
        name: TravelWishName,
    ) -> "TravelWish":
        """Create a travel wish."""
        return TravelWish._create(
            ctx,
            name=name,
            vacation_collection=ParentLink(vacation_collection_ref_id),
        )

    @update_entity_action
    def update(
        self,
        ctx: DomainContext,
        name: UpdateAction[TravelWishName],
    ) -> "TravelWish":
        """Update a travel wish's properties."""
        return self._new_version(
            ctx,
            name=name.or_else(self.name),
        )
