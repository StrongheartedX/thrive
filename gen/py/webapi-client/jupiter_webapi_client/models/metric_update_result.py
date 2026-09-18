from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

if TYPE_CHECKING:
    from ..models.inbox_task import InboxTask
    from ..models.metric import Metric


T = TypeVar("T", bound="MetricUpdateResult")


@_attrs_define
class MetricUpdateResult:
    """MetricUpdate result.

    Attributes:
        updated_metric (Metric): A metric.
        updated_inbox_tasks (list[InboxTask]):
    """

    updated_metric: Metric
    updated_inbox_tasks: list[InboxTask]
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        updated_metric = self.updated_metric.to_dict()

        updated_inbox_tasks = []
        for updated_inbox_tasks_item_data in self.updated_inbox_tasks:
            updated_inbox_tasks_item = updated_inbox_tasks_item_data.to_dict()
            updated_inbox_tasks.append(updated_inbox_tasks_item)

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "updated_metric": updated_metric,
                "updated_inbox_tasks": updated_inbox_tasks,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.inbox_task import InboxTask  # noqa: PLC0415
        from ..models.metric import Metric  # noqa: PLC0415

        d = dict(src_dict)
        updated_metric = Metric.from_dict(d.pop("updated_metric"))

        updated_inbox_tasks = []
        _updated_inbox_tasks = d.pop("updated_inbox_tasks")
        for updated_inbox_tasks_item_data in _updated_inbox_tasks:
            updated_inbox_tasks_item = InboxTask.from_dict(updated_inbox_tasks_item_data)

            updated_inbox_tasks.append(updated_inbox_tasks_item)

        metric_update_result = cls(
            updated_metric=updated_metric,
            updated_inbox_tasks=updated_inbox_tasks,
        )

        metric_update_result.additional_properties = d
        return metric_update_result

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
