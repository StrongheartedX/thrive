"""Compute time-plan activity doneness from plan targets.

Keep in sync with ``compute-doneness.ts``. Doneness is a pure function of the
plan window and the state of activities, inbox tasks, big plans, habits,
chores, and stacks.
"""

from collections import defaultdict
from collections.abc import Iterable
from typing import Final, Protocol

from jupiter.core.apps.big_plans.status import BigPlanStatus
from jupiter.core.apps.time_plans.sub.activity.doneness import TimePlanActivityDoneness
from jupiter.core.apps.time_plans.sub.activity.kind import TimePlanActivityKind
from jupiter.core.common.sub.inbox_tasks.status import InboxTaskStatus
from jupiter.core.named_entity_tag import NamedEntityTag
from jupiter.framework.base.adate import ADate
from jupiter.framework.base.entity_id import EntityId
from jupiter.framework.base.entity_link import EntityLink
from jupiter.framework.base.timestamp import Timestamp

_INBOX_TASK_TYPE: Final[str] = "InboxTask"
_INBOX_MAKE_PROGRESS_EXTRA_DAYS: Final[int] = 30
_BIG_PLAN_MAKE_PROGRESS_EXTRA_DAYS: Final[int] = 60


class _TimePlanView(Protocol):
    @property
    def start_date(self) -> ADate: ...

    @property
    def end_date(self) -> ADate: ...


class _ActivityView(Protocol):
    @property
    def ref_id(self) -> EntityId: ...

    @property
    def kind(self) -> TimePlanActivityKind: ...

    @property
    def target(self) -> EntityLink: ...


class _InboxTaskView(Protocol):
    @property
    def ref_id(self) -> EntityId: ...

    @property
    def status(self) -> InboxTaskStatus: ...

    @property
    def last_modified_time(self) -> Timestamp: ...

    @property
    def owner(self) -> EntityLink: ...


class _BigPlanView(Protocol):
    @property
    def ref_id(self) -> EntityId: ...

    @property
    def status(self) -> BigPlanStatus: ...

    @property
    def last_modified_time(self) -> Timestamp: ...


class _StackMemberView(Protocol):
    @property
    def ref_id(self) -> EntityId: ...

    @property
    def stack_ref_id(self) -> EntityId | None: ...


class _RefView(Protocol):
    @property
    def ref_id(self) -> EntityId: ...


