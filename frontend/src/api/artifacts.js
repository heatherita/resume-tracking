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

export const listSections = async () => {
  const response = await client.get('/sections/');
  return response.data;
};

export const createSection = async (payload) => {
  const response = await client.post('/sections/', payload);
  return response.data;
};

export const updateSection = async (sectionId, payload) => {
  const response = await client.put(`/sections/${sectionId}`, payload);
  return response.data;
};

export const deleteSection = async (sectionId) => {
  const response = await client.delete(`/sections/${sectionId}`);
  return response.data;
};

export const listArtifactSections = async (artifactId) => {
  const response = await client.get(`/artifacts/${artifactId}/sections/`);
  return response.data;
};

export const createSectionForArtifact = async (artifactId, payload) => {
  const response = await client.post(`/artifacts/${artifactId}/sections/`, payload);
  return response.data;
};

export const attachSectionToArtifact = async (artifactId, sectionId) => {
  const response = await client.post(`/artifacts/${artifactId}/sections/${sectionId}`);
  return response.data;
};

export const detachSectionFromArtifact = async (artifactId, sectionId) => {
  const response = await client.delete(`/artifacts/${artifactId}/sections/${sectionId}`);
  return response.data;
};
