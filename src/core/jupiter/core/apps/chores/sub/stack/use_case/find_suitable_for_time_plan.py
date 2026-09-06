"""Find chore stacks suitable for adding to a time plan."""

from jupiter.core.app import AppCore
from jupiter.core.apps.chores.root import Chore
from jupiter.core.apps.chores.sub.stack.root import ChoreStack
from jupiter.core.apps.life_plan.sub.aspects.root import Aspect
from jupiter.core.apps.time_plans.root import TimePlan
from jupiter.core.common.sub.inbox_tasks.root import InboxTaskRepository
from jupiter.core.config import (
    JupiterLoggedInReadonlyContext,
)
from jupiter.core.crown_entity_support import (
    JupiterFindCrownEntityArgs,
    JupiterFindCrownEntityUseCase,
)
from jupiter.core.features import WorkspaceFeature
from jupiter.core.named_entity_tag import NamedEntityTag
from jupiter.framework.base.entity_id import EntityId
from jupiter.framework.base.entity_link import EntityLink
from jupiter.framework.errors import InputValidationError
from jupiter.framework.storage.repository import DomainUnitOfWork
from jupiter.framework.use_case import (
    readonly_use_case,
)
from jupiter.framework.use_case_io import (
    UseCaseResultBase,
    use_case_args,
    use_case_result,
    use_case_result_part,
)


@use_case_args
class ChoreStackFindSuitableForTimePlanArgs(JupiterFindCrownEntityArgs):
    """Args."""

    time_plan_ref_id: EntityId


@use_case_result_part
class ChoreStackFindSuitableForTimePlanResultEntry(UseCaseResultBase):
    """A chore stack with suitability for adding to a time plan."""

    chore_stack: ChoreStack
    chores: list[Chore]
    aspect: Aspect | None
    has_uncompleted_historical_inbox_tasks: bool
    would_generate_in_time_plan: bool


@use_case_result
class ChoreStackFindSuitableForTimePlanResult(UseCaseResultBase):
    """The result."""

    entries: list[ChoreStackFindSuitableForTimePlanResultEntry]


@readonly_use_case(
    WorkspaceFeature.CHORES,
    WorkspaceFeature.TIME_PLANS,
    only_for_component=[AppCore.WEBUI, AppCore.API],
)
class ChoreStackFindSuitableForTimePlanUseCase(
    JupiterFindCrownEntityUseCase[
        ChoreStackFindSuitableForTimePlanArgs, ChoreStackFindSuitableForTimePlanResult
    ]
):
    """Find chore stacks suitable for adding to a time plan."""

    async def _perform_transactional_read(
        self,
        uow: DomainUnitOfWork,
        context: JupiterLoggedInReadonlyContext,
        args: ChoreStackFindSuitableForTimePlanArgs,
    ) -> ChoreStackFindSuitableForTimePlanResult:
        """Execute the command's action."""
        time_plan = await self.load_entity(
            uow,
            context.user.ref_id,
            TimePlan,
            args.time_plan_ref_id,
        )

        if not time_plan.allows_inbox_tasks:
            raise InputValidationError(
                "Chore stacks can only be added to daily or weekly time plans"
            )

        chore_stacks = await self.find_all_entities(
            uow,
            context.user.ref_id,
            ChoreStack,
            allow_archived=False,
        )
        if not chore_stacks:
            return ChoreStackFindSuitableForTimePlanResult(entries=[])

        member_chores = await uow.get_for(Chore).find_all_generic(
            parent_ref_id=None,
            allow_archived=False,
            stack_ref_id=[stack.ref_id for stack in chore_stacks],
        )
        chores_by_stack_ref_id: dict[EntityId, list[Chore]] = {}
        for chore in member_chores:
            if chore.stack_ref_id is None:
                continue
            chores_by_stack_ref_id.setdefault(chore.stack_ref_id, []).append(chore)

        chore_owner_links = [
            EntityLink.std(NamedEntityTag.CHORE.value, chore.ref_id)
            for chore in member_chores
        ]
        owners_with_uncompleted = (
            await uow.get(
                InboxTaskRepository
            ).find_owner_ref_ids_with_uncompleted_tasks(chore_owner_links)
            if chore_owner_links
            else set()
        )

        if context.workspace.is_feature_available(WorkspaceFeature.LIFE_PLAN):
            aspect_ref_ids = list({stack.aspect_ref_id for stack in chore_stacks})
            aspects = (
                await uow.get_for(Aspect).find_all_generic(
                    allow_archived=True,
                    ref_id=aspect_ref_ids,
                )
                if aspect_ref_ids
                else []
            )
            aspect_by_ref_id = {aspect.ref_id: aspect for aspect in aspects}
        else:
            aspect_by_ref_id = None

        return ChoreStackFindSuitableForTimePlanResult(
            entries=[
                ChoreStackFindSuitableForTimePlanResultEntry(
                    chore_stack=stack,
                    chores=chores_by_stack_ref_id.get(stack.ref_id, []),
                    aspect=(
                        aspect_by_ref_id.get(stack.aspect_ref_id)
                        if aspect_by_ref_id is not None
                        else None
                    ),
                    has_uncompleted_historical_inbox_tasks=any(
                        chore.ref_id in owners_with_uncompleted
                        for chore in chores_by_stack_ref_id.get(stack.ref_id, [])
                    ),
                    would_generate_in_time_plan=any(
                        chore.would_generate_in_time_plan(
                            time_plan.start_date,
                            time_plan.end_date,
                        )
                        for chore in chores_by_stack_ref_id.get(stack.ref_id, [])
                    ),
                )
                for stack in chore_stacks
            ],
        )
