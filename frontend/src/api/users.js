import client from './client';

export const listUsers = async () => {
  const response = await client.get('/users');
  return response.data;
};

export const deleteUser = async (userId) => {
  await client.delete(`/users/${userId}`);
};

export const createUser = async (userData) => {
  const response = await client.post('/users/create', userData);
  return response.data;
};

export const updateUser = async (userId, userData) => {
  const response = await client.put(`/users/update/${userId}`, userData);
  return response.data;
}
