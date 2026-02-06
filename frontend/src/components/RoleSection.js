import React, { useEffect, useState } from 'react';
import { createRole, deleteRole, listRoles, updateRole } from '../api/roles';

const LANES = [
  { value: 'software_engineering', label: 'Software Engineering' },
  { value: 'devops', label: 'DevOps' },
  { value: 'security', label: 'Security' },
];

const initialForm = {
  lane: 'software_engineering',
  core_skills: '',
  notes: '',
};

function RoleSection() {
  const [roles, setRoles] = useState([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');
  const [formData, setFormData] = useState(initialForm);
  const [editingId, setEditingId] = useState(null);

  const fetchRoles = async () => {
    setLoading(true);
    setError('');
    try {
      const data = await listRoles();
      setRoles(data);
    } catch (err) {
      setError('Failed to load roles.');
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchRoles();
  }, []);

  const handleChange = (event) => {
    const { name, value } = event.target;
    setFormData((prev) => ({
      ...prev,
      [name]: value,
    }));
  };

  const handleEdit = (role) => {
    setEditingId(role.id);
    setFormData({
      lane: role.lane,
      core_skills: role.core_skills || '',
      notes: role.notes || '',
    });
  };

  const resetForm = () => {
    setEditingId(null);
    setFormData(initialForm);
  };

  const handleSubmit = async (event) => {
    event.preventDefault();
    setError('');
    try {
      if (editingId) {
        const updated = await updateRole(editingId, formData);
        setRoles((prev) => prev.map((role) => (role.id === editingId ? updated : role)));
      } else {
        const created = await createRole(formData);
        setRoles((prev) => [...prev, created]);
      }
      resetForm();
    } catch (err) {
      setError('Failed to save role.');
      console.error(err);
    }
  };

  const handleDelete = async (roleId) => {
    setError('');
    try {
      await deleteRole(roleId);
      setRoles((prev) => prev.filter((role) => role.id !== roleId));
    } catch (err) {
      setError('Failed to delete role.');
      console.error(err);
    }
  };

  return (
    <section className="section">
      <div className="section-header">
        <h2>Roles</h2>
        <button type="button" className="ghost" onClick={fetchRoles} disabled={loading}>
          Refresh
        </button>
      </div>
      {error && <p className="error">{error}</p>}
      <div className="section-grid">
        <form className="card" onSubmit={handleSubmit}>
          <h3>{editingId ? 'Edit Role' : 'Create Role'}</h3>
          <label>
            Lane
            <select name="lane" value={formData.lane} onChange={handleChange}>
              {LANES.map((lane) => (
                <option key={lane.value} value={lane.value}>
                  {lane.label}
                </option>
              ))}
            </select>
          </label>
          <label>
            Core Skills
            <textarea
              name="core_skills"
              value={formData.core_skills}
              onChange={handleChange}
              rows="3"
              required
            />
          </label>
          <label>
            Notes
            <textarea name="notes" value={formData.notes} onChange={handleChange} rows="2" />
          </label>
          <div className="form-actions">
            <button type="submit" className="primary">
              {editingId ? 'Update Role' : 'Create Role'}
            </button>
            {editingId && (
              <button type="button" className="ghost" onClick={resetForm}>
                Cancel
              </button>
            )}
          </div>
        </form>
        <div className="card">
          <h3>Role List</h3>
          {loading ? (
            <p>Loading...</p>
          ) : roles.length === 0 ? (
            <p className="muted">No roles found.</p>
          ) : (
            <table>
              <thead>
                <tr>
                  <th>ID</th>
                  <th>Lane</th>
                  <th>Core Skills</th>
                  <th>Notes</th>
                  <th>Actions</th>
                </tr>
              </thead>
              <tbody>
                {roles.map((role) => (
                  <tr key={role.id}>
                    <td>{role.id}</td>
                    <td>{role.lane}</td>
                    <td>{role.core_skills}</td>
                    <td>{role.notes || '-'}</td>
                    <td className="row-actions">
                      <button type="button" className="ghost" onClick={() => handleEdit(role)}>
                        Edit
                      </button>
                      <button type="button" className="danger" onClick={() => handleDelete(role.id)}>
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

export default RoleSection;