def compute_activity_doneness(
    time_plan: _TimePlanView,
    activities: Iterable[_ActivityView],
    inbox_tasks: Iterable[_InboxTaskView],
    big_plans: Iterable[_BigPlanView] | None = None,
    habits: Iterable[_StackMemberView] | None = None,
    habit_stacks: Iterable[_RefView] | None = None,
    chores: Iterable[_StackMemberView] | None = None,
    chore_stacks: Iterable[_RefView] | None = None,
) -> dict[EntityId, TimePlanActivityDoneness]:
    """Compute doneness for each activity that can be resolved from targets."""
    activity_list = list(activities)
    activity_doneness: dict[EntityId, TimePlanActivityDoneness] = {}

    inbox_tasks_by_ref_id = {it.ref_id: it for it in inbox_tasks}
    todo_owned_inbox_tasks_by_todo_ref_id: dict[EntityId, _InboxTaskView] = {}
    for inbox_task in inbox_tasks_by_ref_id.values():
        if inbox_task.owner.the_type == NamedEntityTag.TODO_TASK.value:
            todo_owned_inbox_tasks_by_todo_ref_id[inbox_task.owner.ref_id] = inbox_task

    big_plans_by_ref_id = {bp.ref_id: bp for bp in big_plans} if big_plans else {}
    habits_by_ref_id = {h.ref_id: h for h in habits} if habits else {}
    habit_stacks_by_ref_id = {s.ref_id: s for s in habit_stacks} if habit_stacks else {}
    chores_by_ref_id = {c.ref_id: c for c in chores} if chores else {}
    chore_stacks_by_ref_id = {s.ref_id: s for s in chore_stacks} if chore_stacks else {}
    activities_by_big_plan_ref_id: defaultdict[EntityId, list[EntityId]] = defaultdict(
        list
    )
    activities_by_habit_ref_id: defaultdict[EntityId, list[EntityId]] = defaultdict(
        list
    )
    activities_by_chore_ref_id: defaultdict[EntityId, list[EntityId]] = defaultdict(
        list
    )

    for activity in activity_list:
        resolved_inbox_task: _InboxTaskView | None = None
        if _is_std_target(activity.target, _INBOX_TASK_TYPE):
            resolved_inbox_task = inbox_tasks_by_ref_id.get(activity.target.ref_id)
        elif _is_std_target(activity.target, NamedEntityTag.TODO_TASK.value):
            resolved_inbox_task = todo_owned_inbox_tasks_by_todo_ref_id.get(
                activity.target.ref_id
            )

        if resolved_inbox_task is None:
            continue

        inbox_doneness = _inbox_task_doneness(
            time_plan, activity.kind, resolved_inbox_task
        )
        activity_doneness[activity.ref_id] = inbox_doneness

        if resolved_inbox_task.owner.the_type == NamedEntityTag.BIG_PLAN.value:
            activities_by_big_plan_ref_id[resolved_inbox_task.owner.ref_id].append(
                activity.ref_id
            )
        elif resolved_inbox_task.owner.the_type == NamedEntityTag.HABIT.value:
            activities_by_habit_ref_id[resolved_inbox_task.owner.ref_id].append(
                activity.ref_id
            )
        elif resolved_inbox_task.owner.the_type == NamedEntityTag.CHORE.value:
            activities_by_chore_ref_id[resolved_inbox_task.owner.ref_id].append(
                activity.ref_id
            )

    for activity in activity_list:
        if not _is_std_target(activity.target, NamedEntityTag.BIG_PLAN.value):
            continue

        if activity.target.ref_id not in big_plans_by_ref_id:
            activity_doneness[activity.ref_id] = TimePlanActivityDoneness.DONE
            continue

        big_plan = big_plans_by_ref_id[activity.target.ref_id]
        some_working_or_done, all_done, _majority_done = _subactivity_flags(
            activity_doneness, activities_by_big_plan_ref_id[big_plan.ref_id]
        )
        big_plan_doneness = _big_plan_doneness(
            time_plan,
            activity.kind,
            big_plan,
            some_working_or_done,
            all_done,
        )
        activity_doneness[activity.ref_id] = big_plan_doneness

    for activity in activity_list:
        if not _is_std_target(activity.target, NamedEntityTag.HABIT.value):
            continue

        if activity.target.ref_id not in habits_by_ref_id:
            activity_doneness[activity.ref_id] = TimePlanActivityDoneness.DONE
            continue

        some_working_or_done, all_done, majority_done = _subactivity_flags(
            activity_doneness, activities_by_habit_ref_id[activity.target.ref_id]
        )
        activity_doneness[activity.ref_id] = _doneness_from_sub_roll_up(
            activity.kind, some_working_or_done, all_done, majority_done
        )

    for activity in activity_list:
        if not _is_std_target(activity.target, NamedEntityTag.HABIT_STACK.value):
            continue

        if activity.target.ref_id not in habit_stacks_by_ref_id:
            activity_doneness[activity.ref_id] = TimePlanActivityDoneness.DONE
            continue

        member_habit_activity_ref_ids = _member_stack_activity_ref_ids(
            activity_list,
            habits_by_ref_id,
            activity.target.ref_id,
            NamedEntityTag.HABIT.value,
        )
        some_working_or_done, all_done, majority_done = _subactivity_flags(
            activity_doneness, member_habit_activity_ref_ids
        )
        activity_doneness[activity.ref_id] = _doneness_from_sub_roll_up(
            activity.kind, some_working_or_done, all_done, majority_done
        )

    for activity in activity_list:
        if not _is_std_target(activity.target, NamedEntityTag.CHORE.value):
            continue

        if activity.target.ref_id not in chores_by_ref_id:
            activity_doneness[activity.ref_id] = TimePlanActivityDoneness.DONE
            continue

        some_working_or_done, all_done, majority_done = _subactivity_flags(
            activity_doneness, activities_by_chore_ref_id[activity.target.ref_id]
        )
        activity_doneness[activity.ref_id] = _doneness_from_sub_roll_up(
            activity.kind, some_working_or_done, all_done, majority_done
        )

    for activity in activity_list:
        if not _is_std_target(activity.target, NamedEntityTag.CHORE_STACK.value):
            continue

        if activity.target.ref_id not in chore_stacks_by_ref_id:
            activity_doneness[activity.ref_id] = TimePlanActivityDoneness.DONE
            continue

        member_chore_activity_ref_ids = _member_stack_activity_ref_ids(
            activity_list,
            chores_by_ref_id,
            activity.target.ref_id,
            NamedEntityTag.CHORE.value,
        )
        some_working_or_done, all_done, majority_done = _subactivity_flags(
            activity_doneness, member_chore_activity_ref_ids
        )
        activity_doneness[activity.ref_id] = _doneness_from_sub_roll_up(
            activity.kind, some_working_or_done, all_done, majority_done
        )

    return activity_doneness


def _is_std_target(target: EntityLink, the_type: str) -> bool:
    """Whether the activity points at ``the_type`` with the std purpose."""
    return target.the_type == the_type and target.purpose == "std"


