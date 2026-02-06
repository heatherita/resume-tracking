import client from './client';

export const listJobs = async () => {
  const response = await client.get('/jobs/');
  return response.data;
};

export const createJob = async (payload) => {
  const response = await client.post('/jobs/', payload);
  return response.data;
};

export const updateJob = async (jobId, payload) => {
  const response = await client.put(`/jobs/${jobId}`, payload);
  return response.data;
};

export const deleteJob = async (jobId) => {
  const response = await client.delete(`/jobs/${jobId}`);
  return response.data;
};
