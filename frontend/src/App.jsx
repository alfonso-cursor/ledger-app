import { useCallback, useEffect, useState } from "react";
import { createExpense, getCategories, getExpenses, getMonthlySummary } from "./api.js";
import ExpenseForm from "./components/ExpenseForm.jsx";
import ExpenseList from "./components/ExpenseList.jsx";
import MonthlyTotal from "./components/MonthlyTotal.jsx";

export default function App() {
  const [categories, setCategories] = useState([]);
  const [expenses, setExpenses] = useState([]);
  const [summary, setSummary] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");

  const load = useCallback(async () => {
    const [nextCategories, nextExpenses, nextSummary] = await Promise.all([
      getCategories(),
      getExpenses(),
      getMonthlySummary(),
    ]);
    setCategories(nextCategories);
    setExpenses(nextExpenses);
    setSummary(nextSummary);
  }, []);

  useEffect(() => {
    let active = true;
    load()
      .catch((err) => {
        if (active) setError(err.message || "Could not load expenses.");
      })
      .finally(() => {
        if (active) setLoading(false);
      });
    return () => {
      active = false;
    };
  }, [load]);

  async function handleAdd(expense) {
    setError("");
    await createExpense(expense);
    const [nextExpenses, nextSummary] = await Promise.all([
      getExpenses(),
      getMonthlySummary(),
    ]);
    setExpenses(nextExpenses);
    setSummary(nextSummary);
  }

  return (
    <main className="page">
      <header className="page-header">
        <div>
          <p className="eyebrow">Ledger</p>
          <h1>Expenses</h1>
        </div>
        <MonthlyTotal summary={summary} loading={loading} />
      </header>
      {error ? <p className="banner">{error}</p> : null}
      <ExpenseForm categories={categories} onAdd={handleAdd} />
      <ExpenseList expenses={expenses} loading={loading} />
    </main>
  );
}
