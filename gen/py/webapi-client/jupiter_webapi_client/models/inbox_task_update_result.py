from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.big_plan_stats import BigPlanStats
    from ..models.inbox_task import InboxTask
    from ..models.record_score_result import RecordScoreResult


T = TypeVar("T", bound="InboxTaskUpdateResult")


@_attrs_define
class InboxTaskUpdateResult:
    """InboxTaskUpdate result.

    Attributes:
        updated_inbox_task (InboxTask): An inbox task.
        record_score_result (None | RecordScoreResult | Unset):
        updated_big_plan_stats (BigPlanStats | None | Unset):
    """

    updated_inbox_task: InboxTask
    record_score_result: None | RecordScoreResult | Unset = UNSET
    updated_big_plan_stats: BigPlanStats | None | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        from ..models.big_plan_stats import BigPlanStats  # noqa: PLC0415
        from ..models.record_score_result import RecordScoreResult  # noqa: PLC0415

        updated_inbox_task = self.updated_inbox_task.to_dict()

        record_score_result: dict[str, Any] | None | Unset
        if isinstance(self.record_score_result, Unset):
            record_score_result = UNSET
        elif isinstance(self.record_score_result, RecordScoreResult):
            record_score_result = self.record_score_result.to_dict()
        else:
            record_score_result = self.record_score_result

        updated_big_plan_stats: dict[str, Any] | None | Unset
        if isinstance(self.updated_big_plan_stats, Unset):
            updated_big_plan_stats = UNSET
        elif isinstance(self.updated_big_plan_stats, BigPlanStats):
            updated_big_plan_stats = self.updated_big_plan_stats.to_dict()
        else:
            updated_big_plan_stats = self.updated_big_plan_stats

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "updated_inbox_task": updated_inbox_task,
            }
        )
        if record_score_result is not UNSET:
            field_dict["record_score_result"] = record_score_result
        if updated_big_plan_stats is not UNSET:
            field_dict["updated_big_plan_stats"] = updated_big_plan_stats

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.big_plan_stats import BigPlanStats  # noqa: PLC0415
        from ..models.inbox_task import InboxTask  # noqa: PLC0415
        from ..models.record_score_result import RecordScoreResult  # noqa: PLC0415

        d = dict(src_dict)
        updated_inbox_task = InboxTask.from_dict(d.pop("updated_inbox_task"))

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

        def _parse_updated_big_plan_stats(data: object) -> BigPlanStats | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                updated_big_plan_stats_type_0 = BigPlanStats.from_dict(data)

                return updated_big_plan_stats_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(BigPlanStats | None | Unset, data)

        updated_big_plan_stats = _parse_updated_big_plan_stats(d.pop("updated_big_plan_stats", UNSET))

        inbox_task_update_result = cls(
            updated_inbox_task=updated_inbox_task,
            record_score_result=record_score_result,
            updated_big_plan_stats=updated_big_plan_stats,
        )

        inbox_task_update_result.additional_properties = d
        return inbox_task_update_result

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
