import client from './client';

export const listRoles = async () => {
  const response = await client.get('/roles/');
  return response.data;
};

export const createRole = async (payload) => {
  const response = await client.post('/roles/', payload);
  return response.data;
};

export const updateRole = async (roleId, payload) => {
  const response = await client.put(`/roles/${roleId}`, payload);
  return response.data;
};

export const deleteRole = async (roleId) => {
  const response = await client.delete(`/roles/${roleId}`);
  return response.data;
};
