import { formatMoney } from "../api.js";

export default function ExpenseList({ expenses, loading }) {
  return (
    <section className="card">
      <h2>Expenses</h2>
      {loading ? <p className="muted">Loading…</p> : null}
      {!loading && expenses.length === 0 ? (
        <p className="muted">No expenses yet. Add one above.</p>
      ) : null}
      {expenses.length > 0 ? (
        <ul className="expense-list">
          {expenses.map((expense) => (
            <li key={expense.id} className="expense-row">
              <div>
                <p className="expense-description">{expense.description}</p>
                <p className="muted expense-meta">
                  <time dateTime={expense.date}>{expense.date}</time>
                  <span className="pill">{expense.category}</span>
                </p>
              </div>
              <p className="expense-amount">{formatMoney(expense.amount)}</p>
            </li>
          ))}
        </ul>
      ) : null}
    </section>
  );
}
