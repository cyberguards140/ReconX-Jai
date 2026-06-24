class PreviewBuilder {
    static getSelections() {
        const selections = {};
        if (!window.currentSchema) return selections;
        
        window.currentSchema.forEach(arg => {
            const flag = arg.flag;
            if (arg.type === 'toggle') {
                const el = document.querySelector(`button.toggle[data-flag="${flag}"]`);
                if (el && el.classList.contains('on')) selections[flag] = true;
            } else if (arg.type === 'multiselect') {
                const els = document.querySelectorAll(`input[type="checkbox"][data-flag="${flag}"]:checked`);
                const vals = Array.from(els).map(e => e.value);
                if (vals.length > 0) selections[flag] = vals;
            } else {
                const el = document.querySelector(`input[data-flag="${flag}"], select[data-flag="${flag}"]`);
                if (el && el.value) selections[flag] = el.value;
            }
        });
        return selections;
    }

    static updatePreview() {
        const target = document.getElementById('targetScope') ? document.getElementById('targetScope').value : '';
        const selections = this.getSelections();
        const binary = window.currentToolId || 'tool';
        
        let cmd = [binary];
        if (window.currentSchema) {
            window.currentSchema.forEach(arg => {
                const flag = arg.flag;
                if (selections[flag]) {
                    const val = selections[flag];
                    if (arg.type === 'toggle') {
                        cmd.push(flag);
                    } else if (arg.type === 'multiselect') {
                        cmd.push(`${flag} ${val.join(',')}`);
                    } else {
                        if (!flag.startsWith('-')) {
                            cmd.push(val);
                        } else {
                            cmd.push(`${flag} ${val}`);
                        }
                    }
                }
            });
        }
        
        if (target) {
            cmd.push(target);
        }
        
        const previewEl = document.getElementById(`${binary}Preview`) || document.getElementById('commandPreview');
        if (previewEl) {
            previewEl.textContent = cmd.join(' ');
        }
    }
}
