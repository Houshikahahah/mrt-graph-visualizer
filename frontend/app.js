// ---------- Animated background (particles + "code drift") ----------
const bg = document.getElementById("bg");
const ctx = bg.getContext("2d");
let W, H, DPR;

function resize() {
  DPR = Math.max(1, Math.min(2, window.devicePixelRatio || 1));
  W = window.innerWidth;
  H = window.innerHeight;
  bg.width = Math.floor(W * DPR);
  bg.height = Math.floor(H * DPR);
  bg.style.width = W + "px";
  bg.style.height = H + "px";
  ctx.setTransform(DPR, 0, 0, DPR, 0, 0);
}
window.addEventListener("resize", resize);
resize();

const particles = Array.from({ length: 80 }, () => ({
  x: Math.random() * W,
  y: Math.random() * H,
  r: 1 + Math.random() * 2,
  vx: (-0.2 + Math.random() * 0.4),
  vy: (0.1 + Math.random() * 0.35),
  a: 0.10 + Math.random() * 0.22
}));

const glyphs = "01<>/{}[]()=+-*";
const streams = Array.from({ length: 18 }, () => ({
  x: Math.random() * W,
  y: Math.random() * H,
  speed: 0.7 + Math.random() * 1.6,
  size: 12 + Math.random() * 10,
  alpha: 0.03 + Math.random() * 0.04
}));

function drawBG() {
  ctx.clearRect(0, 0, W, H);

  // subtle vignette
  const g = ctx.createRadialGradient(W * 0.5, H * 0.45, 80, W * 0.5, H * 0.5, Math.max(W, H));
  g.addColorStop(0, "rgba(43,110,246,0.10)");
  g.addColorStop(1, "rgba(245,247,251,0.95)");
  ctx.fillStyle = g;
  ctx.fillRect(0, 0, W, H);

  // particles
  for (const p of particles) {
    p.x += p.vx;
    p.y += p.vy;
    if (p.x < -20) p.x = W + 20;
    if (p.x > W + 20) p.x = -20;
    if (p.y > H + 30) p.y = -30;

    ctx.beginPath();
    ctx.fillStyle = `rgba(43,110,246,${p.a})`;
    ctx.arc(p.x, p.y, p.r, 0, Math.PI * 2);
    ctx.fill();
  }

  // code drift
  for (const s of streams) {
    s.y += s.speed;
    if (s.y > H + 40) {
      s.y = -40;
      s.x = Math.random() * W;
    }
    ctx.font = `${Math.floor(s.size)}px ui-monospace, SFMono-Regular, Menlo, Monaco, Consolas`;
    ctx.fillStyle = `rgba(43,110,246,${s.alpha})`;
    const text = Array.from({ length: 8 }, () => glyphs[Math.floor(Math.random() * glyphs.length)]).join("");
    ctx.fillText(text, s.x, s.y);
  }

  requestAnimationFrame(drawBG);
}
drawBG();

// ---------- Graph UI (vis-network) ----------
const output = document.getElementById("output");
const statNodes = document.getElementById("statNodes");
const statEdges = document.getElementById("statEdges");
const statPath = document.getElementById("statPath");
const statCost = document.getElementById("statCost");

const startSelect = document.getElementById("startSelect");
const endSelect = document.getElementById("endSelect");

const btnLoad = document.getElementById("btnLoad");
const fileInput = document.getElementById("fileInput");
const btnFit = document.getElementById("btnFit");
const btnReset = document.getElementById("btnReset");
const graphSelect = document.getElementById("graphSelect");

const btnBFS = document.getElementById("btnBFS");
const btnDFS = document.getElementById("btnDFS");
const btnGBFS = document.getElementById("btnGBFS");
const btnAStar = document.getElementById("btnAStar");

const searchBox = document.getElementById("searchBox");
const btnFocus = document.getElementById("btnFocus");
const btnClearPath = document.getElementById("btnClearPath");

let network = null;
let nodesDS = null;
let edgesDS = null;
let edgeWeightMap = null;
let stationById = null;
let crowdingPenaltyByCode = null;

let graphData = null; // { nodes: [...], edges: [...], adjacency: {...} }
const graphCache = new Map(); // path -> normalized graph data

const LINE_COLORS = {
  EW: "#3ddc84",
  NS: "#ff4d4d",
  CC: "#ffb020",
  DT: "#4da3ff",
  NE: "#b46bff",
  TE: "#c7a36c",
  CG: "#ffd166",
  CE: "#ff7cc8"
};
const TRAVEL_COST = 1;
const TRANSFER_COST = 4;

