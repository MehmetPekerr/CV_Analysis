const API_BASE = "http://localhost:8000/api/v1";

const dom = {
  dropZone:          document.getElementById("drop-zone"),
  fileInput:         document.getElementById("file-input"),
  btnBrowse:         document.getElementById("btn-browse"),
  fileListContainer: document.getElementById("file-list-container"),
  fileList:          document.getElementById("file-list"),
  btnClearFiles:     document.getElementById("btn-clear-files"),
  btnAnalyze:        document.getElementById("btn-analyze"),
  btnSpinner:        document.getElementById("btn-spinner"),
  btnIcon:           document.getElementById("btn-icon"),
  btnLabel:          document.getElementById("btn-label"),
  topNInput:         document.getElementById("top-n-input"),
  progressSection:   document.getElementById("analysis-progress"),
  progressBar:       document.getElementById("progress-bar"),
  progressPct:       document.getElementById("progress-pct"),
  steps:             {
    upload:  document.getElementById("step-upload"),
    extract: document.getElementById("step-extract"),
    llm:     document.getElementById("step-llm"),
    rank:    document.getElementById("step-rank"),
  },
  errorBanner:       document.getElementById("error-banner"),
  errorTitle:        document.getElementById("error-title"),
  errorDetail:       document.getElementById("error-detail"),
  resultsSection:    document.getElementById("results-section"),
  candidatesGrid:    document.getElementById("candidates-grid"),
  metaProcessed:     document.getElementById("meta-processed"),
  metaModel:         document.getElementById("meta-model"),
  resultsTopLabel:   document.getElementById("results-top-label"),
  ollamaStatusBadge: document.getElementById("ollama-status-badge"),
  statusText:        document.getElementById("status-text"),
  emptyState:        document.getElementById("empty-state"),
};

let selectedFiles = [];

async function checkOllamaStatus() {
  try {
    const res = await fetch(`${API_BASE}/health`);
    if (!res.ok) throw new Error();
    const data = await res.json();

    if (data.ollama_connected && data.available_models && data.available_models.length > 0) {
      dom.statusText.textContent = "Ollama Connected";
      dom.ollamaStatusBadge.style.background = "rgba(16, 217, 155, 0.08)";
      dom.ollamaStatusBadge.style.borderColor = "rgba(16, 217, 155, 0.2)";
      dom.ollamaStatusBadge.style.color = "var(--success)";
      const dot = dom.ollamaStatusBadge.querySelector(".pulse-dot");
      if (dot) dot.style.background = "var(--success)";

      dom.metaModel.textContent = (data.active_model || data.available_models[0]).split(":")[0];
    } else if (data.ollama_connected) {
      dom.statusText.textContent = "No Model Installed";
      dom.ollamaStatusBadge.style.background = "rgba(255,204,0,0.08)";
      dom.ollamaStatusBadge.style.borderColor = "rgba(255,204,0,0.24)";
      dom.ollamaStatusBadge.style.color = "var(--warning)";
      const dot = dom.ollamaStatusBadge.querySelector(".pulse-dot");
      if (dot) dot.style.background = "var(--warning)";
    } else {
      setOllamaOffline();
    }
  } catch {
    setOllamaOffline();
  }
}

function setOllamaOffline() {
  dom.statusText.textContent = "Ollama Offline";
  dom.ollamaStatusBadge.style.background = "rgba(255,90,112,0.08)";
  dom.ollamaStatusBadge.style.borderColor = "rgba(255,90,112,0.2)";
  dom.ollamaStatusBadge.style.color = "var(--error)";
  const dot = dom.ollamaStatusBadge.querySelector(".pulse-dot");
  if (dot) { dot.style.background = "var(--error)"; dot.style.animation = "none"; }
}

dom.btnBrowse.addEventListener("click", (e) => { e.stopPropagation(); dom.fileInput.click(); });
dom.dropZone.addEventListener("click", () => dom.fileInput.click());
dom.dropZone.addEventListener("keydown", (e) => { if (e.key === "Enter" || e.key === " ") dom.fileInput.click(); });

dom.fileInput.addEventListener("change", (e) => {
  addFiles(Array.from(e.target.files));
  e.target.value = "";
});

dom.dropZone.addEventListener("dragover", (e) => { e.preventDefault(); dom.dropZone.classList.add("drag-over"); });
dom.dropZone.addEventListener("dragleave", () => dom.dropZone.classList.remove("drag-over"));
dom.dropZone.addEventListener("drop", (e) => {
  e.preventDefault();
  dom.dropZone.classList.remove("drag-over");
  const files = Array.from(e.dataTransfer.files).filter(f => f.type === "application/pdf" || f.name.endsWith(".pdf"));
  addFiles(files);
});

