import { describe, expect, it } from "vitest";

import { fieldLabel, formatGap, summarizeValues } from "./format";

describe("summarizeValues", () => {
  it("collapses consecutive values into ranges", () => {
    expect(summarizeValues([1, 2, 3, 5, 7, 8])).toBe("1-3, 5, 7-8");
  });

  it("handles a single value and an empty list", () => {
    expect(summarizeValues([4])).toBe("4");
    expect(summarizeValues([])).toBe("");
  });
});

describe("formatGap", () => {
  it("formats minutes, hours and days", () => {
    expect(formatGap("2026-01-01T00:00:00Z", "2026-01-01T00:15:00Z")).toBe("15m");
    expect(formatGap("2026-01-01T00:00:00Z", "2026-01-02T02:00:00Z")).toBe("1d 2h");
  });
});

describe("fieldLabel", () => {
  it("falls back to the raw name", () => {
    expect(fieldLabel("day_of_week")).toBe("Day of week");
    expect(fieldLabel("second")).toBe("second");
  });
});
