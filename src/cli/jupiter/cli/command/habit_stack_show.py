"""UseCase for showing habit stacks."""

from jupiter.cli.command.rendering import (
    entity_id_to_rich_text,
    entity_name_to_rich_text,
    period_to_rich_text,
)
from jupiter.cli.config import JupiterLoggedInReadonlyCommand
from jupiter.core.apps.habits.sub.stack.use_case.find import (
    HabitStackFindResult,
    HabitStackFindUseCase,
)
from jupiter.core.config import JupiterLoggedInReadonlyContext
from rich.console import Console
from rich.text import Text
from rich.tree import Tree


class HabitStackShow(
    JupiterLoggedInReadonlyCommand[HabitStackFindUseCase, HabitStackFindResult]
):
    """UseCase class for showing habit stacks."""

    def _render_result(
        self,
        console: Console,
        context: JupiterLoggedInReadonlyContext,
        result: HabitStackFindResult,
    ) -> None:
        sorted_stacks = sorted(
            result.entries,
            key=lambda entry: (
                entry.habit_stack.archived,
                entry.habit_stack.period,
                str(entry.habit_stack.name),
            ),
        )

        rich_tree = Tree("📚 Habit Stacks", guide_style="bold bright_blue")

        for entry in sorted_stacks:
            stack_text = Text("")
            stack_text.append(entity_id_to_rich_text(entry.habit_stack.ref_id))
            stack_text.append(" ")
            stack_text.append(entity_name_to_rich_text(entry.habit_stack.name))
            stack_text.append(" ")
            stack_text.append(period_to_rich_text(entry.habit_stack.period))

            if entry.habit_stack.archived:
                stack_text.stylize("gray62")

            stack_tree = rich_tree.add(stack_text)
            if entry.habits:
                for habit in entry.habits:
                    habit_text = Text("")
                    habit_text.append(entity_id_to_rich_text(habit.ref_id))
                    habit_text.append(" ")
                    habit_text.append(entity_name_to_rich_text(habit.name))
                    stack_tree.add(habit_text)

        console.print(rich_tree)
