import { describe, expect, it } from "vitest";

import {
  REVALIDATE_AFTER_AWAY_MS,
  shouldRevalidateOnReturn,
} from "#/core/apps/time_plans/store/revalidate-on-return";

describe("shouldRevalidateOnReturn", () => {
  const away = {
    awayMs: REVALIDATE_AFTER_AWAY_MS,
    pendingMutations: 0,
    busy: false,
  };

  it("reloads after being away long enough", () => {
    expect(shouldRevalidateOnReturn(away)).toBe(true);
  });

  it("doesn't reload after a short look elsewhere", () => {
    expect(
      shouldRevalidateOnReturn({
        ...away,
        awayMs: REVALIDATE_AFTER_AWAY_MS - 1,
      }),
    ).toBe(false);
  });

  it("doesn't reload while edits are still being saved", () => {
    expect(shouldRevalidateOnReturn({ ...away, pendingMutations: 1 })).toBe(
      false,
    );
  });

  it("doesn't reload while navigating or already reloading", () => {
    expect(shouldRevalidateOnReturn({ ...away, busy: true })).toBe(false);
  });

  it("takes a different threshold", () => {
    expect(shouldRevalidateOnReturn({ ...away, awayMs: 1000 }, 1000)).toBe(
      true,
    );
  });
});
