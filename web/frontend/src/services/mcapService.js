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
            console.log('Sending MCAP request with parameters:', {
                model_name: formData.get('model_name'),
                scale_type: formData.get('scale_type'),
                mcap_function: formData.get('mcap_function')
            });
            
            const response = await axios.post(`${API_URL}/process-mcap`, formData, {
                headers: {
                    'Content-Type': 'multipart/form-data',
                },
            });
            
            console.log('MCAP response:', response.data);
            return response.data;
        } catch (error) {
            console.error('MCAP processing error:', error.response?.data || error.message);
            throw error;
        }
    }
};

export default mcapService;