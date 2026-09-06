"""Guest readonly use case for loading a published habit stack."""

from jupiter.core.apps.habits.collection import HabitCollection
from jupiter.core.apps.habits.sub.stack.root import HabitStack
from jupiter.core.apps.habits.sub.stack.service.load import (
    HabitStackLoadResult,
    HabitStackLoadService,
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
class HabitStackLoadPublicArgs(UseCaseArgsBase):
    """HabitStackLoadPublic args."""

    external_id: PublishExternalId


class HabitStackLoadPublicUseCase(
    JupiterGuestReadonlyUseCase[HabitStackLoadPublicArgs, HabitStackLoadResult]
):
    """Load a published habit stack by publish external id."""

    async def _execute(
        self,
        context: JupiterGuestReadonlyContext,
        args: HabitStackLoadPublicArgs,
    ) -> HabitStackLoadResult:
        """Execute the use case."""
        async with self._ports.domain_storage_engine.get_unit_of_work() as uow:
            publish_entity = await uow.get(PublishEntityRepository).load_by_external_id(
                args.external_id
            )

            if publish_entity.status != PublishEntityStatus.ACTIVE:
                raise InputValidationError(
                    "The publish entity is not active and cannot be loaded."
                )

            if publish_entity.owner.the_type != NamedEntityTag.HABIT_STACK.value:
                raise InputValidationError(
                    "The publish entity does not refer to a habit stack."
                )
            if publish_entity.owner.purpose != "std":
                raise InputValidationError(
                    "The publish entity owner link purpose must be 'std'."
                )

            publish_domain = await uow.get_for(PublishDomain).load_by_id(
                publish_entity.publish_domain.ref_id
            )
            habit_collection = await uow.get_for(HabitCollection).load_by_parent(
                publish_domain.workspace.ref_id
            )
            habit_stack = await uow.get_for(HabitStack).load_by_id(
                publish_entity.owner.ref_id,
                allow_archived=False,
            )
            if habit_stack.parent_ref_id != habit_collection.ref_id:
                raise InputValidationError(
                    "The publish entity does not refer to a workspace habit stack."
                )

            return await HabitStackLoadService().do_it(
                uow,
                habit_stack,
                allow_archived=False,
                include_publish_entity=False,
            )
