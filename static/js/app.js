// Fetch summary and expenses, then draw charts using Chart.js
async function fetchJson(path) {
  const r = await fetch(path, { credentials: 'same-origin' });
  if (!r.ok) throw new Error('Network error');
  return r.json();
}

function renderExpenseList(expenses) {
  const el = document.getElementById('expense-list');
  el.innerHTML = '';
  expenses.slice().reverse().forEach(e => {
    const li = document.createElement('li');
    li.className = 'list-group-item d-flex justify-content-between align-items-start';
    li.innerHTML = `<div><strong>${e.category}</strong> <div class="small text-muted">${e.date} - ${e.note || ''}</div></div><div class="d-flex gap-2 align-items-center"><div class="badge bg-secondary rounded-pill">${e.amount}</div><button class="btn btn-sm btn-danger" onclick="deleteExpense('${e.id}')">Remove</button></div>`;
    el.appendChild(li);
  });
}

async function deleteExpense(expenseId) {
  if (!confirm('Are you sure you want to remove this expense?')) return;
  try {
    const r = await fetch(`/remove/${expenseId}`, { method: 'POST', credentials: 'same-origin' });
    if (!r.ok) throw new Error('Failed to remove expense');
    init();
  } catch (err) {
    console.error('Failed to remove expense', err);
    alert('Failed to remove expense');
  }
}

function drawCategoryChart(ctx, data) {
  const labels = Object.keys(data);
  const values = labels.map(k => data[k]);
  return new Chart(ctx, {
    type: 'pie',
    data: { labels, datasets: [{ data: values, backgroundColor: labels.map((_,i)=>`hsl(${(i*47)%360} 70% 55%)`) }] },
    options: { plugins: { legend: { position: 'bottom' } } }
  });
}

function drawMonthChart(ctx, data) {
  const labels = Object.keys(data).sort();
  const values = labels.map(k => data[k]);
  return new Chart(ctx, {
    type: 'line',
    data: { labels, datasets: [{ label: 'Spending', data: values, borderColor: 'rgb(75, 192, 192)', tension: 0.3, fill: false }] },
    options: { scales: { y: { beginAtZero: true } } }
  });
}

function drawBudgetChart(ctx, budget, spent, remaining) {
  return new Chart(ctx, {
    type: 'doughnut',
    data: {
      labels: ['Spent', 'Remaining'],
      datasets: [{
        data: [spent, Math.max(0, remaining)],
        backgroundColor: ['rgb(255, 99, 132)', 'rgb(75, 192, 75)']
      }]
    },
    options: { plugins: { legend: { position: 'bottom' } } }
  });
}
function drawBudgetPie(ctx, budget, expensesForMonth) {
  // Build labels and values from individual expenses, then add Remaining slice
  const values = [];
  const labels = [];
  const colors = [];
  expensesForMonth.forEach((e, i) => {
    const amt = Number(e.amount) || 0;
    const label = (e.note && e.note.trim()) ? `${e.note}` : (e.category || 'Expense');
    labels.push(`${label}`);
    values.push(amt);
    colors.push(`hsl(${(i * 47) % 360} 70% 55%)`);
  });
  const spent = values.reduce((s, v) => s + v, 0);
  const remaining = Math.max(0, (Number(budget) || 0) - spent);
  if (remaining > 0) {
    labels.push('Remaining');
    values.push(remaining);
    colors.push('rgb(75, 192, 75)');
  }

  return new Chart(ctx, {
    type: 'pie',
    data: {
      labels,
      datasets: [{ data: values, backgroundColor: colors }]
    },
    options: { plugins: { legend: { position: 'bottom' } } }
  });
}