function log(msg) {
  output.textContent = msg + "\n" + output.textContent;
}

function setStats(n, e, pathLen = null, cost = null) {
  statNodes.textContent = String(n);
  statEdges.textContent = String(e);
  statPath.textContent = pathLen == null ? "-" : String(pathLen);
  statCost.textContent = formatCost(cost);
}

function formatCost(value) {
  if (value == null || !isFinite(value)) return "-";
  return Number.isInteger(value) ? String(value) : value.toFixed(2);
}

function buildEdgeWeightMap(edges, weights) {
  const map = new Map();
  const hasWeights = weights && typeof weights === "object" && Object.keys(weights).length > 0;
  if (weights && typeof weights === "object") {
    for (const [key, val] of Object.entries(weights)) {
      if (typeof val === "number" && isFinite(val)) map.set(key, val);
    }
  }
  for (const e of edges) {
    const raw = (e && (e.weight ?? e.w ?? e.cost));
    if (typeof raw !== "number" || !isFinite(raw)) continue;
    const w = raw;
    const key = `${e.from}->${e.to}`;
    if (!map.has(key)) map.set(key, w);
    if (!hasWeights) {
      const rev = `${e.to}->${e.from}`;
      if (!map.has(rev)) map.set(rev, w);
    }
  }
  return map;
}

function edgeWeight(a, b) {
  if (edgeWeightMap && edgeWeightMap.has(`${a}->${b}`)) {
    const w = edgeWeightMap.get(`${a}->${b}`);
    if (typeof w === "number" && isFinite(w)) return w;
  }
  const crowding = crowdingPenalty(a);
  const transfer = isTransfer(a, b);
  return TRAVEL_COST + (transfer ? TRANSFER_COST : 0) + crowding;
}

function buildStationIndex(nodes) {
  const map = new Map();
  for (const n of nodes) {
    map.set(n.id, { name: n.name, lines: new Set(n.lines || []) });
  }
  return map;
}

function buildCrowdingPenalty(nodes) {
  const nameToLines = new Map();
  for (const n of nodes) {
    if (!nameToLines.has(n.name)) nameToLines.set(n.name, new Set());
    const set = nameToLines.get(n.name);
    for (const l of (n.lines || [])) set.add(l);
  }
  const byCode = new Map();
  for (const n of nodes) {
    const lineCount = (nameToLines.get(n.name) || new Set()).size;
    let penalty = 0;
    if (lineCount === 2) penalty = 1;
    else if (lineCount >= 3) penalty = 2;
    byCode.set(n.id, penalty);
  }
  return byCode;
}

function crowdingPenalty(code) {
  if (!crowdingPenaltyByCode) return 0;
  return crowdingPenaltyByCode.get(code) || 0;
}

function isTransfer(a, b) {
  if (!stationById) return false;
  const sa = stationById.get(a);
  const sb = stationById.get(b);
  if (!sa || !sb) return false;
  if (sa.name !== sb.name) return false;
  for (const l of sa.lines) if (sb.lines.has(l)) return false;
  return true;
}

function stationColor(lines) {
  // pick first line as primary
  const primary = (lines && lines.length) ? lines[0] : null;
  return primary && LINE_COLORS[primary] ? LINE_COLORS[primary] : "#2b6ef6";
}

function buildNetwork(data) {
  if (network) {
    network.destroy();
    network = null;
  }
  const container = document.getElementById("graph");
  container.innerHTML = "";

  graphData = data;
  edgeWeightMap = buildEdgeWeightMap(data.edges || [], data.weights);
  stationById = buildStationIndex(data.nodes || []);
  crowdingPenaltyByCode = buildCrowdingPenalty(data.nodes || []);

  nodesDS = new vis.DataSet(
    data.nodes.map(n => ({
      id: n.id,
      label: `${n.id}\n${n.name}`,
      title: `${n.name} (${(n.lines || []).join(", ")})`,
      shape: "dot",
      size: 10,
      color: {
        background: stationColor(n.lines),
        border: "rgba(27,42,58,0.22)",
        highlight: { background: "#2b6ef6", border: "rgba(27,42,58,0.30)" }
      },
      font: { color: "rgba(27,42,58,0.92)", size: 12, face: "Manrope, ui-sans-serif" }
    }))
  );

  edgesDS = new vis.DataSet(
    data.edges.map(e => ({
      id: `${e.from}->${e.to}`,
      from: e.from,
      to: e.to,
      width: 1,
      color: { color: "rgba(27,42,58,0.18)", highlight: "rgba(43,110,246,0.75)" }
    }))
  );

  const options = {
    interaction: { hover: true, tooltipDelay: 80 },
    physics: {
      enabled: true,
      stabilization: { iterations: 260 },
      barnesHut: {
        gravitationalConstant: -9000,
        springLength: 110,
        springConstant: 0.025
      }
    },
    edges: { smooth: { type: "continuous" } }
  };

  network = new vis.Network(container, { nodes: nodesDS, edges: edgesDS }, options);

  network.on("click", (params) => {
    if (params.nodes.length) {
      const id = params.nodes[0];
      const node = data.nodes.find(n => n.id === id);
      log(`Clicked: ${id} | ${node?.name || ""} | lines: ${(node?.lines || []).join(", ")}`);
    }
  });

  populateSelects(data.nodes);
  setStats(data.nodes.length, data.edges.length);
  log(`Loaded graph: ${data.nodes.length} nodes, ${data.edges.length} edges`);
}

