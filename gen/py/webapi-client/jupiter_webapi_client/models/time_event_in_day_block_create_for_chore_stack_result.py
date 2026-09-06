from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

if TYPE_CHECKING:
    from ..models.time_event_in_day_block import TimeEventInDayBlock


T = TypeVar("T", bound="TimeEventInDayBlockCreateForChoreStackResult")


@_attrs_define
class TimeEventInDayBlockCreateForChoreStackResult:
    """Result.

    Attributes:
        new_time_events (list[TimeEventInDayBlock]):
    """

    new_time_events: list[TimeEventInDayBlock]
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        new_time_events = []
        for new_time_events_item_data in self.new_time_events:
            new_time_events_item = new_time_events_item_data.to_dict()
            new_time_events.append(new_time_events_item)

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "new_time_events": new_time_events,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.time_event_in_day_block import TimeEventInDayBlock  # noqa: PLC0415

        d = dict(src_dict)
        new_time_events = []
        _new_time_events = d.pop("new_time_events")
        for new_time_events_item_data in _new_time_events:
            new_time_events_item = TimeEventInDayBlock.from_dict(new_time_events_item_data)

            new_time_events.append(new_time_events_item)

        time_event_in_day_block_create_for_chore_stack_result = cls(
            new_time_events=new_time_events,
        )

        time_event_in_day_block_create_for_chore_stack_result.additional_properties = d
        return time_event_in_day_block_create_for_chore_stack_result

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
