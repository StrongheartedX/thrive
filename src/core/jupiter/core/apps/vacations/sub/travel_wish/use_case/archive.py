"""The command for archiving a travel wish."""

from jupiter.core.apps.vacations.sub.travel_wish.root import TravelWish
from jupiter.core.archival_reason import JupiterArchivalReason
from jupiter.core.config import (
    JupiterLoggedInMutationContext,
)
from jupiter.core.crown_entity_support import (
    JupiterArchiveCrownEntityArgs,
    JupiterArchiveCrownEntityUseCase,
)
from jupiter.core.features import WorkspaceFeature
from jupiter.framework.base.entity_id import EntityId
from jupiter.framework.progress_reporter.reporter import ProgressReporter
from jupiter.framework.storage.repository import DomainUnitOfWork
from jupiter.framework.use_case import (
    mutation_use_case,
)
from jupiter.framework.use_case_io import use_case_args
from jupiter.framework.utils.generic_crown_archiver import generic_crown_archiver


@use_case_args
class TravelWishArchiveArgs(JupiterArchiveCrownEntityArgs):
    """Travel wish archive parameters."""

    ref_id: EntityId


@mutation_use_case(WorkspaceFeature.VACATIONS)
class TravelWishArchiveUseCase(
    JupiterArchiveCrownEntityUseCase[TravelWishArchiveArgs, None]
):
    """The command for archiving a travel wish."""

    async def _perform_transactional_mutation(
        self,
        uow: DomainUnitOfWork,
        progress_reporter: ProgressReporter,
        context: JupiterLoggedInMutationContext,
        args: TravelWishArchiveArgs,
    ) -> None:
        """Execute the command's action."""
        await self.check_entity(uow, context.user.ref_id, TravelWish, args.ref_id)

        await generic_crown_archiver(
            context.domain_context,
            uow,
            progress_reporter,
            TravelWish,
            args.ref_id,
            JupiterArchivalReason.USER,
        )