function populateSelects(nodes) {
  const opts = nodes
    .slice()
    .sort((a, b) => a.id.localeCompare(b.id))
    .map(n => `<option value="${n.id}">${n.id}” ${n.name}</option>`)
    .join("");

  startSelect.innerHTML = opts;
  endSelect.innerHTML = opts;

  // default example
  startSelect.value = nodes.find(n => n.id === "CG3")?.id || nodes[0].id;
  endSelect.value = nodes.find(n => n.id === "EW13")?.id || nodes[Math.min(10, nodes.length - 1)].id;
}

// ---------- Path highlighting ----------
function clearPathHighlight() {
  if (!edgesDS || !nodesDS) return;

  edgesDS.forEach(edge => {
    edgesDS.update({
      id: edge.id,
      width: 1,
      color: { color: "rgba(27,42,58,0.18)", highlight: "rgba(43,110,246,0.75)" }
    });
  });

  nodesDS.forEach(node => {
    nodesDS.update({
      id: node.id,
      size: 10,
      color: {
        background: stationColor(getNodeLines(node.id)),
        border: "rgba(27,42,58,0.22)",
        highlight: { background: "#2b6ef6", border: "rgba(27,42,58,0.40)" }
      }
    });
  });

  setStats(graphData.nodes.length, graphData.edges.length, null);
  log("Cleared path highlight.");
}

function getNodeLines(id) {
  return graphData.nodes.find(n => n.id === id)?.lines || [];
}

function highlightPath(path) {
  clearPathHighlight();
  if (!path || path.length < 2) {
    log("No path found.");
    setStats(graphData.nodes.length, graphData.edges.length, 0, 0);
    return;
  }

  // highlight nodes
  for (const id of path) {
    nodesDS.update({
      id,
      size: 14,
      color: {
        background: "#2b6ef6",
        border: "rgba(27,42,58,0.35)",
        highlight: { background: "#2b6ef6", border: "rgba(27,42,58,0.50)" }
      }
    });
  }

  // highlight edges along path
  for (let i = 0; i < path.length - 1; i++) {
    const a = path[i], b = path[i + 1];
    const id1 = `${a}->${b}`;
    const id2 = `${b}->${a}`;

    // your graph JSON may include both directions or only one; try both
    if (edgesDS.get(id1)) edgesDS.update({ id: id1, width: 5, color: { color: "rgba(43,110,246,0.90)" } });
    if (edgesDS.get(id2)) edgesDS.update({ id: id2, width: 5, color: { color: "rgba(43,110,246,0.90)" } });
  }

  const details = buildEdgeDetails(path);
  setStats(graphData.nodes.length, graphData.edges.length, path.length, details.totalCost);
  log(`${details.text}\nHighlighted path (${path.length} stations): ${path.join(" -> ")}`);

  // focus to path
  network.fit({ nodes: path, animation: { duration: 650, easingFunction: "easeInOutQuad" } });
}

function buildEdgeDetails(path) {
  if (!path || path.length < 2) {
    return { totalCost: 0, text: "No edges (start == end)." };
  }
  const lines = ["Detailed edge costs:"];
  let total = 0;
  for (let i = 0; i < path.length - 1; i++) {
    const a = path[i];
    const b = path[i + 1];
    const w = edgeWeight(a, b);
    const cp = crowdingPenalty(a);
    const transfer = isTransfer(a, b);
    lines.push(
      `${a} -> ${b}: cost=${formatCost(w)} (step=${TRAVEL_COST}`
      + `${transfer ? " + transfer=4" : ""}`
      + `${cp > 0 ? ` + crowding(${a})=${cp}` : ""})`
    );
    total += w;
  }
  lines.push(`Recomputed total cost: ${formatCost(total)}`);
  return { totalCost: total, text: lines.join("\n") };
}

