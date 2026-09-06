"""Shared service for archiving a habit stack."""

from jupiter.core.apps.habits.sub.stack.root import HabitStack
from jupiter.core.apps.habits.sub.stack.service.clear_habits import (
    HabitStackClearHabitsService,
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


class HabitStackArchiveService:
    """Shared service for archiving a habit stack."""

    async def do_it(
        self,
        ctx: DomainContext,
        uow: DomainUnitOfWork,
        progress_reporter: ProgressReporter,
        habit_stack: HabitStack,
        archival_reason: JupiterArchivalReason,
    ) -> None:
        """Archive a stack and detach it from member habits."""
        if habit_stack.archived:
            return

        await HabitStackClearHabitsService().do_it(
            ctx, uow, progress_reporter, habit_stack
        )

        habit_stack = habit_stack.mark_archived(ctx, archival_reason)
        await uow.get_for(HabitStack).save(habit_stack)
        await progress_reporter.mark_updated(habit_stack)

        owner_link = EntityLink.std(
            NamedEntityTag.HABIT_STACK.value, habit_stack.ref_id
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
