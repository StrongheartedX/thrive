import type { Chore, ChoreStack } from "@jupiter/webapi-client";
import { RecurringTaskPeriod } from "@jupiter/webapi-client";
import { describe, expect, it } from "vitest";

import {
  UPDATE_CHORE_STACK,
  updateChoreStackArgsFromForm,
} from "#/core/apps/time_plans/store/mutations/update-chore-stack";
import {
  createTimePlanStore,
  seedTimePlanSource,
  selectTimePlanEntities,
} from "#/core/apps/time_plans/store/store";

const MODIFIED = "2026-09-14T10:00:00Z";

function choreStack(fields: Partial<ChoreStack> = {}): ChoreStack {
  return {
    ref_id: "60",
    version: 1,
    archived: false,
    name: "Stored stack",
    period: RecurringTaskPeriod.WEEKLY,
    aspect_ref_id: "1",
    chapter_ref_id: null,
    goal_ref_id: null,
    last_modified_time: "2026-09-01T00:00:00Z",
    ...fields,
  } as ChoreStack;
}

function chore(refId: string, stackRefId: string | null): Chore {
  return {
    ref_id: refId,
    version: 1,
    archived: false,
    name: `Chore ${refId}`,
    stack_ref_id: stackRefId,
    last_modified_time: "2026-09-01T00:00:00Z",
  } as Chore;
}

describe("UPDATE_CHORE_STACK", () => {
  it("renames the stack and moves chores in and out of it", () => {
    const formData = new FormData();
    formData.set("targetChoreStackRefId", "60");
    formData.set("targetChoreStackName", "Edited stack");
    formData.set("targetChoreStackChoreRefIds", "602");

    const args = updateChoreStackArgsFromForm(
      formData,
      MODIFIED,
      "targetChoreStack",
    );
    const entities = UPDATE_CHORE_STACK.applyOptimistic(
      selectTimePlanEntities(
        seedTimePlanSource(createTimePlanStore(), "plan", {
          choreStacks: [choreStack()],
          chores: [chore("601", "60"), chore("602", null)],
        }),
      ),
      args,
    );

    expect(args).toMatchObject({ choreRefIds: ["602"], lifePlan: null });
    expect(entities.choreStacks["60"].name).toBe("Edited stack");
    expect(entities.chores["601"].stack_ref_id).toBeNull();
    expect(entities.chores["602"].stack_ref_id).toBe("60");
  });

  it("merges back the stack and the chores that moved", () => {
    const updatedStack = choreStack({ version: 2 });
    const updatedChores = [chore("602", "60")];

    expect(
      UPDATE_CHORE_STACK.toDelta({
        updated_chore_stack: updatedStack,
        updated_chores: updatedChores,
      }),
    ).toEqual({ choreStacks: [updatedStack], chores: updatedChores });
  });
});