// ---------- Simple algorithms (frontend-only demo) ----------
function bfsFrontend(adjacency, start, end) {
  const q = [start];
  const visited = new Set([start]);
  const parent = new Map([[start, null]]);

  while (q.length) {
    const cur = q.shift();
    if (cur === end) break;
    const nbrs = adjacency[cur] || [];
    for (const nxt of nbrs) {
      if (!visited.has(nxt)) {
        visited.add(nxt);
        parent.set(nxt, cur);
        q.push(nxt);
      }
    }
  }

  if (!parent.has(end)) return null;
  const path = [];
  for (let t = end; t != null; t = parent.get(t)) path.push(t);
  path.reverse();
  return path;
}

function dfsFrontend(adjacency, start, end) {
  const visited = new Set();
  const parent = new Map([[start, null]]);

  function dfs(cur) {
    visited.add(cur);
    if (cur === end) return true;
    const nbrs = adjacency[cur] || [];
    for (const nxt of nbrs) {
      if (!visited.has(nxt)) {
        parent.set(nxt, cur);
        if (dfs(nxt)) return true;
      }
    }
    return false;
  }

  dfs(start);
  if (!parent.has(end)) return null;
  const path = [];
  for (let t = end; t != null; t = parent.get(t)) path.push(t);
  path.reverse();
  return path;
}

// line heuristic used for GBFS + A* (front-end demo)
function buildLineHeuristic(nodes, goalId) {
  const goal = nodes.find(n => n.id === goalId);
  const goalLines = new Set(goal?.lines || []);

  const h = {};
  for (const n of nodes) {
    if (n.id === goalId) h[n.id] = 0;
    else {
      const lines = new Set(n.lines || []);
      let shares = false;
      for (const l of lines) if (goalLines.has(l)) { shares = true; break; }
      h[n.id] = shares ? 1 : 2;
    }
  }
  return h;
}

function gbfsFrontend(adjacency, nodes, start, end) {
  const h = buildLineHeuristic(nodes, end);
  const parent = new Map([[start, null]]);
  const visited = new Set();
  const pq = [{ id: start, p: h[start] }];

  function popMin() {
    pq.sort((a, b) => a.p - b.p);
    return pq.shift();
  }

  while (pq.length) {
    const cur = popMin().id;
    if (visited.has(cur)) continue;
    visited.add(cur);
    if (cur === end) break;

    for (const nxt of (adjacency[cur] || [])) {
      if (!visited.has(nxt)) {
        if (!parent.has(nxt)) parent.set(nxt, cur);
        pq.push({ id: nxt, p: h[nxt] });
      }
    }
  }

  if (!parent.has(end)) return null;
  const path = [];
  for (let t = end; t != null; t = parent.get(t)) path.push(t);
  path.reverse();
  return path;
}

// For now, frontend A* assumes each edge weight=1 (unweighted demo).
// Later you can send real weights from Python.
function astarFrontend(adjacency, nodes, start, end) {
  const h = buildLineHeuristic(nodes, end);
  const g = {};
  const parent = {};
  const visited = new Set();

  for (const n of nodes) { g[n.id] = Infinity; parent[n.id] = null; }
  g[start] = 0;

  const pq = [{ id: start, f: h[start] }];

  function popMin() {
    pq.sort((a, b) => a.f - b.f);
    return pq.shift();
  }

  while (pq.length) {
    const cur = popMin().id;
    if (visited.has(cur)) continue;
    visited.add(cur);
    if (cur === end) break;

    for (const nxt of (adjacency[cur] || [])) {
      const newG = g[cur] + 1;
      if (newG < g[nxt]) {
        g[nxt] = newG;
        parent[nxt] = cur;
        pq.push({ id: nxt, f: newG + h[nxt] });
      }
    }
  }

  if (!isFinite(g[end])) return null;
  const path = [];
  for (let t = end; t != null; t = parent[t]) path.push(t);
  path.reverse();
  return path;
}

// ---------- UI actions ----------
btnFit.addEventListener("click", () => {
  if (network) network.fit({ animation: { duration: 650 } });
});

btnReset.addEventListener("click", () => {
  if (!graphData) return;
  buildNetwork(graphData);
  output.textContent = "";
  log("Reset view.");
});

btnLoad.addEventListener("click", () => fileInput.click());
fileInput.addEventListener("change", async (e) => {
  const file = e.target.files?.[0];
  if (!file) return;
  const text = await file.text();
  const data = normalizeGraphJSON(JSON.parse(text));
  buildNetwork(data);
  cacheManualDataset(file.name, data);
});

