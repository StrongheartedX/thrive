"""Assign chores to a stack and clear membership for chores that left it."""

from jupiter.core.apps.chores.root import Chore
from jupiter.core.apps.chores.sub.stack.root import ChoreStack
from jupiter.framework.context import DomainContext
from jupiter.framework.progress_reporter.reporter import ProgressReporter
from jupiter.framework.storage.repository import DomainUnitOfWork


class ChoreStackAssignChoresService:
    """Keep ``Chore.stack_ref_id`` in sync with a stack's desired members."""

    async def do_it(
        self,
        ctx: DomainContext,
        uow: DomainUnitOfWork,
        progress_reporter: ProgressReporter,
        stack: ChoreStack,
        chores: list[Chore],
    ) -> None:
        """Set membership to exactly ``chores``."""
        current_members = await uow.get_for(Chore).find_all_generic(
            parent_ref_id=None,
            allow_archived=True,
            stack_ref_id=stack.ref_id,
        )
        desired_ref_ids = {chore.ref_id for chore in chores}

        for chore in current_members:
            if chore.ref_id in desired_ref_ids:
                continue
            chore = chore.change_stack(ctx, None)
            await uow.get_for(Chore).save(chore)
            await progress_reporter.mark_updated(chore)

        for chore in chores:
            if chore.stack_ref_id == stack.ref_id:
                continue
            chore = chore.change_stack(ctx, stack.ref_id)
            await uow.get_for(Chore).save(chore)
            await progress_reporter.mark_updated(chore)
