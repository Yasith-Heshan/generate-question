from fastapi import FastAPI, HTTPException
from fastapi.responses import HTMLResponse
from pydantic import BaseModel
import os
from pathlib import Path

app = FastAPI()

PROJECT_ROOT = Path(os.getenv("PROJECT_ROOT", "/project"))
SERVICES = ["backend", "frontend", "sympy"]


def get_env_path(service: str) -> Path:
    if service not in SERVICES:
        raise HTTPException(status_code=404, detail=f"Unknown service: {service}")
    return PROJECT_ROOT / service / ".env"


class EnvBody(BaseModel):
    content: str


@app.get("/api/services")
def list_services():
    return [{"name": s, "exists": (PROJECT_ROOT / s / ".env").exists()} for s in SERVICES]


@app.get("/api/env/{service}")
def get_env(service: str):
    path = get_env_path(service)
    return {"content": path.read_text() if path.exists() else ""}


@app.put("/api/env/{service}")
def save_env(service: str, body: EnvBody):
    path = get_env_path(service)
    path.write_text(body.content)
    return {"ok": True}


@app.get("/", response_class=HTMLResponse)
def index():
    return HTML


HTML = r"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <title>.env Manager</title>
  <style>
    *, *::before, *::after { box-sizing: border-box; margin: 0; padding: 0; }

    :root {
      --bg: #0d1117;
      --surface: #161b22;
      --surface2: #1c2128;
      --border: #30363d;
      --accent: #58a6ff;
      --text: #e6edf3;
      --muted: #8b949e;
      --danger: #f85149;
      --success: #3fb950;
      --warning: #d29922;
    }

    body {
      font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
      background: var(--bg);
      color: var(--text);
      min-height: 100vh;
      display: flex;
      flex-direction: column;
    }

    header {
      padding: 14px 24px;
      border-bottom: 1px solid var(--border);
      display: flex;
      align-items: center;
      gap: 10px;
    }
    header h1 { font-size: 15px; font-weight: 600; }
    .badge {
      background: var(--warning);
      color: #0d1117;
      font-size: 10px;
      font-weight: 700;
      padding: 2px 6px;
      border-radius: 4px;
      letter-spacing: 0.5px;
    }

    .tabs {
      display: flex;
      gap: 4px;
      padding: 12px 24px;
      border-bottom: 1px solid var(--border);
    }
    .tab-btn {
      display: flex;
      align-items: center;
      gap: 7px;
      padding: 6px 14px;
      border-radius: 6px;
      border: 1px solid transparent;
      background: transparent;
      color: var(--muted);
      font-size: 13px;
      font-weight: 500;
      cursor: pointer;
      font-family: 'SFMono-Regular', 'Cascadia Code', monospace;
      transition: all 0.12s;
    }
    .tab-btn:hover { background: var(--surface); color: var(--text); }
    .tab-btn.active { background: var(--surface); color: var(--accent); border-color: var(--border); }
    .dot { width: 7px; height: 7px; border-radius: 50%; flex-shrink: 0; }
    .dot.ok { background: var(--success); }
    .dot.missing { background: var(--danger); }

    main { flex: 1; padding: 24px; max-width: 860px; width: 100%; }

    .toolbar {
      display: flex;
      justify-content: space-between;
      align-items: center;
      margin-bottom: 16px;
    }
    .file-path { font-size: 12px; color: var(--muted); font-family: monospace; }

    .view-toggle {
      display: flex;
      background: var(--surface);
      border: 1px solid var(--border);
      border-radius: 6px;
      overflow: hidden;
    }
    .view-btn {
      padding: 5px 14px;
      font-size: 12px;
      border: none;
      background: transparent;
      color: var(--muted);
      cursor: pointer;
      font-weight: 500;
      transition: all 0.12s;
    }
    .view-btn.active { background: var(--accent); color: #0d1117; font-weight: 600; }

    .env-rows { width: 100%; display: flex; flex-direction: column; gap: 5px; }

    .env-row {
      display: flex;
      align-items: center;
      gap: 8px;
    }
    .env-row.is-comment { opacity: 0.55; }
    .env-row.is-empty { height: 8px; }

    .env-row input {
      background: var(--surface2);
      border: 1px solid var(--border);
      border-radius: 6px;
      color: var(--text);
      font-family: 'SFMono-Regular', 'Cascadia Code', 'Courier New', monospace;
      font-size: 13px;
      padding: 7px 10px;
      outline: none;
      transition: border-color 0.12s;
    }
    .env-row input:focus { border-color: var(--accent); }
    .key-input { flex: 0 0 36%; }
    .val-input { flex: 1; }

    .eq-sign { color: var(--muted); font-family: monospace; font-size: 15px; flex-shrink: 0; }
    .comment-text {
      color: var(--muted);
      font-family: monospace;
      font-size: 13px;
      flex: 1;
    }

    .del-btn {
      background: transparent;
      border: 1px solid transparent;
      color: var(--muted);
      border-radius: 4px;
      width: 28px;
      height: 28px;
      display: flex;
      align-items: center;
      justify-content: center;
      cursor: pointer;
      font-size: 18px;
      line-height: 1;
      flex-shrink: 0;
      transition: all 0.12s;
    }
    .del-btn:hover { color: var(--danger); border-color: var(--danger); background: rgba(248,81,73,0.1); }

    textarea.raw-editor {
      width: 100%;
      min-height: 420px;
      background: var(--surface);
      border: 1px solid var(--border);
      border-radius: 8px;
      color: var(--text);
      font-family: 'SFMono-Regular', 'Cascadia Code', 'Courier New', monospace;
      font-size: 13px;
      padding: 16px;
      outline: none;
      resize: vertical;
      line-height: 1.65;
    }
    textarea.raw-editor:focus { border-color: var(--accent); }

    .actions {
      display: flex;
      gap: 10px;
      margin-top: 16px;
      align-items: center;
    }
    .btn {
      padding: 8px 16px;
      border-radius: 6px;
      border: 1px solid;
      font-size: 13px;
      font-weight: 500;
      cursor: pointer;
      transition: all 0.12s;
    }
    .btn-add { background: transparent; border-color: var(--border); color: var(--text); }
    .btn-add:hover { border-color: var(--accent); color: var(--accent); }
    .btn-save { background: var(--success); border-color: var(--success); color: #0d1117; font-weight: 600; margin-left: auto; }
    .btn-save:hover { opacity: 0.85; }
    .btn-save:disabled { opacity: 0.45; cursor: not-allowed; }

    .empty-state { padding: 48px 0; text-align: center; color: var(--muted); font-size: 14px; }

    .toast {
      position: fixed;
      bottom: 24px;
      right: 24px;
      padding: 10px 16px;
      border-radius: 8px;
      font-size: 13px;
      font-weight: 500;
      opacity: 0;
      transform: translateY(8px);
      transition: opacity 0.2s, transform 0.2s;
      pointer-events: none;
      z-index: 999;
    }
    .toast.show { opacity: 1; transform: translateY(0); }
    .toast.success { background: var(--success); color: #0d1117; }
    .toast.error { background: var(--danger); color: #fff; }
  </style>
</head>
<body>
  <header>
    <h1>⚙ .env Manager</h1>
    <span class="badge">DEV TOOL</span>
  </header>

  <div class="tabs" id="tabs"></div>

  <main>
    <div class="toolbar">
      <span class="file-path" id="file-path"></span>
      <div class="view-toggle">
        <button class="view-btn active" id="btn-form" onclick="setView('form')">Form</button>
        <button class="view-btn" id="btn-raw" onclick="setView('raw')">Raw</button>
      </div>
    </div>

    <div id="form-view">
      <div class="env-rows" id="env-rows"></div>
    </div>

    <textarea class="raw-editor" id="raw-view" style="display:none" spellcheck="false"></textarea>

    <div class="actions">
      <button class="btn btn-add" id="btn-add" onclick="addRow()">+ Add Variable</button>
      <button class="btn btn-save" id="btn-save" onclick="save()">Save</button>
    </div>
  </main>

  <div class="toast" id="toast"></div>

  <script>
    let services = [];
    let currentService = null;
    let rows = [];
    let view = 'form';

    async function init() {
      const res = await fetch('/api/services');
      services = await res.json();
      renderTabs();
      if (services.length > 0) await loadService(services[0].name);
    }

    function renderTabs() {
      document.getElementById('tabs').innerHTML = services.map(s => `
        <button class="tab-btn ${s.name === currentService ? 'active' : ''}" onclick="loadService('${s.name}')">
          <span class="dot ${s.exists ? 'ok' : 'missing'}"></span>${s.name}
        </button>
      `).join('');
    }

    async function loadService(name) {
      currentService = name;
      renderTabs();
      document.getElementById('file-path').textContent = `${name}/.env`;
      const res = await fetch(`/api/env/${name}`);
      const data = await res.json();
      rows = parseEnv(data.content);
      render();
    }

    function parseEnv(text) {
      if (!text) return [];
      return text.split('\n').map(line => {
        const trimmed = line.trim();
        if (!trimmed) return { type: 'empty' };
        if (trimmed.startsWith('#')) return { type: 'comment', raw: line };
        const idx = line.indexOf('=');
        if (idx !== -1) return { type: 'var', key: line.substring(0, idx), value: line.substring(idx + 1) };
        return { type: 'comment', raw: line };
      });
    }

    function serializeRows(r) {
      return r.map(row => {
        if (row.type === 'var') return `${row.key}=${row.value}`;
        if (row.type === 'empty') return '';
        return row.raw || '';
      }).join('\n');
    }

    function render() {
      if (view === 'form') renderForm();
      else renderRaw();
    }

    function renderForm() {
      document.getElementById('form-view').style.display = '';
      document.getElementById('raw-view').style.display = 'none';
      document.getElementById('btn-add').style.display = '';

      const el = document.getElementById('env-rows');
      if (!rows.length) {
        el.innerHTML = '<div class="empty-state">No variables yet — click "+ Add Variable" to start.</div>';
        return;
      }

      el.innerHTML = rows.map((row, i) => {
        if (row.type === 'empty') {
          return `<div class="env-row is-empty" data-i="${i}"></div>`;
        }
        if (row.type === 'comment') {
          return `<div class="env-row is-comment" data-i="${i}">
            <span class="comment-text">${esc(row.raw)}</span>
            <button class="del-btn" onclick="deleteRow(${i})" title="Delete">×</button>
          </div>`;
        }
        return `<div class="env-row" data-i="${i}">
          <input class="key-input" type="text" value="${esc(row.key)}" placeholder="KEY" />
          <span class="eq-sign">=</span>
          <input class="val-input" type="text" value="${esc(row.value)}" placeholder="value" />
          <button class="del-btn" onclick="deleteRow(${i})" title="Delete">×</button>
        </div>`;
      }).join('');
    }

    function renderRaw() {
      document.getElementById('form-view').style.display = 'none';
      document.getElementById('btn-add').style.display = 'none';
      const ta = document.getElementById('raw-view');
      ta.style.display = '';
      ta.value = serializeRows(rows);
    }

    function setView(v) {
      if (v === view) return;
      if (view === 'form') collectFromDom();
      else rows = parseEnv(document.getElementById('raw-view').value);
      view = v;
      document.getElementById('btn-form').classList.toggle('active', v === 'form');
      document.getElementById('btn-raw').classList.toggle('active', v === 'raw');
      render();
    }

    function collectFromDom() {
      document.querySelectorAll('.env-row[data-i]').forEach(el => {
        const i = parseInt(el.dataset.i);
        if (!rows[i] || rows[i].type !== 'var') return;
        const inputs = el.querySelectorAll('input');
        if (inputs.length >= 2) {
          rows[i].key = inputs[0].value;
          rows[i].value = inputs[1].value;
        }
      });
    }

    function deleteRow(i) {
      collectFromDom();
      rows.splice(i, 1);
      renderForm();
    }

    function addRow() {
      collectFromDom();
      rows.push({ type: 'var', key: '', value: '' });
      renderForm();
      const last = document.querySelector('.env-rows .env-row:last-child .key-input');
      if (last) last.focus();
    }

    async function save() {
      const btn = document.getElementById('btn-save');
      btn.disabled = true;
      btn.textContent = 'Saving…';

      let content;
      if (view === 'form') {
        collectFromDom();
        content = serializeRows(rows);
      } else {
        content = document.getElementById('raw-view').value;
        rows = parseEnv(content);
      }

      try {
        const res = await fetch(`/api/env/${currentService}`, {
          method: 'PUT',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({ content }),
        });
        if (res.ok) {
          showToast('Saved ✓', 'success');
          const sr = await fetch('/api/services');
          services = await sr.json();
          renderTabs();
        } else {
          showToast('Save failed', 'error');
        }
      } catch (e) {
        showToast('Error: ' + e.message, 'error');
      }

      btn.disabled = false;
      btn.textContent = 'Save';
    }

    function showToast(msg, type) {
      const el = document.getElementById('toast');
      el.textContent = msg;
      el.className = `toast ${type} show`;
      setTimeout(() => el.classList.remove('show'), 3000);
    }

    function esc(s) {
      return String(s ?? '')
        .replace(/&/g, '&amp;')
        .replace(/</g, '&lt;')
        .replace(/>/g, '&gt;')
        .replace(/"/g, '&quot;');
    }

    init();
  </script>
</body>
</html>
"""
