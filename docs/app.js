// audio-ai-hub — frontend logic.
// Loads data.json (built by format_input.py), renders cards, supports search + category chips + sort.

const state = {
  all: [],
  query: "",
  activeCategories: new Set(),
  sort: "time-desc",
};

const $ = (sel) => document.querySelector(sel);
const $$ = (sel) => Array.from(document.querySelectorAll(sel));

async function boot() {
  try {
    const res = await fetch("data.json", { cache: "no-cache" });
    if (!res.ok) throw new Error(`Failed to fetch data.json (HTTP ${res.status})`);
    state.all = await res.json();
  } catch (err) {
    $("#grid").innerHTML = `<p class="empty-state">Could not load data.json (${err.message}). If you're viewing this locally, run <code>python3 format_input.py</code> first.</p>`;
    return;
  }
  renderHeroStats();
  renderCategoryFilter();
  bindControls();
  render();
}

function renderHeroStats() {
  const total = state.all.length;
  const cats = new Set(state.all.map((c) => c.Category)).size;
  const latest = state.all.map((c) => c.Time).sort().slice(-1)[0] || "—";
  $("#hero-stats").innerHTML = `
    <div class="stat"><strong>${total}</strong>entries</div>
    <div class="stat"><strong>${cats}</strong>categories</div>
    <div class="stat"><strong>${latest}</strong>latest</div>
  `;
}

function renderCategoryFilter() {
  const counts = state.all.reduce((acc, c) => {
    acc[c.Category] = (acc[c.Category] || 0) + 1;
    return acc;
  }, {});
  const order = [
    "Model and Methods",
    "Speech Recognition",
    "Speech Synthesis",
    "Audio Generation",
    "Benchmark",
    "Dataset Resource",
    "Multimodal",
    "Survey",
    "Study",
    "Safety",
    "Chatbot",
  ];
  const cats = order.filter((c) => counts[c]);
  $("#category-filter").innerHTML = cats
    .map(
      (c) =>
        `<button class="chip" type="button" data-category="${escape(c)}" aria-pressed="false">${escape(c)}<span class="count">${counts[c]}</span></button>`
    )
    .join("");
  $$("#category-filter .chip").forEach((el) => {
    el.addEventListener("click", () => {
      const cat = el.dataset.category;
      if (state.activeCategories.has(cat)) {
        state.activeCategories.delete(cat);
        el.setAttribute("aria-pressed", "false");
      } else {
        state.activeCategories.add(cat);
        el.setAttribute("aria-pressed", "true");
      }
      render();
    });
  });
}

function bindControls() {
  $("#search").addEventListener("input", (e) => {
    state.query = e.target.value.trim().toLowerCase();
    render();
  });
  $("#sort").addEventListener("change", (e) => {
    state.sort = e.target.value;
    render();
  });
}

function filtered() {
  const q = state.query;
  return state.all.filter((c) => {
    if (state.activeCategories.size && !state.activeCategories.has(c.Category)) return false;
    if (!q) return true;
    const hay = [
      c.Abbreviation,
      c.Title,
      c.Author,
      c.Affiliation,
      c.Type,
      c.Description,
    ]
      .filter(Boolean)
      .join(" ")
      .toLowerCase();
    return hay.includes(q);
  });
}

function sorted(rows) {
  const xs = rows.slice();
  if (state.sort === "time-asc") xs.sort((a, b) => a.Time.localeCompare(b.Time));
  else if (state.sort === "abbrev-asc") xs.sort((a, b) => a.Abbreviation.localeCompare(b.Abbreviation));
  else xs.sort((a, b) => b.Time.localeCompare(a.Time));
  return xs;
}

function render() {
  const rows = sorted(filtered());
  $("#result-count").textContent = `${rows.length} of ${state.all.length}`;
  if (!rows.length) {
    $("#grid").innerHTML = "";
    $("#empty-state").hidden = false;
    return;
  }
  $("#empty-state").hidden = true;
  $("#grid").innerHTML = rows.map(cardHTML).join("");
}

function cardHTML(c) {
  const links = [
    c.Paper_Link && link(c.Paper_Link, "Paper"),
    c.GitHub_Link && link(c.GitHub_Link, "Code"),
    c.HF_Link && link(c.HF_Link, "🤗 HF"),
    c.Demo_Link && link(c.Demo_Link, "Demo"),
    c.Other_Link && link(c.Other_Link, "Site"),
  ]
    .filter(Boolean)
    .join("");
  const tags = [
    c.Category && `<span class="tag tag-cat">${escape(c.Category)}</span>`,
    c.Type && c.Type !== c.Category && `<span class="tag">${escape(c.Type)}</span>`,
    c.Audio_Input === "Yes" && `<span class="tag">Audio In</span>`,
    c.Audio_Output === "Yes" && `<span class="tag">Audio Out</span>`,
    c.Language && c.Language !== "-" && `<span class="tag">${escape(c.Language)}</span>`,
  ]
    .filter(Boolean)
    .join("");
  return `<article class="card">
    <header class="card-head">
      <span class="card-abbrev">${escape(c.Abbreviation || "")}</span>
      <span class="card-time">${escape(c.Time || "")}</span>
    </header>
    <p class="card-title">${escape(c.Title || "")}</p>
    ${c.Affiliation ? `<p class="card-affil">${escape(c.Affiliation)}</p>` : ""}
    <div class="tags">${tags}</div>
    ${c.Description ? `<p class="card-desc">${escape(c.Description)}</p>` : ""}
    <footer class="card-links">${links}</footer>
  </article>`;
}

function link(href, label) {
  return `<a href="${escape(href)}" target="_blank" rel="noopener noreferrer">${escape(label)}</a>`;
}

function escape(s) {
  if (s == null) return "";
  return String(s)
    .replace(/&/g, "&amp;")
    .replace(/</g, "&lt;")
    .replace(/>/g, "&gt;")
    .replace(/"/g, "&quot;")
    .replace(/'/g, "&#39;");
}

boot();
