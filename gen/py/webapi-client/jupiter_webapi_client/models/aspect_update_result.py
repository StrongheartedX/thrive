from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

if TYPE_CHECKING:
    from ..models.aspect import Aspect


T = TypeVar("T", bound="AspectUpdateResult")


@_attrs_define
class AspectUpdateResult:
    """AspectUpdate result.

    Attributes:
        updated_aspect (Aspect): The aspect.
    """

    updated_aspect: Aspect
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        updated_aspect = self.updated_aspect.to_dict()

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "updated_aspect": updated_aspect,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.aspect import Aspect  # noqa: PLC0415

        d = dict(src_dict)
        updated_aspect = Aspect.from_dict(d.pop("updated_aspect"))

        aspect_update_result = cls(
            updated_aspect=updated_aspect,
        )

        aspect_update_result.additional_properties = d
        return aspect_update_result

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
