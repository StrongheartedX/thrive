from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

if TYPE_CHECKING:
    from ..models.life_plan import LifePlan


T = TypeVar("T", bound="LifePlanUpdateResult")


@_attrs_define
class LifePlanUpdateResult:
    """LifePlanUpdate result.

    Attributes:
        updated_life_plan (LifePlan): A aspect collection.
    """

    updated_life_plan: LifePlan
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        updated_life_plan = self.updated_life_plan.to_dict()

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "updated_life_plan": updated_life_plan,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.life_plan import LifePlan  # noqa: PLC0415

        d = dict(src_dict)
        updated_life_plan = LifePlan.from_dict(d.pop("updated_life_plan"))

        life_plan_update_result = cls(
            updated_life_plan=updated_life_plan,
        )

        life_plan_update_result.additional_properties = d
        return life_plan_update_result

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
