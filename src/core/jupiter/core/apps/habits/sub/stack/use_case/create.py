"""The command for creating a habit stack."""

from jupiter.core.apps.habits.collection import HabitCollection
from jupiter.core.apps.habits.sub.habit.root import Habit
from jupiter.core.apps.habits.sub.stack.name import HabitStackName
from jupiter.core.apps.habits.sub.stack.root import HabitStack
from jupiter.core.apps.habits.sub.stack.service.assign_habits import (
    HabitStackAssignHabitsService,
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
class HabitStackCreateArgs(JupiterCreateCrownEntityArgs):
    """Habit stack creation parameters."""

    name: HabitStackName
    period: RecurringTaskPeriod
    habit_ref_ids: list[EntityId]
    aspect_ref_id: EntityId | None
    chapter_ref_id: EntityId | None
    goal_ref_id: EntityId | None


@use_case_result
class HabitStackCreateResult(UseCaseResultBase):
    """Habit stack creation result."""

    new_habit_stack: HabitStack


@mutation_use_case(WorkspaceFeature.HABITS)
class HabitStackCreateUseCase(
    JupiterCreateCrownEntityUseCase[HabitStackCreateArgs, HabitStackCreateResult]
):
    """The command for creating a habit stack."""

    async def _perform_transactional_mutation(
        self,
        uow: DomainUnitOfWork,
        progress_reporter: ProgressReporter,
        context: JupiterLoggedInMutationContext,
        args: HabitStackCreateArgs,
    ) -> HabitStackCreateResult:
        """Execute the command's action."""
        workspace = context.workspace

        if not workspace.is_feature_available(WorkspaceFeature.LIFE_PLAN):
            if args.aspect_ref_id is not None:
                raise UnavailableForContextError(WorkspaceFeature.LIFE_PLAN)
            if args.chapter_ref_id is not None:
                raise UnavailableForContextError(WorkspaceFeature.LIFE_PLAN)
            if args.goal_ref_id is not None:
                raise UnavailableForContextError(WorkspaceFeature.LIFE_PLAN)

        habit_collection = await uow.get_for(HabitCollection).load_by_parent(
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

        if len(args.habit_ref_ids) != len(set(args.habit_ref_ids)):
            raise InputValidationError("Habit ref ids must be unique")

        habits: list[Habit] = []
        if args.habit_ref_ids:
            habits = await self.find_all_entities(
                uow,
                context.user.ref_id,
                Habit,
                args.habit_ref_ids,
            )
            if len(habits) != len(args.habit_ref_ids):
                raise InputValidationError("Some habits could not be found")
            for habit in habits:
                if habit.gen_params.period != args.period:
                    raise InputValidationError(
                        f"Habit '{habit.name}' does not match the stack period"
                    )

        new_habit_stack = HabitStack.new_habit_stack(
            context.domain_context,
            habit_collection_ref_id=habit_collection.ref_id,
            name=args.name,
            period=args.period,
            aspect_ref_id=the_aspect.ref_id,
            chapter_ref_id=args.chapter_ref_id,
            goal_ref_id=args.goal_ref_id,
        )
        new_habit_stack = await self.create_entity(
            context.domain_context,
            uow,
            progress_reporter,
            context.user.ref_id,
            new_habit_stack,
        )

        await HabitStackAssignHabitsService().do_it(
            context.domain_context,
            uow,
            progress_reporter,
            new_habit_stack,
            habits,
        )

        return HabitStackCreateResult(new_habit_stack=new_habit_stack)
