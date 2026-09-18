/* generated using openapi-typescript-codegen -- do not edit */
/* istanbul ignore file */
/* tslint:disable */
/* eslint-disable */
import type { BigPlan } from './BigPlan';
import type { BigPlanLoadResult } from './BigPlanLoadResult';
import type { Chore } from './Chore';
import type { ChoreLoadResult } from './ChoreLoadResult';
import type { ChoreStack } from './ChoreStack';
import type { ChoreStackLoadResult } from './ChoreStackLoadResult';
import type { Habit } from './Habit';
import type { HabitLoadResult } from './HabitLoadResult';
import type { HabitStack } from './HabitStack';
import type { HabitStackLoadResult } from './HabitStackLoadResult';
import type { InboxTask } from './InboxTask';
import type { InboxTaskLoadResult } from './InboxTaskLoadResult';
import type { TimeEventInDayBlock } from './TimeEventInDayBlock';
import type { TimePlanActivity } from './TimePlanActivity';
import type { TodoTask } from './TodoTask';
import type { TodoTaskLoadResult } from './TodoTaskLoadResult';
/**
 * TimePlanActivityLoadForPanel result.
 *
 * The target and its details are as for ``TimePlanActivityLoadResult``, except
 * that the details leave out what the panel doesn't show: habits carry no
 * streak marks, nothing carries its publish entity, and the tasks are the
 * ones still worth showing (see the load services). The lists the editors
 * pick from come from the time plan view itself, which loads them once.
 *
 */
export type TimePlanActivityLoadForPanelResult = {
    time_plan_activity: TimePlanActivity;
    time_event_blocks: Array<TimeEventInDayBlock>;
    target_inbox_task?: (InboxTask | null);
    target_inbox_task_info?: (InboxTaskLoadResult | null);
    target_big_plan?: (BigPlan | null);
    target_big_plan_info?: (BigPlanLoadResult | null);
    target_todo_task?: (TodoTask | null);
    target_todo_task_info?: (TodoTaskLoadResult | null);
    target_habit?: (Habit | null);
    target_habit_info?: (HabitLoadResult | null);
    target_habit_stack?: (HabitStack | null);
    target_habit_stack_info?: (HabitStackLoadResult | null);
    target_chore?: (Chore | null);
    target_chore_info?: (ChoreLoadResult | null);
    target_chore_stack?: (ChoreStack | null);
    target_chore_stack_info?: (ChoreStackLoadResult | null);
    stack_inbox_tasks: Array<InboxTask>;
};

