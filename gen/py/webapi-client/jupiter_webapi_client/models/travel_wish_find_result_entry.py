from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

if TYPE_CHECKING:
    from ..models.access_status import AccessStatus
    from ..models.contact import Contact
    from ..models.location import Location
    from ..models.tag import Tag
    from ..models.travel_wish import TravelWish
    from ..models.user_light import UserLight


T = TypeVar("T", bound="TravelWishFindResultEntry")


@_attrs_define
class TravelWishFindResultEntry:
    """A travel wish find result entry.

    Attributes:
        travel_wish (TravelWish): A travel wish.
        tags (list[Tag]):
        contacts (list[Contact]):
        locations (list[Location]):
        owner (UserLight): A user's ref id, name, and email address.
        access_status (AccessStatus): The effective access status of a principal over a resource.
    """

    travel_wish: TravelWish
    tags: list[Tag]
    contacts: list[Contact]
    locations: list[Location]
    owner: UserLight
    access_status: AccessStatus
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        travel_wish = self.travel_wish.to_dict()

        tags = []
        for tags_item_data in self.tags:
            tags_item = tags_item_data.to_dict()
            tags.append(tags_item)

        contacts = []
        for contacts_item_data in self.contacts:
            contacts_item = contacts_item_data.to_dict()
            contacts.append(contacts_item)

        locations = []
        for locations_item_data in self.locations:
            locations_item = locations_item_data.to_dict()
            locations.append(locations_item)

        owner = self.owner.to_dict()

        access_status = self.access_status.to_dict()

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "travel_wish": travel_wish,
                "tags": tags,
                "contacts": contacts,
                "locations": locations,
                "owner": owner,
                "access_status": access_status,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.access_status import AccessStatus  # noqa: PLC0415
        from ..models.contact import Contact  # noqa: PLC0415
        from ..models.location import Location  # noqa: PLC0415
        from ..models.tag import Tag  # noqa: PLC0415
        from ..models.travel_wish import TravelWish  # noqa: PLC0415
        from ..models.user_light import UserLight  # noqa: PLC0415

        d = dict(src_dict)
        travel_wish = TravelWish.from_dict(d.pop("travel_wish"))

        tags = []
        _tags = d.pop("tags")
        for tags_item_data in _tags:
            tags_item = Tag.from_dict(tags_item_data)

            tags.append(tags_item)

        contacts = []
        _contacts = d.pop("contacts")
        for contacts_item_data in _contacts:
            contacts_item = Contact.from_dict(contacts_item_data)

            contacts.append(contacts_item)

        locations = []
        _locations = d.pop("locations")
        for locations_item_data in _locations:
            locations_item = Location.from_dict(locations_item_data)

            locations.append(locations_item)

        owner = UserLight.from_dict(d.pop("owner"))

        access_status = AccessStatus.from_dict(d.pop("access_status"))

        travel_wish_find_result_entry = cls(
            travel_wish=travel_wish,
            tags=tags,
            contacts=contacts,
            locations=locations,
            owner=owner,
            access_status=access_status,
        )

        travel_wish_find_result_entry.additional_properties = d
        return travel_wish_find_result_entry

    @property
    def additional_keys(self) -> list[str]:
        return list(self.additional_properties.keys())

    def __getitem__(self, key: str) -> Any:
        return self.additional_properties[key]

    def __setitem__(self, key: str, value: Any) -> None:
        self.additional_properties[key] = value

    def __delitem__(self, key: str) -> None:
        del self.additional_properties[key]

    def __contains__(self, key: str) -> bool:
        return key in self.additional_properties