function addFiles(newFiles) {
  const existing = new Set(selectedFiles.map(f => f.name + f.size));
  const filtered = newFiles.filter(f => {
    const isPdf = f.type === "application/pdf" || f.name.toLowerCase().endsWith(".pdf");
    return isPdf && !existing.has(f.name + f.size);
  });
  selectedFiles = [...selectedFiles, ...filtered];
  renderFileList();
}

function removeFile(index) {
  selectedFiles.splice(index, 1);
  renderFileList();
}

function renderFileList() {
  dom.fileList.innerHTML = "";
  if (selectedFiles.length === 0) {
    dom.fileListContainer.classList.remove("visible");
    dom.btnAnalyze.disabled = true;
    return;
  }

  dom.fileListContainer.classList.add("visible");
  dom.btnAnalyze.disabled = false;

  selectedFiles.forEach((file, idx) => {
    const item = document.createElement("div");
    item.className = "file-item";
    item.setAttribute("role", "listitem");
    item.innerHTML = `
      <span class="file-icon">
        <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round">
          <path d="M14 2H6a2 2 0 00-2 2v16a2 2 0 002 2h12a2 2 0 002-2V8z"/><polyline points="14 2 14 8 20 8"/>
        </svg>
      </span>
      <span class="file-name" title="${escHtml(file.name)}">${escHtml(file.name)}</span>
      <span class="file-size">${formatBytes(file.size)}</span>
      <button class="file-remove" aria-label="Remove ${escHtml(file.name)}" data-idx="${idx}">
        <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
          <line x1="18" y1="6" x2="6" y2="18"/><line x1="6" y1="6" x2="18" y2="18"/>
        </svg>
      </button>
    `;
    dom.fileList.appendChild(item);
  });

  dom.fileList.querySelectorAll(".file-remove").forEach(btn => {
    btn.addEventListener("click", () => removeFile(parseInt(btn.dataset.idx)));
  });
}

dom.btnClearFiles.addEventListener("click", () => {
  selectedFiles = [];
  renderFileList();
});

dom.btnAnalyze.addEventListener("click", runAnalysis);

async function runAnalysis() {
  if (selectedFiles.length === 0) return;

  hideError();
  hideResults();
  setLoading(true);
  showProgress(true);
  setStep("upload", "active");

  const formData = new FormData();
  selectedFiles.forEach(f => formData.append("files", f, f.name));

  const topN = parseInt(dom.topNInput.value) || 5;

  animateProgress(0, 20, 400);
  await sleep(400);
  setStep("upload", "done");
  setStep("extract", "active");
  animateProgress(20, 45, 600);

  let data;
  try {
    await sleep(300);
    setStep("extract", "done");
    setStep("llm", "active");
    animateProgress(45, 85, 1200);

    const res = await fetch(`${API_BASE}/analyze?top_n=${topN}`, {
      method: "POST",
      body: formData,
    });

    setStep("llm", "done");
    setStep("rank", "active");
    animateProgress(85, 100, 500);
    await sleep(500);
    setStep("rank", "done");

    if (!res.ok) {
      const errBody = await res.json().catch(() => ({ detail: "Unknown server error." }));
      const msg = errBody.detail?.message || errBody.detail || `HTTP ${res.status}`;
      const detail = Array.isArray(errBody.detail?.skipped)
        ? errBody.detail.skipped.join(" | ")
        : "";
      showError("Analysis Failed", msg, detail);
      return;
    }

    data = await res.json();
  } catch (err) {
    showError(
      "Connection Error",
      "Could not reach the backend API.",
      "Make sure the backend server is running on port 8000. " + (err.message || "")
    );
    return;
  } finally {
    setLoading(false);
    showProgress(false);
  }

  if (!data || !data.topCandidates || data.topCandidates.length === 0) {
    showError(
      "No Candidates Scored",
      "The backend processed the files but could not produce candidate scores.",
      "Check the selected Ollama model and try again."
    );
    dom.emptyState.classList.add("visible");
    dom.resultsSection.classList.remove("visible");
    return;
  }

  renderResults(data);
}

function renderResults(data) {
  dom.metaProcessed.textContent = data.processedCVCount ?? "—";
  dom.resultsTopLabel.textContent = `(${data.topCandidates.length})`;
  dom.candidatesGrid.innerHTML = "";
  dom.emptyState.classList.remove("visible");

  data.topCandidates.forEach(candidate => {
    const card = buildCandidateCard(candidate);
    dom.candidatesGrid.appendChild(card);
  });

  dom.resultsSection.classList.add("visible");
  dom.resultsSection.scrollIntoView({ behavior: "smooth", block: "start" });

  requestAnimationFrame(() => {
    dom.candidatesGrid.querySelectorAll(".bar-fill").forEach(bar => {
      const target = bar.dataset.score;
      setTimeout(() => { bar.style.width = target + "%"; }, 100);
    });
  });
}

