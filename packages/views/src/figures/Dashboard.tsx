// Copyright © 2026 Christopher Snow

// The shop's dashboard as the reporting tool shows it on Monday morning: its title, when it last
// refreshed, and one bar per value it shows. The bars run across the page, one row per day, and
// are a list whose items carry their day and value as text, so the chart and its words are one
// thing and every label stays readable on a phone.

import { z } from "zod";

import { CHANGE_IDS, formatValue, recordOf, storage, week } from "@ms/lab";
import type { InteractiveProps } from "@platform/lesson-runtime";

import { withProps } from "../props";
import { showDay, showTime } from "../show";
import { format, useViewStrings } from "../strings";

const Props = z.object({ changes: z.array(z.enum(CHANGE_IDS)).default([]) });

export const Dashboard = withProps(
  Props,
  function Dashboard({ data }: InteractiveProps & { data: z.infer<typeof Props> }) {
    const strings = useViewStrings();
    const r = recordOf(storage(week(data.changes)), "sales_dashboard");
    const values = r.content.rows.map((row) => ({
      day: String(row[0]),
      value: Number(row[1] ?? 0),
      text: formatValue(row[1] ?? null, r.content.columns[1]!.type),
    }));
    const max = Math.max(1, ...values.map((v) => v.value));
    const title = r.title ?? "";
    return (
      <div className="dashboard">
        <div className="dashboard-head">
          <span className="dashboard-title">{title}</span>
          <span className="dashboard-meta">
            {format(strings.refreshed, { time: showTime(r.lastWritten) })}
          </span>
        </div>
        <ol
          className="bars"
          aria-label={format(strings.chartLabel, { title, time: showTime(r.lastWritten) })}
        >
          {values.map((v) => (
            <li key={v.day} className="bar-item">
              <span className="bar-label">{showDay(v.day, strings.weekdays)}</span>
              <span className="bar-track" aria-hidden="true">
                <span className="bar" style={{ width: `${Math.round((v.value / max) * 100)}%` }} />
              </span>
              <span className="bar-value">{v.text}</span>
            </li>
          ))}
        </ol>
      </div>
    );
  },
);
