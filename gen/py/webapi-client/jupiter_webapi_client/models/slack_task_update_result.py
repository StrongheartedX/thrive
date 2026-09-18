from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

if TYPE_CHECKING:
    from ..models.inbox_task import InboxTask
    from ..models.slack_task import SlackTask


T = TypeVar("T", bound="SlackTaskUpdateResult")


@_attrs_define
class SlackTaskUpdateResult:
    """SlackTaskUpdate result.

    Attributes:
        updated_slack_task (SlackTask): A Slack task which needs to be converted into an inbox task.
        updated_inbox_task (InboxTask): An inbox task.
    """

    updated_slack_task: SlackTask
    updated_inbox_task: InboxTask
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        updated_slack_task = self.updated_slack_task.to_dict()

        updated_inbox_task = self.updated_inbox_task.to_dict()

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "updated_slack_task": updated_slack_task,
                "updated_inbox_task": updated_inbox_task,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.inbox_task import InboxTask  # noqa: PLC0415
        from ..models.slack_task import SlackTask  # noqa: PLC0415

        d = dict(src_dict)
        updated_slack_task = SlackTask.from_dict(d.pop("updated_slack_task"))

        updated_inbox_task = InboxTask.from_dict(d.pop("updated_inbox_task"))

        slack_task_update_result = cls(
            updated_slack_task=updated_slack_task,
            updated_inbox_task=updated_inbox_task,
        )

        slack_task_update_result.additional_properties = d
        return slack_task_update_result

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
