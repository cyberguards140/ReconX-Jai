class FormGenerator {
    static async generateForm(toolId, containerId) {
        const container = document.getElementById(containerId);
        if (!container) return;
        
        container.innerHTML = '<div style="padding:16px;color:var(--muted)">Loading...</div>';
        
        const schema = await SchemaLoader.loadToolArguments(toolId);
        const args = schema.arguments || [];
        
        if (args.length === 0) {
            container.innerHTML = '<div style="padding:16px;color:var(--muted)">No configuration available for this tool.</div>';
            return;
        }

        let html = '<div class="dynamic-form" style="padding:8px 0;">';
        for (const arg of args) {
            html += FieldRenderer.renderField(arg);
        }
        html += '</div>';
        
        container.innerHTML = html;
        window.currentToolId = toolId;
        window.currentSchema = args;
        
        // Initial preview build
        PreviewBuilder.updatePreview();
    }
}
