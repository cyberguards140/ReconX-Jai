let ws;

function connectWebSocket() {
    const wsUrl = `ws://${window.location.host}/api/v1/ws/live`;
    ws = new WebSocket(wsUrl);

    ws.onopen = () => {
        console.log("WebSocket Connected");
        const termBody = document.getElementById('termBody');
        if (termBody) {
            termBody.innerHTML += `<span class="tline ti">ReconX Backend WebSocket Connected.</span><br/>`;
            termBody.scrollTop = termBody.scrollHeight;
        }
    };

    ws.onmessage = (event) => {
        try {
            const data = JSON.parse(event.data);
            const termBody = document.getElementById('termBody');
            
            if (data.type === "terminal_output" && termBody) {
                // Add [tool_id] tag if it's stdout/stderr
                let cssClass = data.output_type === 'stderr' ? 'te' : 'tval';
                let content = data.content.replace(/</g, "&lt;").replace(/>/g, "&gt;");
                termBody.innerHTML += `<span class="${cssClass}">[${data.tool_id}] ${content}</span><br/>`;
                termBody.scrollTop = termBody.scrollHeight;
            } else if (data.type === "job_status") {
                const badge = document.getElementById(`${data.tool_id}Badge`);
                if (badge) {
                    badge.textContent = data.status;
                    badge.style.display = 'inline-block';
                    if (data.status === 'running') badge.className = 'badge b-run';
                    else if (data.status === 'completed') badge.className = 'badge b-done';
                    else if (data.status === 'failed') badge.className = 'badge b-err';
                    else badge.className = 'badge';
                }
                
                // Toast Notifications
                if (window.toast) {
                    if (data.status === 'completed' && data.tool_id !== 'all') {
                        window.toast(`Task ${data.tool_id} completed`, "green");
                    } else if (data.status === 'failed') {
                        window.toast(`Task ${data.tool_id} failed!`, "red");
                    } else if (data.status === 'stopped') {
                        window.toast(`Task ${data.tool_id === 'all' ? 'Pipeline' : data.tool_id} stopped`, "amber");
                    } else if (data.status === 'paused') {
                        window.toast(`Task ${data.tool_id === 'all' ? 'Pipeline' : data.tool_id} paused`, "amber");
                    }
                }
                
                // Pipeline global state reset
                if (data.tool_id === 'all' && (data.status === 'stopped' || data.status === 'completed' || data.status === 'failed')) {
                    if (window.isRunning !== undefined) {
                        window.isRunning = false;
                        const runBtn = document.getElementById('runBtn');
                        const runBtnTxt = document.getElementById('runBtnTxt');
                        const runIcon = document.querySelector('.run-icon');
                        if (runBtnTxt) runBtnTxt.textContent = "Run All Tools";
                        if (runIcon) runIcon.textContent = "▶";
                        if (runBtn) runBtn.classList.remove('running');
                    }
                }
            } else if (data.type === "new_asset") {
                // Instantly update dashboard counters based on new asset discovery
                if (data.asset_type === "subdomain" || data.asset_type === "domain") {
                    const el = document.getElementById("statTarget");
                    if(el) {
                        let c = parseInt(el.textContent) || 0;
                        el.textContent = c + 1;
                    }
                } else if (data.asset_type === "port") {
                    const el = document.getElementById("statPorts");
                    if(el) {
                        let c = parseInt(el.textContent) || 0;
                        el.textContent = c + 1;
                    }
                } else if (data.asset_type === "service") {
                    const el = document.getElementById("statServices");
                    if(el) {
                        let c = parseInt(el.textContent) || 0;
                        el.textContent = c + 1;
                    }
                }
            } else if (data.type === "new_finding") {
                const el = document.getElementById("findingsCount");
                if (el) {
                    let c = parseInt(el.textContent) || 0;
                    el.textContent = c + 1;
                }
                // Optional: Append a finding card to #view-findings
            } else if (data.type === "new_web_asset") {
                // If there were a counter for web assets we would increment it here
                console.log("New Web Asset:", data);
            } else if (data.type === "new_secret" || data.type === "new_technology") {
                console.log("Web Application Intelligence:", data);
            } else if (data.type === "new_cloud_asset") {
                console.log("Cloud Asset Discovered:", data);
            } else if (data.type === "public_exposure") {
                console.warn("Public Cloud Exposure Detected:", data);
            } else if (data.type === "campaign_started" || data.type === "campaign_completed") {
                console.log("Campaign Event:", data);
            } else if (data.type === "alert_generated") {
                console.warn(`[ALERT] ${data.severity}: ${data.message}`);
                // Update a notification bell in a real dashboard here
            } else if (data.type === "job_queued") {
                console.log("Job Queued:", data);
            } else if (data.type === "new_asset" || data.type === "risk_changed" || data.type === "relationship_created" || data.type === "timeline_event") {
                console.log("Intelligence Event:", data);
            } else if (data.type === "screenshot_captured" || data.type === "screenshot_processed") {
                console.log("Visual Recon Event:", data);
            } else if (data.type === "new_cve_correlated" || data.type === "ioc_match_found" || data.type === "exposure_detected") {
                console.log("Threat Intelligence Event:", data);
            } else if (data.type === "user_logged_in" || data.type === "role_changed" || data.type === "approval_requested") {
                console.log("Enterprise Auth Event:", data);
            } else if (data.type === "plugin_installed" || data.type === "plugin_enabled") {
                console.log("Plugin Extension Event:", data);
            } else if (data.type === "node_registered" || data.type === "health_alert" || data.type === "job_assigned") {
                console.log("Distributed Cluster Event:", data);
            } else if (data.type === "snapshot_created" || data.type === "trend_updated" || data.type === "kpi_updated" || data.type === "forecast_generated" || data.type === "exposure_changed" || data.type === "risk_updated") {
                console.log("Analytics Data Event:", data);
            } else if (data.type === "entity_created" || data.type === "relationship_added" || data.type === "attack_path_updated" || data.type === "investigation_created" || data.type === "cluster_updated") {
                console.log("Knowledge Graph Event:", data);
            } else if (data.type === "exposure_created" || data.type === "risk_updated" || data.type === "owner_assigned" || data.type === "remediation_started" || data.type === "exposure_closed" || data.type === "posture_updated") {
                console.log("Continuous Exposure Management Event:", data);
            } else if (data.type === "campaign_created" || data.type === "task_assigned" || data.type === "milestone_completed" || data.type === "evidence_uploaded" || data.type === "campaign_closed" || data.type === "scope_updated") {
                console.log("Campaign Management Event:", data);
            } else if (data.type === "case_created" || data.type === "case_assigned" || data.type === "evidence_added" || data.type === "review_submitted" || data.type === "case_closed" || data.type === "artifact_generated") {
                console.log("Case Management Event:", data);
            } else {
                console.log("WS Message:", data);
            }
        } catch(e) {
            console.log("WS Raw Message:", event.data);
        }
    };

    ws.onclose = () => {
        console.log("WebSocket Disconnected. Reconnecting in 3s...");
        setTimeout(connectWebSocket, 3000);
    };
    
    ws.onerror = (err) => {
        console.error("WebSocket Error:", err);
    };
}

document.addEventListener("DOMContentLoaded", connectWebSocket);
