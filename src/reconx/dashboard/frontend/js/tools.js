let toolConfigs = {};
let activeTools = new Set();
let expandedTools = new Set();

async function renderDynamicTools() {
    const container = document.getElementById('dynamic-tools-container');
    if (!container) return;
    
    // Fetch tools list
    const res = await fetch('/api/tools');
    const tools = await res.json();
    
    // For MVP, we render just Nmap dynamically as per requirement to show proof of concept 
    // while keeping exact visual layout. We can filter by category later.
    const nmap = tools.find(t => t.id === 'nmap');
    if (!nmap) return;
    
    // Render Nmap
    if (!document.getElementById('tool-card-nmap')) {
        const card = await buildToolCard(nmap.id);
        container.appendChild(card);
    }
}

async function buildToolCard(toolId) {
    const res = await fetch(`/api/tools/${toolId}/schema`);
    const schema = await res.json();
    
    const cfgRes = await fetch(`/api/tools/${toolId}/config`);
    toolConfigs[toolId] = await cfgRes.json();
    
    const card = document.createElement('div');
    card.className = 'tool-card';
    card.id = `tool-card-${toolId}`;
    
    // Header
    const hdr = document.createElement('div');
    hdr.className = 'tool-hdr';
    hdr.onclick = () => toggleToolExpand(toolId);
    
    const nameSpan = document.createElement('span');
    nameSpan.className = 'tool-name';
    nameSpan.textContent = schema.name;
    
    const badge = document.createElement('span');
    badge.className = 'badge b-active';
    badge.id = `${toolId}Badge`;
    badge.style.display = 'none'; // Only show if active
    
    const runDiv = document.createElement('div');
    const runBtn = document.createElement('button');
    runBtn.className = 'icon-btn';
    runBtn.title = 'Run Tool';
    runBtn.textContent = '▶';
    runBtn.onclick = (e) => {
        e.stopPropagation();
        runToolJob(toolId);
    };
    
    const stopBtn = document.createElement('button');
    stopBtn.className = 'icon-btn';
    stopBtn.title = 'Stop Tool';
    stopBtn.textContent = '■';
    stopBtn.onclick = (e) => {
        e.stopPropagation();
        stopToolJob(toolId);
    };
    runDiv.appendChild(runBtn);
    runDiv.appendChild(stopBtn);
    
    const expandIcon = document.createElement('span');
    expandIcon.className = 'tool-expand-icon';
    expandIcon.innerHTML = ' ▼';
    
    hdr.appendChild(nameSpan);
    hdr.appendChild(badge);
    hdr.appendChild(runDiv);
    hdr.appendChild(expandIcon);
    
    const preview = document.createElement('div');
    preview.className = 'tool-desc';
    preview.id = `${toolId}Preview`;
    preview.textContent = "Loading command...";
    
    // Body (Expanded content)
    const body = document.createElement('div');
    body.className = 'tool-expanded';
    body.id = `${toolId}Expand`;
    body.style.display = 'none'; // Default collapsed
    
    const grid = document.createElement('div');
    grid.className = 'grid-2';
    
    // Profiles
    const profRes = await fetch(`/api/tools/${toolId}/profiles`);
    const profiles = await profRes.json();
    
    if (profiles.length > 0) {
        const pGrp = document.createElement('div');
        pGrp.className = 'inp-grp';
        const pLbl = document.createElement('label');
        pLbl.textContent = 'Profile Presets';
        const pSel = document.createElement('select');
        pSel.className = 'inp';
        pSel.innerHTML = `<option value="">-- Custom --</option>`;
        profiles.forEach(p => {
            pSel.innerHTML += `<option value="${p.name}">${p.name}</option>`;
        });
        pSel.onchange = (e) => applyProfile(toolId, profiles, e.target.value);
        pGrp.appendChild(pLbl);
        pGrp.appendChild(pSel);
        grid.appendChild(pGrp);
    }
    
    // Toggles container
    const togglesRow = document.createElement('div');
    togglesRow.className = 'opt-row';
    togglesRow.style.gridColumn = '1 / -1';
    
    schema.arguments.forEach(arg => {
        if (arg.type === 'toggle') {
            const lbl = document.createElement('label');
            lbl.className = 'cb-lbl';
            const cb = document.createElement('input');
            cb.type = 'checkbox';
            cb.checked = toolConfigs[toolId][arg.flag] === 'true' || toolConfigs[toolId][arg.flag] === true;
            cb.onchange = (e) => updateToolConfig(toolId, arg.flag, e.target.checked);
            lbl.appendChild(cb);
            lbl.appendChild(document.createTextNode(` ${arg.flag}`));
            togglesRow.appendChild(lbl);
        } else if (arg.type === 'textbox' || arg.type === 'number') {
            const grp = document.createElement('div');
            grp.className = 'inp-grp';
            const lbl = document.createElement('label');
            lbl.textContent = `Argument: ${arg.flag}`;
            const inp = document.createElement('input');
            inp.type = 'text';
            inp.className = 'inp';
            inp.value = toolConfigs[toolId][arg.flag] || '';
            inp.oninput = (e) => updateToolConfig(toolId, arg.flag, e.target.value);
            grp.appendChild(lbl);
            grp.appendChild(inp);
            grid.appendChild(grp);
        }
    });
    
    grid.appendChild(togglesRow);
    body.appendChild(grid);
    
    card.appendChild(hdr);
    card.appendChild(preview);
    card.appendChild(body);
    
    setTimeout(() => refreshCommand(toolId), 100);
    return card;
}

