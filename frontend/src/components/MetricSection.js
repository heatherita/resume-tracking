import React, { useEffect, useState } from 'react';
import { createMetric, deleteMetric, listMetricsForArtifact, updateMetric } from '../api/metrics';
import { formatDateTime } from './dateUtils';

const FONT_OPTIONS = [
  { value: '', label: 'None' },
  { value: '12pt', label: '12pt' },
  { value: '10pt', label: '10pt' },
];

const initialForm = {
  artifact_id: '',
  name: '',
  notes: '',
  active: true,
  ai_generated: false,
  bullet_points: false,
  artifact_format_details: '',
  font_size: '',
};

function MetricSection() {
  const [metrics, setMetrics] = useState([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');
  const [formData, setFormData] = useState(initialForm);
  const [editingId, setEditingId] = useState(null);
  const [filterArtifactId, setFilterArtifactId] = useState('');

  const fetchMetrics = async (artifactId) => {
    if (!artifactId) {
      setMetrics([]);
      return;
    }
    setLoading(true);
    setError('');
    try {
      const data = await listMetricsForArtifact(artifactId);
      setMetrics(data);
    } catch (err) {
      setError('Failed to load metrics.');
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchMetrics(filterArtifactId);
  }, [filterArtifactId]);

  const handleChange = (event) => {
    const { name, value, type, checked } = event.target;
    setFormData((prev) => ({
      ...prev,
      [name]: type === 'checkbox' ? checked : value,
    }));
  };

  const resetForm = () => {
    setEditingId(null);
    setFormData(initialForm);
  };

  const handleEdit = (metric) => {
    setEditingId(metric.id);
    setFormData({
      artifact_id: metric.artifact_id,
      name: metric.name || '',
      notes: metric.notes || '',
      active: Boolean(metric.active),
      ai_generated: Boolean(metric.ai_generated),
      bullet_points: Boolean(metric.bullet_points),
      artifact_format_details: metric.artifact_format_details || '',
      font_size: metric.font_size || '',
    });
  };

  const handleSubmit = async (event) => {
    event.preventDefault();
    setError('');
    const artifactId = Number(formData.artifact_id);
    if (!artifactId) {
      setError('Artifact ID is required.');
      return;
    }
    const payload = {
      name: formData.name,
      notes: formData.notes || null,
      active: Boolean(formData.active),
      ai_generated: Boolean(formData.ai_generated),
      bullet_points: formData.bullet_points === '' ? null : Boolean(formData.bullet_points),
      artifact_format_details: formData.artifact_format_details || null,
      font_size: formData.font_size || null,
    };

    try {
      if (editingId) {
        const updated = await updateMetric(editingId, payload);
        setMetrics((prev) => prev.map((metric) => (metric.id === editingId ? updated : metric)));
      } else {
        const created = await createMetric(artifactId, payload);
        setMetrics((prev) => [...prev, created]);
      }
      setFilterArtifactId(String(artifactId));
      resetForm();
    } catch (err) {
      setError('Failed to save metric.');
      console.error(err);
    }
  };

  const handleDelete = async (metricId) => {
    setError('');
    try {
      await deleteMetric(metricId);
      setMetrics((prev) => prev.filter((metric) => metric.id !== metricId));
    } catch (err) {
      setError('Failed to delete metric.');
      console.error(err);
    }
  };

  return (
    <section className="section">
      <div className="section-header">
        <h2>Artifact Metrics</h2>
        <div className="filter">
          <label>
            Artifact ID
            <input
              type="number"
              min="1"
              value={filterArtifactId}
              onChange={(event) => setFilterArtifactId(event.target.value)}
              placeholder="Filter by artifact"
            />
          </label>
        </div>
      </div>
      {error && <p className="error">{error}</p>}
      <div className="section-grid">
        <form className="card" onSubmit={handleSubmit}>
          <h3>{editingId ? 'Edit Metric' : 'Create Metric'}</h3>
          <label>
            Artifact ID
            <input
              type="number"
              name="artifact_id"
              value={formData.artifact_id}
              onChange={handleChange}
              min="1"
              required
            />
          </label>
          <label>
            Name
            <input name="name" value={formData.name} onChange={handleChange} required />
          </label>
          <label>
            Notes
            <textarea name="notes" value={formData.notes} onChange={handleChange} rows="2" />
          </label>
          <label className="checkbox">
            <input type="checkbox" name="active" checked={formData.active} onChange={handleChange} />
            Active
          </label>
          <label className="checkbox">
            <input
              type="checkbox"
              name="ai_generated"
              checked={formData.ai_generated}
              onChange={handleChange}
            />
            AI Generated
          </label>
          <label className="checkbox">
            <input
              type="checkbox"
              name="bullet_points"
              checked={formData.bullet_points}
              onChange={handleChange}
            />
            Bullet Points
          </label>
          <label>
            Format Details
            <input
              name="artifact_format_details"
              value={formData.artifact_format_details}
              onChange={handleChange}
            />
          </label>
          <label>
            Font Size
            <select name="font_size" value={formData.font_size} onChange={handleChange}>
              {FONT_OPTIONS.map((option) => (
                <option key={option.value} value={option.value}>
                  {option.label}
                </option>
              ))}
            </select>
          </label>
          <div className="form-actions">
            <button type="submit" className="primary">
              {editingId ? 'Update Metric' : 'Create Metric'}
            </button>
            {editingId && (
              <button type="button" className="ghost" onClick={resetForm}>
                Cancel
              </button>
            )}
          </div>
        </form>
        <div className="card">
          <h3>Metric List</h3>
          {loading ? (
            <p>Loading...</p>
          ) : metrics.length === 0 ? (
            <p className="muted">No metrics found for this artifact.</p>
          ) : (
            <table>
              <thead>
                <tr>
                  <th>ID</th>
                  <th>Name</th>
                  <th>Active</th>
                  <th>AI</th>
                  <th>Bullets</th>
                  <th>Font</th>
                  <th>Created</th>
                  <th>Actions</th>
                </tr>
              </thead>
              <tbody>
                {metrics.map((metric) => (
                  <tr key={metric.id}>
                    <td>{metric.id}</td>
                    <td>{metric.name}</td>
                    <td>{metric.active ? 'Yes' : 'No'}</td>
                    <td>{metric.ai_generated ? 'Yes' : 'No'}</td>
                    <td>{metric.bullet_points ? 'Yes' : 'No'}</td>
                    <td>{metric.font_size || '-'}</td>
                    <td>{formatDateTime(metric.created_at)}</td>
                    <td className="row-actions">
                      <button type="button" className="ghost" onClick={() => handleEdit(metric)}>
                        Edit
                      </button>
                      <button type="button" className="danger" onClick={() => handleDelete(metric.id)}>
                        Delete
                      </button>
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          )}
        </div>
      </div>
    </section>
  );
}

export default MetricSection;
