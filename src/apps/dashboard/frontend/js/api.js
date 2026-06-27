async function loadDashboardData() {
    try {
        const res = await fetch('/api/v1/projects/active');
        const data = await res.json();
        
        const breadcrumbCurrent = document.querySelector('.breadcrumb .current');
        if (breadcrumbCurrent) {
            breadcrumbCurrent.textContent = data.project || 'None';
        }
        
        const statTarget = document.getElementById('statTarget');
        if (statTarget) statTarget.textContent = data.project ? "Loaded from API" : "No Project";
        
        // Restore Config State
        if (data.config) {
            if (data.config.target && document.getElementById('targetScope')) {
                document.getElementById('targetScope').value = data.config.target;
            }
            if (data.config.threads && document.getElementById('threadsScope')) {
                document.getElementById('threadsScope').value = data.config.threads;
            }
            if (data.config.api_key && document.getElementById('apiKeyScope')) {
                document.getElementById('apiKeyScope').value = data.config.api_key;
            }
            if (data.config.wordlist && document.getElementById('wordlistScope')) {
                // Must wait for wordlists to load first
                setTimeout(() => document.getElementById('wordlistScope').value = data.config.wordlist, 500);
            }
        }
        
        // Load Findings
        const findingsRes = await fetch('/api/v1/findings/');
        const findings = await findingsRes.json();
        const findingsView = document.getElementById('view-findings');
        const findingsCount = document.getElementById('findingsCount');
        if (findingsView && findingsCount) {
            findingsCount.textContent = findings.length;
            findingsView.innerHTML = '';
            findings.forEach(f => {
                let badgeClass = 'fb-info';
                if(f.severity === 'critical') badgeClass = 'fb-open'; // Map critical to red
                if(f.severity === 'high') badgeClass = 'fb-open';
                if(f.severity === 'medium') badgeClass = 'fb-warn'; // Map medium to yellow
                findingsView.innerHTML += `
                <div class="finding-card ${badgeClass.replace('fb-', '')}">
                  <div class="finding-header">
                    <div>
                      <div class="finding-title">${f.title || 'Unknown'}</div>
                      <div class="finding-meta">${f.description || ''} · ${f.source_tool || 'System'}</div>
                    </div>
                    <span class="finding-badge ${badgeClass}">${f.severity ? f.severity.toUpperCase() : 'INFO'}</span>
                  </div>
                </div>`;
            });
        }
        
        // Load History
        const scansRes = await fetch('/api/v1/scans/');
        const scans = await scansRes.json();
        const historyView = document.getElementById('view-history');
        if (historyView) {
            historyView.innerHTML = '';
            scans.forEach(s => {
                const icon = s.status === 'completed' ? '✓' : (s.status === 'failed' ? '✗' : '▶');
                historyView.innerHTML += `
                <div class="h-row">
                  <div class="h-icon s">${icon}</div>
                  <div>
                    <div class="h-target">${s.target_id || 'Unknown Target'}</div>
                    <div class="h-detail">${s.scan_type || 'Workflow'} · Status: ${s.status || 'unknown'}</div>
                  </div>
                  <div class="h-time">${s.started_at ? s.started_at.split(' ')[0] : 'Today'}</div>
                </div>`;
            });
        }
        
        // Stats
        const statPorts = document.getElementById('statPorts');
        if (statPorts) statPorts.textContent = findings.filter(f => f.title && f.title.includes('Open')).length;
        
        const statServices = document.getElementById('statServices');
        if (statServices) statServices.textContent = findings.filter(f => f.title && f.title.includes('HTTP')).length;
        
        const statLastScan = document.getElementById('statLastScan');
        if (statLastScan && scans.length > 0) statLastScan.textContent = scans[scans.length-1].started_at || "-";
        
        const statDuration = document.getElementById('statDuration');
        if (statDuration) statDuration.textContent = scans.length > 0 ? "5s" : "0s";
        
        // Wordlists
        const wordlistRes = await fetch('/api/v1/wordlists/');
        const wordlists = await wordlistRes.json();
        const wordlistSelect = document.getElementById('wordlistScope');
        if (wordlistSelect && wordlistSelect.options.length <= 4) { // Only populate if not already populated
            wordlistSelect.innerHTML = '';
            wordlists.forEach(w => {
                const opt = document.createElement('option');
                opt.value = w.id;
                opt.textContent = `${w.name} (${w.size})`;
                wordlistSelect.appendChild(opt);
            });
        }
        
    } catch (err) {
        console.error("API Connection Error:", err);
    }
}