function buildCandidateCard(candidate) {
  const { rank, candidateName, pdfFileName, detailedScores, averageScore, shortEvaluation } = candidate;

  const card = document.createElement("article");
  card.className = `candidate-card rank-${rank}`;
  card.setAttribute("aria-label", `Rank ${rank}: ${candidateName}`);

  const rankEmoji = rank === 1 ? "🥇" : rank === 2 ? "🥈" : rank === 3 ? "🥉" : rank;

  const criteria = [
    { key: "universityAndDepartment", label: "Education",    cls: "edu"    },
    { key: "foreignLanguages",        label: "Languages",    cls: "lang"   },
    { key: "projects",                label: "Projects",     cls: "proj"   },
    { key: "internships",             label: "Internships",  cls: "intern" },
    { key: "aiCompetency",            label: "AI Skills",    cls: "ai"     },
  ];

  const barsHTML = criteria.map(c => {
    const score = detailedScores[c.key] ?? 0;
    return `
      <div class="score-row">
        <span class="score-criterion">${c.label}</span>
        <div class="bar-track">
          <div class="bar-fill ${c.cls}" data-score="${score}" style="width:0%"></div>
        </div>
        <span class="bar-score">${score}</span>
      </div>
    `;
  }).join("");

  card.innerHTML = `
    <div class="card-rank-glow"></div>
    <div class="card-top">
      <div class="rank-badge">${rankEmoji}</div>
      <div class="card-info">
        <div class="candidate-name">${escHtml(candidateName)}</div>
        <div class="candidate-file">
          <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round">
            <path d="M14 2H6a2 2 0 00-2 2v16a2 2 0 002 2h12a2 2 0 002-2V8z"/>
            <polyline points="14 2 14 8 20 8"/>
          </svg>
          ${escHtml(pdfFileName)}
        </div>
      </div>
      <div class="card-score">
        <span class="score-value">${averageScore.toFixed(1)}</span>
        <div class="score-label">avg score</div>
      </div>
    </div>
    <div class="score-bars">${barsHTML}</div>
    ${shortEvaluation ? `<div class="card-evaluation">${escHtml(shortEvaluation)}</div>` : ""}
  `;

  return card;
}

function setLoading(isLoading) {
  dom.btnAnalyze.disabled = isLoading;
  dom.btnSpinner.style.display = isLoading ? "block" : "none";
  dom.btnIcon.style.display = isLoading ? "none" : "block";
  dom.btnLabel.textContent = isLoading ? "Analyzing..." : "Analyze CVs";
}

function showProgress(visible) {
  dom.progressSection.classList.toggle("visible", visible);
  if (visible) {
    Object.values(dom.steps).forEach(s => {
      s.classList.remove("active", "done");
    });
    dom.progressBar.style.width = "0%";
    dom.progressPct.textContent = "0%";
  } else {
    setTimeout(() => dom.progressSection.classList.remove("visible"), 400);
  }
}

function setStep(name, state) {
  const el = dom.steps[name];
  if (!el) return;
  el.classList.remove("active", "done");
  if (state) el.classList.add(state);
}

function animateProgress(from, to, durationMs) {
  const start = performance.now();
  const step = (now) => {
    const elapsed = now - start;
    const t = Math.min(elapsed / durationMs, 1);
    const eased = 1 - Math.pow(1 - t, 3);
    const value = Math.round(from + (to - from) * eased);
    dom.progressBar.style.width = value + "%";
    dom.progressPct.textContent = value + "%";
    if (t < 1) requestAnimationFrame(step);
  };
  requestAnimationFrame(step);
}

function showError(title, message, detail = "") {
  dom.errorTitle.textContent = title;
  dom.errorDetail.textContent = detail ? `${message} — ${detail}` : message;
  dom.errorBanner.classList.add("visible");
}

function hideError() {
  dom.errorBanner.classList.remove("visible");
}

function hideResults() {
  dom.resultsSection.classList.remove("visible");
  dom.emptyState.classList.remove("visible");
}

function formatBytes(bytes) {
  if (bytes < 1024) return bytes + " B";
  if (bytes < 1024 * 1024) return (bytes / 1024).toFixed(1) + " KB";
  return (bytes / (1024 * 1024)).toFixed(1) + " MB";
}

function escHtml(str) {
  if (!str) return "";
  return String(str)
    .replace(/&/g, "&amp;")
    .replace(/</g, "&lt;")
    .replace(/>/g, "&gt;")
    .replace(/"/g, "&quot;");
}

function sleep(ms) {
  return new Promise(r => setTimeout(r, ms));
}

checkOllamaStatus();
