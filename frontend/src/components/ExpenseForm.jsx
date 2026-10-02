import { useState } from "react";
import { todayISO } from "../api.js";

const EMPTY = {
  amount: "",
  description: "",
  category: "",
  date: todayISO(),
};

export default function ExpenseForm({ categories, onAdd }) {
  const [form, setForm] = useState(EMPTY);
  const [error, setError] = useState("");
  const [saving, setSaving] = useState(false);

  function update(field, value) {
    setForm((current) => ({ ...current, [field]: value }));
  }

  async function handleSubmit(event) {
    event.preventDefault();
    setError("");

    const description = form.description.trim();
    const amount = form.amount.trim();
    if (!amount || Number(amount) <= 0) {
      setError("Enter an amount greater than 0.");
      return;
    }
    if (!/^\d+(\.\d{1,2})?$/.test(amount)) {
      setError("Use a positive amount with up to 2 decimal places.");
      return;
    }
    if (!description) {
      setError("Add a short description.");
      return;
    }
    if (!form.category) {
      setError("Pick a category.");
      return;
    }
    if (!form.date) {
      setError("Pick a date.");
      return;
    }

    setSaving(true);
    try {
      await onAdd({
        amount,
        description,
        category: form.category,
        date: form.date,
      });
      setForm({ ...EMPTY, date: todayISO(), category: form.category });
    } catch (err) {
      setError(err.message || "Could not save the expense.");
    } finally {
      setSaving(false);
    }
  }

  return (
    <form className="card form" onSubmit={handleSubmit}>
      <h2>Add expense</h2>
      <div className="fields">
        <label>
          Amount
          <input
            type="text"
            inputMode="decimal"
            placeholder="0.00"
            value={form.amount}
            onChange={(event) => update("amount", event.target.value)}
            required
          />
        </label>
        <label>
          Category
          <select
            value={form.category}
            onChange={(event) => update("category", event.target.value)}
            required
          >
            <option value="">Select</option>
            {categories.map((category) => (
              <option key={category} value={category}>
                {category}
              </option>
            ))}
          </select>
        </label>
        <label>
          Date
          <input
            type="date"
            value={form.date}
            onChange={(event) => update("date", event.target.value)}
            required
          />
        </label>
        <label className="span-2">
          Description
          <input
            type="text"
            maxLength={200}
            placeholder="What was this for?"
            value={form.description}
            onChange={(event) => update("description", event.target.value)}
            required
          />
        </label>
      </div>
      {error ? <p className="form-error">{error}</p> : null}
      <button type="submit" disabled={saving}>
        {saving ? "Saving…" : "Add expense"}
      </button>
    </form>
  );
}
