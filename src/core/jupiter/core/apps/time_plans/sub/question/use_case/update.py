"""Use case for updating a time plan question."""

from jupiter.core.app import AppCore
from jupiter.core.apps.time_plans.domain import TimePlanDomain
from jupiter.core.apps.time_plans.sub.question.root import TimePlanQuestion
from jupiter.core.config import (
    JupiterLoggedInMutationContext,
)
from jupiter.core.features import WorkspaceFeature
from jupiter.core.leaf_support_entity_support import (
    JupiterUpdateLeafSupportEntityArgs,
    JupiterUpdateLeafSupportEntityUseCase,
)
from jupiter.framework.base.entity_id import EntityId
from jupiter.framework.base.entity_name import EntityName
from jupiter.framework.progress_reporter.reporter import ProgressReporter
from jupiter.framework.storage.repository import DomainUnitOfWork
from jupiter.framework.update_action import UpdateAction
from jupiter.framework.use_case import mutation_use_case
from jupiter.framework.use_case_io import (
    UseCaseResultBase,
    use_case_args,
    use_case_result,
)


@use_case_args
class TimePlanQuestionUpdateArgs(JupiterUpdateLeafSupportEntityArgs):
    """TimePlanQuestionUpdate args."""

    ref_id: EntityId
    name: UpdateAction[EntityName]


@use_case_result
class TimePlanQuestionUpdateResult(UseCaseResultBase):
    """TimePlanQuestionUpdate result."""

    updated_time_plan_question: TimePlanQuestion


@mutation_use_case(
    WorkspaceFeature.TIME_PLANS, only_for_component=[AppCore.WEBUI, AppCore.API]
)
class TimePlanQuestionUpdateUseCase(
    JupiterUpdateLeafSupportEntityUseCase[
        TimePlanQuestionUpdateArgs, TimePlanQuestionUpdateResult
    ]
):
    """Use case for updating a time plan question."""

    async def _perform_transactional_mutation(
        self,
        uow: DomainUnitOfWork,
        progress_reporter: ProgressReporter,
        context: JupiterLoggedInMutationContext,
        args: TimePlanQuestionUpdateArgs,
    ) -> TimePlanQuestionUpdateResult:
        """Execute the command's action."""
        _, time_plan_question = await self.load_in_parent(
            uow,
            TimePlanDomain,
            TimePlanQuestion,
            args.ref_id,
            context.workspace.ref_id,
        )
        time_plan_question = time_plan_question.update(
            ctx=context.domain_context,
            name=args.name,
        )
        time_plan_question = await uow.get_for(TimePlanQuestion).save(
            time_plan_question
        )

        return TimePlanQuestionUpdateResult(
            updated_time_plan_question=time_plan_question
        )
