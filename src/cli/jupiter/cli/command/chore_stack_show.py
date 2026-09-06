"""UseCase for showing chore stacks."""

from jupiter.cli.command.rendering import (
    entity_id_to_rich_text,
    entity_name_to_rich_text,
    period_to_rich_text,
)
from jupiter.cli.config import JupiterLoggedInReadonlyCommand
from jupiter.core.apps.chores.sub.stack.use_case.find import (
    ChoreStackFindResult,
    ChoreStackFindUseCase,
)
from jupiter.core.config import JupiterLoggedInReadonlyContext
from rich.console import Console
from rich.text import Text
from rich.tree import Tree


class ChoreStackShow(
    JupiterLoggedInReadonlyCommand[ChoreStackFindUseCase, ChoreStackFindResult]
):
    """UseCase class for showing chore stacks."""

    def _render_result(
        self,
        console: Console,
        context: JupiterLoggedInReadonlyContext,
        result: ChoreStackFindResult,
    ) -> None:
        sorted_stacks = sorted(
            result.entries,
            key=lambda entry: (
                entry.chore_stack.archived,
                entry.chore_stack.period,
                str(entry.chore_stack.name),
            ),
        )

        rich_tree = Tree("📚 Chore Stacks", guide_style="bold bright_blue")

        for entry in sorted_stacks:
            stack_text = Text("")
            stack_text.append(entity_id_to_rich_text(entry.chore_stack.ref_id))
            stack_text.append(" ")
            stack_text.append(entity_name_to_rich_text(entry.chore_stack.name))
            stack_text.append(" ")
            stack_text.append(period_to_rich_text(entry.chore_stack.period))

            if entry.chore_stack.archived:
                stack_text.stylize("gray62")

            stack_tree = rich_tree.add(stack_text)
            if entry.chores:
                for chore in entry.chores:
                    chore_text = Text("")
                    chore_text.append(entity_id_to_rich_text(chore.ref_id))
                    chore_text.append(" ")
                    chore_text.append(entity_name_to_rich_text(chore.name))
                    stack_tree.add(chore_text)

        console.print(rich_tree)
