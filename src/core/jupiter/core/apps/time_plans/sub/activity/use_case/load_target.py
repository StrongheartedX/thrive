"""Use case for loading a time plan activity and what it targets."""

from jupiter.core.app import AppCore
from jupiter.core.apps.big_plans.root import BigPlan
from jupiter.core.apps.chores.root import Chore
from jupiter.core.apps.chores.sub.stack.root import ChoreStack
from jupiter.core.apps.habits.sub.habit.root import Habit
from jupiter.core.apps.habits.sub.stack.root import HabitStack
from jupiter.core.apps.time_plans.sub.activity.root import TimePlanActivity
from jupiter.core.apps.todo.root import TodoTask
from jupiter.core.common.sub.inbox_tasks.root import InboxTask
from jupiter.core.config import (
    JupiterLoggedInReadonlyContext,
)
from jupiter.core.crown_entity_support import (
    JupiterLoadCrownEntityArgs,
    JupiterLoadCrownEntityUseCase,
)
from jupiter.core.features import WorkspaceFeature
from jupiter.framework.base.entity_id import EntityId
from jupiter.framework.storage.repository import DomainUnitOfWork
from jupiter.framework.use_case import (
    readonly_use_case,
)
from jupiter.framework.use_case_io import (
    UseCaseResultBase,
    use_case_args,
    use_case_result,
)


@use_case_args
class TimePlanActivityLoadTargetArgs(JupiterLoadCrownEntityArgs):
    """TimePlanActivityLoadTarget args."""

    ref_id: EntityId
    allow_archived: bool | None


@use_case_result
class TimePlanActivityLoadTargetResult(UseCaseResultBase):
    """TimePlanActivityLoadTarget result."""

    time_plan_activity: TimePlanActivity
    target_inbox_task: InboxTask | None
    target_big_plan: BigPlan | None
    target_todo_task: TodoTask | None
    target_habit: Habit | None
    target_habit_stack: HabitStack | None
    target_chore: Chore | None
    target_chore_stack: ChoreStack | None
    # The members of a habit or chore stack target.
    habit_stack_members: list[Habit]
    chore_stack_members: list[Chore]


@readonly_use_case(WorkspaceFeature.TIME_PLANS, only_for_component=[AppCore.WEBUI])
class TimePlanActivityLoadTargetUseCase(
    JupiterLoadCrownEntityUseCase[
        TimePlanActivityLoadTargetArgs, TimePlanActivityLoadTargetResult
    ]
):
    """Use case for loading a time plan activity and what it targets.

    For callers that name an activity or place events on it, and so need its
    target but none of the target's details.
    """

    async def _perform_transactional_read(
        self,
        uow: DomainUnitOfWork,
        context: JupiterLoggedInReadonlyContext,
        args: TimePlanActivityLoadTargetArgs,
    ) -> TimePlanActivityLoadTargetResult:
        """Execute the command's action."""
        allow_archived = args.allow_archived or False
        workspace = context.workspace

        time_plan_activity = await self.load_entity(
            uow,
            context.user.ref_id,
            TimePlanActivity,
            args.ref_id,
            allow_archived=allow_archived,
        )

        target_inbox_task = None
        target_big_plan = None
        target_todo_task = None
        target_habit = None
        target_habit_stack = None
        target_chore = None
        target_chore_stack = None
        habit_stack_members: list[Habit] = []
        chore_stack_members: list[Chore] = []

        # Activity targets are loadable whenever the activity is - access to the
        # time plan / activity does not require separate ACL on the target.
        target_ref_id = time_plan_activity.target.ref_id
        if time_plan_activity.is_target_inbox_task:
            target_inbox_task = await uow.get_for(InboxTask).load_by_id(
                target_ref_id, allow_archived=allow_archived
            )
        elif time_plan_activity.is_target_big_plan:
            if workspace.is_feature_available(WorkspaceFeature.BIG_PLANS):
                target_big_plan = await uow.get_for(BigPlan).load_by_id(
                    target_ref_id, allow_archived=allow_archived
                )
        elif time_plan_activity.is_target_todo_task:
            if workspace.is_feature_available(WorkspaceFeature.TODO_TASK):
                target_todo_task = await uow.get_for(TodoTask).load_by_id(
                    target_ref_id, allow_archived=allow_archived
                )
        elif time_plan_activity.is_target_habit:
            if workspace.is_feature_available(WorkspaceFeature.HABITS):
                target_habit = await uow.get_for(Habit).load_by_id(
                    target_ref_id, allow_archived=allow_archived
                )
        elif time_plan_activity.is_target_habit_stack:
            if workspace.is_feature_available(WorkspaceFeature.HABITS):
                target_habit_stack = await uow.get_for(HabitStack).load_by_id(
                    target_ref_id, allow_archived=allow_archived
                )
                habit_stack_members = await uow.get_for(Habit).find_all_generic(
                    parent_ref_id=None,
                    allow_archived=allow_archived,
                    stack_ref_id=target_habit_stack.ref_id,
                )
        elif time_plan_activity.is_target_chore:
            if workspace.is_feature_available(WorkspaceFeature.CHORES):
                target_chore = await uow.get_for(Chore).load_by_id(
                    target_ref_id, allow_archived=allow_archived
                )
        elif time_plan_activity.is_target_chore_stack:
            if workspace.is_feature_available(WorkspaceFeature.CHORES):
                target_chore_stack = await uow.get_for(ChoreStack).load_by_id(
                    target_ref_id, allow_archived=allow_archived
                )
                chore_stack_members = await uow.get_for(Chore).find_all_generic(
                    parent_ref_id=None,
                    allow_archived=allow_archived,
                    stack_ref_id=target_chore_stack.ref_id,
                )

        return TimePlanActivityLoadTargetResult(
            time_plan_activity=time_plan_activity,
            target_inbox_task=target_inbox_task,
            target_big_plan=target_big_plan,
            target_todo_task=target_todo_task,
            target_habit=target_habit,
            target_habit_stack=target_habit_stack,
            target_chore=target_chore,
            target_chore_stack=target_chore_stack,
            habit_stack_members=habit_stack_members,
            chore_stack_members=chore_stack_members,
        )
