import { z } from "zod";

/** A checkbox (or switch) field: "on" when checked, missing otherwise. */
export const CheckboxAsBoolean = z
  .string()
  .optional()
  .transform((value) => value === "on");
