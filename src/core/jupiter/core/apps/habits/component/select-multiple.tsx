import type {
  EntityId,
  Habit,
  RecurringTaskPeriod,
} from "@jupiter/webapi-client";
import { Autocomplete, TextField } from "@mui/material";
import { useEffect, useMemo, useState } from "react";

import { autocompleteSingleLineSx } from "#/core/common/component/autocomplete";
import { PeriodTag } from "#/core/common/component/period-tag";
import { sortHabitsNaturally } from "#/core/apps/habits/root";

interface HabitSelectMultipleProps {
  name: string;
  label: string;
  allHabits: Habit[];
  defaultValue?: EntityId[];
  value?: EntityId[];
  onChange?: (value: EntityId[]) => void;
  filterPeriod?: RecurringTaskPeriod;
  inputsEnabled?: boolean;
}

export function HabitSelectMultiple(props: HabitSelectMultipleProps) {
  const filteredHabits = useMemo(() => {
    const matching = props.filterPeriod
      ? props.allHabits.filter(
          (habit) => habit.gen_params.period === props.filterPeriod,
        )
      : props.allHabits;
    return sortHabitsNaturally(matching);
  }, [props.allHabits, props.filterPeriod]);

  const allHabitsByRefId = useMemo(
    () => new Map(filteredHabits.map((habit) => [habit.ref_id, habit])),
    [filteredHabits],
  );

  const [selectedHabits, setSelectedHabits] = useState(
    selectedHabitsToOptions(props.value, props.defaultValue, allHabitsByRefId),
  );

  useEffect(() => {
    setSelectedHabits(
      selectedHabitsToOptions(
        props.value,
        props.defaultValue,
        allHabitsByRefId,
      ),
    );
  }, [props.value, props.defaultValue, props.allHabits, allHabitsByRefId]);

  return (
    <>
      <Autocomplete
        autoHighlight
        multiple
        filterSelectedOptions
        disabled={props.inputsEnabled === false}
        id={props.name}
        options={filteredHabits.map(habitToOption)}
        sx={autocompleteSingleLineSx}
        value={selectedHabits}
        onChange={(e, v) => {
          setSelectedHabits(v);
          if (props.onChange) {
            props.onChange(v.map((option) => option.habit_ref_id));
          }
        }}
        isOptionEqualToValue={(o, v) => o.habit_ref_id === v.habit_ref_id}
        getOptionLabel={(option) => option.label}
        renderOption={(optionProps, option) => (
          <li
            {...optionProps}
            key={option.habit_ref_id}
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
        value={selectedHabits.map((option) => option.habit_ref_id).join(",")}
      />
    </>
  );
}

function selectedHabitsToOptions(
  value: EntityId[] | undefined,
  defaultValue: EntityId[] | undefined,
  allHabitsByRefId: Map<EntityId, Habit>,
) {
  const habitRefIds = value ?? defaultValue ?? [];
  return habitRefIds
    .map((refId) => allHabitsByRefId.get(refId))
    .filter((habit): habit is Habit => habit !== undefined)
    .map(habitToOption);
}

function habitToOption(habit: Habit) {
  return {
    habit_ref_id: habit.ref_id,
    label: habit.name,
    period: habit.gen_params.period,
  };
}
