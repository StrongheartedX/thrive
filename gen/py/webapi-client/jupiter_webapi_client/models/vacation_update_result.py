from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

if TYPE_CHECKING:
    from ..models.time_event_full_days_block import TimeEventFullDaysBlock
    from ..models.vacation import Vacation


T = TypeVar("T", bound="VacationUpdateResult")


@_attrs_define
class VacationUpdateResult:
    """VacationUpdate result.

    Attributes:
        updated_vacation (Vacation): A vacation.
        updated_time_event_full_days_block (TimeEventFullDaysBlock): A full day block of time.
    """

    updated_vacation: Vacation
    updated_time_event_full_days_block: TimeEventFullDaysBlock
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        updated_vacation = self.updated_vacation.to_dict()

        updated_time_event_full_days_block = self.updated_time_event_full_days_block.to_dict()

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "updated_vacation": updated_vacation,
                "updated_time_event_full_days_block": updated_time_event_full_days_block,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.time_event_full_days_block import TimeEventFullDaysBlock  # noqa: PLC0415
        from ..models.vacation import Vacation  # noqa: PLC0415

        d = dict(src_dict)
        updated_vacation = Vacation.from_dict(d.pop("updated_vacation"))

        updated_time_event_full_days_block = TimeEventFullDaysBlock.from_dict(
            d.pop("updated_time_event_full_days_block")
        )

        vacation_update_result = cls(
            updated_vacation=updated_vacation,
            updated_time_event_full_days_block=updated_time_event_full_days_block,
        )

        vacation_update_result.additional_properties = d
        return vacation_update_result

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
