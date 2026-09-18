from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.big_plan import BigPlan
    from ..models.inbox_task import InboxTask
    from ..models.record_score_result import RecordScoreResult


T = TypeVar("T", bound="BigPlanUpdateResult")


@_attrs_define
class BigPlanUpdateResult:
    """BigPlanUpdate result.

    Attributes:
        updated_big_plan (BigPlan): A big plan.
        updated_inbox_tasks (list[InboxTask]):
        record_score_result (None | RecordScoreResult | Unset):
    """

    updated_big_plan: BigPlan
    updated_inbox_tasks: list[InboxTask]
    record_score_result: None | RecordScoreResult | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        from ..models.record_score_result import RecordScoreResult  # noqa: PLC0415

        updated_big_plan = self.updated_big_plan.to_dict()

        updated_inbox_tasks = []
        for updated_inbox_tasks_item_data in self.updated_inbox_tasks:
            updated_inbox_tasks_item = updated_inbox_tasks_item_data.to_dict()
            updated_inbox_tasks.append(updated_inbox_tasks_item)

        record_score_result: dict[str, Any] | None | Unset
        if isinstance(self.record_score_result, Unset):
            record_score_result = UNSET
        elif isinstance(self.record_score_result, RecordScoreResult):
            record_score_result = self.record_score_result.to_dict()
        else:
            record_score_result = self.record_score_result

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "updated_big_plan": updated_big_plan,
                "updated_inbox_tasks": updated_inbox_tasks,
            }
        )
        if record_score_result is not UNSET:
            field_dict["record_score_result"] = record_score_result

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.big_plan import BigPlan  # noqa: PLC0415
        from ..models.inbox_task import InboxTask  # noqa: PLC0415
        from ..models.record_score_result import RecordScoreResult  # noqa: PLC0415

        d = dict(src_dict)
        updated_big_plan = BigPlan.from_dict(d.pop("updated_big_plan"))

        updated_inbox_tasks = []
        _updated_inbox_tasks = d.pop("updated_inbox_tasks")
        for updated_inbox_tasks_item_data in _updated_inbox_tasks:
            updated_inbox_tasks_item = InboxTask.from_dict(updated_inbox_tasks_item_data)

            updated_inbox_tasks.append(updated_inbox_tasks_item)

        def _parse_record_score_result(data: object) -> None | RecordScoreResult | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                record_score_result_type_0 = RecordScoreResult.from_dict(data)

                return record_score_result_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(None | RecordScoreResult | Unset, data)

        record_score_result = _parse_record_score_result(d.pop("record_score_result", UNSET))

        big_plan_update_result = cls(
            updated_big_plan=updated_big_plan,
            updated_inbox_tasks=updated_inbox_tasks,
            record_score_result=record_score_result,
        )

        big_plan_update_result.additional_properties = d
        return big_plan_update_result

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
