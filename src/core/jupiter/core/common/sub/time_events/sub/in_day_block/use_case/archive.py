"""Use case for archiving the in day event."""

from jupiter.core.archival_reason import JupiterArchivalReason
from jupiter.core.common.sub.access.access_level import AccessLevel
from jupiter.core.common.sub.time_events.domain import TimeEventDomain
from jupiter.core.common.sub.time_events.sub.in_day_block.root import (
    ALLOWED_TIME_EVENT_IN_DAY_OWNER_TYPES,
    TimeEventInDayBlock,
)
from jupiter.core.config import (
    JupiterLoggedInMutationContext,
)
from jupiter.core.leaf_support_entity_support import (
    JupiterArchiveLeafSupportEntityArgs,
    JupiterArchiveLeafSupportEntityUseCase,
)
from jupiter.framework.base.entity_id import EntityId
from jupiter.framework.errors import InputValidationError
from jupiter.framework.progress_reporter.reporter import ProgressReporter
from jupiter.framework.storage.repository import DomainUnitOfWork
from jupiter.framework.use_case import (
    mutation_use_case,
)
from jupiter.framework.use_case_io import (
    UseCaseResultBase,
    use_case_args,
    use_case_result,
)
from jupiter.framework.utils.generic_crown_archiver import generic_crown_archiver


@use_case_args
class TimeEventInDayBlockArchiveArgs(JupiterArchiveLeafSupportEntityArgs):
    """Args."""

    ref_id: EntityId


@use_case_result
class TimeEventInDayBlockArchiveResult(UseCaseResultBase):
    """Result."""

    archived_time_event_in_day_block: TimeEventInDayBlock


@mutation_use_case()
class TimeEventInDayBlockArchiveUseCase(
    JupiterArchiveLeafSupportEntityUseCase[
        TimeEventInDayBlockArchiveArgs, TimeEventInDayBlockArchiveResult
    ]
):
    """Use case for archiving the in day event."""

    async def _perform_transactional_mutation(
        self,
        uow: DomainUnitOfWork,
        progress_reporter: ProgressReporter,
        context: JupiterLoggedInMutationContext,
        args: TimeEventInDayBlockArchiveArgs,
    ) -> TimeEventInDayBlockArchiveResult:
        """Execute the command's action."""
        _, time_event_block = await self.load_for_owner(
            uow,
            TimeEventDomain,
            TimeEventInDayBlock,
            args.ref_id,
            context.user.ref_id,
            context.workspace.ref_id,
            ALLOWED_TIME_EVENT_IN_DAY_OWNER_TYPES,
            AccessLevel.WRITER,
        )
        if not time_event_block.can_be_modified_independently:
            raise InputValidationError("Cannot archive a linked task")
        await generic_crown_archiver(
            context.domain_context,
            uow,
            progress_reporter,
            TimeEventInDayBlock,
            args.ref_id,
            JupiterArchivalReason.USER,
        )
        return TimeEventInDayBlockArchiveResult(
            archived_time_event_in_day_block=await uow.get_for(
                TimeEventInDayBlock
            ).load_by_id(args.ref_id, allow_archived=True)
        )
