from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

if TYPE_CHECKING:
    from ..models.time_plan_activity import TimePlanActivity


T = TypeVar("T", bound="TimePlanActivityUpdateResult")


@_attrs_define
class TimePlanActivityUpdateResult:
    """TimePlanActivityUpdate result.

    Attributes:
        updated_time_plan_activity (TimePlanActivity): A certain activity that happens in a plan.
    """

    updated_time_plan_activity: TimePlanActivity
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        updated_time_plan_activity = self.updated_time_plan_activity.to_dict()

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "updated_time_plan_activity": updated_time_plan_activity,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.time_plan_activity import TimePlanActivity  # noqa: PLC0415

        d = dict(src_dict)
        updated_time_plan_activity = TimePlanActivity.from_dict(d.pop("updated_time_plan_activity"))

        time_plan_activity_update_result = cls(
            updated_time_plan_activity=updated_time_plan_activity,
        )

        time_plan_activity_update_result.additional_properties = d
        return time_plan_activity_update_result

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
