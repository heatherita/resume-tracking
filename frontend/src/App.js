import React, { useMemo, useState } from 'react';
import './App.css';
import RoleSection from './components/RoleSection';
import JobSection from './components/JobSection';
import ArtifactSection from './components/ArtifactSection';
import MetricSection from './components/MetricSection';
import ApplicationSection from './components/ApplicationSection';

function App() {
  const tabs = useMemo(
    () => [
      { id: 'roles', label: 'Roles', content: <RoleSection /> },
      { id: 'jobs', label: 'Jobs', content: <JobSection /> },
      { id: 'applications', label: 'Applications', content: <ApplicationSection /> },
      { id: 'artifacts', label: 'Artifacts', content: <ArtifactSection /> },
      { id: 'metrics', label: 'Metrics', content: <MetricSection /> },
    ],
    []
  );
  const [activeTab, setActiveTab] = useState(tabs[0].id);

  return (
    <div className="App">
      <header className="App-header">
        <h1>Resume Tracking Admin</h1>
        <p>Manage roles, jobs, artifacts, metrics, and applications.</p>
      </header>
      <main className="container">
        <div className="tabs">
          {tabs.map((tab) => (
            <button
              key={tab.id}
              type="button"
              className={`tab ${activeTab === tab.id ? 'active' : ''}`}
              onClick={() => setActiveTab(tab.id)}
            >
              {tab.label}
            </button>
          ))}
        </div>
        {tabs.map((tab) => (
          <div
            key={tab.id}
            className={`tab-panel ${activeTab === tab.id ? 'active' : 'hidden'}`}
            hidden={activeTab !== tab.id}
          >
            {tab.content}
          </div>
        ))}
      </main>
    </div>
  );
}

export default App;