function toggleToolExpand(toolId) {
    const el = document.getElementById(`${toolId}Expand`);
    if(el.style.display === 'none') {
        el.style.display = 'block';
    } else {
        el.style.display = 'none';
    }
}

async function updateToolConfig(toolId, flag, val) {
    if(!toolConfigs[toolId]) toolConfigs[toolId] = {};
    toolConfigs[toolId][flag] = val;
    await refreshCommand(toolId);
    
    // Save state in background
    fetch(`/api/tools/${toolId}/config`, {
        method: 'POST',
        headers: {'Content-Type': 'application/json'},
        body: JSON.stringify(toolConfigs[toolId])
    });
}

function applyProfile(toolId, profiles, profileName) {
    if(!profileName) return;
    const prof = profiles.find(p => p.name === profileName);
    if(prof) {
        toolConfigs[toolId] = {...prof.config};
        // Re-render UI
        const container = document.getElementById('dynamic-tools-container');
        document.getElementById(`tool-card-${toolId}`).remove();
        buildToolCard(toolId).then(card => container.appendChild(card));
        
        // Save
        fetch(`/api/tools/${toolId}/config`, {
            method: 'POST',
            headers: {'Content-Type': 'application/json'},
            body: JSON.stringify(toolConfigs[toolId])
        });
    }
}

async function refreshCommand(toolId) {
    const target = document.getElementById('targetScope') ? document.getElementById('targetScope').value : '';
    const res = await fetch(`/api/tools/${toolId}/command`, {
        method: 'POST',
        headers: {'Content-Type': 'application/json'},
        body: JSON.stringify({target: target, config: toolConfigs[toolId]})
    });
    const data = await res.json();
    const preview = document.getElementById(`${toolId}Preview`);
    if (preview) {
        preview.textContent = data.command || 'Error generating command';
    }
}

async function runToolJob(toolId) {
    const target = document.getElementById('targetScope') ? document.getElementById('targetScope').value : '';
    const res = await fetch('/api/jobs/create', {
        method: 'POST',
        headers: {'Content-Type': 'application/json'},
        body: JSON.stringify({tool_id: toolId, target: target, config: toolConfigs[toolId]})
    });
    if (!res.ok) alert("Failed to queue job");
}

let activeJobs = {}; // Keep track for stopping

async function stopToolJob(toolId) {
    // For MVP, fetch running jobs, find matching tool, and stop it.
    const res = await fetch('/api/jobs/running');
    const running = await res.json();
    const job = running.find(j => j.tool_id === toolId);
    if(job) {
        await fetch(`/api/jobs/${job.id}/stop`, {method: 'POST'});
    } else {
        alert("No active job found for " + toolId);
    }
}

document.addEventListener("DOMContentLoaded", () => {
    renderDynamicTools();
    const targetScope = document.getElementById('targetScope');
    if(targetScope) {
        targetScope.addEventListener('input', () => {
            Object.keys(toolConfigs).forEach(id => refreshCommand(id));
        });
    }
});
