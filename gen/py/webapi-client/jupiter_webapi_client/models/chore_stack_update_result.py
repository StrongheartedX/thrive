from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

if TYPE_CHECKING:
    from ..models.chore import Chore
    from ..models.chore_stack import ChoreStack


T = TypeVar("T", bound="ChoreStackUpdateResult")


@_attrs_define
class ChoreStackUpdateResult:
    """ChoreStackUpdate result.

    Attributes:
        updated_chore_stack (ChoreStack): A chore stack.
        updated_chores (list[Chore]):
    """

    updated_chore_stack: ChoreStack
    updated_chores: list[Chore]
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        updated_chore_stack = self.updated_chore_stack.to_dict()

        updated_chores = []
        for updated_chores_item_data in self.updated_chores:
            updated_chores_item = updated_chores_item_data.to_dict()
            updated_chores.append(updated_chores_item)

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "updated_chore_stack": updated_chore_stack,
                "updated_chores": updated_chores,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.chore import Chore  # noqa: PLC0415
        from ..models.chore_stack import ChoreStack  # noqa: PLC0415

        d = dict(src_dict)
        updated_chore_stack = ChoreStack.from_dict(d.pop("updated_chore_stack"))

        updated_chores = []
        _updated_chores = d.pop("updated_chores")
        for updated_chores_item_data in _updated_chores:
            updated_chores_item = Chore.from_dict(updated_chores_item_data)

            updated_chores.append(updated_chores_item)

        chore_stack_update_result = cls(
            updated_chore_stack=updated_chore_stack,
            updated_chores=updated_chores,
        )

        chore_stack_update_result.additional_properties = d
        return chore_stack_update_result

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
