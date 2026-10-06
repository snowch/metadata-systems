// Copyright © 2026 Christopher Snow

// A figure checks its props against its own schema, and says so in its place when they do not
// fit, so a lesson that names a figure wrongly shows the problem instead of a broken page.

import type { ComponentType } from "react";
import type { z } from "zod";

import type { InteractiveProps } from "@platform/lesson-runtime";

import { format, useViewStrings } from "./strings";

export function withProps<S extends z.ZodType>(
  schema: S,
  View: ComponentType<InteractiveProps & { data: z.infer<S> }>,
): ComponentType<InteractiveProps> {
  function Checked(props: InteractiveProps) {
    const strings = useViewStrings();
    const parsed = schema.safeParse(props.interactive.props);
    if (!parsed.success) {
      const message = parsed.error.issues
        .map((i) => `${i.path.join(".") || "props"}: ${i.message}`)
        .join("; ");
      return (
        <p role="note" className="interactive-problem">
          {format(strings.problem, { message })}
        </p>
      );
    }
    return <View {...props} data={parsed.data} />;
  }
  Checked.displayName = `Checked(${View.displayName ?? View.name})`;
  return Checked;
}
