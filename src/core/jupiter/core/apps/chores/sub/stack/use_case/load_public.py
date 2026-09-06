"""Guest readonly use case for loading a published chore stack."""

from jupiter.core.apps.chores.collection import ChoreCollection
from jupiter.core.apps.chores.sub.stack.root import ChoreStack
from jupiter.core.apps.chores.sub.stack.service.load import (
    ChoreStackLoadResult,
    ChoreStackLoadService,
)
from jupiter.core.common.sub.publish.root import PublishDomain
from jupiter.core.common.sub.publish.sub.entity.external_id import PublishExternalId
from jupiter.core.common.sub.publish.sub.entity.root import PublishEntityRepository
from jupiter.core.common.sub.publish.sub.entity.status import PublishEntityStatus
from jupiter.core.config import (
    JupiterGuestReadonlyContext,
    JupiterGuestReadonlyUseCase,
)
from jupiter.core.named_entity_tag import NamedEntityTag
from jupiter.framework.errors import InputValidationError
from jupiter.framework.use_case_io import UseCaseArgsBase, use_case_args


@use_case_args
class ChoreStackLoadPublicArgs(UseCaseArgsBase):
    """ChoreStackLoadPublic args."""

    external_id: PublishExternalId


class ChoreStackLoadPublicUseCase(
    JupiterGuestReadonlyUseCase[ChoreStackLoadPublicArgs, ChoreStackLoadResult]
):
    """Load a published chore stack by publish external id."""

    async def _execute(
        self,
        context: JupiterGuestReadonlyContext,
        args: ChoreStackLoadPublicArgs,
    ) -> ChoreStackLoadResult:
        """Execute the use case."""
        async with self._ports.domain_storage_engine.get_unit_of_work() as uow:
            publish_entity = await uow.get(PublishEntityRepository).load_by_external_id(
                args.external_id
            )

            if publish_entity.status != PublishEntityStatus.ACTIVE:
                raise InputValidationError(
                    "The publish entity is not active and cannot be loaded."
                )

            if publish_entity.owner.the_type != NamedEntityTag.CHORE_STACK.value:
                raise InputValidationError(
                    "The publish entity does not refer to a chore stack."
                )
            if publish_entity.owner.purpose != "std":
                raise InputValidationError(
                    "The publish entity owner link purpose must be 'std'."
                )

            publish_domain = await uow.get_for(PublishDomain).load_by_id(
                publish_entity.publish_domain.ref_id
            )
            chore_collection = await uow.get_for(ChoreCollection).load_by_parent(
                publish_domain.workspace.ref_id
            )
            chore_stack = await uow.get_for(ChoreStack).load_by_id(
                publish_entity.owner.ref_id,
                allow_archived=False,
            )
            if chore_stack.parent_ref_id != chore_collection.ref_id:
                raise InputValidationError(
                    "The publish entity does not refer to a workspace chore stack."
                )

            return await ChoreStackLoadService().do_it(
                uow,
                chore_stack,
                allow_archived=False,
                include_publish_entity=False,
            )
