import client from './client';

export const listApplications = async () => {
  const response = await client.get('/applications/');
  return response.data;
};

export const createApplication = async (payload) => {
  const response = await client.post('/applications/', payload);
  return response.data;
};

export const updateApplication = async (applicationId, payload) => {
  const response = await client.put(`/applications/${applicationId}`, payload);
  return response.data;
};

export const deleteApplication = async (applicationId) => {
  const response = await client.delete(`/applications/${applicationId}`);
  return response.data;
};
