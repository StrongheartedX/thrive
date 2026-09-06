import type { EntityId, HabitStack } from "@jupiter/webapi-client";
import { Autocomplete, TextField } from "@mui/material";
import { useEffect, useMemo, useState } from "react";

import { autocompleteSingleLineSx } from "#/core/common/component/autocomplete";
import { PeriodTag } from "#/core/common/component/period-tag";
import { sortHabitStacksNaturally } from "#/core/apps/habits/root";

interface HabitStackSelectSingleProps {
  name: string;
  label: string;
  allowNone?: boolean;
  allStacks: HabitStack[];
  defaultValue?: EntityId | null;
  value?: EntityId | null;
  onChange?: (value: EntityId | undefined) => void;
  inputsEnabled?: boolean;
}

export function HabitStackSelectSingle(props: HabitStackSelectSingleProps) {
  const allStacksByRefId = useMemo(
    () => new Map(props.allStacks.map((stack) => [stack.ref_id, stack])),
    [props.allStacks],
  );

  const sortedStacks = sortHabitStacksNaturally(props.allStacks);
  const allStacksAsOptions = sortedStacks.map(stackToOption);

  const [selectedStack, setSelectedStack] = useState(
    selectedStackToOption(props.value, props.defaultValue, allStacksByRefId),
  );
  useEffect(() => {
    setSelectedStack(
      selectedStackToOption(props.value, props.defaultValue, allStacksByRefId),
    );
  }, [
    props.allowNone,
    props.value,
    props.defaultValue,
    props.allStacks,
    allStacksByRefId,
  ]);

  return (
    <>
      <Autocomplete
        autoHighlight
        disableClearable={!props.allowNone}
        disabled={props.inputsEnabled === false}
        id={props.name}
        options={allStacksAsOptions}
        sx={{
          width: "100%",
          minWidth: 0,
          ...autocompleteSingleLineSx,
        }}
        value={selectedStack}
        onChange={(e, v) => {
          if (!props.allowNone && !v) {
            return;
          }

          setSelectedStack(v || undefined);
          if (props.onChange) {
            props.onChange(v?.stack_ref_id);
          }
        }}
        isOptionEqualToValue={(o, v) =>
          (o === undefined && v === undefined) ||
          o?.stack_ref_id === v?.stack_ref_id
        }
        getOptionLabel={(option) => option?.label || ""}
        renderOption={(optionProps, option) => (
          <li
            {...optionProps}
            key={option.stack_ref_id || "none"}
            style={{ display: "flex", alignItems: "center", gap: 1 }}
          >
            {option.label} <PeriodTag period={option.period} />
          </li>
        )}
        renderInput={(params) => <TextField {...params} label={props.label} />}
      />
      <input
        type="hidden"
        name={props.name}
        value={selectedStack?.stack_ref_id || ""}
      />
    </>
  );
}

function selectedStackToOption(
  value: EntityId | null | undefined,
  defaultValue: EntityId | null | undefined,
  allStacksByRefId: Map<EntityId, HabitStack>,
) {
  const stackRefId = value || defaultValue;
  const stack = stackRefId ? allStacksByRefId.get(stackRefId) : undefined;

  if (stackRefId === undefined || stackRefId === null || stack === undefined) {
    return undefined;
  }
  return stackToOption(stack);
}

function stackToOption(stack: HabitStack) {
  return {
    stack_ref_id: stack.ref_id,
    label: stack.name,
    period: stack.period,
  };
}
