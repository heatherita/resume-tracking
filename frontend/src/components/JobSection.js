import React, { useEffect, useState } from 'react';
import { createJob, deleteJob, listJobs, updateJob } from '../api/jobs';
import { formatDateTime, toInputDateTime } from './dateUtils';

const STATUS_OPTIONS = [
  { value: 'interested', label: 'Interested' },
  { value: 'applied', label: 'Applied' },
  { value: 'rejected', label: 'Rejected' },
  { value: 'offer', label: 'Offer' },
  { value: 'negotiating', label: 'Negotiating' },
];

const initialForm = {
  company: '',
  title: '',
  posting_url: '',
  required_skills: '',
  date_found: '',
  status: 'interested',
  fit_score: '',
  notes: '',
  role_id: '',
};

function JobSection() {
  const [jobs, setJobs] = useState([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');
  const [formData, setFormData] = useState(initialForm);
  const [editingId, setEditingId] = useState(null);

  const fetchJobs = async () => {
    setLoading(true);
    setError('');
    try {
      const data = await listJobs();
      setJobs(data);
    } catch (err) {
      setError('Failed to load jobs.');
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchJobs();
  }, []);

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

  const handleEdit = (job) => {
    setEditingId(job.id);
    setFormData({
      company: job.company || '',
      title: job.title || '',
      posting_url: job.posting_url || '',
      required_skills: job.required_skills || '',
      date_found: toInputDateTime(job.date_found),
      status: job.status || 'interested',
      fit_score: job.fit_score ?? '',
      notes: job.notes || '',
      role_id: job.role_id ?? '',
    });
  };

  const handleSubmit = async (event) => {
    event.preventDefault();
    setError('');
    const payload = {
      company: formData.company,
      title: formData.title,
      posting_url: formData.posting_url || null,
      required_skills: formData.required_skills || null,
      date_found: formData.date_found ? new Date(formData.date_found).toISOString() : null,
      status: formData.status,
      fit_score: formData.fit_score === '' ? null : Number(formData.fit_score),
      notes: formData.notes || null,
      role_id: Number(formData.role_id),
    };

    try {
      if (editingId) {
        const updated = await updateJob(editingId, payload);
        setJobs((prev) => prev.map((job) => (job.id === editingId ? updated : job)));
      } else {
        const created = await createJob(payload);
        setJobs((prev) => [...prev, created]);
      }
      resetForm();
    } catch (err) {
      setError('Failed to save job.');
      console.error(err);
    }
  };

  const handleDelete = async (jobId) => {
    setError('');
    try {
      await deleteJob(jobId);
      setJobs((prev) => prev.filter((job) => job.id !== jobId));
    } catch (err) {
      setError('Failed to delete job.');
      console.error(err);
    }
  };

  return (
    <section className="section">
      <div className="section-header">
        <h2>Jobs</h2>
        <button type="button" className="ghost" onClick={fetchJobs} disabled={loading}>
          Refresh
        </button>
      </div>
      {error && <p className="error">{error}</p>}
      <div className="section-grid">
        <form className="card" onSubmit={handleSubmit}>
          <h3>{editingId ? 'Edit Job' : 'Create Job'}</h3>
          <label>
            Company
            <input name="company" value={formData.company} onChange={handleChange} required />
          </label>
          <label>
            Title
            <input name="title" value={formData.title} onChange={handleChange} required />
          </label>
          <label>
            Posting URL
            <input name="posting_url" value={formData.posting_url} onChange={handleChange} />
          </label>
          <label>
            Required Skills
            <textarea
              name="required_skills"
              value={formData.required_skills}
              onChange={handleChange}
              rows="2"
            />
          </label>
          <label>
            Date Found
            <input
              type="datetime-local"
              name="date_found"
              value={formData.date_found}
              onChange={handleChange}
            />
          </label>
          <label>
            Status
            <select name="status" value={formData.status} onChange={handleChange}>
              {STATUS_OPTIONS.map((status) => (
                <option key={status.value} value={status.value}>
                  {status.label}
                </option>
              ))}
            </select>
          </label>
          <label>
            Fit Score
            <input
              type="number"
              name="fit_score"
              value={formData.fit_score}
              onChange={handleChange}
              min="0"
              max="100"
            />
          </label>
          <label>
            Role ID
            <input
              type="number"
              name="role_id"
              value={formData.role_id}
              onChange={handleChange}
              min="1"
              required
            />
          </label>
          <label>
            Notes
            <textarea name="notes" value={formData.notes} onChange={handleChange} rows="2" />
          </label>
          <div className="form-actions">
            <button type="submit" className="primary">
              {editingId ? 'Update Job' : 'Create Job'}
            </button>
            {editingId && (
              <button type="button" className="ghost" onClick={resetForm}>
                Cancel
              </button>
            )}
          </div>
        </form>
        <div className="card">
          <h3>Job List</h3>
          {loading ? (
            <p>Loading...</p>
          ) : jobs.length === 0 ? (
            <p className="muted">No jobs found.</p>
          ) : (
            <table>
              <thead>
                <tr>
                  <th>ID</th>
                  <th>Company</th>
                  <th>Title</th>
                  <th>Status</th>
                  <th>Role ID</th>
                  <th>Date Found</th>
                  <th>Actions</th>
                </tr>
              </thead>
              <tbody>
                {jobs.map((job) => (
                  <tr key={job.id}>
                    <td>{job.id}</td>
                    <td>{job.company}</td>
                    <td>{job.title}</td>
                    <td>{job.status}</td>
                    <td>{job.role_id}</td>
                    <td>{formatDateTime(job.date_found)}</td>
                    <td className="row-actions">
                      <button type="button" className="ghost" onClick={() => handleEdit(job)}>
                        Edit
                      </button>
                      <button type="button" className="danger" onClick={() => handleDelete(job.id)}>
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

export default JobSection;