document.addEventListener("DOMContentLoaded", () => {
    loadDashboardData();
    
    // Inject dynamic buttons to modals to make them functional
    const deleteActions = document.querySelector('#deleteModal .modal-actions');
    if (deleteActions && !deleteActions.querySelector('.btn-danger')) {
        const btn = document.createElement('button');
        btn.className = 'btn btn-danger';
        btn.textContent = 'Confirm Delete';
        btn.onclick = () => {
            const pname = prompt("Type project name to delete:");
            window.deleteProjectFromUI(pname);
        };
        deleteActions.appendChild(btn);
    }
    
    const switchActions = document.querySelector('#switchModal .modal-actions');
    if (switchActions && !switchActions.querySelector('.btn-primary')) {
        const btn = document.createElement('button');
        btn.className = 'btn btn-primary';
        btn.textContent = 'Switch';
        btn.onclick = async () => {
            const res = await fetch('/api/v1/projects/');
            const projs = await res.json();
            const names = projs.map(p => p.name).join(', ');
            const pname = prompt("Available: " + (names || "None") + "\n\nType project to switch to:");
            window.switchProjectFromUI(pname);
        };
        switchActions.appendChild(btn);
    }

    const newActions = document.querySelector('#newModal .modal-actions');
    if (newActions && !newActions.querySelector('.btn-primary')) {
        const btn = document.createElement('button');
        btn.className = 'btn btn-primary';
        btn.textContent = 'Create';
        btn.onclick = () => {
            const pname = document.getElementById('newProjectName').value || prompt("New Project Name:");
            window.createProjectFromUI(pname, "");
        };
        newActions.appendChild(btn);
    }
});

window.createProjectFromUI = async function(name, desc) {
    if (!name) return;
    const res = await fetch('/api/v1/projects/create', {
        method: 'POST',
        headers: {'Content-Type': 'application/json'},
        body: JSON.stringify({name: name, description: desc || ""})
    });
    if(res.ok) {
        await window.switchProjectFromUI(name);
        closeModal('newModal');
    } else {
        alert("Creation failed or already exists");
    }
};

window.switchProjectFromUI = async function(name) {
    if (!name) return;
    const res = await fetch('/api/v1/projects/switch', {
        method: 'POST',
        headers: {'Content-Type': 'application/json'},
        body: JSON.stringify({name: name})
    });
    if(res.ok) {
        closeModal('switchModal');
        loadDashboardData();
    } else {
        alert("Switch failed: Project not found");
    }
};

window.deleteProjectFromUI = async function(name) {
    if (!name) return;
    const res = await fetch('/api/v1/projects/delete', {
        method: 'DELETE',
        headers: {'Content-Type': 'application/json'},
        body: JSON.stringify({name: name})
    });
    if(res.ok) {
        closeModal('deleteModal');
        loadDashboardData();
    } else {
        alert("Delete failed");
    }
};

window.saveConfigState = async function() {
    const config = {};
    const t = document.getElementById('targetScope');
    if (t) config.target = t.value;
    
    const w = document.getElementById('wordlistScope');
    if (w) config.wordlist = w.value;
    
    const th = document.getElementById('threadsScope');
    if (th) config.threads = parseInt(th.value) || 50;
    
    const k = document.getElementById('apiKeyScope');
    if (k) config.api_key = k.value;
    
    try {
        await fetch('/api/v1/projects/active/config', {
            method: 'POST',
            headers: {'Content-Type': 'application/json'},
            body: JSON.stringify({config: config})
        });
        
        // Also save keys to secure storage endpoint (Stage 17)
        if (config.api_key && !config.api_key.includes('*')) {
            await fetch('/api/v1/keys', {
                method: 'POST',
                headers: {'Content-Type': 'application/json'},
                body: JSON.stringify({keys: {"global": config.api_key}})
            });
        }
    } catch(e) {
        console.error("Failed to save config state:", e);
    }
};

document.addEventListener("DOMContentLoaded", () => {
    ['targetScope', 'wordlistScope', 'threadsScope', 'apiKeyScope'].forEach(id => {
        const el = document.getElementById(id);
        if (el) el.addEventListener('change', window.saveConfigState);
    });
});