async function init() {
  try {
    const [summary, expenses, budgetResp] = await Promise.all([fetchJson('/api/summary'), fetchJson('/api/expenses'), fetchJson('/api/budget')]);
    renderExpenseList(expenses || []);
    const catCtx = document.getElementById('categoryChart').getContext('2d');
    const monCtx = document.getElementById('monthChart').getContext('2d');
    const budCtx = document.getElementById('budgetChart').getContext('2d');
    drawCategoryChart(catCtx, summary.by_category || {});
    drawMonthChart(monCtx, summary.by_month || {});

    const budget = Number(summary.monthly_budget ?? budgetResp.monthly_budget) || 0;
    const currentMonth = summary.current_month || new Date().toISOString().slice(0,7);

    // Filter expenses for the current month (YYYY-MM prefix)
    const expensesForMonth = (expenses || []).filter(e => e.date && e.date.startsWith(currentMonth)).map(e => ({
      id: e.id,
      amount: Number(e.amount) || 0,
      note: e.note || '',
      category: e.category || 'Other'
    }));

    drawBudgetPie(budCtx, budget, expensesForMonth);

    const spent = expensesForMonth.reduce((s, e) => s + e.amount, 0);
    const remaining = Math.max(0, budget - spent);
    updateBudgetDisplay(budget, spent, remaining, currentMonth);
    updateSavedDisplay(budget, expensesForMonth, spent, remaining);
    attachBudgetHandler();
  } catch (err) {
    console.error('Could not load data', err);
  }
}

function updateSavedDisplay(budget, expensesForMonth, spent, remaining) {
  const el = document.getElementById('saved-content');
  if (!el) return;
  const saved = Math.max(0, remaining);
  const percentSpent = budget > 0 ? ((spent / budget) * 100).toFixed(1) : 0;

  let itemsHtml = '';
  if (expensesForMonth.length === 0) {
    itemsHtml = '<div class="mb-2 text-muted">No expenses this month</div>';
  } else {
    itemsHtml = '<ul class="list-unstyled mb-2">' + expensesForMonth.map(e => `<li>${(e.note && e.note.trim())? e.note : e.category}: <span class=\"text-danger\">$${e.amount.toFixed(2)}</span></li>`).join('') + '</ul>';
  }

  el.innerHTML = `
    <div class="mb-2">
      <strong>Monthly Budget:</strong> $${budget.toFixed(2)}
    </div>
    ${itemsHtml}
    <div class="mb-2">
      <strong>Total Spent:</strong> <span class="text-danger">$${spent.toFixed(2)}</span> (${percentSpent}%)
    </div>
    <div class="mb-2">
      <strong>Saved Amount:</strong> <span class="text-success">$${saved.toFixed(2)}</span>
    </div>
  `;
}

function updateBudgetDisplay(budget, spent, remaining, month) {
  const el = document.getElementById('budget-display');
  if (!el) return;
  const m = month || new Date().toISOString().slice(0,7);
  el.innerHTML = `<div><strong>${m}</strong> — Budget: <span class="fw-bold">${budget.toFixed(2)}</span>, Spent: <span class="fw-bold text-danger">${spent.toFixed(2)}</span>, Remaining: <span class="fw-bold text-success">${remaining.toFixed(2)}</span></div>`;
}

function attachBudgetHandler(){
  const form = document.getElementById('budget-form');
  if (!form) return;
  const input = document.getElementById('budget-input');
  const btn = document.getElementById('budget-save');
  form.addEventListener('submit', async (e)=>{
    e.preventDefault();
    const val = parseFloat(input.value || 0);
    try{
      const r = await fetch('/api/budget', { method: 'POST', credentials: 'same-origin', headers: {'Content-Type':'application/json'}, body: JSON.stringify({amount: val}) });
      if (!r.ok) throw new Error('Could not save');
      const data = await r.json();
      // refresh summary to update display
      const summary = await fetchJson('/api/summary');
      updateBudgetDisplay(data.monthly_budget || 0, summary.spent_current_month || 0, summary.remaining || 0, summary.current_month);
      input.value = '';
    }catch(err){
      console.error('Failed to save budget', err);
      alert('Failed to save budget');
    }
  });
}

document.addEventListener('DOMContentLoaded', init);
