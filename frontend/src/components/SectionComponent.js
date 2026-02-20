import React, { useEffect, useState } from 'react';
import {
  createSection,
  deleteSection,
  listArtifactSections,
  listArtifacts,
  listSections,
  updateSection,
} from '../api/artifacts';

const SECTION_TYPES = [
  { value: 'header', label: 'Header' },
  { value: 'text', label: 'Text' },
  { value: 'bullets', label: 'Bullets' },
];

const initialForm = {
  name: '',
  type: 'header',
  content: '',
};

function SectionComponent() {
  const [sections, setSections] = useState([]);
  const [artifacts, setArtifacts] = useState([]);
  const [filterArtifactId, setFilterArtifactId] = useState('');
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');
  const [formData, setFormData] = useState(initialForm);
  const [editingId, setEditingId] = useState(null);

  const fetchSections = async () => {
    setLoading(true);
    setError('');
    try {
      const data = await listSections();
      setSections(data);
    } catch (err) {
      setError('Failed to load sections.');
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  const fetchArtifacts = async () => {
    setError('');
    try {
      const data = await listArtifacts();
      setArtifacts(data);
    } catch (err) {
      setError('Failed to load artifacts.');
      console.error(err);
    }
  };

  const fetchSectionsForArtifact = async (artifactId) => {
    if (!artifactId) {
      fetchSections();
      return;
    }
    setLoading(true);
    setError('');
    try {
      const data = await listArtifactSections(artifactId);
      setSections(data);
    } catch (err) {
      setError('Failed to load sections for artifact.');
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  const getArtifactLabel = (artifactId) => {
    const artifact = artifacts.find((item) => item.id === Number(artifactId));
    if (!artifact) return `Artifact ID ${artifactId}`;
    const version = artifact.version_name ? ` - ${artifact.version_name}` : '';
    return `${artifact.type}${version} (ID ${artifact.id})`;
  };

  useEffect(() => {
    fetchSections();
    fetchArtifacts();
  }, []);

  useEffect(() => {
    fetchSectionsForArtifact(filterArtifactId);
  }, [filterArtifactId]);

  const handleChange = (event) => {
    const { name, value } = event.target;
    setFormData((prev) => ({
      ...prev,
      [name]: value,
    }));
  };

  const resetForm = () => {
    setEditingId(null);
    setFormData(initialForm);
  };

  const handleEdit = (section) => {
    setEditingId(section.id);
    setFormData({
      name: section.name || '',
      type: section.type || 'header',
      content: section.content || '',
    });
  };

  const handleSubmit = async (event) => {
    event.preventDefault();
    setError('');
    const payload = {
      name: formData.name,
      type: formData.type,
      content: formData.content,
    };

    try {
      if (editingId) {
        const updated = await updateSection(editingId, payload);
        setSections((prev) => prev.map((section) => (section.id === editingId ? updated : section)));
      } else {
        const created = await createSection(payload);
        setSections((prev) => [...prev, created]);
      }
      resetForm();
    } catch (err) {
      setError('Failed to save section.');
      console.error(err);
    }
  };

  const handleDelete = async (sectionId) => {
    setError('');
    try {
      await deleteSection(sectionId);
      setSections((prev) => prev.filter((section) => section.id !== sectionId));
    } catch (err) {
      setError('Failed to delete section.');
      console.error(err);
    }
  };

  return (
    <section className="section">
      <div className="section-header">
        <h2>Sections</h2>
        <div className="filter">
          <label>
            Filter by Artifact
            <select value={filterArtifactId} onChange={(event) => setFilterArtifactId(event.target.value)}>
              <option value="">All sections</option>
              {artifacts.map((artifact) => (
                <option key={artifact.id} value={artifact.id}>
                  {getArtifactLabel(artifact.id)}
                </option>
              ))}
            </select>
          </label>
          <button
            type="button"
            className="ghost"
            onClick={() => (filterArtifactId ? fetchSectionsForArtifact(filterArtifactId) : fetchSections())}
            disabled={loading}
          >
            Refresh
          </button>
        </div>
      </div>
      {error && <p className="error">{error}</p>}
      <div className="section-grid">
        <form className="card" onSubmit={handleSubmit}>
          <h3>{editingId ? 'Edit Section' : 'Create Section'}</h3>
          <label>
            Name
            <input name="name" value={formData.name} onChange={handleChange} required />
          </label>
          <label>
            Type
            <select name="type" value={formData.type} onChange={handleChange}>
              {SECTION_TYPES.map((option) => (
                <option key={option.value} value={option.value}>
                  {option.label}
                </option>
              ))}
            </select>
          </label>
          <label>
            Content
            <textarea name="content" value={formData.content} onChange={handleChange} rows="4" required />
          </label>
          <div className="form-actions">
            <button type="submit" className="primary">
              {editingId ? 'Update Section' : 'Create Section'}
            </button>
            {editingId && (
              <button type="button" className="ghost" onClick={resetForm}>
                Cancel
              </button>
            )}
          </div>
        </form>
        <div className="card">
          <h3>Section List</h3>
          {loading ? (
            <p>Loading...</p>
          ) : sections.length === 0 ? (
            <p className="muted">No sections found.</p>
          ) : (
            <table>
              <thead>
                <tr>
                  <th>ID</th>
                  <th>Name</th>
                  <th>Type</th>
                  <th>Content</th>
                  <th>Actions</th>
                </tr>
              </thead>
              <tbody>
                {sections.map((section) => (
                  <tr key={section.id}>
                    <td>{section.id}</td>
                    <td>{section.name}</td>
                    <td>{section.type}</td>
                    <td>{section.content}</td>
                    <td className="row-actions">
                      <button type="button" className="ghost" onClick={() => handleEdit(section)}>
                        Edit
                      </button>
                      <button type="button" className="danger" onClick={() => handleDelete(section.id)}>
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

export default SectionComponent;
