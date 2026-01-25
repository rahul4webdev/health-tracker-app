import api from './api';

export const createFoodLog = async (foodData) => {
  const response = await api.post('/api/nutrition/food-log', foodData);
  return response.data;
};

export const getFoodLogs = async (params = {}) => {
  const response = await api.get('/api/nutrition/food-log', { params });
  return response.data;
};

export const getFoodLog = async (id) => {
  const response = await api.get(`/api/nutrition/food-log/${id}`);
  return response.data;
};

export const updateFoodLog = async (id, foodData) => {
  const response = await api.put(`/api/nutrition/food-log/${id}`, foodData);
  return response.data;
};

export const deleteFoodLog = async (id) => {
  await api.delete(`/api/nutrition/food-log/${id}`);
};

export const getDailySummary = async (date) => {
  const response = await api.get('/api/nutrition/daily-summary', {
    params: { date },
  });
  return response.data;
};
