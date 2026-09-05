from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

if TYPE_CHECKING:
    from ..models.travel_wish import TravelWish


T = TypeVar("T", bound="TravelWishCreateResult")


@_attrs_define
class TravelWishCreateResult:
    """Travel wish creation result.

    Attributes:
        new_travel_wish (TravelWish): A travel wish.
    """

    new_travel_wish: TravelWish
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        new_travel_wish = self.new_travel_wish.to_dict()

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "new_travel_wish": new_travel_wish,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.travel_wish import TravelWish  # noqa: PLC0415

        d = dict(src_dict)
        new_travel_wish = TravelWish.from_dict(d.pop("new_travel_wish"))

        travel_wish_create_result = cls(
            new_travel_wish=new_travel_wish,
        )

        travel_wish_create_result.additional_properties = d
        return travel_wish_create_result

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
