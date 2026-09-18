from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

if TYPE_CHECKING:
    from ..models.workspace import Workspace


T = TypeVar("T", bound="WorkspaceUpdateResult")


@_attrs_define
class WorkspaceUpdateResult:
    """WorkspaceUpdate result.

    Attributes:
        updated_workspace (Workspace): The workspace where everything happens.
    """

    updated_workspace: Workspace
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        updated_workspace = self.updated_workspace.to_dict()

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "updated_workspace": updated_workspace,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.workspace import Workspace  # noqa: PLC0415

        d = dict(src_dict)
        updated_workspace = Workspace.from_dict(d.pop("updated_workspace"))

        workspace_update_result = cls(
            updated_workspace=updated_workspace,
        )

        workspace_update_result.additional_properties = d
        return workspace_update_result

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
