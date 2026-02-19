import React, { useEffect, useMemo, useState } from 'react';
import {
  attachSectionToArtifact,
  createArtifact,
  deleteArtifact,
  detachSectionFromArtifact,
  listArtifactSections,
  listArtifacts,
  listSections,
  updateArtifact,
} from '../api/artifacts';
import { listApplications } from '../api/applications';
import { formatDateTime } from './dateUtils';

const TYPE_OPTIONS = [
  { value: 'resume', label: 'Resume' },
  { value: 'cover_letter', label: 'Cover Letter' },
];

const initialArtifactForm = {
  type: 'resume',
  version_name: '',
  location: '',
  notes: '',
  active: true,
  application_id: '',
};

function ArtifactSection() {
  const [artifacts, setArtifacts] = useState([]);
  const [sections, setSections] = useState([]);
  const [artifactSections, setArtifactSections] = useState([]);
  const [selectedArtifactId, setSelectedArtifactId] = useState('');
  const [sectionToAttachId, setSectionToAttachId] = useState('');
  const [sectionOrder, setSectionOrder] = useState(1);
  const [loading, setLoading] = useState(false);
  const [applications, setApplications] = useState([]);
  const [error, setError] = useState('');

  const [artifactForm, setArtifactForm] = useState(initialArtifactForm);
  const [editingArtifactId, setEditingArtifactId] = useState(null);

  const fetchArtifacts = async () => {
    setLoading(true);
    setError('');
    try {
      const data = await listArtifacts();
      setArtifacts(data);
      setSelectedArtifactId((prev) => {
        if (prev && data.some((artifact) => artifact.id === Number(prev))) return prev;
        return data.length > 0 ? String(data[0].id) : '';
      });
    } catch (err) {
      setError('Failed to load artifacts.');
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  const fetchSections = async () => {
    setError('');
    try {
      const data = await listSections();
      setSections(data);
    } catch (err) {
      setError('Failed to load sections.');
      console.error(err);
    }
  };

  const fetchApplications = async () => {
    setError('');
    try {
      const data = await listApplications();
      setApplications(data);
    } catch (err) {
      setError('Failed to load applications.');
      console.error(err);
    }
  };

  const fetchArtifactSections = async (artifactId) => {
    if (!artifactId) {
      setArtifactSections([]);
      return;
    }
    setError('');
    try {
      const data = await listArtifactSections(artifactId);
      setArtifactSections(data);
    } catch (err) {
      setError('Failed to load artifact sections.');
      console.error(err);
    }
  };

  useEffect(() => {
    fetchArtifacts();
    fetchSections();
    fetchApplications();
  }, []);

  useEffect(() => {
    fetchArtifactSections(selectedArtifactId);
  }, [selectedArtifactId]);

  useEffect(() => {
    const maxOrder = artifactSections.reduce((max, section) => Math.max(max, Number(section.section_order || 0)), 0);
    setSectionOrder(maxOrder + 1);
  }, [artifactSections]);

  const getApplicationAndJobNameById = (applicationId) => {
    const application = applications.find((a) => a.id === applicationId);
    if (!application) return `Application ID ${applicationId}`;
    const job = application.job;
    return job ? `${job.company} - ${job.title}` : `Application ID ${applicationId}`;
  };

  const handleArtifactChange = (event) => {
    const { name, value, type, checked } = event.target;
    setArtifactForm((prev) => ({
      ...prev,
      [name]: type === 'checkbox' ? checked : value,
    }));
  };

  const resetArtifactForm = () => {
    setEditingArtifactId(null);
    setArtifactForm(initialArtifactForm);
  };

  const handleEditArtifact = (artifact) => {
    setEditingArtifactId(artifact.id);
    setArtifactForm({
      type: artifact.type,
      version_name: artifact.version_name || '',
      location: artifact.location || '',
      notes: artifact.notes || '',
      active: Boolean(artifact.active),
      application_id: artifact.application_id || '',
    });
  };

  const handleArtifactSubmit = async (event) => {
    event.preventDefault();
    setError('');
    const payload = {
      type: artifactForm.type,
      version_name: artifactForm.version_name,
      location: artifactForm.location || null,
      notes: artifactForm.notes || null,
      active: Boolean(artifactForm.active),
      application_id: Number(artifactForm.application_id) || null,
    };

    try {
      if (editingArtifactId) {
        const updated = await updateArtifact(editingArtifactId, payload);
        setArtifacts((prev) => prev.map((artifact) => (artifact.id === editingArtifactId ? updated : artifact)));
      } else {
        const created = await createArtifact(payload);
        setArtifacts((prev) => [...prev, created]);
        setSelectedArtifactId(String(created.id));
      }
      resetArtifactForm();
    } catch (err) {
      setError('Failed to save artifact.');
      console.error(err);
    }
  };

  const handleDeleteArtifact = async (artifactId) => {
    setError('');
    try {
      await deleteArtifact(artifactId);
      setArtifacts((prev) => prev.filter((artifact) => artifact.id !== artifactId));
      if (String(artifactId) === String(selectedArtifactId)) {
        setSelectedArtifactId('');
      }
    } catch (err) {
      setError('Failed to delete artifact.');
      console.error(err);
    }
  };

  const handleAttachSection = async () => {
    if (!selectedArtifactId || !sectionToAttachId) return;
    setError('');
    try {
      await attachSectionToArtifact(selectedArtifactId, sectionToAttachId, { section_order: Number(sectionOrder) });
      const latest = await listArtifactSections(selectedArtifactId);
      setArtifactSections(latest);
      setSectionToAttachId('');
      setSectionOrder((prev) => prev + 1);
    } catch (err) {
      setError('Failed to attach section.');
      console.error(err);
    }
  };

  const handleDetachSection = async (sectionId) => {
    if (!selectedArtifactId) return;
    setError('');
    try {
      await detachSectionFromArtifact(selectedArtifactId, sectionId);
      setArtifactSections((prev) => prev.filter((section) => section.id !== sectionId));
    } catch (err) {
      setError('Failed to detach section.');
      console.error(err);
    }
  };

  const attachableSections = useMemo(() => {
    const attachedIds = new Set(artifactSections.map((section) => section.id));
    return sections.filter((section) => !attachedIds.has(section.id));
  }, [sections, artifactSections]);

  const selectedArtifact = useMemo(
    () => artifacts.find((artifact) => String(artifact.id) === String(selectedArtifactId)) || null,
    [artifacts, selectedArtifactId]
  );

  return (
    <section className="section">
      <div className="section-header">
        <h2>Artifacts</h2>
        <button
          type="button"
          className="ghost"
          onClick={() => {
            fetchArtifacts();
            fetchSections();
          }}
          disabled={loading}
        >
          Refresh
        </button>
      </div>
      {error && <p className="error">{error}</p>}

      <div className="section-grid">
        <form className="card" onSubmit={handleArtifactSubmit}>
          <h3>{editingArtifactId ? 'Edit Artifact' : 'Create Artifact'}</h3>
          <label>
            Type
            <select name="type" value={artifactForm.type} onChange={handleArtifactChange}>
              {TYPE_OPTIONS.map((option) => (
                <option key={option.value} value={option.value}>
                  {option.label}
                </option>
              ))}
            </select>
          </label>
          <label>
            Application
            <select name="application_id" value={artifactForm.application_id} onChange={handleArtifactChange}>
              <option value="">Select an application</option>
              {applications.map((app) => (
                <option key={app.id} value={app.id}>
                  {getApplicationAndJobNameById(app.id)}
                </option>
              ))}
            </select>
          </label>
          <label>
            Version Name
            <input name="version_name" value={artifactForm.version_name} onChange={handleArtifactChange} required />
          </label>
          <label>
            Location
            <input name="location" value={artifactForm.location} onChange={handleArtifactChange} />
          </label>
          <label>
            Notes
            <textarea name="notes" value={artifactForm.notes} onChange={handleArtifactChange} rows="2" />
          </label>
          <label className="checkbox">
            <input type="checkbox" name="active" checked={artifactForm.active} onChange={handleArtifactChange} />
            Active
          </label>
          <div className="form-actions">
            <button type="submit" className="primary">
              {editingArtifactId ? 'Update Artifact' : 'Create Artifact'}
            </button>
            {editingArtifactId && (
              <button type="button" className="ghost" onClick={resetArtifactForm}>
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
                  <th>Application</th>
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
                    <td>{getApplicationAndJobNameById(artifact.application_id)}</td>
                    <td>{artifact.version_name}</td>
                    <td>{artifact.active ? 'Yes' : 'No'}</td>
                    <td>{formatDateTime(artifact.created_at)}</td>
                    <td className="row-actions">
                      <button type="button" className="ghost" onClick={() => setSelectedArtifactId(String(artifact.id))}>
                        Select
                      </button>
                      <button type="button" className="ghost" onClick={() => handleEditArtifact(artifact)}>
                        Edit
                      </button>
                      <button type="button" className="danger" onClick={() => handleDeleteArtifact(artifact.id)}>
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

      <div className="section-grid" style={{ marginTop: '20px' }}>
        <div className="card">
          <h3>Sections for Selected Artifact</h3>
          <p className="muted">
            {selectedArtifact
              ? `Selected: #${selectedArtifact.id} ${selectedArtifact.version_name}`
              : 'Select an artifact from the Artifact List first.'}
          </p>

          <div className="form-actions" style={{ marginBottom: '12px' }}>
            <select value={sectionToAttachId} onChange={(event) => setSectionToAttachId(event.target.value)}>
              <option value="">Attach existing section...</option>
              {attachableSections.map((section) => (
                <option key={section.id} value={section.id}>
                  #{section.id} {section.name} ({section.type})
                </option>
              ))}
            </select>
            <input
              type="number"
              min="1"
              value={sectionOrder}
              onChange={(event) => setSectionOrder(Number(event.target.value))}
              style={{ maxWidth: '120px' }}
            />
            <button
              type="button"
              className="ghost"
              onClick={handleAttachSection}
              disabled={!selectedArtifactId || !sectionToAttachId}
            >
              Attach
            </button>
          </div>

          {!selectedArtifactId ? (
            <p className="muted">Select an artifact to view attached sections.</p>
          ) : artifactSections.length === 0 ? (
            <p className="muted">No sections attached yet.</p>
          ) : (
            <table>
              <thead>
                <tr>
                  <th>ID</th>
                  <th>Name</th>
                  <th>Type</th>
                  <th>Order</th>
                  <th>Actions</th>
                </tr>
              </thead>
              <tbody>
                {artifactSections.map((section) => (
                  <tr key={section.id}>
                    <td>{section.id}</td>
                    <td>{section.name}</td>
                    <td>{section.type}</td>
                    <td>{section.section_order}</td>
                    <td className="row-actions">
                      <button type="button" className="ghost" onClick={() => handleDetachSection(section.id)}>
                        Detach
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
