"""Tests for the life plan note section rules."""

import pytest
from jupiter.core.apps.life_plan.note_sections import (
    period_allows_aspects_in_note,
    period_allows_goals_in_note,
)
from jupiter.core.common.recurring_task_period import RecurringTaskPeriod

ASPECTS_ALLOWED = [
    (RecurringTaskPeriod.DAILY, False),
    (RecurringTaskPeriod.WEEKLY, False),
    (RecurringTaskPeriod.MONTHLY, True),
    (RecurringTaskPeriod.QUARTERLY, True),
    (RecurringTaskPeriod.YEARLY, True),
]

GOALS_ALLOWED = [
    (RecurringTaskPeriod.DAILY, False),
    (RecurringTaskPeriod.WEEKLY, False),
    (RecurringTaskPeriod.MONTHLY, False),
    (RecurringTaskPeriod.QUARTERLY, True),
    (RecurringTaskPeriod.YEARLY, True),
]


@pytest.mark.parametrize(("period", "allowed"), ASPECTS_ALLOWED)
def test_period_allows_aspects_in_note(
    period: RecurringTaskPeriod, allowed: bool
) -> None:
    """Aspects show up in notes from the monthly period upwards."""
    assert period_allows_aspects_in_note(period) is allowed


@pytest.mark.parametrize(("period", "allowed"), GOALS_ALLOWED)
def test_period_allows_goals_in_note(
    period: RecurringTaskPeriod, allowed: bool
) -> None:
    """Goals show up in notes from the quarterly period upwards."""
    assert period_allows_goals_in_note(period) is allowed
