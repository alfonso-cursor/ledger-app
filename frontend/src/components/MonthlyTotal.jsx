import { formatMoney, formatMonth } from "../api.js";

export default function MonthlyTotal({ summary, loading }) {
  return (
    <section className="card total-card" aria-live="polite">
      <p className="eyebrow">This month</p>
      {loading || !summary ? (
        <p className="total-amount">—</p>
      ) : (
        <>
          <p className="total-amount">{formatMoney(summary.total)}</p>
          <p className="muted">
            {formatMonth(summary.month)} · {summary.count}{" "}
            {summary.count === 1 ? "expense" : "expenses"}
          </p>
        </>
      )}
    </section>
  );
}
