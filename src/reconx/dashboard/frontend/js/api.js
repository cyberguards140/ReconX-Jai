async function loadDashboardData() {
    try {
        const res = await fetch('/api/project');
        const data = await res.json();
        
        const breadcrumbCurrent = document.querySelector('.breadcrumb .current');
        if (breadcrumbCurrent) {
            breadcrumbCurrent.textContent = data.project || 'None';
        }
        
        const statTarget = document.getElementById('statTarget');
        if (statTarget) statTarget.textContent = "Loaded from API";
        
        const statPorts = document.getElementById('statPorts');
        if (statPorts) statPorts.textContent = "0";
        
        const statServices = document.getElementById('statServices');
        if (statServices) statServices.textContent = "0";
        
        const statLastScan = document.getElementById('statLastScan');
        if (statLastScan) statLastScan.textContent = "-";
        
        const statDuration = document.getElementById('statDuration');
        if (statDuration) statDuration.textContent = "0s";
        
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
            const res = await fetch('/api/projects');
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
            const pname = prompt("New Project Name:");
            window.createProjectFromUI(pname, "");
        };
        newActions.appendChild(btn);
    }
});

window.createProjectFromUI = async function(name, desc) {
    if (!name) return;
    const res = await fetch('/api/project/create', {
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
    const res = await fetch('/api/project/switch', {
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
    const res = await fetch('/api/project/delete', {
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
