"""Shared service for archiving a chore stack."""

from jupiter.core.apps.chores.sub.stack.root import ChoreStack
from jupiter.core.apps.chores.sub.stack.service.clear_chores import (
    ChoreStackClearChoresService,
)
from jupiter.core.archival_reason import JupiterArchivalReason
from jupiter.core.common.sub.contacts.sub.link.service.archive import (
    ContactLinkArchiveService,
)
from jupiter.core.common.sub.locations.sub.link.service.archive import (
    LocationLinkArchiveService,
)
from jupiter.core.common.sub.notes.service.archive import (
    NoteArchiveService,
)
from jupiter.core.common.sub.tags.sub.link.service.archive import TagLinkArchiveService
from jupiter.core.named_entity_tag import NamedEntityTag
from jupiter.framework.base.entity_link import EntityLink
from jupiter.framework.context import DomainContext
from jupiter.framework.progress_reporter.reporter import ProgressReporter
from jupiter.framework.storage.repository import DomainUnitOfWork


class ChoreStackArchiveService:
    """Shared service for archiving a chore stack."""

    async def do_it(
        self,
        ctx: DomainContext,
        uow: DomainUnitOfWork,
        progress_reporter: ProgressReporter,
        chore_stack: ChoreStack,
        archival_reason: JupiterArchivalReason,
    ) -> None:
        """Archive a stack and detach it from member chores."""
        if chore_stack.archived:
            return

        await ChoreStackClearChoresService().do_it(
            ctx, uow, progress_reporter, chore_stack
        )

        chore_stack = chore_stack.mark_archived(ctx, archival_reason)
        await uow.get_for(ChoreStack).save(chore_stack)
        await progress_reporter.mark_updated(chore_stack)

        owner_link = EntityLink.std(
            NamedEntityTag.CHORE_STACK.value, chore_stack.ref_id
        )
        await NoteArchiveService().archive_for_owner(
            ctx,
            uow,
            owner_link,
            archival_reason,
        )
        await TagLinkArchiveService().archive_for_entity(
            ctx,
            uow,
            owner_link,
            archival_reason,
        )
        await ContactLinkArchiveService().archive_for_entity(
            ctx,
            uow,
            owner_link,
            archival_reason,
        )
        await LocationLinkArchiveService().archive_for_entity(
            ctx,
            uow,
            owner_link,
            archival_reason,
        )
