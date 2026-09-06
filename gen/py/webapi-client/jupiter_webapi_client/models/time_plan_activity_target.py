from enum import StrEnum


class TimePlanActivityTarget(StrEnum):
    BIG_PLAN = "big-plan"
    CHORE = "chore"
    CHORE_STACK = "chore-stack"
    HABIT = "habit"
    HABIT_STACK = "habit-stack"
    INBOX_TASK = "inbox-task"
    TODO_TASK = "todo-task"

    def __str__(self) -> str:
        return str(self.value)
