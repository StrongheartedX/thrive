from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

if TYPE_CHECKING:
    from ..models.time_event_in_day_block import TimeEventInDayBlock


T = TypeVar("T", bound="TimeEventInDayBlockUpdateResult")


@_attrs_define
class TimeEventInDayBlockUpdateResult:
    """TimeEventInDayBlockUpdate result.

    Attributes:
        updated_time_event_in_day_block (TimeEventInDayBlock): Time event.
    """

    updated_time_event_in_day_block: TimeEventInDayBlock
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        updated_time_event_in_day_block = self.updated_time_event_in_day_block.to_dict()

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "updated_time_event_in_day_block": updated_time_event_in_day_block,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.time_event_in_day_block import TimeEventInDayBlock  # noqa: PLC0415

        d = dict(src_dict)
        updated_time_event_in_day_block = TimeEventInDayBlock.from_dict(d.pop("updated_time_event_in_day_block"))

        time_event_in_day_block_update_result = cls(
            updated_time_event_in_day_block=updated_time_event_in_day_block,
        )

        time_event_in_day_block_update_result.additional_properties = d
        return time_event_in_day_block_update_result

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