def _modified_in_time_plan_window(
    time_plan: _TimePlanView, last_modified_time: Timestamp, extra_days: int
) -> bool:
    """Whether last_modified sits in [start of start_date, end of end_date+extra]."""
    return (
        time_plan.start_date.to_timestamp_at_start_of_day()
        <= last_modified_time
        <= time_plan.end_date.add_days(extra_days).to_timestamp_at_end_of_day()
    )


def _inbox_task_doneness(
    time_plan: _TimePlanView,
    kind: TimePlanActivityKind,
    inbox_task: _InboxTaskView,
) -> TimePlanActivityDoneness:
    """Doneness for an inbox-task or todo-task activity."""
    if kind == TimePlanActivityKind.FINISH:
        if inbox_task.status.is_completed:
            return TimePlanActivityDoneness.DONE
        if inbox_task.status.is_working:
            return TimePlanActivityDoneness.WORKING
        return TimePlanActivityDoneness.NOT_DONE

    modified_in_time_plan = (
        inbox_task.status.is_working_or_more
        and _modified_in_time_plan_window(
            time_plan,
            inbox_task.last_modified_time,
            _INBOX_MAKE_PROGRESS_EXTRA_DAYS,
        )
    )
    if inbox_task.status.is_completed or modified_in_time_plan:
        return TimePlanActivityDoneness.DONE
    if inbox_task.status.is_working:
        return TimePlanActivityDoneness.WORKING
    return TimePlanActivityDoneness.NOT_DONE


def _big_plan_doneness(
    time_plan: _TimePlanView,
    kind: TimePlanActivityKind,
    big_plan: _BigPlanView,
    some_working_or_done: bool,
    all_done: bool,
) -> TimePlanActivityDoneness:
    """Doneness for a big-plan activity, including inbox-task subactivities."""
    if kind == TimePlanActivityKind.FINISH:
        if big_plan.status.is_completed:
            return TimePlanActivityDoneness.DONE
        if some_working_or_done:
            return TimePlanActivityDoneness.WORKING
        return TimePlanActivityDoneness.NOT_DONE

    modified_in_time_plan = (
        big_plan.status.is_working_or_more
        and _modified_in_time_plan_window(
            time_plan,
            big_plan.last_modified_time,
            _BIG_PLAN_MAKE_PROGRESS_EXTRA_DAYS,
        )
    )
    if big_plan.status.is_completed or all_done:
        return TimePlanActivityDoneness.DONE
    if modified_in_time_plan or some_working_or_done:
        return TimePlanActivityDoneness.WORKING
    return TimePlanActivityDoneness.NOT_DONE


def _subactivity_flags(
    activity_doneness: dict[EntityId, TimePlanActivityDoneness],
    sub_ref_ids: list[EntityId],
) -> tuple[bool, bool, bool]:
    """Return (some working or done, all done, majority done) for subactivities."""
    if len(sub_ref_ids) == 0:
        return False, False, False
    some_working_or_done = any(
        activity_doneness[a]
        in (TimePlanActivityDoneness.WORKING, TimePlanActivityDoneness.DONE)
        for a in sub_ref_ids
    )
    all_done = all(
        activity_doneness[a] == TimePlanActivityDoneness.DONE for a in sub_ref_ids
    )
    majority_done = (
        sum(
            1
            for a in sub_ref_ids
            if activity_doneness[a] == TimePlanActivityDoneness.DONE
        )
        / len(sub_ref_ids)
    ) > 0.5
    return some_working_or_done, all_done, majority_done


def _doneness_from_sub_roll_up(
    kind: TimePlanActivityKind,
    some_working_or_done: bool,
    all_done: bool,
    majority_done: bool,
) -> TimePlanActivityDoneness:
    """Habit/chore/stack doneness from already-computed subactivity flags."""
    if kind == TimePlanActivityKind.FINISH:
        if all_done:
            return TimePlanActivityDoneness.DONE
        if some_working_or_done:
            return TimePlanActivityDoneness.WORKING
        return TimePlanActivityDoneness.NOT_DONE

    if majority_done:
        return TimePlanActivityDoneness.DONE
    if some_working_or_done:
        return TimePlanActivityDoneness.WORKING
    return TimePlanActivityDoneness.NOT_DONE


def _member_stack_activity_ref_ids(
    activities: list[_ActivityView],
    members_by_ref_id: dict[EntityId, _StackMemberView],
    stack_ref_id: EntityId,
    member_type: str,
) -> list[EntityId]:
    """Activity ref ids for members of a habit or chore stack."""
    member_activity_ref_ids: list[EntityId] = []
    for member_activity in activities:
        if not _is_std_target(member_activity.target, member_type):
            continue
        member = members_by_ref_id.get(member_activity.target.ref_id)
        if member is None or member.stack_ref_id != stack_ref_id:
            continue
        member_activity_ref_ids.append(member_activity.ref_id)
    return member_activity_ref_ids
