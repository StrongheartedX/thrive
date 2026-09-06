"""The command for updating a chore stack."""

from jupiter.core.apps.chores.root import Chore
from jupiter.core.apps.chores.sub.stack.name import ChoreStackName
from jupiter.core.apps.chores.sub.stack.root import ChoreStack
from jupiter.core.apps.chores.sub.stack.service.assign_chores import (
    ChoreStackAssignChoresService,
)
from jupiter.core.apps.life_plan.sub.aspects.root import Aspect
from jupiter.core.apps.life_plan.sub.chapters.root import Chapter
from jupiter.core.apps.life_plan.sub.goals.root import Goal
from jupiter.core.config import (
    JupiterLoggedInMutationContext,
)
from jupiter.core.crown_entity_support import (
    JupiterUpdateCrownEntityArgs,
    JupiterUpdateCrownEntityUseCase,
)
from jupiter.core.features import WorkspaceFeature
from jupiter.framework.base.entity_id import EntityId
from jupiter.framework.errors import InputValidationError
from jupiter.framework.progress_reporter.reporter import ProgressReporter
from jupiter.framework.storage.repository import DomainUnitOfWork
from jupiter.framework.update_action import UpdateAction
from jupiter.framework.use_case import (
    UnavailableForContextError,
    mutation_use_case,
)
from jupiter.framework.use_case_io import use_case_args


@use_case_args
class ChoreStackUpdateArgs(JupiterUpdateCrownEntityArgs):
    """Chore stack update parameters."""

    ref_id: EntityId
    name: UpdateAction[ChoreStackName]
    chore_ref_ids: UpdateAction[list[EntityId]]
    aspect_ref_id: UpdateAction[EntityId]
    chapter_ref_id: UpdateAction[EntityId | None]
    goal_ref_id: UpdateAction[EntityId | None]


@mutation_use_case(WorkspaceFeature.CHORES)
class ChoreStackUpdateUseCase(
    JupiterUpdateCrownEntityUseCase[ChoreStackUpdateArgs, None]
):
    """The command for updating a chore stack."""

    async def _perform_transactional_mutation(
        self,
        uow: DomainUnitOfWork,
        progress_reporter: ProgressReporter,
        context: JupiterLoggedInMutationContext,
        args: ChoreStackUpdateArgs,
    ) -> None:
        """Execute the command's action."""
        workspace = context.workspace

        chore_stack = await self.load_entity(
            uow, context.user.ref_id, ChoreStack, args.ref_id
        )

        if not workspace.is_feature_available(WorkspaceFeature.LIFE_PLAN):
            if (
                args.aspect_ref_id.should_change
                and args.aspect_ref_id.just_the_value is not None
            ):
                raise UnavailableForContextError(WorkspaceFeature.LIFE_PLAN)
            if (
                args.chapter_ref_id.should_change
                and args.chapter_ref_id.just_the_value is not None
            ):
                raise UnavailableForContextError(WorkspaceFeature.LIFE_PLAN)
            if (
                args.goal_ref_id.should_change
                and args.goal_ref_id.just_the_value is not None
            ):
                raise UnavailableForContextError(WorkspaceFeature.LIFE_PLAN)

        if workspace.is_feature_available(WorkspaceFeature.LIFE_PLAN):
            new_aspect_ref_id = args.aspect_ref_id.or_else(chore_stack.aspect_ref_id)
            new_chapter_ref_id = args.chapter_ref_id.or_else(chore_stack.chapter_ref_id)
            new_goal_ref_id = args.goal_ref_id.or_else(chore_stack.goal_ref_id)
            aspect_changing = (
                args.aspect_ref_id.should_change
                and new_aspect_ref_id != chore_stack.aspect_ref_id
            )
            chapter_changing = (
                args.chapter_ref_id.should_change
                and new_chapter_ref_id != chore_stack.chapter_ref_id
            )
            goal_changing = (
                args.goal_ref_id.should_change
                and new_goal_ref_id != chore_stack.goal_ref_id
            )

            if aspect_changing or chapter_changing or goal_changing:
                aspect = await self.load_entity(
                    uow,
                    context.user.ref_id,
                    Aspect,
                    new_aspect_ref_id,
                )

                if chapter_changing and new_chapter_ref_id is not None:
                    chapter = await self.load_entity(
                        uow, context.user.ref_id, Chapter, new_chapter_ref_id
                    )
                    if chapter.aspect_ref_id != aspect.ref_id:
                        raise InputValidationError(
                            f"Chapter does not belong to aspect '{aspect.name}'"
                        )

                if goal_changing and new_goal_ref_id is not None:
                    goal = await self.load_entity(
                        uow, context.user.ref_id, Goal, new_goal_ref_id
                    )
                    if goal.aspect_ref_id != aspect.ref_id:
                        raise InputValidationError(
                            f"Goal does not belong to aspect '{aspect.name}'"
                        )

        chore_stack = chore_stack.update(
            context.domain_context,
            name=args.name,
            aspect_ref_id=args.aspect_ref_id,
            chapter_ref_id=args.chapter_ref_id,
            goal_ref_id=args.goal_ref_id,
        )
        await uow.get_for(ChoreStack).save(chore_stack)
        await progress_reporter.mark_updated(chore_stack)

        if args.chore_ref_ids.should_change:
            chore_ref_ids = args.chore_ref_ids.just_the_value
            if len(chore_ref_ids) != len(set(chore_ref_ids)):
                raise InputValidationError("Chore ref ids must be unique")

            chores: list[Chore] = []
            if chore_ref_ids:
                chores = await self.find_all_entities(
                    uow,
                    context.user.ref_id,
                    Chore,
                    chore_ref_ids,
                )
                if len(chores) != len(chore_ref_ids):
                    raise InputValidationError("Some chores could not be found")
                for chore in chores:
                    if chore.gen_params.period != chore_stack.period:
                        raise InputValidationError(
                            f"Chore '{chore.name}' does not match the stack period"
                        )

            await ChoreStackAssignChoresService().do_it(
                context.domain_context,
                uow,
                progress_reporter,
                chore_stack,
                chores,
            )