if (graphSelect) {
  graphSelect.addEventListener("change", () => {
    const selected = graphSelect.value;
    const label = graphSelect.selectedOptions?.[0]?.textContent || selected;
    loadGraphFromPath(selected, label);
  });
}

btnClearPath.addEventListener("click", clearPathHighlight);

btnFocus.addEventListener("click", () => {
  const q = searchBox.value.trim().toLowerCase();
  if (!q || !graphData) return;

  const found = graphData.nodes.find(n =>
    n.id.toLowerCase() === q || n.name.toLowerCase().includes(q)
  );

  if (!found) {
    log(`Not found: ${searchBox.value}`);
    return;
  }

  network.focus(found.id, { scale: 1.4, animation: { duration: 650 } });
  nodesDS.update({ id: found.id, size: 18, color: { background: "#2b6ef6", border: "rgba(27,42,58,0.45)" } });
  log(`Focused: ${found.id}” ${found.name}`);
});

btnBFS.addEventListener("click", () => {
  if (!graphData) return;
  const start = startSelect.value;
  const end = endSelect.value;
  const path = bfsFrontend(graphData.adjacency, start, end);
  log(`[BFS] ${start} -> ${end}`);
  highlightPath(path);
});

btnDFS.addEventListener("click", () => {
  if (!graphData) return;
  const start = startSelect.value;
  const end = endSelect.value;
  const path = dfsFrontend(graphData.adjacency, start, end);
  log(`[DFS] ${start} -> ${end}`);
  highlightPath(path);
});

btnGBFS.addEventListener("click", () => {
  if (!graphData) return;
  const start = startSelect.value;
  const end = endSelect.value;
  const path = gbfsFrontend(graphData.adjacency, graphData.nodes, start, end);
  log(`[GBFS] ${start} -> ${end} (line-heuristic)`);
  highlightPath(path);
});

btnAStar.addEventListener("click", () => {
  if (!graphData) return;
  const start = startSelect.value;
  const end = endSelect.value;
  const path = astarFrontend(graphData.adjacency, graphData.nodes, start, end);
  log(`[A*] ${start} -> ${end} (demo weights=1)`);
  highlightPath(path);
});

// ---------- Load sample data on boot ----------
const defaultGraphPath = graphSelect?.value || "./data/graph.json";
loadGraphFromPath(defaultGraphPath, graphSelect?.selectedOptions?.[0]?.textContent || defaultGraphPath);

// Support slightly different JSON shapes
function normalizeGraphJSON(j) {
  // Expected:
  // { nodes:[{id,name,lines}], edges:[{from,to}], adjacency:{id:[...]}}
  // If adjacency missing, build from edges.
  const nodes = j.nodes || [];
  const edges = j.edges || [];
  const weights = j.weights || null;

  let adjacency = j.adjacency;
  if (!adjacency) {
    adjacency = {};
    for (const n of nodes) adjacency[n.id] = [];
    for (const e of edges) {
      if (!adjacency[e.from]) adjacency[e.from] = [];
      adjacency[e.from].push(e.to);
      if (!adjacency[e.to]) adjacency[e.to] = [];
      adjacency[e.to].push(e.from);
    }
  }

  return { nodes, edges, adjacency, weights };
}

async function loadGraphFromPath(path, label) {
  if (graphCache.has(path)) {
    const cached = graphCache.get(path);
    buildNetwork(cached);
    output.textContent = "";
    if (label) log(`Loaded dataset: ${label} (${cached.nodes.length} nodes, ${cached.edges.length} edges)`);
    return;
  }

  try {
    const res = await fetch(path, { cache: "no-store" });
    if (!res.ok) throw new Error("load failed");
    const data = normalizeGraphJSON(await res.json());
    graphCache.set(path, data);
    buildNetwork(data);
    output.textContent = "";
    if (label) log(`Loaded dataset: ${label} (${data.nodes.length} nodes, ${data.edges.length} edges)`);
  } catch (err) {
    output.textContent = "Could not load sample JSON. If you're opening index.html directly, "
      + "start a local server or use Load JSON once and I'll remember it.\n\n"
      + "Quick fix:\n"
      + "1) open terminal in frontend/\n"
      + "2) run: python -m http.server 5173\n"
      + "3) open: http://localhost:5173\n";
  }
}

function cacheManualDataset(filename, data) {
  const name = (filename || "").toLowerCase();
  let key = null;
  if (name.includes("future")) key = "data/graph_future.json";
  else if (name.includes("graph.json") || name.includes("today")) key = "data/graph.json";

  if (key) {
    graphCache.set(key, data);
    if (graphSelect) graphSelect.value = key;
  }
}


