import axios from 'axios';

const API_URL = process.env.REACT_APP_API_URL || 'http://localhost:8000/api/v1';

// Configuration globale d'axios
axios.defaults.baseURL = API_URL;
axios.defaults.headers.common['Accept'] = 'application/json';

const getModels = async () => {
    try {
        console.log('Fetching models...');
        const response = await axios.get(`${API_URL}/models/`);
        console.log('Models response:', response.data);
        return response.data.models;
    } catch (error) {
        console.error('Error fetching models:', error);
        console.error('Error details:', error.response?.data);
        throw new Error('Impossible de récupérer la liste des modèles');
    }
};

const getScaleTypes = async () => {
    try {
        console.log('Fetching scale types...');
        const response = await axios.get(`${API_URL}/scale-types/`);
        console.log('Scale types response:', response.data);
        return response.data.scale_types;
    } catch (error) {
        console.error('Error fetching scale types:', error);
        console.error('Error details:', error.response?.data);
        throw new Error('Impossible de récupérer les types d\'échelle');
    }
};

const getMcapFunctions = async () => {
    try {
        console.log('Fetching MCAP functions...');
        const response = await axios.get(`${API_URL}/mcap-functions/`);
        console.log('MCAP functions response:', response.data);
        return response.data.mcap_functions;
    } catch (error) {
        console.error('Error fetching MCAP functions:', error);
        console.error('Error details:', error.response?.data);
        throw new Error('Impossible de récupérer les fonctions MCAP');
    }
};

const processMcap = async (formData) => {
    try {
        console.log('Sending request to:', `${API_URL}/process-mcap/`);
        const response = await axios.post(`${API_URL}/process-mcap/`, formData, {
            headers: {
                'Content-Type': 'multipart/form-data'
            }
        });
        console.log('Process MCAP response:', response.data);
        return response.data;
    } catch (error) {
        console.error('Error in processMcap:', error);
        console.error('Error details:', error.response?.data);
        throw error.response?.data || error.message;
    }
};

export default {
    getModels,
    getScaleTypes,
    getMcapFunctions,
    processMcap
};