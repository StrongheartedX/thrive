"""Use case for loading what the time plan view's activity panel shows."""

from jupiter.core.app import AppCore
from jupiter.core.apps.big_plans.root import BigPlan
from jupiter.core.apps.big_plans.service.load import (
    BigPlanLoadResult,
    BigPlanLoadService,
)
from jupiter.core.apps.chores.root import Chore
from jupiter.core.apps.chores.service.load import ChoreLoadResult, ChoreLoadService
from jupiter.core.apps.chores.sub.stack.root import ChoreStack
from jupiter.core.apps.chores.sub.stack.service.load import (
    ChoreStackLoadResult,
    ChoreStackLoadService,
)
from jupiter.core.apps.habits.sub.habit.root import Habit
from jupiter.core.apps.habits.sub.habit.service.load import (
    HabitLoadResult,
    HabitLoadService,
)
from jupiter.core.apps.habits.sub.stack.root import HabitStack
from jupiter.core.apps.habits.sub.stack.service.load import (
    HabitStackLoadResult,
    HabitStackLoadService,
)
from jupiter.core.apps.time_plans.sub.activity.root import TimePlanActivity
from jupiter.core.apps.todo.root import TodoTask
from jupiter.core.apps.todo.service.load import TodoTaskLoadResult, TodoTaskLoadService
from jupiter.core.common.sub.inbox_tasks.root import InboxTask, InboxTaskRepository
from jupiter.core.common.sub.inbox_tasks.service.load import (
    InboxTaskLoadResult,
    InboxTaskLoadService,
)
from jupiter.core.common.sub.inbox_tasks.status import InboxTaskStatus
from jupiter.core.common.sub.time_events.sub.in_day_block.root import (
    TimeEventInDayBlock,
)
from jupiter.core.config import (
    JupiterLoggedInReadonlyContext,
)
from jupiter.core.crown_entity_support import (
    JupiterFindCrownEntityArgs,
    JupiterFindCrownEntityUseCase,
)
from jupiter.core.features import WorkspaceFeature
from jupiter.core.named_entity_tag import NamedEntityTag
from jupiter.framework.base.entity_id import EntityId
from jupiter.framework.base.entity_link import EntityLink
from jupiter.framework.base.timestamp import Timestamp
from jupiter.framework.storage.repository import DomainUnitOfWork
from jupiter.framework.use_case import (
    readonly_use_case,
)
from jupiter.framework.use_case_io import (
    UseCaseResultBase,
    use_case_args,
    use_case_result,
)

# How far back a big plan's finished tasks are still worth showing.
RECENTLY_DONE_DAYS = 30


@use_case_args
class TimePlanActivityLoadForPanelArgs(JupiterFindCrownEntityArgs):
    """TimePlanActivityLoadForPanel args."""

    ref_id: EntityId
    allow_archived: bool | None


@use_case_result
class TimePlanActivityLoadForPanelResult(UseCaseResultBase):
    """TimePlanActivityLoadForPanel result.

    The target and its details are as for ``TimePlanActivityLoadResult``, except
    that the details leave out what the panel doesn't show: habits carry no
    streak marks, nothing carries its publish entity, and the tasks are the
    ones still worth showing (see the load services). The lists the editors
    pick from come from the time plan view itself, which loads them once.
    """

    time_plan_activity: TimePlanActivity
    time_event_blocks: list[TimeEventInDayBlock]
    target_inbox_task: InboxTask | None
    target_inbox_task_info: InboxTaskLoadResult | None
    target_big_plan: BigPlan | None
    target_big_plan_info: BigPlanLoadResult | None
    target_todo_task: TodoTask | None
    target_todo_task_info: TodoTaskLoadResult | None
    target_habit: Habit | None
    target_habit_info: HabitLoadResult | None
    target_habit_stack: HabitStack | None
    target_habit_stack_info: HabitStackLoadResult | None
    target_chore: Chore | None
    target_chore_info: ChoreLoadResult | None
    target_chore_stack: ChoreStack | None
    target_chore_stack_info: ChoreStackLoadResult | None
    # The inbox tasks of a habit or chore stack's members.
    stack_inbox_tasks: list[InboxTask]


