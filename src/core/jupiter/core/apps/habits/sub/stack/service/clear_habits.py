"""Clear stack membership from habits that belong to a stack."""

from jupiter.core.apps.habits.sub.habit.root import Habit
from jupiter.core.apps.habits.sub.stack.root import HabitStack
from jupiter.framework.context import DomainContext
from jupiter.framework.progress_reporter.reporter import ProgressReporter
from jupiter.framework.storage.repository import DomainUnitOfWork


class HabitStackClearHabitsService:
    """Remove a stack from every habit that currently references it."""

    async def do_it(
        self,
        ctx: DomainContext,
        uow: DomainUnitOfWork,
        progress_reporter: ProgressReporter,
        stack: HabitStack,
    ) -> None:
        """Clear ``stack_ref_id`` on all member habits."""
        habits = await uow.get_for(Habit).find_all_generic(
            parent_ref_id=None,
            allow_archived=True,
            stack_ref_id=stack.ref_id,
        )
        for habit in habits:
            habit = habit.change_stack(ctx, None)
            await uow.get_for(Habit).save(habit)
            await progress_reporter.mark_updated(habit)
