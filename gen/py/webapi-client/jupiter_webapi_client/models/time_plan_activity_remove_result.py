from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

T = TypeVar("T", bound="TimePlanActivityRemoveResult")


@_attrs_define
class TimePlanActivityRemoveResult:
    """Result.

    Attributes:
        removed_time_plan_activity_ref_ids (list[str]):
    """

    removed_time_plan_activity_ref_ids: list[str]
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        removed_time_plan_activity_ref_ids = self.removed_time_plan_activity_ref_ids

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "removed_time_plan_activity_ref_ids": removed_time_plan_activity_ref_ids,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        removed_time_plan_activity_ref_ids = cast(list[str], d.pop("removed_time_plan_activity_ref_ids"))

        time_plan_activity_remove_result = cls(
            removed_time_plan_activity_ref_ids=removed_time_plan_activity_ref_ids,
        )

        time_plan_activity_remove_result.additional_properties = d
        return time_plan_activity_remove_result

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
