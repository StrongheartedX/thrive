import type { HabitStack } from "@jupiter/webapi-client";

import { LinkTag } from "#/core/infra/component/link-tag";

interface Props {
  habitStack: HabitStack;
}

export function HabitStackTag(props: Props) {
  return <LinkTag label={props.habitStack.name} color="info" />;
}
