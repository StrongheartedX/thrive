"""Shared service for removing a habit stack."""

from jupiter.core.apps.habits.sub.stack.root import HabitStack
from jupiter.core.apps.habits.sub.stack.service.clear_habits import (
    HabitStackClearHabitsService,
)
from jupiter.core.common.sub.contacts.sub.link.service.remove import (
    ContactLinkRemoveService,
)
from jupiter.core.common.sub.locations.sub.link.service.remove import (
    LocationLinkRemoveService,
)
from jupiter.core.common.sub.notes.service.remove import (
    NoteRemoveService,
)
from jupiter.core.common.sub.tags.sub.link.service.remove import TagLinkRemoveService
from jupiter.core.named_entity_tag import NamedEntityTag
from jupiter.framework.base.entity_id import EntityId
from jupiter.framework.base.entity_link import EntityLink
from jupiter.framework.context import DomainContext
from jupiter.framework.progress_reporter.reporter import ProgressReporter
from jupiter.framework.storage.repository import DomainUnitOfWork


class HabitStackRemoveService:
    """Shared service for removing a habit stack."""

    async def remove(
        self,
        ctx: DomainContext,
        uow: DomainUnitOfWork,
        progress_reporter: ProgressReporter,
        ref_id: EntityId,
    ) -> None:
        """Hard remove a habit stack and detach member habits."""
        habit_stack = await uow.get_for(HabitStack).load_by_id(
            ref_id, allow_archived=True
        )

        await HabitStackClearHabitsService().do_it(
            ctx, uow, progress_reporter, habit_stack
        )

        owner_link = EntityLink.std(
            NamedEntityTag.HABIT_STACK.value, habit_stack.ref_id
        )
        await NoteRemoveService().remove_for_owner(ctx, uow, owner_link)
        await TagLinkRemoveService().remove_for_entity(ctx, uow, owner_link)
        await ContactLinkRemoveService().remove_for_entity(ctx, uow, owner_link)
        await LocationLinkRemoveService().remove_for_entity(ctx, uow, owner_link)

        await uow.get_for(HabitStack).remove(ctx, ref_id)
        await progress_reporter.mark_removed(habit_stack)
