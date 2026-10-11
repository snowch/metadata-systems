// Copyright © 2026 Christopher Snow

// Monday morning's dashboard, as Chapters 1 and 2 show it: its title, when it was refreshed, and a
// bar per day. The values come from the shop's engine (notebook/front_dashboard.py writes
// dashboard.json, and notebook/tests/test_front.py fails if the file differs from what the engine
// gives); the page draws them and computes nothing.

import data from "../dashboard.json";
import { fill } from "../fill";
import { STRINGS } from "../strings";

const NB_HYPHEN = "‑";
const FIRST_DAY = Date.UTC(2026, 8, 7); // Monday 7 September 2026, the week's first day

/** A refresh time as the dashboard shows it: "2026‑09‑14 03:00:09 UTC". */
const showTime = (t: string) =>
  `${t.slice(0, 10).replaceAll("-", NB_HYPHEN)} ${t.slice(11, 19)} UTC`;

/** A day as "Thu 10". */
function showDay(day: string): string {
  const offset = Math.round((Date.parse(`${day}T00:00:00Z`) - FIRST_DAY) / 86_400_000);
  return `${STRINGS.weekdays[((offset % 7) + 7) % 7] ?? ""} ${Number(day.slice(8, 10))}`;
}

export function Dashboard() {
  const time = showTime(data.lastRefreshed);
  const max = Math.max(1, ...data.values.map((v) => v.pence));
  return (
    <div className="dashboard">
      <div className="dashboard-head">
        <span className="dashboard-title">{data.title}</span>
        <span className="dashboard-meta">{fill(STRINGS.refreshed, { time })}</span>
      </div>
      <ol className="bars" aria-label={fill(STRINGS.chartLabel, { title: data.title, time })}>
        {data.values.map((v) => (
          <li key={v.day} className="bar-item">
            <span className="bar-label">{showDay(v.day)}</span>
            <span className="bar-track" aria-hidden="true">
              <span className="bar" style={{ width: `${Math.round((v.pence / max) * 100)}%` }} />
            </span>
            <span className="bar-value">{v.shown}</span>
          </li>
        ))}
      </ol>
    </div>
  );
}
