"""Rules for which life plan sections a note of a certain period can have."""

from jupiter.core.common.recurring_task_period import RecurringTaskPeriod


def period_allows_aspects_in_note(period: RecurringTaskPeriod) -> bool:
    """Whether a note for this period can have a section for each aspect."""
    return period >= RecurringTaskPeriod.MONTHLY


def period_allows_goals_in_note(period: RecurringTaskPeriod) -> bool:
    """Whether a note for this period can have a section for each goal."""
    return period >= RecurringTaskPeriod.QUARTERLY
