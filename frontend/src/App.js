import React from 'react';
import './App.css';
import RoleSection from './components/RoleSection';
import JobSection from './components/JobSection';
import ArtifactSection from './components/ArtifactSection';
import MetricSection from './components/MetricSection';
import ApplicationSection from './components/ApplicationSection';

function App() {
  return (
    <div className="App">
      <header className="App-header">
        <h1>Resume Tracking Admin</h1>
        <p>Manage roles, jobs, artifacts, metrics, and applications.</p>
      </header>
      <main className="container">
        <RoleSection />
        <JobSection />
        <ArtifactSection />
        <MetricSection />
        <ApplicationSection />
      </main>
    </div>
  );
}

export default App;
