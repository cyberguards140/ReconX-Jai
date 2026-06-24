class SchemaLoader {
    static async loadToolArguments(toolId) {
        try {
            const response = await fetch(`/api/tools/${toolId}/arguments`);
            return await response.json();
        } catch (error) {
            console.error('Error loading schema for', toolId, error);
            return { arguments: [] };
        }
    }
}
