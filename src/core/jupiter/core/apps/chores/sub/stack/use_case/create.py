"""The command for creating a chore stack."""

from jupiter.core.apps.chores.collection import ChoreCollection
from jupiter.core.apps.chores.root import Chore
from jupiter.core.apps.chores.sub.stack.name import ChoreStackName
from jupiter.core.apps.chores.sub.stack.root import ChoreStack
from jupiter.core.apps.chores.sub.stack.service.assign_chores import (
    ChoreStackAssignChoresService,
)
from jupiter.core.apps.life_plan.root import LifePlan
from jupiter.core.apps.life_plan.sub.aspects.root import Aspect, AspectRepository
from jupiter.core.apps.life_plan.sub.chapters.root import Chapter
from jupiter.core.apps.life_plan.sub.goals.root import Goal
from jupiter.core.common.recurring_task_period import RecurringTaskPeriod
from jupiter.core.config import (
    JupiterLoggedInMutationContext,
)
from jupiter.core.crown_entity_support import (
    JupiterCreateCrownEntityArgs,
    JupiterCreateCrownEntityUseCase,
)
from jupiter.core.features import (
    WorkspaceFeature,
)
from jupiter.framework.base.entity_id import EntityId
from jupiter.framework.errors import InputValidationError
from jupiter.framework.progress_reporter.reporter import ProgressReporter
from jupiter.framework.storage.repository import DomainUnitOfWork
from jupiter.framework.use_case import (
    UnavailableForContextError,
    mutation_use_case,
)
from jupiter.framework.use_case_io import (
    UseCaseResultBase,
    use_case_args,
    use_case_result,
)


@use_case_args
class ChoreStackCreateArgs(JupiterCreateCrownEntityArgs):
    """Chore stack creation parameters."""

    name: ChoreStackName
    period: RecurringTaskPeriod
    chore_ref_ids: list[EntityId]
    aspect_ref_id: EntityId | None
    chapter_ref_id: EntityId | None
    goal_ref_id: EntityId | None


@use_case_result
class ChoreStackCreateResult(UseCaseResultBase):
    """Chore stack creation result."""

    new_chore_stack: ChoreStack


@mutation_use_case(WorkspaceFeature.CHORES)
class ChoreStackCreateUseCase(
    JupiterCreateCrownEntityUseCase[ChoreStackCreateArgs, ChoreStackCreateResult]
):
    """The command for creating a chore stack."""

    async def _perform_transactional_mutation(
        self,
        uow: DomainUnitOfWork,
        progress_reporter: ProgressReporter,
        context: JupiterLoggedInMutationContext,
        args: ChoreStackCreateArgs,
    ) -> ChoreStackCreateResult:
        """Execute the command's action."""
        workspace = context.workspace

        if not workspace.is_feature_available(WorkspaceFeature.LIFE_PLAN):
            if args.aspect_ref_id is not None:
                raise UnavailableForContextError(WorkspaceFeature.LIFE_PLAN)
            if args.chapter_ref_id is not None:
                raise UnavailableForContextError(WorkspaceFeature.LIFE_PLAN)
            if args.goal_ref_id is not None:
                raise UnavailableForContextError(WorkspaceFeature.LIFE_PLAN)

        chore_collection = await uow.get_for(ChoreCollection).load_by_parent(
            workspace.ref_id,
        )

        if args.aspect_ref_id is None:
            life_plan = await uow.get_for(LifePlan).load_by_parent(
                workspace.ref_id,
            )
            the_aspect = await uow.get(AspectRepository).load_root_aspect(
                life_plan.ref_id
            )
        else:
            the_aspect = await self.load_entity(
                uow, context.user.ref_id, Aspect, args.aspect_ref_id
            )

        if args.chapter_ref_id is not None:
            chapter = await self.load_entity(
                uow, context.user.ref_id, Chapter, args.chapter_ref_id
            )
            if chapter.aspect_ref_id != the_aspect.ref_id:
                raise InputValidationError(
                    f"Chapter does not belong to aspect '{the_aspect.name}'"
                )

        if args.goal_ref_id is not None:
            goal = await self.load_entity(
                uow, context.user.ref_id, Goal, args.goal_ref_id
            )
            if goal.aspect_ref_id != the_aspect.ref_id:
                raise InputValidationError(
                    f"Goal does not belong to aspect '{the_aspect.name}'"
                )

        if len(args.chore_ref_ids) != len(set(args.chore_ref_ids)):
            raise InputValidationError("Chore ref ids must be unique")

        chores: list[Chore] = []
        if args.chore_ref_ids:
            chores = await self.find_all_entities(
                uow,
                context.user.ref_id,
                Chore,
                args.chore_ref_ids,
            )
            if len(chores) != len(args.chore_ref_ids):
                raise InputValidationError("Some chores could not be found")
            for chore in chores:
                if chore.gen_params.period != args.period:
                    raise InputValidationError(
                        f"Chore '{chore.name}' does not match the stack period"
                    )

        new_chore_stack = ChoreStack.new_chore_stack(
            context.domain_context,
            chore_collection_ref_id=chore_collection.ref_id,
            name=args.name,
            period=args.period,
            aspect_ref_id=the_aspect.ref_id,
            chapter_ref_id=args.chapter_ref_id,
            goal_ref_id=args.goal_ref_id,
        )
        new_chore_stack = await self.create_entity(
            context.domain_context,
            uow,
            progress_reporter,
            context.user.ref_id,
            new_chore_stack,
        )

        await ChoreStackAssignChoresService().do_it(
            context.domain_context,
            uow,
            progress_reporter,
            new_chore_stack,
            chores,
        )

        return ChoreStackCreateResult(new_chore_stack=new_chore_stack)
