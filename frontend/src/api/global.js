import client from './client';

export const listLabels = async () => {
  const response = await client.get('/labels/');
  return response.data;
};
