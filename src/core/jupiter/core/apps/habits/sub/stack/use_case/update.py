"""The command for updating a habit stack."""

from jupiter.core.apps.habits.sub.habit.root import Habit
from jupiter.core.apps.habits.sub.stack.name import HabitStackName
from jupiter.core.apps.habits.sub.stack.root import HabitStack
from jupiter.core.apps.habits.sub.stack.service.assign_habits import (
    HabitStackAssignHabitsService,
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
class HabitStackUpdateArgs(JupiterUpdateCrownEntityArgs):
    """Habit stack update parameters."""

    ref_id: EntityId
    name: UpdateAction[HabitStackName]
    habit_ref_ids: UpdateAction[list[EntityId]]
    aspect_ref_id: UpdateAction[EntityId]
    chapter_ref_id: UpdateAction[EntityId | None]
    goal_ref_id: UpdateAction[EntityId | None]


@mutation_use_case(WorkspaceFeature.HABITS)
class HabitStackUpdateUseCase(
    JupiterUpdateCrownEntityUseCase[HabitStackUpdateArgs, None]
):
    """The command for updating a habit stack."""

    async def _perform_transactional_mutation(
        self,
        uow: DomainUnitOfWork,
        progress_reporter: ProgressReporter,
        context: JupiterLoggedInMutationContext,
        args: HabitStackUpdateArgs,
    ) -> None:
        """Execute the command's action."""
        workspace = context.workspace

        habit_stack = await self.load_entity(
            uow, context.user.ref_id, HabitStack, args.ref_id
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
            new_aspect_ref_id = args.aspect_ref_id.or_else(habit_stack.aspect_ref_id)
            new_chapter_ref_id = args.chapter_ref_id.or_else(habit_stack.chapter_ref_id)
            new_goal_ref_id = args.goal_ref_id.or_else(habit_stack.goal_ref_id)
            aspect_changing = (
                args.aspect_ref_id.should_change
                and new_aspect_ref_id != habit_stack.aspect_ref_id
            )
            chapter_changing = (
                args.chapter_ref_id.should_change
                and new_chapter_ref_id != habit_stack.chapter_ref_id
            )
            goal_changing = (
                args.goal_ref_id.should_change
                and new_goal_ref_id != habit_stack.goal_ref_id
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

        habit_stack = habit_stack.update(
            context.domain_context,
            name=args.name,
            aspect_ref_id=args.aspect_ref_id,
            chapter_ref_id=args.chapter_ref_id,
            goal_ref_id=args.goal_ref_id,
        )
        await uow.get_for(HabitStack).save(habit_stack)
        await progress_reporter.mark_updated(habit_stack)

        if args.habit_ref_ids.should_change:
            habit_ref_ids = args.habit_ref_ids.just_the_value
            if len(habit_ref_ids) != len(set(habit_ref_ids)):
                raise InputValidationError("Habit ref ids must be unique")

            habits: list[Habit] = []
            if habit_ref_ids:
                habits = await self.find_all_entities(
                    uow,
                    context.user.ref_id,
                    Habit,
                    habit_ref_ids,
                )
                if len(habits) != len(habit_ref_ids):
                    raise InputValidationError("Some habits could not be found")
                for habit in habits:
                    if habit.gen_params.period != habit_stack.period:
                        raise InputValidationError(
                            f"Habit '{habit.name}' does not match the stack period"
                        )

            await HabitStackAssignHabitsService().do_it(
                context.domain_context,
                uow,
                progress_reporter,
                habit_stack,
                habits,
            )
