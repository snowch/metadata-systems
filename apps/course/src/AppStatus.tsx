// Copyright © 2026 Christopher Snow

import { useEffect, useRef } from "react";
import { appStatus } from "../../../offline/status.js";
import { base } from "./offline";

export function AppStatus() {
  const host = useRef<HTMLDivElement>(null);
  useEffect(() => {
    const status = appStatus(base);
    host.current?.append(status.node);
    return () => status.dispose();
  }, []);
  return <div ref={host} />;
}
