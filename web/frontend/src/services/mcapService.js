import axios from 'axios';

const API_URL = 'http://localhost:8000/api/v1';

const mcapService = {
    async getModels() {
        const response = await fetch(`${API_URL}/models`);
        const data = await response.json();
        return data.models;
    },

    async getScaleTypes() {
        const response = await fetch(`${API_URL}/scale-types`);
        const data = await response.json();
        return data.scale_types;
    },

    async getMcapFunctions() {
        const response = await fetch(`${API_URL}/mcap-functions`);
        const data = await response.json();
        return data.mcap_functions;
    },

    async processMcap(formData) {
        try {
            const response = await axios.post(`${API_URL}/process-mcap`, formData, {
                headers: {
                    'Content-Type': 'multipart/form-data',
                },
            });

            if (response.status !== 200) {
                throw new Error('Server error: ' + response.statusText);
            }

            if (!response.data || !response.data.data) {
                throw new Error('Invalid response format');
            }

            return {
                status: 'success',
                data: response.data.data
            };

        } catch (error) {
            if (error.response?.data?.error) {
                // Server provided error message
                throw new Error(error.response.data.error);
            } else if (error.response?.status === 400) {
                // Scale type error handling
                throw new Error('Invalid scale type for input data. Try using "free" scale type.');
            } else {
                // Generic error
                throw new Error('Failed to process files: ' + error.message);
            }
        }
    },

    _ensureObject(data) {
        if (!data) return {};
        return typeof data === 'string' ? JSON.parse(data) : data;
    }
};

export default mcapService;