export const CURRENCY = "EUR";

async function request(path, options = {}) {
  const response = await fetch(path, {
    ...options,
    headers: {
      "Content-Type": "application/json",
      ...options.headers,
    },
  });

  if (!response.ok) {
    let message = `Request failed (${response.status})`;
    try {
      const body = await response.json();
      if (typeof body.detail === "string") {
        message = body.detail;
      } else if (Array.isArray(body.detail)) {
        message = body.detail.map((item) => item.msg).filter(Boolean).join(", ");
      }
    } catch {
      // Keep the status fallback when the body is not JSON.
    }
    throw new Error(message || `Request failed (${response.status})`);
  }

  return response.json();
}

export function getCategories() {
  return request("/api/categories").then((body) => body.categories);
}

export function getExpenses() {
  return request("/api/expenses");
}

export function createExpense(expense) {
  return request("/api/expenses", {
    method: "POST",
    body: JSON.stringify(expense),
  });
}

export function getMonthlySummary(month) {
  const query = month ? `?month=${encodeURIComponent(month)}` : "";
  return request(`/api/summary/monthly${query}`);
}

export function formatMoney(amount) {
  return new Intl.NumberFormat(undefined, {
    style: "currency",
    currency: CURRENCY,
  }).format(Number(amount));
}

export function formatMonth(yyyyMm) {
  const [year, month] = yyyyMm.split("-").map(Number);
  return new Date(year, month - 1, 1).toLocaleDateString(undefined, {
    month: "long",
    year: "numeric",
  });
}

export function todayISO() {
  const now = new Date();
  const local = new Date(now.getTime() - now.getTimezoneOffset() * 60000);
  return local.toISOString().slice(0, 10);
}
