"""Find habit stacks suitable for adding to a time plan."""

from jupiter.core.app import AppCore
from jupiter.core.apps.habits.sub.habit.root import Habit
from jupiter.core.apps.habits.sub.stack.root import HabitStack
from jupiter.core.apps.life_plan.sub.aspects.root import Aspect
from jupiter.core.apps.time_plans.root import TimePlan
from jupiter.core.common.sub.inbox_tasks.root import InboxTaskRepository
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
from jupiter.framework.errors import InputValidationError
from jupiter.framework.storage.repository import DomainUnitOfWork
from jupiter.framework.use_case import (
    readonly_use_case,
)
from jupiter.framework.use_case_io import (
    UseCaseResultBase,
    use_case_args,
    use_case_result,
    use_case_result_part,
)


@use_case_args
class HabitStackFindSuitableForTimePlanArgs(JupiterFindCrownEntityArgs):
    """Args."""

    time_plan_ref_id: EntityId


@use_case_result_part
class HabitStackFindSuitableForTimePlanResultEntry(UseCaseResultBase):
    """A habit stack with suitability for adding to a time plan."""

    habit_stack: HabitStack
    habits: list[Habit]
    aspect: Aspect | None
    has_uncompleted_historical_inbox_tasks: bool
    would_generate_in_time_plan: bool


@use_case_result
class HabitStackFindSuitableForTimePlanResult(UseCaseResultBase):
    """The result."""

    entries: list[HabitStackFindSuitableForTimePlanResultEntry]


@readonly_use_case(
    WorkspaceFeature.HABITS,
    WorkspaceFeature.TIME_PLANS,
    only_for_component=[AppCore.WEBUI, AppCore.API],
)
class HabitStackFindSuitableForTimePlanUseCase(
    JupiterFindCrownEntityUseCase[
        HabitStackFindSuitableForTimePlanArgs, HabitStackFindSuitableForTimePlanResult
    ]
):
    """Find habit stacks suitable for adding to a time plan."""

    async def _perform_transactional_read(
        self,
        uow: DomainUnitOfWork,
        context: JupiterLoggedInReadonlyContext,
        args: HabitStackFindSuitableForTimePlanArgs,
    ) -> HabitStackFindSuitableForTimePlanResult:
        """Execute the command's action."""
        time_plan = await self.load_entity(
            uow,
            context.user.ref_id,
            TimePlan,
            args.time_plan_ref_id,
        )

        if not time_plan.allows_inbox_tasks:
            raise InputValidationError(
                "Habit stacks can only be added to daily or weekly time plans"
            )

        habit_stacks = await self.find_all_entities(
            uow,
            context.user.ref_id,
            HabitStack,
            allow_archived=False,
        )
        if not habit_stacks:
            return HabitStackFindSuitableForTimePlanResult(entries=[])

        member_habits = await uow.get_for(Habit).find_all_generic(
            parent_ref_id=None,
            allow_archived=False,
            stack_ref_id=[stack.ref_id for stack in habit_stacks],
        )
        habits_by_stack_ref_id: dict[EntityId, list[Habit]] = {}
        for habit in member_habits:
            if habit.stack_ref_id is None:
                continue
            habits_by_stack_ref_id.setdefault(habit.stack_ref_id, []).append(habit)

        habit_owner_links = [
            EntityLink.std(NamedEntityTag.HABIT.value, habit.ref_id)
            for habit in member_habits
        ]
        owners_with_uncompleted = (
            await uow.get(
                InboxTaskRepository
            ).find_owner_ref_ids_with_uncompleted_tasks(habit_owner_links)
            if habit_owner_links
            else set()
        )

        if context.workspace.is_feature_available(WorkspaceFeature.LIFE_PLAN):
            aspect_ref_ids = list({stack.aspect_ref_id for stack in habit_stacks})
            aspects = (
                await uow.get_for(Aspect).find_all_generic(
                    allow_archived=True,
                    ref_id=aspect_ref_ids,
                )
                if aspect_ref_ids
                else []
            )
            aspect_by_ref_id = {aspect.ref_id: aspect for aspect in aspects}
        else:
            aspect_by_ref_id = None

        return HabitStackFindSuitableForTimePlanResult(
            entries=[
                HabitStackFindSuitableForTimePlanResultEntry(
                    habit_stack=stack,
                    habits=habits_by_stack_ref_id.get(stack.ref_id, []),
                    aspect=(
                        aspect_by_ref_id.get(stack.aspect_ref_id)
                        if aspect_by_ref_id is not None
                        else None
                    ),
                    has_uncompleted_historical_inbox_tasks=any(
                        habit.ref_id in owners_with_uncompleted
                        for habit in habits_by_stack_ref_id.get(stack.ref_id, [])
                    ),
                    would_generate_in_time_plan=any(
                        habit.would_generate_in_time_plan(
                            time_plan.start_date,
                            time_plan.end_date,
                        )
                        for habit in habits_by_stack_ref_id.get(stack.ref_id, [])
                    ),
                )
                for stack in habit_stacks
            ],
        )
