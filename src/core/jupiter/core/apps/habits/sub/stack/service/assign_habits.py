"""Assign habits to a stack and clear membership for habits that left it."""

from jupiter.core.apps.habits.sub.habit.root import Habit
from jupiter.core.apps.habits.sub.stack.root import HabitStack
from jupiter.framework.context import DomainContext
from jupiter.framework.progress_reporter.reporter import ProgressReporter
from jupiter.framework.storage.repository import DomainUnitOfWork


class HabitStackAssignHabitsService:
    """Keep ``Habit.stack_ref_id`` in sync with a stack's desired members."""

    async def do_it(
        self,
        ctx: DomainContext,
        uow: DomainUnitOfWork,
        progress_reporter: ProgressReporter,
        stack: HabitStack,
        habits: list[Habit],
    ) -> list[Habit]:
        """Set membership to exactly ``habits``, returning the habits that changed."""
        current_members = await uow.get_for(Habit).find_all_generic(
            parent_ref_id=None,
            allow_archived=True,
            stack_ref_id=stack.ref_id,
        )
        desired_ref_ids = {habit.ref_id for habit in habits}
        changed_habits: list[Habit] = []

        for habit in current_members:
            if habit.ref_id in desired_ref_ids:
                continue
            habit = habit.change_stack(ctx, None)
            habit = await uow.get_for(Habit).save(habit)
            await progress_reporter.mark_updated(habit)
            changed_habits.append(habit)

        for habit in habits:
            if habit.stack_ref_id == stack.ref_id:
                continue
            habit = habit.change_stack(ctx, stack.ref_id)
            habit = await uow.get_for(Habit).save(habit)
            await progress_reporter.mark_updated(habit)
            changed_habits.append(habit)

        return changed_habits
