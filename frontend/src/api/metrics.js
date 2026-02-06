import client from './client';

export const listMetricsForArtifact = async (artifactId) => {
  const response = await client.get(`/artifacts/${artifactId}/metrics/`);
  return response.data;
};

export const createMetric = async (artifactId, payload) => {
  const response = await client.post(`/artifacts/${artifactId}/metrics/`, payload);
  return response.data;
};

export const updateMetric = async (metricId, payload) => {
  const response = await client.put(`/metrics/${metricId}`, payload);
  return response.data;
};

export const deleteMetric = async (metricId) => {
  const response = await client.delete(`/metrics/${metricId}`);
  return response.data;
};
