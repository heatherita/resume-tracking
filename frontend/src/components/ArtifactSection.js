import React, { useEffect, useState } from 'react';
import { createArtifact, deleteArtifact, listArtifacts, updateArtifact } from '../api/artifacts';
import { formatDateTime } from './dateUtils';

const TYPE_OPTIONS = [
  { value: 'resume', label: 'Resume' },
  { value: 'bullets', label: 'Bullets' },
  { value: 'cover_letter', label: 'Cover Letter' },
];

const initialForm = {
  type: 'resume',
  version_name: '',
  location: '',
  notes: '',
  active: true,
};

function ArtifactSection() {
  const [artifacts, setArtifacts] = useState([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');
  const [formData, setFormData] = useState(initialForm);
  const [editingId, setEditingId] = useState(null);

  const fetchArtifacts = async () => {
    setLoading(true);
    setError('');
    try {
      const data = await listArtifacts();
      setArtifacts(data);
    } catch (err) {
      setError('Failed to load artifacts.');
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchArtifacts();
  }, []);

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

  const handleEdit = (artifact) => {
    setEditingId(artifact.id);
    setFormData({
      type: artifact.type,
      version_name: artifact.version_name || '',
      location: artifact.location || '',
      notes: artifact.notes || '',
      active: Boolean(artifact.active),
    });
  };

  const handleSubmit = async (event) => {
    event.preventDefault();
    setError('');
    const payload = {
      type: formData.type,
      version_name: formData.version_name,
      location: formData.location || null,
      notes: formData.notes || null,
      active: Boolean(formData.active),
    };

    try {
      if (editingId) {
        const updated = await updateArtifact(editingId, payload);
        setArtifacts((prev) => prev.map((artifact) => (artifact.id === editingId ? updated : artifact)));
      } else {
        const created = await createArtifact(payload);
        setArtifacts((prev) => [...prev, created]);
      }
      resetForm();
    } catch (err) {
      setError('Failed to save artifact.');
      console.error(err);
    }
  };

  const handleDelete = async (artifactId) => {
    setError('');
    try {
      await deleteArtifact(artifactId);
      setArtifacts((prev) => prev.filter((artifact) => artifact.id !== artifactId));
    } catch (err) {
      setError('Failed to delete artifact.');
      console.error(err);
    }
  };

  return (
    <section className="section">
      <div className="section-header">
        <h2>Artifacts</h2>
        <button type="button" className="ghost" onClick={fetchArtifacts} disabled={loading}>
          Refresh
        </button>
      </div>
      {error && <p className="error">{error}</p>}
      <div className="section-grid">
        <form className="card" onSubmit={handleSubmit}>
          <h3>{editingId ? 'Edit Artifact' : 'Create Artifact'}</h3>
          <label>
            Type
            <select name="type" value={formData.type} onChange={handleChange}>
              {TYPE_OPTIONS.map((option) => (
                <option key={option.value} value={option.value}>
                  {option.label}
                </option>
              ))}
            </select>
          </label>
          <label>
            Version Name
            <input name="version_name" value={formData.version_name} onChange={handleChange} required />
          </label>
          <label>
            Location
            <input name="location" value={formData.location} onChange={handleChange} />
          </label>
          <label>
            Notes
            <textarea name="notes" value={formData.notes} onChange={handleChange} rows="2" />
          </label>
          <label className="checkbox">
            <input type="checkbox" name="active" checked={formData.active} onChange={handleChange} />
            Active
          </label>
          <div className="form-actions">
            <button type="submit" className="primary">
              {editingId ? 'Update Artifact' : 'Create Artifact'}
            </button>
            {editingId && (
              <button type="button" className="ghost" onClick={resetForm}>
                Cancel
              </button>
            )}
          </div>
        </form>
        <div className="card">
          <h3>Artifact List</h3>
          {loading ? (
            <p>Loading...</p>
          ) : artifacts.length === 0 ? (
            <p className="muted">No artifacts found.</p>
          ) : (
            <table>
              <thead>
                <tr>
                  <th>ID</th>
                  <th>Type</th>
                  <th>Version</th>
                  <th>Active</th>
                  <th>Created</th>
                  <th>Actions</th>
                </tr>
              </thead>
              <tbody>
                {artifacts.map((artifact) => (
                  <tr key={artifact.id}>
                    <td>{artifact.id}</td>
                    <td>{artifact.type}</td>
                    <td>{artifact.version_name}</td>
                    <td>{artifact.active ? 'Yes' : 'No'}</td>
                    <td>{formatDateTime(artifact.created_at)}</td>
                    <td className="row-actions">
                      <button type="button" className="ghost" onClick={() => handleEdit(artifact)}>
                        Edit
                      </button>
                      <button type="button" className="danger" onClick={() => handleDelete(artifact.id)}>
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

export default ArtifactSection;
