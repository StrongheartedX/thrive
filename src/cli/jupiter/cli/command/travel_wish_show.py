"""UseCase for showing travel wishes."""

from jupiter.cli.command.rendering import (
    entity_id_to_rich_text,
    entity_name_to_rich_text,
)
from jupiter.cli.config import JupiterLoggedInReadonlyCommand
from jupiter.core.apps.vacations.sub.travel_wish.use_case.find import (
    TravelWishFindResult,
    TravelWishFindUseCase,
)
from jupiter.core.config import JupiterLoggedInReadonlyContext
from rich.console import Console
from rich.text import Text
from rich.tree import Tree


class TravelWishShow(
    JupiterLoggedInReadonlyCommand[TravelWishFindUseCase, TravelWishFindResult]
):
    """UseCase class for showing travel wishes."""

    def _render_result(
        self,
        console: Console,
        context: JupiterLoggedInReadonlyContext,
        result: TravelWishFindResult,
    ) -> None:
        sorted_travel_wishes = sorted(
            result.entries,
            key=lambda v: (
                v.travel_wish.archived,
                str(v.travel_wish.name),
            ),
        )

        rich_tree = Tree("✈️ Travel Wishes", guide_style="bold bright_blue")

        for entry in sorted_travel_wishes:
            travel_wish_text = Text("")
            travel_wish_text.append(entity_id_to_rich_text(entry.travel_wish.ref_id))
            travel_wish_text.append(" ")
            travel_wish_text.append(entity_name_to_rich_text(entry.travel_wish.name))

            if entry.travel_wish.archived:
                travel_wish_text.stylize("gray62")

            rich_tree.add(travel_wish_text)

        console.print(rich_tree)
