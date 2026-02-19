import React, { useEffect, useState } from 'react';
import { createApplication, deleteApplication, listApplications, updateApplication } from '../api/applications';
import { listJobs } from '../api/jobs';
import { formatDate, toInputDate } from './dateUtils';

const RESPONSE_OPTIONS = [
  { value: '', label: 'None' },
  { value: 'no_response', label: 'No Response' },
  { value: 'rejected', label: 'Rejected' },
  { value: 'interview', label: 'Interview' },
  { value: 'offer', label: 'Offer' },
];

const initialForm = {
  job_id: '',
  date_sent: '',
  contact: '',
  response: '',
  next_action_date: '',
  notes: '',
  active: true,
};

function ApplicationSection() {
  const [applications, setApplications] = useState([]);
  const [loading, setLoading] = useState(false);
  const [jobs, setJobs] = useState([]);
  const [error, setError] = useState('');
  const [formData, setFormData] = useState(initialForm);
  const [editingId, setEditingId] = useState(null);

  const fetchApplications = async () => {
    setLoading(true);
    setError('');
    try {
      const data = await listApplications();
      setApplications(data);
    } catch (err) {
      setError('Failed to load applications.');
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  const fetchJobs = async () => {
    setError('');
    try {
      const data = await listJobs();
      setJobs(data);
    } catch (err) {
      setError('Failed to load jobs.');
      console.error(err);
    }
  }

  useEffect(() => {
    fetchApplications();
    fetchJobs();
  }, []);



  const getJobTitleById = (jobId) => {
    const job = jobs.find((j) => j.id === jobId);
    return job ? `${job.company} - ${job.title}` : `Job ID ${jobId}`;
  }

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

  const handleEdit = (application) => {
    setEditingId(application.id);
    setFormData({
      job_id: application.job_id ?? '',
      date_sent: toInputDate(application.date_sent),
      contact: application.contact || '',
      response: application.response || '',
      next_action_date: toInputDate(application.next_action_date),
      notes: application.notes || '',
      active: Boolean(application.active),
    });
  };

  const handleSubmit = async (event) => {
    event.preventDefault();
    setError('');
    const payload = {
      job_id: Number(formData.job_id),
      date_sent: formData.date_sent ? new Date(formData.date_sent).toISOString() : null,
      contact: formData.contact || null,
      response: formData.response || null,
      next_action_date: formData.next_action_date || null,
      notes: formData.notes || null,
      active: Boolean(formData.active),
    };

    try {
      if (editingId) {
        const updated = await updateApplication(editingId, payload);
        setApplications((prev) => prev.map((item) => (item.id === editingId ? updated : item)));
      } else {
        const created = await createApplication(payload);
        setApplications((prev) => [...prev, created]);
      }
      resetForm();
    } catch (err) {
      setError('Failed to save application.');
      console.error(err);
    }
  };

  const handleDelete = async (applicationId) => {
    setError('');
    try {
      await deleteApplication(applicationId);
      setApplications((prev) => prev.filter((item) => item.id !== applicationId));
    } catch (err) {
      setError('Failed to delete application.');
      console.error(err);
    }
  };

  return (
    <section className="section">
      <div className="section-header">
        <h2>Applications</h2>
        <button type="button" className="ghost" onClick={fetchApplications} disabled={loading}>
          Refresh
        </button>
      </div>
      {error && <p className="error">{error}</p>}
      <div className="section-grid">
        <form className="card" onSubmit={handleSubmit}>
          <h3>{editingId ? 'Edit Application' : 'Create Application'}</h3>
          <label>
            Job
            <select name="job_id" value={formData.job_id} onChange={handleChange} required>
              <option value="">Select a job</option>
              {jobs.map((job) => (
                <option key={job.id} value={job.id}>
                  {getJobTitleById(job.id)}
                </option>
              ))}
            </select>
          </label>
          <label>
            Date Sent
            <input
              type="date-local"
              name="date_sent"
              value={formData.date_sent}
              onChange={handleChange}
            />
          </label>
          <label>
            Contact
            <input name="contact" value={formData.contact} onChange={handleChange} />
          </label>
          <label>
            Response
            <select name="response" value={formData.response} onChange={handleChange}>
              {RESPONSE_OPTIONS.map((option) => (
                <option key={option.value} value={option.value}>
                  {option.label}
                </option>
              ))}
            </select>
          </label>
          <label>
            Next Action Date
            <input
              type="date"
              name="next_action_date"
              value={formData.next_action_date}
              onChange={handleChange}
            />
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
              {editingId ? 'Update Application' : 'Create Application'}
            </button>
            {editingId && (
              <button type="button" className="ghost" onClick={resetForm}>
                Cancel
              </button>
            )}
          </div>
        </form>
        <div className="card">
          <h3>Application List</h3>
          {loading ? (
            <p>Loading...</p>
          ) : applications.length === 0 ? (
            <p className="muted">No applications found.</p>
          ) : (
            <table>
              <thead>
                <tr>
                  <th>ID</th>
                  <th>Job</th>
                  <th>Response</th>
                  <th>Active</th>
                  <th>Date Sent</th>
                  <th>Next Action</th>
                  <th>Actions</th>
                </tr>
              </thead>
              <tbody>
                {applications.map((application) => (
                  <tr key={application.id}>
                    <td>{application.id}</td>
                    <td>{getJobTitleById(application.job_id)}</td>
                    <td>{application.response || '-'}</td>
                    <td>{application.active ? 'Yes' : 'No'}</td>
                    <td>{formatDate(application.date_sent)}</td>
                    <td>{formatDate(application.next_action_date)}</td>
                    <td className="row-actions">
                      <button type="button" className="ghost" onClick={() => handleEdit(application)}>
                        Edit
                      </button>
                      <button type="button" className="danger" onClick={() => handleDelete(application.id)}>
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

export default ApplicationSection;
