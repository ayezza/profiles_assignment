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
            
            // Log detailed response
            console.log('Raw axios response:', {
                status: response.status,
                statusText: response.statusText,
                headers: response.headers,
                data: response.data
            });

            if (!response.data || !response.data.data) {
                throw new Error('Invalid response format');
            }

            // Transform response data to match expected format
            const transformedResponse = {
                status: response.data.status,
                data: {
                    ...response.data.data,
                    ranking_matrix: this._ensureObject(response.data.data.ranking_matrix),
                    result_matrix: this._ensureObject(response.data.data.result_matrix)
                }
            };

            console.log('Transformed response:', transformedResponse);
            return transformedResponse;

        } catch (error) {
            console.error('MCAP service error:', error);
            throw error;
        }
    },

    _ensureObject(data) {
        if (!data) return {};
        return typeof data === 'string' ? JSON.parse(data) : data;
    }
};

export default mcapService;