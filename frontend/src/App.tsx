import { FormEvent, useEffect, useState } from "react";

import { CronError, ExplainResponse, explain } from "./api";
import { fieldLabel, formatGap, summarizeValues } from "./format";

const EXAMPLES = ["*/15 * * * *", "0 9 * * MON-FRI", "30 2 1 * *", "0 0 15 * SUN"];

export default function App() {
  const [expression, setExpression] = useState("0 9 * * MON-FRI");
  const [result, setResult] = useState<ExplainResponse | null>(null);
  const [error, setError] = useState<CronError | null>(null);
  const [loading, setLoading] = useState(false);

  async function run(value: string) {
    setLoading(true);
    try {
      setResult(await explain(value));
      setError(null);
    } catch (err) {
      setResult(null);
      setError(err instanceof CronError ? err : new CronError(String(err), null));
    } finally {
      setLoading(false);
    }
  }

  useEffect(() => {
    void run(expression);
    // Only explain the initial example on mount; later runs are user-triggered.
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, []);

  function onSubmit(event: FormEvent) {
    event.preventDefault();
    void run(expression);
  }

  return (
    <main>
      <h1>CronLens</h1>
      <p className="tagline">Explain, validate and preview cron schedules.</p>

      <form onSubmit={onSubmit}>
        <input
          aria-label="Cron expression"
          value={expression}
          onChange={(event) => setExpression(event.target.value)}
          spellCheck={false}
        />
        <button type="submit" disabled={loading}>
          Explain
        </button>
      </form>

      <div className="examples">
        {EXAMPLES.map((example) => (
          <button
            key={example}
            type="button"
            onClick={() => {
              setExpression(example);
              void run(example);
            }}
          >
            {example}
          </button>
        ))}
      </div>

      {error && (
        <p className="error" role="alert">
          {error.field ? `${fieldLabel(error.field)}: ` : ""}
          {error.message}
        </p>
      )}

      {result && (
        <>
          <p className="description">{result.description}</p>

          <h2>Fields</h2>
          <table>
            <tbody>
              {result.fields.map((field) => (
                <tr key={field.name}>
                  <th>{fieldLabel(field.name)}</th>
                  <td>
                    <code>{field.source}</code>
                  </td>
                  <td>{summarizeValues(field.values)}</td>
                </tr>
              ))}
            </tbody>
          </table>

          <h2>Next runs (UTC)</h2>
          {result.next_runs.length === 0 ? (
            <p>This schedule never fires within the next five years.</p>
          ) : (
            <ol>
              {result.next_runs.map((run, index) => (
                <li key={run}>
                  {run.replace("T", " ").replace(/:00Z$/, "")}
                  {index > 0 && (
                    <span className="gap">+{formatGap(result.next_runs[index - 1], run)}</span>
                  )}
                </li>
              ))}
            </ol>
          )}
        </>
      )}
    </main>
  );
}
