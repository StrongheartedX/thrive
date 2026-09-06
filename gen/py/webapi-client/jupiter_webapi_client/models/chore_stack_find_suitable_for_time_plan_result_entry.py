from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.aspect import Aspect
    from ..models.chore import Chore
    from ..models.chore_stack import ChoreStack


T = TypeVar("T", bound="ChoreStackFindSuitableForTimePlanResultEntry")


@_attrs_define
class ChoreStackFindSuitableForTimePlanResultEntry:
    """A chore stack with suitability for adding to a time plan.

    Attributes:
        chore_stack (ChoreStack): A chore stack.
        chores (list[Chore]):
        has_uncompleted_historical_inbox_tasks (bool):
        would_generate_in_time_plan (bool):
        aspect (Aspect | None | Unset):
    """

    chore_stack: ChoreStack
    chores: list[Chore]
    has_uncompleted_historical_inbox_tasks: bool
    would_generate_in_time_plan: bool
    aspect: Aspect | None | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        from ..models.aspect import Aspect  # noqa: PLC0415

        chore_stack = self.chore_stack.to_dict()

        chores = []
        for chores_item_data in self.chores:
            chores_item = chores_item_data.to_dict()
            chores.append(chores_item)

        has_uncompleted_historical_inbox_tasks = self.has_uncompleted_historical_inbox_tasks

        would_generate_in_time_plan = self.would_generate_in_time_plan

        aspect: dict[str, Any] | None | Unset
        if isinstance(self.aspect, Unset):
            aspect = UNSET
        elif isinstance(self.aspect, Aspect):
            aspect = self.aspect.to_dict()
        else:
            aspect = self.aspect

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "chore_stack": chore_stack,
                "chores": chores,
                "has_uncompleted_historical_inbox_tasks": has_uncompleted_historical_inbox_tasks,
                "would_generate_in_time_plan": would_generate_in_time_plan,
            }
        )
        if aspect is not UNSET:
            field_dict["aspect"] = aspect

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.aspect import Aspect  # noqa: PLC0415
        from ..models.chore import Chore  # noqa: PLC0415
        from ..models.chore_stack import ChoreStack  # noqa: PLC0415

        d = dict(src_dict)
        chore_stack = ChoreStack.from_dict(d.pop("chore_stack"))

        chores = []
        _chores = d.pop("chores")
        for chores_item_data in _chores:
            chores_item = Chore.from_dict(chores_item_data)

            chores.append(chores_item)

        has_uncompleted_historical_inbox_tasks = d.pop("has_uncompleted_historical_inbox_tasks")

        would_generate_in_time_plan = d.pop("would_generate_in_time_plan")

        def _parse_aspect(data: object) -> Aspect | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                aspect_type_0 = Aspect.from_dict(data)

                return aspect_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(Aspect | None | Unset, data)

        aspect = _parse_aspect(d.pop("aspect", UNSET))

        chore_stack_find_suitable_for_time_plan_result_entry = cls(
            chore_stack=chore_stack,
            chores=chores,
            has_uncompleted_historical_inbox_tasks=has_uncompleted_historical_inbox_tasks,
            would_generate_in_time_plan=would_generate_in_time_plan,
            aspect=aspect,
        )

        chore_stack_find_suitable_for_time_plan_result_entry.additional_properties = d
        return chore_stack_find_suitable_for_time_plan_result_entry

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
