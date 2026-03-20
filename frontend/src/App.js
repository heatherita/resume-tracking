import React, { useMemo, useState, useEffect } from 'react';
import './App.css';
import {
  listLabels,
} from './api/global';
import RoleSection from './components/RoleSection';
import JobSection from './components/JobSection';
import ArtifactSection from './components/ArtifactSection';
import MetricSection from './components/MetricSection';
import ApplicationSection from './components/ApplicationSection';
import SectionComponent from './components/SectionComponent';
import UserForm from './components/UserForm';

function App() {
  const [activeTab, setActiveTab] = useState('roles');
  const [refreshCounter, setRefreshCounter] = useState(0);
  const [laneLabels, setLaneLabels] = useState(0);
  const [jobStatusLabels, setJobStatusLabels] = useState(0);
  const [applicationResponseLabels, setApplicationResponseLabels] = useState(0);
  const [sectionTypeLabels, setSectionTypeLabels] = useState(0);

  const fetchLabels = async () => {
    try {
      const data = await listLabels();
      console.log(data.application_response_labels)
      setJobStatusLabels(data.job_status_labels)
      setLaneLabels(data.lane_labels)
      setApplicationResponseLabels(data.application_response_labels)
      setSectionTypeLabels(data.section_type_labels)
    } catch (err) {
      console.error(err);
    }
  };

  useEffect(() => {
    fetchLabels();
  }, []);

  const handleTabClick = (tabId) => {
    setActiveTab(tabId);
    setRefreshCounter((prev) => prev + 1);
  };

  const tabs = useMemo(
    () => [
      { id: 'roles', label: 'Roles', content: <RoleSection refreshKey={`${activeTab}-${refreshCounter}`} laneLabels={laneLabels} /> },
      { id: 'jobs', label: 'Jobs', content: <JobSection refreshKey={`${activeTab}-${refreshCounter}`} jobStatusLabels={jobStatusLabels} /> },
      { id: 'applications', label: 'Applications', content: <ApplicationSection refreshKey={`${activeTab}-${refreshCounter}`} applicationResponseLabels={applicationResponseLabels} /> },
      { id: 'artifacts', label: 'Artifacts', content: <ArtifactSection refreshKey={`${activeTab}-${refreshCounter}`} /> },
      { id: 'sections', label: 'Sections', content: <SectionComponent refreshKey={`${activeTab}-${refreshCounter}`} sectionTypeLabels ={sectionTypeLabels}/> },
      { id: 'metrics', label: 'Metrics', content: <MetricSection refreshKey={`${activeTab}-${refreshCounter}`} /> },
      { id: 'users', label: 'Users', content: <UserForm refreshKey={`${activeTab}-${refreshCounter}`} /> },

    ],
    [activeTab, refreshCounter]
  );


  return (
    <div className="App">
      <header className="App-header">
        <h1>Resume Tracking Admin</h1>
        <p>Manage roles, jobs, applications, artifacts, sections, and metrics.</p>
      </header>
      <main className="container">
        <div className="tabs">
          {tabs.map((tab) => (
            <button
              key={tab.id}
              type="button"
              className={`tab ${activeTab === tab.id ? 'active' : ''}`}
              onClick={() => handleTabClick(tab.id)}
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
