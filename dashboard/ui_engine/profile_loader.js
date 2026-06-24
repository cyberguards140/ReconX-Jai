class ProfileLoader {
    static async loadProfiles(toolId) {
        try {
            const response = await fetch(`/api/tools/${toolId}/profiles`);
            return await response.json();
        } catch (error) {
            console.error('Error loading profiles', error);
            return [];
        }
    }
}
