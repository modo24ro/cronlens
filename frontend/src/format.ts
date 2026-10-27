const FIELD_LABELS: Record<string, string> = {
  minute: "Minute",
  hour: "Hour",
  day_of_month: "Day of month",
  month: "Month",
  day_of_week: "Day of week",
};

export function fieldLabel(name: string): string {
  return FIELD_LABELS[name] ?? name;
}

/** Collapse sorted numbers into ranges: [1,2,3,5] -> "1-3, 5". */
export function summarizeValues(values: number[]): string {
  const parts: string[] = [];
  let start = values[0];
  let prev = values[0];
  for (const value of values.slice(1).concat(Number.NaN)) {
    if (value === prev + 1) {
      prev = value;
      continue;
    }
    if (start !== undefined) {
      parts.push(start === prev ? `${start}` : `${start}-${prev}`);
    }
    start = value;
    prev = value;
  }
  return parts.join(", ");
}

/** Human-friendly gap between two ISO timestamps, e.g. "15m" or "1d 2h". */
export function formatGap(fromIso: string, toIso: string): string {
  let minutes = Math.round((Date.parse(toIso) - Date.parse(fromIso)) / 60000);
  const days = Math.floor(minutes / 1440);
  minutes -= days * 1440;
  const hours = Math.floor(minutes / 60);
  minutes -= hours * 60;
  const parts = [days && `${days}d`, hours && `${hours}h`, minutes && `${minutes}m`].filter(Boolean);
  return parts.length ? parts.join(" ") : "0m";
}
