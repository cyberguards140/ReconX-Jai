class FieldRenderer {
    static renderToggle(arg) {
        return `
        <div class="toggle-row" id="field_${arg.flag}">
          <span class="toggle-lbl">${arg.name} (${arg.flag})</span>
          <button type="button" class="toggle ${arg.default ? 'on' : ''}" data-flag="${arg.flag}" onclick="this.classList.toggle('on'); PreviewBuilder.updatePreview();"></button>
        </div>`;
    }

    static renderText(arg) {
        return `
        <div class="form-group" id="field_${arg.flag}">
          <label class="form-label">${arg.name} ${arg.required ? '<span class="req">*</span>' : ''}</label>
          <input type="text" class="inp" data-flag="${arg.flag}" placeholder="${arg.default || ''}" value="${arg.default || ''}" oninput="PreviewBuilder.updatePreview()"/>
        </div>`;
    }
    
    static renderNumber(arg) {
        return `
        <div class="form-group" id="field_${arg.flag}">
          <label class="form-label">${arg.name} ${arg.required ? '<span class="req">*</span>' : ''}</label>
          <input type="number" class="inp" data-flag="${arg.flag}" value="${arg.default || ''}" oninput="PreviewBuilder.updatePreview()"/>
        </div>`;
    }

    static renderDropdown(arg) {
        const options = (arg.options || []).map(o => `<option value="${o}" ${o == arg.default ? 'selected' : ''}>${o}</option>`).join('');
        return `
        <div class="form-group" id="field_${arg.flag}">
          <label class="form-label">${arg.name} ${arg.required ? '<span class="req">*</span>' : ''}</label>
          <select class="inp" data-flag="${arg.flag}" onchange="PreviewBuilder.updatePreview()">
             ${options}
          </select>
        </div>`;
    }

    static renderMultiSelect(arg) {
        const options = (arg.options || []).map(o => `
            <label style="font-size:11px;color:var(--text);display:flex;align-items:center;gap:4px;">
                <input type="checkbox" data-flag="${arg.flag}" value="${o}" ${(arg.default||[]).includes(o) ? 'checked' : ''} onchange="PreviewBuilder.updatePreview()">
                ${o}
            </label>
        `).join('');
        return `
        <div class="form-group" id="field_${arg.flag}">
          <label class="form-label">${arg.name} ${arg.required ? '<span class="req">*</span>' : ''}</label>
          <div style="display:flex;flex-wrap:wrap;gap:8px;padding:4px 0;">${options}</div>
        </div>`;
    }

    static renderFile(arg) {
        return `
        <div class="form-group" id="field_${arg.flag}">
          <label class="form-label">${arg.name} ${arg.required ? '<span class="req">*</span>' : ''}</label>
          <div style="display:flex;gap:6px;">
              <input type="text" class="inp" data-flag="${arg.flag}" placeholder="Select file..." disabled style="flex:1"/>
              <button class="btn btn-ghost" type="button">Browse</button>
          </div>
        </div>`;
    }
    
    static renderAPIKey(arg) {
        return `
        <div class="form-group" id="field_${arg.flag}">
          <label class="form-label">${arg.name} ${arg.required ? '<span class="req">*</span>' : ''}</label>
          <input type="password" class="inp" data-flag="${arg.flag}" placeholder="sk-..." value="${arg.default || ''}" oninput="PreviewBuilder.updatePreview()"/>
        </div>`;
    }

    static renderField(arg) {
        switch (arg.type) {
            case 'toggle': return this.renderToggle(arg);
            case 'text': return this.renderText(arg);
            case 'number': return this.renderNumber(arg);
            case 'dropdown': return this.renderDropdown(arg);
            case 'multiselect': return this.renderMultiSelect(arg);
            case 'file': return this.renderFile(arg);
            case 'apikey': return this.renderAPIKey(arg);
            default: return this.renderText(arg);
        }
    }
}
