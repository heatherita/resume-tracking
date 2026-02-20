import React, { useEffect, useState } from 'react';
import { createUser, deleteUser, listUsers, updateUser } from '../api/users';

const initialForm = {
  username: '',
  full_name: '',
  email: '',
  phone: '',
  address: '',
  city: '',
  state: '',
  postal_code: '',
  is_active: true,
};

function UserForm() {
  const [users, setUsers] = useState([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');
  const [formData, setFormData] = useState(initialForm);
  const [editingId, setEditingId] = useState(null);

  const fetchUsers = async () => {
    setLoading(true);
    setError('');
    try {
      const data = await listUsers();
      setUsers(data);
    } catch (err) {
      setError('Failed to load users.');
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchUsers();
  }, []);

  const handleChange = (event) => {
    const { name, value, type, checked } = event.target;
    setFormData((prev) => ({
      ...prev,
      [name]: type === 'checkbox' ? checked : value,
    }));
  };

  const handleEdit = (user) => {
    setEditingId(user.id);
    setFormData({
      username: user.username,
      full_name: user.full_name,
      email: user.email,
      phone: user.phone || '',
      address: user.address || '',
      city: user.city || '',
      state: user.state || '',
      postal_code: user.postal_code || '',
      is_active: user.is_active,
    });
  }

  const resetForm = () => {
    setEditingId(null);
    setFormData(initialForm);
  };

  const handleSubmit = async (event) => {
    event.preventDefault();
    setError('');
    try {
      if (editingId) {
        const updated = await updateUser(editingId, formData);
        setUsers((prev) => prev.map((user) => (user.id === editingId ? updated : user)));
      } else {
        const created = await createUser(formData);
        setUsers((prev) => [...prev, created]);
      }
      resetForm();
    } catch (err) {
      setError('Failed to update user.');
      console.error(err);
      // return;
    }
  };

  // const payload = {
  //   username: formData.username.trim(),
  //   full_name: formData.full_name.trim(),
  //   email: formData.email.trim(),
  //   phone: formData.phone.trim() || null,
  //   address: formData.address.trim() || null,
  //   is_active: Boolean(formData.is_active),
  // };

  //   try {
  //     await createUser(payload);
  //     await fetchUsers();
  //     resetForm();
  //   } catch (err) {
  //     setError('Failed to create user.');
  //     console.error(err);
  //   }
  // };

  const handleDelete = async (userId) => {
    setError('');
    try {
      await deleteUser(userId);
      setUsers((prev) => prev.filter((user) => user.id !== userId));
    } catch (err) {
      setError('Failed to deactivate user.');
      console.error(err);
    }
  };

  return (
    <section className="section">
      <div className="section-header">
        <h2>Users</h2>
        <button type="button" className="ghost" onClick={fetchUsers} disabled={loading}>
          Refresh
        </button>
      </div>
      {error && <p className="error">{error}</p>}
      <div className="section-grid">
        <form className="card" onSubmit={handleSubmit}>
          <h3>{editingId ? 'Edit User' : 'Create User'}</h3>
          <label>
            Username
            <input name="username" value={formData.username} onChange={handleChange} required />
          </label>
          <label>
            Full Name
            <input name="full_name" value={formData.full_name} onChange={handleChange} required />
          </label>
          <label>
            Email
            <input
              type="email"
              name="email"
              value={formData.email}
              onChange={handleChange}
              pattern={"^[^\\s@]+@[^\\s@]+\\.[^\\s@]+$"}
              title="Enter a valid email address (example: name@example.com)."
              required
            />
          </label>
          <label>
            Phone
            <input
              type="tel"
              name="phone"
              value={formData.phone}
              onChange={handleChange}
              pattern={"^\\+?1?[\\s.-]?(?:\\(\\d{3}\\)|\\d{3})[\\s.-]?\\d{3}[\\s.-]?\\d{4}$"}
              title="Enter a valid phone number (example: 732-555-1234)."
              required
            />
          </label>
          <label>
            Address
            <input name="address" value={formData.address} onChange={handleChange} />
          </label>
          <label>
            City
            <input name="city" value={formData.city} onChange={handleChange} />
          </label>
          <label>
            State
            <input name="state" value={formData.state} onChange={handleChange} />
          </label>
          <label>
            Postal Code
            <input
              name="postal_code"
              value={formData.postal_code}
              onChange={handleChange}
              pattern={"^\\d{5}(?:[-\\s]\\d{4})?$"}
              title="Enter a valid postal code (example: 12345 or 12345-6789)."
            />
          </label>
          <label className="checkbox">
            <input type="checkbox" name="is_active" checked={formData.is_active} onChange={handleChange} />
            Active
          </label>
          <div className="form-actions">
            <button type="submit" className="primary">
              {editingId ? 'Update User' : 'Create User'}
            </button>
            <button type="button" className="ghost" onClick={resetForm}>
              Reset
            </button>
          </div>
        </form>
        <div className="card">
          <h3>User List</h3>
          {loading ? (
            <p>Loading...</p>
          ) : users.length === 0 ? (
            <p className="muted">No users found.</p>
          ) : (
            <table>
              <thead>
                <tr>
                  <th>ID</th>
                  <th>Username</th>
                  <th>Full Name</th>
                  <th>Email</th>
                  <th>Phone</th>
                  <th>Address</th>
                  <th>Status</th>
                  <th>Actions</th>
                </tr>
              </thead>
              <tbody>
                {users.map((user) => (
                  <tr key={user.id}>
                    <td>{user.id}</td>
                    <td>{user.username}</td>
                    <td>{user.full_name}</td>
                    <td>{user.email}</td>
                    <td>{user.phone || '-'}</td>
                    <td>{user.address || '-'}</td>
                    <td>{user.is_active ? 'Active' : 'Inactive'}</td>
                    <td className="row-actions">
                      <button type="button" className="secondary" onClick={() => handleEdit(user)}>
                        Edit
                      </button>
                      <button type="button" className="danger" onClick={() => handleDelete(user.id)}>
                        Deactivate
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

export default UserForm;
