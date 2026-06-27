/* ═══════════ STATE ═══════════ */
window.isRunning = false;

/* ═══════════ TABS ═══════════ */
const categoryInfo = {
  'recon': { title: 'Recon & Info Gathering', desc: 'Discover live hosts, open ports, subdomains, and exposed services.' },
  'vuln': { title: 'Vulnerability Scanning', desc: 'Identify CVEs, misconfigurations, and known security flaws.' },
  'web': { title: 'Web Enumeration', desc: 'Fuzz directories, discover APIs, and analyze web applications.' },
  'cloud': { title: 'Cloud Assessment', desc: 'Audit AWS, Azure, GCP buckets, permissions, and IAM roles.' }
};

function switchTab(el, id) {
  document.querySelectorAll('.topnav-center .tab').forEach(t => t.classList.remove('active'));
  if (el) el.classList.add('active');
  
  if (categoryInfo[id]) {
    document.getElementById('panelTitle').textContent = categoryInfo[id].title;
    document.getElementById('panelDesc').textContent = categoryInfo[id].desc;
  }
  
  if (window.switchCategory) {
      window.switchCategory(id);
  }
}

function switchRTab(name, el) {
  ['terminal','findings','history'].forEach(v => {
    const view = document.getElementById('view-'+v);
    if(view) {
        view.style.display = 'none';
        view.classList.remove('visible');
    }
  });
  document.querySelectorAll('.rtab').forEach(t => t.classList.remove('active'));
  const view = document.getElementById('view-'+name);
  if (view) { 
      view.style.display = 'flex'; 
      if(view.classList.contains('findings-panel') || view.classList.contains('history-panel')) { 
          view.style.display='block'; 
          view.classList.add('visible'); 
      } 
  }
  if (el) el.classList.add('active');
}

/* ═══════════ MODALS ═══════════ */
function openModal(id) {
  const el = document.getElementById(id);
  if (el) el.classList.add('open');
}

function closeModal(id) {
  const el = document.getElementById(id);
  if (el) el.classList.remove('open');
}

document.querySelectorAll('.overlay').forEach(o => {
  o.addEventListener('click', e => { if(e.target===o) o.classList.remove('open'); });
});

window.confirmNew = function() {
    const name = document.getElementById('newProjectName')?.value;
    const target = document.getElementById('newProjectTarget')?.value;
    if (window.createProjectFromUI) {
        window.createProjectFromUI(name, "Target: " + target);
    }
};

window.confirmDelete = function() {
    const pname = prompt("Type the exact project name to confirm deletion:");
    if (window.deleteProjectFromUI) {
        window.deleteProjectFromUI(pname);
    }
};

/* ═══════════ RUN TOOLS ═══════════ */
async function runAllTools() {
    const runBtn = document.getElementById('runBtn');
    const runBtnTxt = document.getElementById('runBtnTxt');
    const runIcon = document.querySelector('.run-icon');
    
    if (window.isRunning) {
        // Stop logic
        try {
            await fetch('/api/v1/scans/pipeline/stop', { method: 'POST' });
            toast("Pipeline stopped", "red");
        } catch (e) {
            toast("Failed to stop pipeline", "red");
        }
        window.isRunning = false;
        if(runBtnTxt) runBtnTxt.textContent = "Run All Tools";
        if(runIcon) runIcon.textContent = "▶";
        if(runBtn) runBtn.classList.remove('running');
        return;
    }
    
    window.isRunning = true;
    if(runBtnTxt) runBtnTxt.textContent = "Stop All Tools";
    if(runIcon) runIcon.textContent = "■";
    if(runBtn) runBtn.classList.add('running');
    
    switchRTab('terminal', document.getElementById('tab-terminal'));
    const termBody = document.getElementById('termBody');
    if (termBody) termBody.innerHTML = '';
    
    // Connect to actual backend API
    const target = document.getElementById('targetScope')?.value;
    const wordlist = document.getElementById('wordlistScope')?.value;
    const apiKey = document.getElementById('apiKeyScope')?.value;
    
    if (!target) {
        toast("Missing Target Scope", "red");
        window.isRunning = false;
        if(runBtnTxt) runBtnTxt.textContent = "Run All Tools";
        if(runIcon) runIcon.textContent = "▶";
        if(runBtn) runBtn.classList.remove('running');
        return;
    }
    
    let api_keys_dict = null;
    if (apiKey) {
        api_keys_dict = {"default": apiKey};
    }
    
    try {
        const res = await fetch('/api/v1/scans/pipeline/start', {
            method: 'POST',
            headers: {'Content-Type': 'application/json'},
            body: JSON.stringify({
                target: target,
                wordlist: wordlist,
                api_keys: api_keys_dict
            })
        });
        const data = await res.json();
        toast(data.message || "Pipeline started", "blue");
    } catch (e) {
        toast("Failed to start scan", "red");
        window.isRunning = false;
        if(runBtnTxt) runBtnTxt.textContent = "Run All Tools";
        if(runIcon) runIcon.textContent = "▶";
        if(runBtn) runBtn.classList.remove('running');
    }
}

/* ═══════════ TERMINAL UI ═══════════ */
function copyLog() {
  const text = document.getElementById('termBody')?.innerText || "";
  navigator.clipboard.writeText(text).then(()=>toast('Log copied to clipboard','blue')).catch(()=>{});
}

function renderLog(lines) {
  const b = document.getElementById('termBody');
  if(!b) return;
  b.innerHTML += lines.map(l => `<span class="tline ${l.c}">${l.h || '&nbsp;'}</span>\n`).join('');
  b.scrollTop = b.scrollHeight;
}

/* ═══════════ TOAST ═══════════ */
function toast(msg, color='green') {
  const t = document.getElementById('toast');
  const d = document.getElementById('toastDot');
  const m = document.getElementById('toastMsg');
  if(!t || !d || !m) return;
  const colors = {green:'var(--green)', blue:'var(--blue)', red:'var(--red)', amber:'var(--amber)'};
  d.style.background = colors[color]||'var(--green)';
  m.textContent = msg;
  t.classList.add('show');
  setTimeout(()=>t.classList.remove('show'), 3000);
}

document.addEventListener("DOMContentLoaded", () => {
    // init tabs
    switchRTab('terminal', document.getElementById('tab-terminal'));
});
