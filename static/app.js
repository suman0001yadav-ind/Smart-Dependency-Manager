const $ = (id) => document.getElementById(id);
let currentGraph = {};

function toast(message, error = false) {
  const el = $("toast");
  el.textContent = message;
  el.className = "toast show" + (error ? " error" : "");
  clearTimeout(toast.timer);
  toast.timer = setTimeout(() => el.className = "toast", 2800);
}
async function api(url, options = {}) {
  const response = await fetch(url, {
    headers: {"Content-Type": "application/json"},
    ...options
  });
  const data = await response.json();
  if (!response.ok) throw new Error(data.error || "Something went wrong.");
  return data;
}
function escapeHtml(value) {
  return String(value).replace(/[&<>"']/g, c => ({"&":"&amp;","<":"&lt;",">":"&gt;",'"':"&quot;","'":"&#39;"}[c]));
}
async function refresh() {
  const data = await api("/api/graph");
  currentGraph = data.graph || {};
  const tasks = Object.keys(currentGraph);
  const edges = Object.values(currentGraph).reduce((n, list) => n + list.length, 0);
  $("taskCount").textContent = tasks.length;
  $("dependencyCount").textContent = edges;
  $("taskListCount").textContent = `${tasks.length} TASKS`;
  $("taskList").innerHTML = tasks.length ? tasks.map(task => `
    <div class="task-row"><div><div class="task-name">${escapeHtml(task)}</div>
    <div class="task-meta">${currentGraph[task].length} dependent task(s)</div></div>
    <button class="delete-btn" data-delete="${escapeHtml(task)}">Remove</button></div>`).join("") :
    '<div class="empty">No tasks yet. Add your first task above.</div>';
  for (const id of ["prerequisite", "dependent"]) {
    const select = $(id), old = select.value;
    select.innerHTML = '<option value="">Select task</option>' + tasks.map(t => `<option value="${escapeHtml(t)}">${escapeHtml(t)}</option>`).join("");
    if (tasks.includes(old)) select.value = old;
  }
  const cycle = await api("/api/cycle");
  $("graphStatus").textContent = cycle.has_cycle ? "Cycle found" : "Valid DAG";
  $("graphStatus").style.color = cycle.has_cycle ? "#d65d65" : "#159b72";
  $("graphHint").textContent = cycle.has_cycle ? "Review task connections" : "No circular dependencies";
  renderGraph();
}
function renderGraph() {
  const tasks = Object.keys(currentGraph);
  const canvas = $("graphCanvas");
  if (!tasks.length) { canvas.innerHTML = '<div class="empty">Add tasks to see your graph.</div>'; return; }
  const width = Math.max(canvas.clientWidth, 350), height = 310;
  const indegree = Object.fromEntries(tasks.map(t => [t, 0]));
  tasks.forEach(t => (currentGraph[t] || []).forEach(d => { if (indegree[d] !== undefined) indegree[d]++; }));
  const level = {};
  const queue = tasks.filter(t => indegree[t] === 0);
  queue.forEach(t => level[t] = 0);
  for (let i = 0; i < queue.length; i++) {
    const t = queue[i];
    (currentGraph[t] || []).forEach(d => {
      level[d] = Math.max(level[d] ?? 0, level[t] + 1);
      indegree[d]--;
      if (indegree[d] === 0) queue.push(d);
    });
  }
  tasks.forEach(t => { if (level[t] === undefined) level[t] = 0; });
  const groups = {};
  tasks.forEach(t => (groups[level[t]] ||= []).push(t));
  const maxLevel = Math.max(...Object.keys(groups).map(Number), 0);
  const positions = {};
  Object.entries(groups).forEach(([lv, group]) => group.forEach((t, i) => {
    positions[t] = {x: 75 + Number(lv) * (width - 150) / Math.max(maxLevel, 1), y: (height / (group.length + 1)) * (i + 1)};
  }));
  let edges = "";
  tasks.forEach(t => (currentGraph[t] || []).forEach(d => {
    if (!positions[d]) return;
    const a = positions[t], b = positions[d];
    const x1 = a.x + 52, y1 = a.y, x2 = b.x - 52, y2 = b.y;
    edges += `<path class="graph-edge" marker-end="url(#arrow)" d="M${x1},${y1} C${(x1+x2)/2},${y1} ${(x1+x2)/2},${y2} ${x2},${y2}"/>`;
  }));
  let nodes = tasks.map(t => {
    const p = positions[t], label = t.length > 14 ? t.slice(0, 12) + "…" : t;
    return `<g class="graph-node"><rect x="${p.x-52}" y="${p.y-17}" width="104" height="34"/><text x="${p.x}" y="${p.y+4}" text-anchor="middle">${escapeHtml(label)}</text></g>`;
  }).join("");
  canvas.innerHTML = `<svg class="graph-svg" viewBox="0 0 ${width} ${height}" role="img" aria-label="Task dependency graph"><defs><marker id="arrow" markerWidth="7" markerHeight="7" refX="5" refY="3" orient="auto"><path d="M0 0 L6 3 L0 6" fill="none" stroke="#91a8cc"/></marker></defs>${edges}${nodes}</svg>`;
}
$("taskForm").addEventListener("submit", async e => {
  e.preventDefault();
  try { const data = await api("/api/tasks", {method:"POST", body:JSON.stringify({task:$("taskInput").value})}); $("taskInput").value=""; await refresh(); toast(data.message); }
  catch(err) { toast(err.message, true); }
});
$("dependencyForm").addEventListener("submit", async e => {
  e.preventDefault();
  try { const data = await api("/api/dependencies", {method:"POST", body:JSON.stringify({prerequisite:$("prerequisite").value, dependent:$("dependent").value})}); await refresh(); toast(data.message); }
  catch(err) { toast(err.message, true); }
});
$("taskList").addEventListener("click", async e => {
  const task = e.target.dataset.delete;
  if (!task) return;
  if (!confirm(`Remove "${task}" and its related dependencies?`)) return;
  try { const data = await api("/api/tasks/" + encodeURIComponent(task), {method:"DELETE"}); await refresh(); toast(data.message); }
  catch(err) { toast(err.message, true); }
});
async function runOrder(algo) {
  try {
    const data = await api("/api/order/" + algo);
    $("orderResult").innerHTML = `<b>${data.algorithm} execution order</b><div class="order-list">${data.order.map((t,i)=>`<span class="order-chip"><b>${i+1}.</b>${escapeHtml(t)}</span>`).join("")}</div>`;
  } catch(err) { $("orderResult").textContent = err.message; toast(err.message, true); }
}
$("runBfs").addEventListener("click", () => runOrder("bfs"));
$("runDfs").addEventListener("click", () => runOrder("dfs"));
$("checkCycle").addEventListener("click", async () => {
  try { const data = await api("/api/cycle"); toast(data.has_cycle ? "Circular dependency detected." : "No circular dependency detected."); }
  catch(err) { toast(err.message, true); }
});
$("runBenchmark").addEventListener("click", async () => {
  $("benchmarkResult").innerHTML = '<div class="empty">Running benchmark…</div>';
  try {
    const data = await api("/api/benchmark");
    const max = Math.max(...data.results.flatMap(r => [r.bfs, r.dfs]), 0.001);
    $("benchmarkResult").innerHTML = data.results.map(r => `
      <div class="bench-row"><b>${r.tasks}</b><div>BFS <span class="bench-value">${r.bfs} ms</span><div class="bar-wrap"><div class="bar" style="width:${Math.max(1,r.bfs/max*100)}%"></div></div></div>
      <div>DFS <span class="bench-value">${r.dfs} ms</span><div class="bar-wrap"><div class="bar dfs" style="width:${Math.max(1,r.dfs/max*100)}%"></div></div></div></div>`).join("");
  } catch(err) { $("benchmarkResult").textContent = err.message; }
});
window.addEventListener("resize", renderGraph);
refresh().catch(err => toast(err.message, true));
