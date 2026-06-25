class ValidationHandler {
    static validate() {
        const target = document.getElementById('targetScope');
        if (target && !target.value.trim()) {
            return { valid: false, message: "Target Scope is required" };
        }
        
        if (!window.currentSchema) return { valid: true };
        
        const selections = PreviewBuilder.getSelections();
        for (const arg of window.currentSchema) {
            if (arg.required && !selections[arg.flag]) {
                return { valid: false, message: `${arg.name} is required` };
            }
        }
        
        return { valid: true };
    }
}
