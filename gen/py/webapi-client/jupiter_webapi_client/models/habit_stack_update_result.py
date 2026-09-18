from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

if TYPE_CHECKING:
    from ..models.habit import Habit
    from ..models.habit_stack import HabitStack


T = TypeVar("T", bound="HabitStackUpdateResult")


@_attrs_define
class HabitStackUpdateResult:
    """HabitStackUpdate result.

    Attributes:
        updated_habit_stack (HabitStack): A habit stack.
        updated_habits (list[Habit]):
    """

    updated_habit_stack: HabitStack
    updated_habits: list[Habit]
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        updated_habit_stack = self.updated_habit_stack.to_dict()

        updated_habits = []
        for updated_habits_item_data in self.updated_habits:
            updated_habits_item = updated_habits_item_data.to_dict()
            updated_habits.append(updated_habits_item)

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "updated_habit_stack": updated_habit_stack,
                "updated_habits": updated_habits,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.habit import Habit  # noqa: PLC0415
        from ..models.habit_stack import HabitStack  # noqa: PLC0415

        d = dict(src_dict)
        updated_habit_stack = HabitStack.from_dict(d.pop("updated_habit_stack"))

        updated_habits = []
        _updated_habits = d.pop("updated_habits")
        for updated_habits_item_data in _updated_habits:
            updated_habits_item = Habit.from_dict(updated_habits_item_data)

            updated_habits.append(updated_habits_item)

        habit_stack_update_result = cls(
            updated_habit_stack=updated_habit_stack,
            updated_habits=updated_habits,
        )

        habit_stack_update_result.additional_properties = d
        return habit_stack_update_result

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
