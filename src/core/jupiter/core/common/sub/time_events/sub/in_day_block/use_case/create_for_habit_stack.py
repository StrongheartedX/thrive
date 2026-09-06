"""Use case for creating time events for every habit in a stack."""

from jupiter.core.apps.habits.sub.habit.root import Habit
from jupiter.core.apps.habits.sub.stack.root import HabitStack
from jupiter.core.common.sub.time_events.domain import TimeEventDomain
from jupiter.core.common.sub.time_events.sub.in_day_block.root import (
    TimeEventInDayBlock,
)
from jupiter.core.common.time_in_day import TimeInDay
from jupiter.core.config import (
    JupiterLoggedInMutationContext,
)
from jupiter.core.leaf_support_entity_support import (
    JupiterCreateLeafSupportEntityArgs,
    JupiterCreateLeafSupportEntityUseCase,
)
from jupiter.framework.base.adate import ADate
from jupiter.framework.base.entity_id import EntityId
from jupiter.framework.progress_reporter.reporter import ProgressReporter
from jupiter.framework.storage.repository import DomainUnitOfWork
from jupiter.framework.use_case import (
    mutation_use_case,
)
from jupiter.framework.use_case_io import (
    UseCaseResultBase,
    use_case_args,
    use_case_result,
)


@use_case_args
class TimeEventInDayBlockCreateForHabitStackArgs(JupiterCreateLeafSupportEntityArgs):
    """Args."""

    habit_stack_ref_id: EntityId
    start_date: ADate
    start_time_in_day: TimeInDay
    duration_mins: int
    buffer_before_mins: int | None
    buffer_after_mins: int | None


@use_case_result
class TimeEventInDayBlockCreateForHabitStackResult(UseCaseResultBase):
    """Result."""

    new_time_events: list[TimeEventInDayBlock]


@mutation_use_case()
class TimeEventInDayBlockCreateForHabitStackUseCase(
    JupiterCreateLeafSupportEntityUseCase[
        TimeEventInDayBlockCreateForHabitStackArgs,
        TimeEventInDayBlockCreateForHabitStackResult,
    ]
):
    """Use case for creating time events for every habit in a stack."""

    async def _perform_transactional_mutation(
        self,
        uow: DomainUnitOfWork,
        progress_reporter: ProgressReporter,
        context: JupiterLoggedInMutationContext,
        args: TimeEventInDayBlockCreateForHabitStackArgs,
    ) -> TimeEventInDayBlockCreateForHabitStackResult:
        """Execute the command's action."""
        habit_stack, owner_workspace_ref_id = await self.load_owner_entity(
            uow, context.user.ref_id, HabitStack, args.habit_stack_ref_id
        )
        time_event_domain = await self.load_parent(
            uow, TimeEventDomain, owner_workspace_ref_id
        )

        member_habits = await uow.get_for(Habit).find_all_generic(
            parent_ref_id=None,
            allow_archived=False,
            stack_ref_id=habit_stack.ref_id,
        )

        new_time_events: list[TimeEventInDayBlock] = []
        for habit in member_habits:
            new_time_event = TimeEventInDayBlock.new_time_event_for_habit(
                context.domain_context,
                time_event_domain_ref_id=time_event_domain.ref_id,
                habit_ref_id=habit.ref_id,
                start_date=args.start_date,
                start_time_in_day=args.start_time_in_day,
                duration_mins=args.duration_mins,
                buffer_before_mins=args.buffer_before_mins,
                buffer_after_mins=args.buffer_after_mins,
            )
            new_time_event = await uow.get_for(TimeEventInDayBlock).create(
                new_time_event
            )
            new_time_events.append(new_time_event)

        return TimeEventInDayBlockCreateForHabitStackResult(
            new_time_events=new_time_events
        )
