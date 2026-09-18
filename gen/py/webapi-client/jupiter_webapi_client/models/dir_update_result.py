from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

if TYPE_CHECKING:
    from ..models.dir_ import Dir


T = TypeVar("T", bound="DirUpdateResult")


@_attrs_define
class DirUpdateResult:
    """DirUpdate result.

    Attributes:
        updated_dir (Dir): A directory in the doc collection.
    """

    updated_dir: Dir
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        updated_dir = self.updated_dir.to_dict()

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "updated_dir": updated_dir,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.dir_ import Dir  # noqa: PLC0415

        d = dict(src_dict)
        updated_dir = Dir.from_dict(d.pop("updated_dir"))

        dir_update_result = cls(
            updated_dir=updated_dir,
        )

        dir_update_result.additional_properties = d
        return dir_update_result

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
