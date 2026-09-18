from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

if TYPE_CHECKING:
    from ..models.contact import Contact


T = TypeVar("T", bound="ContactUpdateResult")


@_attrs_define
class ContactUpdateResult:
    """ContactUpdate result.

    Attributes:
        updated_contact (Contact): A contact.
    """

    updated_contact: Contact
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        updated_contact = self.updated_contact.to_dict()

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "updated_contact": updated_contact,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.contact import Contact  # noqa: PLC0415

        d = dict(src_dict)
        updated_contact = Contact.from_dict(d.pop("updated_contact"))

        contact_update_result = cls(
            updated_contact=updated_contact,
        )

        contact_update_result.additional_properties = d
        return contact_update_result

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
