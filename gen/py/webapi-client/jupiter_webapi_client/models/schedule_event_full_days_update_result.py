from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

if TYPE_CHECKING:
    from ..models.schedule_event_full_days import ScheduleEventFullDays
    from ..models.time_event_full_days_block import TimeEventFullDaysBlock


T = TypeVar("T", bound="ScheduleEventFullDaysUpdateResult")


@_attrs_define
class ScheduleEventFullDaysUpdateResult:
    """ScheduleEventFullDaysUpdate result.

    Attributes:
        updated_schedule_event_full_days (ScheduleEventFullDays): A full day block in a schedule.
        updated_time_event_full_days_block (TimeEventFullDaysBlock): A full day block of time.
    """

    updated_schedule_event_full_days: ScheduleEventFullDays
    updated_time_event_full_days_block: TimeEventFullDaysBlock
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        updated_schedule_event_full_days = self.updated_schedule_event_full_days.to_dict()

        updated_time_event_full_days_block = self.updated_time_event_full_days_block.to_dict()

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "updated_schedule_event_full_days": updated_schedule_event_full_days,
                "updated_time_event_full_days_block": updated_time_event_full_days_block,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.schedule_event_full_days import ScheduleEventFullDays  # noqa: PLC0415
        from ..models.time_event_full_days_block import TimeEventFullDaysBlock  # noqa: PLC0415

        d = dict(src_dict)
        updated_schedule_event_full_days = ScheduleEventFullDays.from_dict(d.pop("updated_schedule_event_full_days"))

        updated_time_event_full_days_block = TimeEventFullDaysBlock.from_dict(
            d.pop("updated_time_event_full_days_block")
        )

        schedule_event_full_days_update_result = cls(
            updated_schedule_event_full_days=updated_schedule_event_full_days,
            updated_time_event_full_days_block=updated_time_event_full_days_block,
        )

        schedule_event_full_days_update_result.additional_properties = d
        return schedule_event_full_days_update_result

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
