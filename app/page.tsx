"use client";
import { useState } from "react";

type Stats = { numbers: number[]; sum: number; product: number; mean: number; };

function getError(err: unknown) {
  if (err instanceof Error) return err.message;
  try { return JSON.stringify(err); } catch { return "Request failed"; }
}

export default function Home() {
  const [raw, setRaw] = useState("1, 2, 3, 4, 5");
  const [stats, setStats] = useState<Stats | null>(null);
  const [error, setError] = useState<string | null>(null);
  const [loading, setLoading] = useState(false);

  async function onSubmit(e: React.FormEvent<HTMLFormElement>) {
    e.preventDefault();
    setError(null); setStats(null); setLoading(true);
    try {
      const isLocal = typeof window !== "undefined" &&
        (window.location.hostname === "localhost" || window.location.hostname === "127.0.0.1");
      const apiUrl = isLocal ? "http://localhost:8000/" : "/api/calc";

      const tokens = raw.replace(/,/g, " ").trim().split(/\s+/).filter(Boolean);
      const numbers = tokens.map(Number);
      if (numbers.some(n => Number.isNaN(n))) throw new Error("Please enter only numbers.");

      const res = await fetch(apiUrl, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ numbers }),
      });

      const ct = res.headers.get("content-type") || "";
      const data = ct.includes("application/json") ? await res.json() : await res.text();
      if (!res.ok) throw new Error(typeof data === "string" ? data : data?.detail || "Request failed");
      if (typeof data === "string") throw new Error("Server returned non-JSON response.");

      setStats(data as Stats);
    } catch (err) {
      setError(getError(err));
    } finally {
      setLoading(false);
    }
  }

  return (
    <main style={styles.main}>
      <div style={styles.card}>
        <h1 style={styles.title}>Zelus Test — Calculator</h1>
        <form onSubmit={onSubmit} style={styles.form}>
          <textarea
            rows={4}
            value={raw}
            onChange={(e) => setRaw(e.target.value)}
            placeholder="e.g. 10, 3.5, -2, 7"
            style={styles.textarea}
          />
          <button type="submit" style={styles.button} disabled={loading}>
            {loading ? "Calculating…" : "Calculate"}
          </button>
        </form>
        {error && <p style={styles.error}>⚠️ {error}</p>}
        {stats && (
          <div style={styles.results}>
            <ul style={styles.ul}>
              <li><strong>Numbers:</strong> {stats.numbers.join(", ")}</li>
              <li><strong>Sum:</strong> {stats.sum}</li>
              <li><strong>Product:</strong> {stats.product}</li>
              <li><strong>Mean:</strong> {stats.mean}</li>
            </ul>
          </div>
        )}
      </div>
    </main>
  );
}

const styles: Record<string, React.CSSProperties> = {
  main: { minHeight: "100dvh", display: "grid", placeItems: "center", padding: 24, background: "#0b1020" },
  card: { width: "100%", maxWidth: 720, background: "#121933", color: "#e6e9f5", padding: 24, borderRadius: 16 },
  form: { display: "grid", gap: 12, marginTop: 16 },
  textarea: { padding: 12, borderRadius: 10 },
  button: { padding: "10px 14px", borderRadius: 10, cursor: "pointer" },
  error: { color: "#ffb4b4", marginTop: 8 },
  results: { marginTop: 16, background: "#0d1430", padding: 16, borderRadius: 12 },
  ul: { lineHeight: 1.9 },
  title: { margin: 0, fontSize: 28 },
};
