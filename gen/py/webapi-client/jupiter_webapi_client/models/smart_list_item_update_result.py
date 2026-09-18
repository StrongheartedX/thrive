from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

if TYPE_CHECKING:
    from ..models.smart_list_item import SmartListItem


T = TypeVar("T", bound="SmartListItemUpdateResult")


@_attrs_define
class SmartListItemUpdateResult:
    """SmartListItemUpdate result.

    Attributes:
        updated_smart_list_item (SmartListItem): A smart list item.
    """

    updated_smart_list_item: SmartListItem
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        updated_smart_list_item = self.updated_smart_list_item.to_dict()

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "updated_smart_list_item": updated_smart_list_item,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.smart_list_item import SmartListItem  # noqa: PLC0415

        d = dict(src_dict)
        updated_smart_list_item = SmartListItem.from_dict(d.pop("updated_smart_list_item"))

        smart_list_item_update_result = cls(
            updated_smart_list_item=updated_smart_list_item,
        )

        smart_list_item_update_result.additional_properties = d
        return smart_list_item_update_result

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
