import React, { useState, useEffect } from 'react';

const Dashboard = () => {
  const [stats, setStats] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetchDashboard();
  }, []);

  const fetchDashboard = async () => {
    try {
      const response = await fetch('/api/dashboard', {
        credentials: 'include'
      });
      if (response.ok) {
        const data = await response.json();
        setStats(data);
      }
    } catch (error) {
      console.error('Failed to fetch dashboard:', error);
    } finally {
      setLoading(false);
    }
  };

  if (loading) {
    return <div className="loading">Loading dashboard...</div>;
  }

  if (!stats) {
    return <div className="container">Failed to load dashboard</div>;
  }

  return (
    <div className="container">
      <h1 className="mb-3">Dashboard</h1>
      
      <h2 className="mb-2">Projects Overview</h2>
      <div className="dashboard-grid">
        <div className="stat-card">
          <div className="stat-label">Total Projects</div>
          <div className="stat-value">{stats.projects.total}</div>
        </div>
        <div className="stat-card">
          <div className="stat-label">Active Projects</div>
          <div className="stat-value">{stats.projects.active}</div>
        </div>
        <div className="stat-card">
          <div className="stat-label">Completed Projects</div>
          <div className="stat-value">{stats.projects.completed}</div>
        </div>
      </div>

      <h2 className="mb-2 mt-3">Tasks Overview</h2>
      <div className="dashboard-grid">
        <div className="stat-card">
          <div className="stat-label">Total Tasks</div>
          <div className="stat-value">{stats.tasks.total}</div>
        </div>
        <div className="stat-card">
          <div className="stat-label">To Do</div>
          <div className="stat-value">{stats.tasks.todo}</div>
        </div>
        <div className="stat-card">
          <div className="stat-label">In Progress</div>
          <div className="stat-value">{stats.tasks.in_progress}</div>
        </div>
        <div className="stat-card">
          <div className="stat-label">Completed</div>
          <div className="stat-value">{stats.tasks.completed}</div>
        </div>
      </div>

      <h2 className="mb-2 mt-3">Recent Tasks</h2>
      {stats.recent_tasks.length === 0 ? (
        <p>No tasks yet. Create a project and add some tasks!</p>
      ) : (
        <div>
          {stats.recent_tasks.map(task => (
            <div key={task.id} className="card">
              <div className="card-header">
                <div>
                  <h3 className="card-title">{task.title}</h3>
                  <p style={{fontSize: '0.875rem', color: '#666', marginTop: '0.25rem'}}>
                    {task.description || 'No description'}
                  </p>
                </div>
                <div style={{display: 'flex', gap: '0.5rem'}}>
                  <span className={`badge badge-${task.status.replace('_', '-')}`}>
                    {task.status.replace('_', ' ')}
                  </span>
                  <span className={`badge badge-${task.priority}`}>
                    {task.priority}
                  </span>
                </div>
              </div>
            </div>
          ))}
        </div>
      )}
    </div>
  );
};

export default Dashboard;
