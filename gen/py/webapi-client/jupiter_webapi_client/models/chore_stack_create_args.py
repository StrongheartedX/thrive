from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.recurring_task_period import RecurringTaskPeriod
from ..types import UNSET, Unset

T = TypeVar("T", bound="ChoreStackCreateArgs")


@_attrs_define
class ChoreStackCreateArgs:
    """Chore stack creation parameters.

    Attributes:
        name (str): The chore stack name.
        period (RecurringTaskPeriod): A period for a particular task.
        chore_ref_ids (list[str]):
        aspect_ref_id (None | str | Unset):
        chapter_ref_id (None | str | Unset):
        goal_ref_id (None | str | Unset):
    """

    name: str
    period: RecurringTaskPeriod
    chore_ref_ids: list[str]
    aspect_ref_id: None | str | Unset = UNSET
    chapter_ref_id: None | str | Unset = UNSET
    goal_ref_id: None | str | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        name = self.name

        period = self.period.value

        chore_ref_ids = self.chore_ref_ids

        aspect_ref_id: None | str | Unset
        if isinstance(self.aspect_ref_id, Unset):
            aspect_ref_id = UNSET
        else:
            aspect_ref_id = self.aspect_ref_id

        chapter_ref_id: None | str | Unset
        if isinstance(self.chapter_ref_id, Unset):
            chapter_ref_id = UNSET
        else:
            chapter_ref_id = self.chapter_ref_id

        goal_ref_id: None | str | Unset
        if isinstance(self.goal_ref_id, Unset):
            goal_ref_id = UNSET
        else:
            goal_ref_id = self.goal_ref_id

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "name": name,
                "period": period,
                "chore_ref_ids": chore_ref_ids,
            }
        )
        if aspect_ref_id is not UNSET:
            field_dict["aspect_ref_id"] = aspect_ref_id
        if chapter_ref_id is not UNSET:
            field_dict["chapter_ref_id"] = chapter_ref_id
        if goal_ref_id is not UNSET:
            field_dict["goal_ref_id"] = goal_ref_id

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        name = d.pop("name")

        period = RecurringTaskPeriod(d.pop("period"))

        chore_ref_ids = cast(list[str], d.pop("chore_ref_ids"))

        def _parse_aspect_ref_id(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        aspect_ref_id = _parse_aspect_ref_id(d.pop("aspect_ref_id", UNSET))

        def _parse_chapter_ref_id(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        chapter_ref_id = _parse_chapter_ref_id(d.pop("chapter_ref_id", UNSET))

        def _parse_goal_ref_id(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        goal_ref_id = _parse_goal_ref_id(d.pop("goal_ref_id", UNSET))

        chore_stack_create_args = cls(
            name=name,
            period=period,
            chore_ref_ids=chore_ref_ids,
            aspect_ref_id=aspect_ref_id,
            chapter_ref_id=chapter_ref_id,
            goal_ref_id=goal_ref_id,
        )

        chore_stack_create_args.additional_properties = d
        return chore_stack_create_args

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
