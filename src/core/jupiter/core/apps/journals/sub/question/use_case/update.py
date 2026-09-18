"""Use case for updating a journal question."""

from jupiter.core.app import AppCore
from jupiter.core.apps.journals.collection import JournalCollection
from jupiter.core.apps.journals.sub.question.root import JournalQuestion
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
class JournalQuestionUpdateArgs(JupiterUpdateLeafSupportEntityArgs):
    """JournalQuestionUpdate args."""

    ref_id: EntityId
    name: UpdateAction[EntityName]


@use_case_result
class JournalQuestionUpdateResult(UseCaseResultBase):
    """JournalQuestionUpdate result."""

    updated_journal_question: JournalQuestion


@mutation_use_case(
    WorkspaceFeature.JOURNALS, only_for_component=[AppCore.WEBUI, AppCore.API]
)
class JournalQuestionUpdateUseCase(
    JupiterUpdateLeafSupportEntityUseCase[
        JournalQuestionUpdateArgs, JournalQuestionUpdateResult
    ]
):
    """Use case for updating a journal question."""

    async def _perform_transactional_mutation(
        self,
        uow: DomainUnitOfWork,
        progress_reporter: ProgressReporter,
        context: JupiterLoggedInMutationContext,
        args: JournalQuestionUpdateArgs,
    ) -> JournalQuestionUpdateResult:
        """Execute the command's action."""
        _, journal_question = await self.load_in_parent(
            uow,
            JournalCollection,
            JournalQuestion,
            args.ref_id,
            context.workspace.ref_id,
        )
        journal_question = journal_question.update(
            ctx=context.domain_context,
            name=args.name,
        )
        journal_question = await uow.get_for(JournalQuestion).save(journal_question)

        return JournalQuestionUpdateResult(updated_journal_question=journal_question)
