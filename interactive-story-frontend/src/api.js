import axios from 'axios';

const API_URL = 'http://127.0.0.1:5000';

const register = async (username, password) => {
  return await axios.post(
    `${API_URL}/register`,
    { username, password },
    { headers: { 'Content-Type': 'application/json' } }
  );
};


const login = async (username, password) => {
  const response = await axios.post(`${API_URL}/login`, { username, password });
  if (response.data.access_token) {
    localStorage.setItem('user', JSON.stringify(response.data));
  }
  return response.data;
};

const getCurrentUser = () => {
  return JSON.parse(localStorage.getItem('user'));
};

const api = {
  register,
  login,
  getCurrentUser,
};

export default api;

