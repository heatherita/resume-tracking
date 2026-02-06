export const toInputDateTime = (value) => {
  if (!value) return '';
  const date = new Date(value);
  const tzOffsetMs = date.getTimezoneOffset() * 60000;
  return new Date(date.getTime() - tzOffsetMs).toISOString().slice(0, 16);
};

export const toInputDate = (value) => {
  if (!value) return '';
  const date = new Date(value);
  const tzOffsetMs = date.getTimezoneOffset() * 60000;
  return new Date(date.getTime() - tzOffsetMs).toISOString().slice(0, 10);
};

export const formatDateTime = (value) => {
  if (!value) return '';
  return new Date(value).toLocaleString();
};

export const formatDate = (value) => {
  if (!value) return '';
  return new Date(value).toLocaleDateString();
};
