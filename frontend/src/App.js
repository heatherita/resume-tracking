import React, { useState, useEffect } from 'react';
import axios from 'axios';
import './App.css';
import UserList from './components/UserList';
import UserForm from './components/UserForm';

const API_BASE_URL = 'http://localhost:8000/api';

function App() {
  const [users, setUsers] = useState([]);
  const [loading, setLoading] = useState(false);

  useEffect(() => {
    fetchUsers();
  }, []);

  const fetchUsers = async () => {
    setLoading(true);
    try {
      const response = await axios.get(`${API_BASE_URL}/users/`);
      setUsers(response.data);
    } catch (error) {
      console.error('Error fetching users:', error);
    } finally {
      setLoading(false);
    }
  };

  const handleCreateUser = async (userData) => {
    try {
      const response = await axios.post(`${API_BASE_URL}/users/`, userData);
      setUsers([...users, response.data]);
    } catch (error) {
      console.error('Error creating user:', error);
    }
  };

  const handleDeleteUser = async (userId) => {
    try {
      await axios.delete(`${API_BASE_URL}/users/${userId}`);
      setUsers(users.filter(user => user.id !== userId));
    } catch (error) {
      console.error('Error deleting user:', error);
    }
  };

  return (
    <div className="App">
      <header className="App-header">
        <h1>FastAPI + React App</h1>
      </header>
      <main>
        <div className="container">
          <UserForm onCreateUser={handleCreateUser} />
          {loading ? (
            <p>Loading...</p>
          ) : (
            <UserList users={users} onDeleteUser={handleDeleteUser} />
          )}
        </div>
      </main>
    </div>
  );
}

export default App;