@readonly_use_case(WorkspaceFeature.TIME_PLANS, only_for_component=[AppCore.WEBUI])
class TimePlanActivityLoadForPanelUseCase(
    JupiterFindCrownEntityUseCase[
        TimePlanActivityLoadForPanelArgs, TimePlanActivityLoadForPanelResult
    ]
):
    """Use case for loading what the time plan view's activity panel shows.

    Everything the panel needs beyond what the time plan view already has, in
    one go.
    """

    async def _perform_transactional_read(
        self,
        uow: DomainUnitOfWork,
        context: JupiterLoggedInReadonlyContext,
        args: TimePlanActivityLoadForPanelArgs,
    ) -> TimePlanActivityLoadForPanelResult:
        """Execute the command's action."""
        allow_archived = args.allow_archived or False
        workspace = context.workspace
        user_ref_id = context.user.ref_id

        time_plan_activity = await self.load_entity(
            uow,
            user_ref_id,
            TimePlanActivity,
            args.ref_id,
            allow_archived=allow_archived,
        )

        time_event_blocks = await uow.get_for(TimeEventInDayBlock).find_all_generic(
            allow_archived=False,
            owner=EntityLink.std(
                NamedEntityTag.TIME_PLAN_ACTIVITY.value,
                time_plan_activity.ref_id,
            ),
        )

        target_inbox_task = None
        target_inbox_task_info = None
        target_big_plan = None
        target_big_plan_info = None
        target_todo_task = None
        target_todo_task_info = None
        target_habit = None
        target_habit_info = None
        target_habit_stack = None
        target_habit_stack_info = None
        target_chore = None
        target_chore_info = None
        target_chore_stack = None
        target_chore_stack_info = None
        stack_inbox_tasks: list[InboxTask] = []

        # Activity targets are loadable whenever the activity is - access to the
        # time plan / activity does not require separate ACL on the target.
        target_ref_id = time_plan_activity.target.ref_id
        if time_plan_activity.is_target_inbox_task:
            target_inbox_task = await uow.get_for(InboxTask).load_by_id(
                target_ref_id, allow_archived=allow_archived
            )
            target_inbox_task_info = await InboxTaskLoadService().do_it(
                uow,
                target_inbox_task,
                user_ref_id=user_ref_id,
                allow_archived=allow_archived,
            )
        elif time_plan_activity.is_target_big_plan:
            if workspace.is_feature_available(WorkspaceFeature.BIG_PLANS):
                target_big_plan = await uow.get_for(BigPlan).load_by_id(
                    target_ref_id, allow_archived=allow_archived
                )
                target_big_plan_info = await BigPlanLoadService().do_it(
                    uow,
                    workspace.ref_id,
                    target_big_plan,
                    user_ref_id=user_ref_id,
                    allow_archived=allow_archived,
                    include_publish_entity=False,
                    # What's still to do, and what was finished recently.
                    only_active_inbox_tasks=True,
                    inbox_tasks_completed_after=Timestamp.from_date_and_time(
                        self._time_provider.get_current_time().value.subtract(
                            days=RECENTLY_DONE_DAYS
                        )
                    ),
                )
        elif time_plan_activity.is_target_todo_task:
            if workspace.is_feature_available(WorkspaceFeature.TODO_TASK):
                target_todo_task = await uow.get_for(TodoTask).load_by_id(
                    target_ref_id, allow_archived=allow_archived
                )
                target_todo_task_info = await TodoTaskLoadService().do_it(
                    uow,
                    workspace.ref_id,
                    target_todo_task,
                    user_ref_id=user_ref_id,
                    allow_archived=allow_archived,
                )
        elif time_plan_activity.is_target_habit:
            if workspace.is_feature_available(WorkspaceFeature.HABITS):
                target_habit = await uow.get_for(Habit).load_by_id(
                    target_ref_id, allow_archived=allow_archived
                )
                today = self._time_provider.get_current_date()
                target_habit_info = await HabitLoadService(self._time_provider).do_it(
                    uow,
                    workspace.ref_id,
                    target_habit,
                    user_ref_id=user_ref_id,
                    allow_archived=allow_archived,
                    # The panel shows no streaks, so only the narrowest range.
                    include_streak_marks_earliest_date=today,
                    include_streak_marks_latest_date=today,
                    include_publish_entity=False,
                    # The panel lists what's still to do, not the whole history.
                    only_active_inbox_tasks=True,
                )
        elif time_plan_activity.is_target_habit_stack:
            if workspace.is_feature_available(WorkspaceFeature.HABITS):
                target_habit_stack = await uow.get_for(HabitStack).load_by_id(
                    target_ref_id, allow_archived=allow_archived
                )
                target_habit_stack_info = await HabitStackLoadService().do_it(
                    uow,
                    target_habit_stack,
                    user_ref_id=user_ref_id,
                    allow_archived=allow_archived,
                    include_publish_entity=False,
                )
                stack_inbox_tasks = await self._members_inbox_tasks(
                    uow,
                    NamedEntityTag.HABIT,
                    [habit.ref_id for habit in target_habit_stack_info.habits],
                )
        elif time_plan_activity.is_target_chore:
            if workspace.is_feature_available(WorkspaceFeature.CHORES):
                target_chore = await uow.get_for(Chore).load_by_id(
                    target_ref_id, allow_archived=allow_archived
                )
                target_chore_info = await ChoreLoadService().do_it(
                    uow,
                    workspace.ref_id,
                    target_chore,
                    user_ref_id=user_ref_id,
                    allow_archived=allow_archived,
                    include_publish_entity=False,
                    # The panel lists what's still to do, not the whole history.
                    only_active_inbox_tasks=True,
                )
        elif time_plan_activity.is_target_chore_stack:
            if workspace.is_feature_available(WorkspaceFeature.CHORES):
                target_chore_stack = await uow.get_for(ChoreStack).load_by_id(
                    target_ref_id, allow_archived=allow_archived
                )
                target_chore_stack_info = await ChoreStackLoadService().do_it(
                    uow,
                    target_chore_stack,
                    user_ref_id=user_ref_id,
                    allow_archived=allow_archived,
                    include_publish_entity=False,
                )
                stack_inbox_tasks = await self._members_inbox_tasks(
                    uow,
                    NamedEntityTag.CHORE,
                    [chore.ref_id for chore in target_chore_stack_info.chores],
                )

        return TimePlanActivityLoadForPanelResult(
            time_plan_activity=time_plan_activity,
            time_event_blocks=time_event_blocks,
            target_inbox_task=target_inbox_task,
            target_inbox_task_info=target_inbox_task_info,
            target_big_plan=target_big_plan,
            target_big_plan_info=target_big_plan_info,
            target_todo_task=target_todo_task,
            target_todo_task_info=target_todo_task_info,
            target_habit=target_habit,
            target_habit_info=target_habit_info,
            target_habit_stack=target_habit_stack,
            target_habit_stack_info=target_habit_stack_info,
            target_chore=target_chore,
            target_chore_info=target_chore_info,
            target_chore_stack=target_chore_stack,
            target_chore_stack_info=target_chore_stack_info,
            stack_inbox_tasks=stack_inbox_tasks,
        )

    async def _members_inbox_tasks(
        self,
        uow: DomainUnitOfWork,
        member_tag: NamedEntityTag,
        member_ref_ids: list[EntityId],
    ) -> list[InboxTask]:
        if not member_ref_ids:
            return []
        return await uow.get(InboxTaskRepository).find_all_for_owner_created_desc(
            owner=[
                EntityLink.std(member_tag.value, ref_id) for ref_id in member_ref_ids
            ],
            allow_archived=False,
            filter_status=InboxTaskStatus.all_workable_statuses(),
        )
