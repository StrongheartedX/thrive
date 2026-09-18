"""Shared doneness cases, run against the Python implementation.

The same JSON is used by ``compute-doneness.test.ts`` so the TypeScript port
stays pinned to these rules.
"""

import json
from dataclasses import dataclass
from pathlib import Path
from typing import Any, cast

import pendulum
import pytest
from jupiter.core.apps.big_plans.status import BigPlanStatus
from jupiter.core.apps.time_plans.sub.activity.compute_doneness import (
    compute_activity_doneness,
)
from jupiter.core.apps.time_plans.sub.activity.kind import TimePlanActivityKind
from jupiter.core.common.sub.inbox_tasks.status import InboxTaskStatus
from jupiter.framework.base.adate import ADate
from jupiter.framework.base.entity_id import EntityId
from jupiter.framework.base.entity_link import EntityLink
from jupiter.framework.base.timestamp import Timestamp
from pendulum.datetime import DateTime
from pendulum.tz.timezone import UTC

_CASES_PATH = Path(__file__).with_name("compute_doneness.cases.json")


@dataclass(frozen=True)
class _Plan:
    start_date: ADate
    end_date: ADate


@dataclass(frozen=True)
class _Activity:
    ref_id: EntityId
    kind: TimePlanActivityKind
    target: EntityLink


@dataclass(frozen=True)
class _Inbox:
    ref_id: EntityId
    status: InboxTaskStatus
    last_modified_time: Timestamp
    owner: EntityLink


@dataclass(frozen=True)
class _BigPlan:
    ref_id: EntityId
    status: BigPlanStatus
    last_modified_time: Timestamp


@dataclass(frozen=True)
class _Member:
    ref_id: EntityId
    stack_ref_id: EntityId | None


@dataclass(frozen=True)
class _Ref:
    ref_id: EntityId


def _load_cases() -> list[dict[str, Any]]:
    with _CASES_PATH.open() as handle:
        return cast(list[dict[str, Any]], json.load(handle))


def _entity_id(raw: str) -> EntityId:
    return EntityId(raw)


def _link(wire: str) -> EntityLink:
    the_type, purpose, ref_id = wire.rsplit(":", 2)
    return EntityLink(the_type=the_type, ref_id=_entity_id(ref_id), purpose=purpose)


def _timestamp(raw: str) -> Timestamp:
    parsed = pendulum.parse(raw, tz=UTC)
    if not isinstance(parsed, DateTime):
        raise ValueError(f"Expected a datetime timestamp, got {raw!r}")
    return Timestamp.from_date_and_time(parsed)


def _members(raw_members: list[dict[str, Any]] | None) -> list[_Member] | None:
    if raw_members is None:
        return None
    return [
        _Member(
            ref_id=_entity_id(member["ref_id"]),
            stack_ref_id=(
                _entity_id(member["stack_ref_id"])
                if member.get("stack_ref_id") is not None
                else None
            ),
        )
        for member in raw_members
    ]


def _refs(raw_refs: list[dict[str, Any]] | None) -> list[_Ref] | None:
    if raw_refs is None:
        return None
    return [_Ref(ref_id=_entity_id(raw["ref_id"])) for raw in raw_refs]


@pytest.mark.parametrize("case", _load_cases(), ids=lambda case: case["name"])
def test_compute_activity_doneness_matches_shared_cases(
    case: dict[str, Any],
) -> None:
    """Each shared JSON case produces the expected doneness map."""
    time_plan = _Plan(
        start_date=ADate.from_str(case["time_plan"]["start_date"]),
        end_date=ADate.from_str(case["time_plan"]["end_date"]),
    )
    activities = [
        _Activity(
            ref_id=_entity_id(activity["ref_id"]),
            kind=TimePlanActivityKind(activity["kind"]),
            target=_link(activity["target"]),
        )
        for activity in case["activities"]
    ]
    inbox_tasks = [
        _Inbox(
            ref_id=_entity_id(inbox_task["ref_id"]),
            status=InboxTaskStatus(inbox_task["status"]),
            last_modified_time=_timestamp(inbox_task["last_modified_time"]),
            owner=_link(inbox_task["owner"]),
        )
        for inbox_task in case["inbox_tasks"]
    ]
    big_plans = (
        [
            _BigPlan(
                ref_id=_entity_id(big_plan["ref_id"]),
                status=BigPlanStatus(big_plan["status"]),
                last_modified_time=_timestamp(big_plan["last_modified_time"]),
            )
            for big_plan in case["big_plans"]
        ]
        if "big_plans" in case
        else None
    )

    result = compute_activity_doneness(
        time_plan,
        activities,
        inbox_tasks,
        big_plans,
        _members(case.get("habits")),
        _refs(case.get("habit_stacks")),
        _members(case.get("chores")),
        _refs(case.get("chore_stacks")),
    )

    actual = {str(ref_id): doneness.value for ref_id, doneness in result.items()}
    assert actual == case["expected"]
