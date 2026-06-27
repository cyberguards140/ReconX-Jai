let toolConfigs = {};
let allTools = [];
let activeTools = new Set();
let expandedTools = new Set();
let currentCategory = 'recon'; // Default tab

async function renderDynamicTools() {
    const container = document.getElementById('dynamic-tools-container');
    if (!container) return;
    
    // Fetch tools list once
    if (allTools.length === 0) {
        const res = await fetch('/api/v1/tools/');
        allTools = await res.json();
    }
    
    // Clear container
    container.innerHTML = '';
    
    // Render tools matching current category
    for (const tool of allTools) {
        if (tool.category === currentCategory) {
            const card = await buildToolCard(tool.id);
            container.appendChild(card);
        }
    }
}

window.switchCategory = function(catId) {
    currentCategory = catId;
    renderDynamicTools();
};

window.runCategoryTools = function() {
    allTools.forEach(t => {
        if (t.enabled && t.category === currentCategory && window.runToolJob) {
            window.runToolJob(t.id);
        }
    });
};

async function buildToolCard(toolId) {
    const res = await fetch(`/api/v1/tools/${toolId}/schema`);
    const schema = await res.json();
    
    const cfgRes = await fetch(`/api/v1/tools/${toolId}/config`);
    toolConfigs[toolId] = await cfgRes.json();
    
    const card = document.createElement('div');
    card.className = 'tool-item active';
    card.id = `tool-card-${toolId}`;
    
    // Header
    const hdr = document.createElement('div');
    hdr.className = 'tool-row';
    hdr.onclick = () => toggleToolExpand(toolId);
    
    const nameRow = document.createElement('div');
    nameRow.className = 'tool-name-row';
    
    const nameSpan = document.createElement('span');
    nameSpan.className = 'tool-name';
    nameSpan.textContent = schema.name;
    
    const badge = document.createElement('span');
    badge.className = 'badge b-active';
    badge.id = `${toolId}Badge`;
    badge.textContent = 'active';
    
    nameRow.appendChild(nameSpan);
    nameRow.appendChild(badge);
    
    const actionsRow = document.createElement('div');
    actionsRow.className = 'tool-actions';
    
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
    
    const expandBtn = document.createElement('button');
    expandBtn.className = 'icon-btn';
    expandBtn.textContent = '›';
    expandBtn.onclick = (e) => {
        e.stopPropagation();
        toggleToolExpand(toolId);
    };
    
    actionsRow.appendChild(runBtn);
    actionsRow.appendChild(stopBtn);
    actionsRow.appendChild(expandBtn);
    
    hdr.appendChild(nameRow);
    hdr.appendChild(actionsRow);
    
    const preview = document.createElement('div');
    preview.className = 'tool-desc';
    preview.id = `${toolId}Preview`;
    preview.textContent = "Loading command...";
    
    card.appendChild(hdr);
    card.appendChild(preview);
    
    // Body (Expanded content)
    const body = document.createElement('div');
    body.className = 'tool-expanded';
    body.id = `${toolId}Expand`;
    body.style.display = 'none'; // Default collapsed
    
    // Profiles
    const profRes = await fetch(`/api/v1/tools/${toolId}/profiles`);
    const profiles = await profRes.json();
    
    if (profiles.length > 0) {
        const pRow = document.createElement('div');
        pRow.className = 'sub-row';
        const pGrp = document.createElement('div');
        pGrp.className = 'form-group';
        const pLbl = document.createElement('label');
        pLbl.className = 'form-label';
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
        pRow.appendChild(pGrp);
        body.appendChild(pRow);
    }
    
    let currentSubRow = null;
    let textArgCount = 0;
    
    schema.arguments.forEach(arg => {
        if (arg.type === 'textbox' || arg.type === 'number') {
            if (textArgCount % 2 === 0) {
                currentSubRow = document.createElement('div');
                currentSubRow.className = 'sub-row';
                body.appendChild(currentSubRow);
            }
            
            const grp = document.createElement('div');
            grp.className = 'form-group';
            const lbl = document.createElement('label');
            lbl.className = 'form-label';
            lbl.textContent = arg.flag;
            const inp = document.createElement('input');
            inp.type = arg.type === 'number' ? 'number' : 'text';
            inp.className = 'inp';
            inp.value = toolConfigs[toolId][arg.flag] || '';
            inp.oninput = (e) => updateToolConfig(toolId, arg.flag, e.target.value);
            grp.appendChild(lbl);
            grp.appendChild(inp);
            currentSubRow.appendChild(grp);
            
            textArgCount++;
        }
    });

    schema.arguments.forEach(arg => {
        if (arg.type === 'toggle') {
            const tRow = document.createElement('div');
            tRow.className = 'toggle-row';
            
            const tLbl = document.createElement('span');
            tLbl.className = 'toggle-lbl';
            tLbl.textContent = arg.flag;
            
            const tBtn = document.createElement('button');
            const isActive = toolConfigs[toolId][arg.flag] === 'true' || toolConfigs[toolId][arg.flag] === true;
            tBtn.className = 'toggle' + (isActive ? ' on' : '');
            tBtn.onclick = (e) => {
                const nowActive = !tBtn.classList.contains('on');
                if(nowActive) tBtn.classList.add('on');
                else tBtn.classList.remove('on');
                updateToolConfig(toolId, arg.flag, nowActive);
            };
            
            tRow.appendChild(tLbl);
            tRow.appendChild(tBtn);
            body.appendChild(tRow);
        }
    });

    const note = document.createElement('p');
    note.className = 'expand-note';
    note.textContent = 'These options override general settings for this tool only.';
    body.appendChild(note);

    const targetRow = document.createElement('div');
    targetRow.className = 'sub-row';
    const targetGrp = document.createElement('div');
    targetGrp.className = 'form-group';
    const targetLbl = document.createElement('label');
    targetLbl.className = 'form-label';
    targetLbl.textContent = 'Target for this tool (optional override)';
    const targetInp = document.createElement('input');
    targetInp.type = 'text';
    targetInp.className = 'inp';
    targetInp.id = `${toolId}TargetOverride`;
    targetInp.placeholder = 'host / CIDR / URL';
    targetInp.oninput = () => refreshCommand(toolId);
    targetGrp.appendChild(targetLbl);
    targetGrp.appendChild(targetInp);
    targetRow.appendChild(targetGrp);
    body.appendChild(targetRow);

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
    fetch(`/api/v1/tools/${toolId}/config`, {
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
        fetch(`/api/v1/tools/${toolId}/config`, {
            method: 'POST',
            headers: {'Content-Type': 'application/json'},
            body: JSON.stringify(toolConfigs[toolId])
        });
    }
}

async function refreshCommand(toolId) {
    const override = document.getElementById(`${toolId}TargetOverride`);
    const globalTarget = document.getElementById('targetScope') ? document.getElementById('targetScope').value : '';
    const target = (override && override.value) ? override.value : globalTarget;
    const res = await fetch(`/api/v1/tools/${toolId}/command`, {
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
    const override = document.getElementById(`${toolId}TargetOverride`);
    const globalTarget = document.getElementById('targetScope') ? document.getElementById('targetScope').value : '';
    const target = (override && override.value) ? override.value : globalTarget;
    const res = await fetch('/api/v1/jobs/create', {
        method: 'POST',
        headers: {'Content-Type': 'application/json'},
        body: JSON.stringify({tool_id: toolId, target: target, config: toolConfigs[toolId]})
    });
    if (!res.ok) alert("Failed to queue job");
}

let activeJobs = {}; // Keep track for stopping

async function stopToolJob(toolId) {
    // For MVP, fetch running jobs, find matching tool, and stop it.
    const res = await fetch('/api/v1/jobs/running');
    const running = await res.json();
    const job = running.find(j => j.tool_id === toolId);
    if(job) {
        await fetch(`/api/v1/jobs/${job.id}/stop`, {method: 'POST'});
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
