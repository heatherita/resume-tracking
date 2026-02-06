import client from './client';

export const listArtifacts = async () => {
  const response = await client.get('/artifacts/');
  return response.data;
};

export const createArtifact = async (payload) => {
  const response = await client.post('/artifacts/', payload);
  return response.data;
};

export const updateArtifact = async (artifactId, payload) => {
  const response = await client.put(`/artifacts/${artifactId}`, payload);
  return response.data;
};

export const deleteArtifact = async (artifactId) => {
  const response = await client.delete(`/artifacts/${artifactId}`);
  return response.data;
};
