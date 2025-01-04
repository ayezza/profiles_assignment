import axios from 'axios';

const API_URL = 'http://localhost:8000';

export const processMatrices = async (data) => {
  const response = await axios.post(`${API_URL}/process`, data);
  return response.data;
}; 