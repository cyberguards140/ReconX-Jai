class PresetLoader {
    static async loadPresets(toolId) {
        try {
            const response = await fetch(`/api/tools/${toolId}/presets`);
            return await response.json();
        } catch (error) {
            console.error('Error loading presets', error);
            return [];
        }
    }
    
    static applyPreset(preset) {
        const flags = preset.flags || {};
        for (const [flag, val] of Object.entries(flags)) {
            // Apply toggles
            const toggle = document.querySelector(`button.toggle[data-flag="${flag}"]`);
            if (toggle) {
                if (val) toggle.classList.add('on');
                else toggle.classList.remove('on');
                continue;
            }
            // Apply text/number/select
            const input = document.querySelector(`input[data-flag="${flag}"], select[data-flag="${flag}"]`);
            if (input) {
                input.value = val;
            }
        }
        PreviewBuilder.updatePreview();
    }
}
