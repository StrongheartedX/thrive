from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

if TYPE_CHECKING:
    from ..models.chore_stack_update_args_aspect_ref_id import ChoreStackUpdateArgsAspectRefId
    from ..models.chore_stack_update_args_chapter_ref_id import ChoreStackUpdateArgsChapterRefId
    from ..models.chore_stack_update_args_chore_ref_ids import ChoreStackUpdateArgsChoreRefIds
    from ..models.chore_stack_update_args_goal_ref_id import ChoreStackUpdateArgsGoalRefId
    from ..models.chore_stack_update_args_name import ChoreStackUpdateArgsName


T = TypeVar("T", bound="ChoreStackUpdateArgs")


@_attrs_define
class ChoreStackUpdateArgs:
    """Chore stack update parameters.

    Attributes:
        ref_id (str): A generic entity id.
        name (ChoreStackUpdateArgsName):
        chore_ref_ids (ChoreStackUpdateArgsChoreRefIds):
        aspect_ref_id (ChoreStackUpdateArgsAspectRefId):
        chapter_ref_id (ChoreStackUpdateArgsChapterRefId):
        goal_ref_id (ChoreStackUpdateArgsGoalRefId):
    """

    ref_id: str
    name: ChoreStackUpdateArgsName
    chore_ref_ids: ChoreStackUpdateArgsChoreRefIds
    aspect_ref_id: ChoreStackUpdateArgsAspectRefId
    chapter_ref_id: ChoreStackUpdateArgsChapterRefId
    goal_ref_id: ChoreStackUpdateArgsGoalRefId
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        ref_id = self.ref_id

        name = self.name.to_dict()

        chore_ref_ids = self.chore_ref_ids.to_dict()

        aspect_ref_id = self.aspect_ref_id.to_dict()

        chapter_ref_id = self.chapter_ref_id.to_dict()

        goal_ref_id = self.goal_ref_id.to_dict()

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "ref_id": ref_id,
                "name": name,
                "chore_ref_ids": chore_ref_ids,
                "aspect_ref_id": aspect_ref_id,
                "chapter_ref_id": chapter_ref_id,
                "goal_ref_id": goal_ref_id,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.chore_stack_update_args_aspect_ref_id import ChoreStackUpdateArgsAspectRefId  # noqa: PLC0415
        from ..models.chore_stack_update_args_chapter_ref_id import ChoreStackUpdateArgsChapterRefId  # noqa: PLC0415
        from ..models.chore_stack_update_args_chore_ref_ids import ChoreStackUpdateArgsChoreRefIds  # noqa: PLC0415
        from ..models.chore_stack_update_args_goal_ref_id import ChoreStackUpdateArgsGoalRefId  # noqa: PLC0415
        from ..models.chore_stack_update_args_name import ChoreStackUpdateArgsName  # noqa: PLC0415

        d = dict(src_dict)
        ref_id = d.pop("ref_id")

        name = ChoreStackUpdateArgsName.from_dict(d.pop("name"))

        chore_ref_ids = ChoreStackUpdateArgsChoreRefIds.from_dict(d.pop("chore_ref_ids"))

        aspect_ref_id = ChoreStackUpdateArgsAspectRefId.from_dict(d.pop("aspect_ref_id"))

        chapter_ref_id = ChoreStackUpdateArgsChapterRefId.from_dict(d.pop("chapter_ref_id"))

        goal_ref_id = ChoreStackUpdateArgsGoalRefId.from_dict(d.pop("goal_ref_id"))

        chore_stack_update_args = cls(
            ref_id=ref_id,
            name=name,
            chore_ref_ids=chore_ref_ids,
            aspect_ref_id=aspect_ref_id,
            chapter_ref_id=chapter_ref_id,
            goal_ref_id=goal_ref_id,
        )

        chore_stack_update_args.additional_properties = d
        return chore_stack_update_args

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
