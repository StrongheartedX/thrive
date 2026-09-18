from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

if TYPE_CHECKING:
    from ..models.inbox_task import InboxTask
    from ..models.occasion import Occasion
    from ..models.time_event_full_days_block import TimeEventFullDaysBlock


T = TypeVar("T", bound="OccasionUpdateResult")


@_attrs_define
class OccasionUpdateResult:
    """OccasionUpdate result.

    Attributes:
        updated_occasion (Occasion): An occasion.
        updated_inbox_tasks (list[InboxTask]):
        updated_time_event_full_days_blocks (list[TimeEventFullDaysBlock]):
    """

    updated_occasion: Occasion
    updated_inbox_tasks: list[InboxTask]
    updated_time_event_full_days_blocks: list[TimeEventFullDaysBlock]
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        updated_occasion = self.updated_occasion.to_dict()

        updated_inbox_tasks = []
        for updated_inbox_tasks_item_data in self.updated_inbox_tasks:
            updated_inbox_tasks_item = updated_inbox_tasks_item_data.to_dict()
            updated_inbox_tasks.append(updated_inbox_tasks_item)

        updated_time_event_full_days_blocks = []
        for updated_time_event_full_days_blocks_item_data in self.updated_time_event_full_days_blocks:
            updated_time_event_full_days_blocks_item = updated_time_event_full_days_blocks_item_data.to_dict()
            updated_time_event_full_days_blocks.append(updated_time_event_full_days_blocks_item)

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "updated_occasion": updated_occasion,
                "updated_inbox_tasks": updated_inbox_tasks,
                "updated_time_event_full_days_blocks": updated_time_event_full_days_blocks,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.inbox_task import InboxTask  # noqa: PLC0415
        from ..models.occasion import Occasion  # noqa: PLC0415
        from ..models.time_event_full_days_block import TimeEventFullDaysBlock  # noqa: PLC0415

        d = dict(src_dict)
        updated_occasion = Occasion.from_dict(d.pop("updated_occasion"))

        updated_inbox_tasks = []
        _updated_inbox_tasks = d.pop("updated_inbox_tasks")
        for updated_inbox_tasks_item_data in _updated_inbox_tasks:
            updated_inbox_tasks_item = InboxTask.from_dict(updated_inbox_tasks_item_data)

            updated_inbox_tasks.append(updated_inbox_tasks_item)

        updated_time_event_full_days_blocks = []
        _updated_time_event_full_days_blocks = d.pop("updated_time_event_full_days_blocks")
        for updated_time_event_full_days_blocks_item_data in _updated_time_event_full_days_blocks:
            updated_time_event_full_days_blocks_item = TimeEventFullDaysBlock.from_dict(
                updated_time_event_full_days_blocks_item_data
            )

            updated_time_event_full_days_blocks.append(updated_time_event_full_days_blocks_item)

        occasion_update_result = cls(
            updated_occasion=updated_occasion,
            updated_inbox_tasks=updated_inbox_tasks,
            updated_time_event_full_days_blocks=updated_time_event_full_days_blocks,
        )

        occasion_update_result.additional_properties = d
        return occasion_update_result

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
