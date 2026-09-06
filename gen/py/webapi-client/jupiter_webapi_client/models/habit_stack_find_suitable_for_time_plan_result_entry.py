from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.aspect import Aspect
    from ..models.habit import Habit
    from ..models.habit_stack import HabitStack


T = TypeVar("T", bound="HabitStackFindSuitableForTimePlanResultEntry")


@_attrs_define
class HabitStackFindSuitableForTimePlanResultEntry:
    """A habit stack with suitability for adding to a time plan.

    Attributes:
        habit_stack (HabitStack): A habit stack.
        habits (list[Habit]):
        has_uncompleted_historical_inbox_tasks (bool):
        would_generate_in_time_plan (bool):
        aspect (Aspect | None | Unset):
    """

    habit_stack: HabitStack
    habits: list[Habit]
    has_uncompleted_historical_inbox_tasks: bool
    would_generate_in_time_plan: bool
    aspect: Aspect | None | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        from ..models.aspect import Aspect  # noqa: PLC0415

        habit_stack = self.habit_stack.to_dict()

        habits = []
        for habits_item_data in self.habits:
            habits_item = habits_item_data.to_dict()
            habits.append(habits_item)

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
                "habit_stack": habit_stack,
                "habits": habits,
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
        from ..models.habit import Habit  # noqa: PLC0415
        from ..models.habit_stack import HabitStack  # noqa: PLC0415

        d = dict(src_dict)
        habit_stack = HabitStack.from_dict(d.pop("habit_stack"))

        habits = []
        _habits = d.pop("habits")
        for habits_item_data in _habits:
            habits_item = Habit.from_dict(habits_item_data)

            habits.append(habits_item)

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

        habit_stack_find_suitable_for_time_plan_result_entry = cls(
            habit_stack=habit_stack,
            habits=habits,
            has_uncompleted_historical_inbox_tasks=has_uncompleted_historical_inbox_tasks,
            would_generate_in_time_plan=would_generate_in_time_plan,
            aspect=aspect,
        )

        habit_stack_find_suitable_for_time_plan_result_entry.additional_properties = d
        return habit_stack_find_suitable_for_time_plan_result_entry

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
