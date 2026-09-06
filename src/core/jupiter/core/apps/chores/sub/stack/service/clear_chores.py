"""Clear stack membership from chores that belong to a stack."""

from jupiter.core.apps.chores.root import Chore
from jupiter.core.apps.chores.sub.stack.root import ChoreStack
from jupiter.framework.context import DomainContext
from jupiter.framework.progress_reporter.reporter import ProgressReporter
from jupiter.framework.storage.repository import DomainUnitOfWork


class ChoreStackClearChoresService:
    """Remove a stack from every chore that currently references it."""

    async def do_it(
        self,
        ctx: DomainContext,
        uow: DomainUnitOfWork,
        progress_reporter: ProgressReporter,
        stack: ChoreStack,
    ) -> None:
        """Clear ``stack_ref_id`` on all member chores."""
        chores = await uow.get_for(Chore).find_all_generic(
            parent_ref_id=None,
            allow_archived=True,
            stack_ref_id=stack.ref_id,
        )
        for chore in chores:
            chore = chore.change_stack(ctx, None)
            await uow.get_for(Chore).save(chore)
            await progress_reporter.mark_updated(chore)
