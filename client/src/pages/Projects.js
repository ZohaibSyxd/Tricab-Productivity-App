import React, { useState, useEffect } from 'react';
import { Link } from 'react-router-dom';

const Projects = () => {
  const [projects, setProjects] = useState([]);
  const [loading, setLoading] = useState(true);
  const [showModal, setShowModal] = useState(false);
  const [currentProject, setCurrentProject] = useState(null);
  const [formData, setFormData] = useState({
    name: '',
    description: '',
    status: 'active'
  });
  const [error, setError] = useState('');
  const [page, setPage] = useState(1);
  const [totalPages, setTotalPages] = useState(1);

  useEffect(() => {
    fetchProjects();
  }, [page]);

  const fetchProjects = async () => {
    try {
      const response = await fetch(`/api/projects?page=${page}`, {
        credentials: 'include'
      });
      if (response.ok) {
        const data = await response.json();
        setProjects(data.projects);
        setTotalPages(data.pages);
      }
    } catch (error) {
      console.error('Failed to fetch projects:', error);
    } finally {
      setLoading(false);
    }
  };

  const openModal = (project = null) => {
    if (project) {
      setCurrentProject(project);
      setFormData({
        name: project.name,
        description: project.description || '',
        status: project.status
      });
    } else {
      setCurrentProject(null);
      setFormData({ name: '', description: '', status: 'active' });
    }
    setShowModal(true);
    setError('');
  };

  const closeModal = () => {
    setShowModal(false);
    setCurrentProject(null);
    setFormData({ name: '', description: '', status: 'active' });
    setError('');
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError('');

    try {
      const url = currentProject 
        ? `/api/projects/${currentProject.id}`
        : '/api/projects';
      const method = currentProject ? 'PATCH' : 'POST';

      const response = await fetch(url, {
        method,
        headers: { 'Content-Type': 'application/json' },
        credentials: 'include',
        body: JSON.stringify(formData)
      });

      if (!response.ok) {
        const errorData = await response.json();
        throw new Error(errorData.error || 'Failed to save project');
      }

      closeModal();
      fetchProjects();
    } catch (err) {
      setError(err.message);
    }
  };

  const handleDelete = async (id) => {
    if (!window.confirm('Are you sure you want to delete this project? This will also delete all tasks.')) {
      return;
    }

    try {
      const response = await fetch(`/api/projects/${id}`, {
        method: 'DELETE',
        credentials: 'include'
      });

      if (response.ok) {
        fetchProjects();
      }
    } catch (error) {
      console.error('Failed to delete project:', error);
    }
  };

  if (loading) {
    return <div className="loading">Loading projects...</div>;
  }

  return (
    <div className="container">
      <div className="flex justify-between align-center mb-3">
        <h1>My Projects</h1>
        <button onClick={() => openModal()} className="btn btn-primary">
          + New Project
        </button>
      </div>

      {projects.length === 0 ? (
        <div className="text-center" style={{padding: '3rem'}}>
          <p style={{fontSize: '1.25rem', color: '#666'}}>No projects yet.</p>
          <button onClick={() => openModal()} className="btn btn-primary mt-2">
            Create Your First Project
          </button>
        </div>
      ) : (
        <>
          <div>
            {projects.map(project => (
              <div key={project.id} className="card">
                <div className="card-header">
                  <div>
                    <Link to={`/projects/${project.id}`} style={{textDecoration: 'none', color: 'inherit'}}>
                      <h3 className="card-title">{project.name}</h3>
                    </Link>
                    <p style={{fontSize: '0.875rem', color: '#666', marginTop: '0.25rem'}}>
                      {project.description || 'No description'}
                    </p>
                    <span className={`badge badge-${project.status} mt-1`}>
                      {project.status}
                    </span>
                  </div>
                  <div className="card-actions">
                    <button onClick={() => openModal(project)} className="btn btn-secondary">
                      Edit
                    </button>
                    <button onClick={() => handleDelete(project.id)} className="btn btn-danger">
                      Delete
                    </button>
                  </div>
                </div>
              </div>
            ))}
          </div>

          {totalPages > 1 && (
            <div className="pagination">
              <button 
                onClick={() => setPage(p => Math.max(1, p - 1))}
                disabled={page === 1}
              >
                Previous
              </button>
              <span>Page {page} of {totalPages}</span>
              <button 
                onClick={() => setPage(p => Math.min(totalPages, p + 1))}
                disabled={page === totalPages}
              >
                Next
              </button>
            </div>
          )}
        </>
      )}

      {showModal && (
        <div className="modal-overlay" onClick={closeModal}>
          <div className="modal-content" onClick={(e) => e.stopPropagation()}>
            <div className="modal-header">
              <h2 className="modal-title">
                {currentProject ? 'Edit Project' : 'New Project'}
              </h2>
              <button className="modal-close" onClick={closeModal}>&times;</button>
            </div>
            {error && <div className="alert alert-error">{error}</div>}
            <form onSubmit={handleSubmit}>
              <div className="form-group">
                <label className="form-label">Project Name</label>
                <input
                  type="text"
                  className="form-input"
                  value={formData.name}
                  onChange={(e) => setFormData({...formData, name: e.target.value})}
                  required
                />
              </div>
              <div className="form-group">
                <label className="form-label">Description</label>
                <textarea
                  className="form-textarea"
                  value={formData.description}
                  onChange={(e) => setFormData({...formData, description: e.target.value})}
                />
              </div>
              <div className="form-group">
                <label className="form-label">Status</label>
                <select
                  className="form-select"
                  value={formData.status}
                  onChange={(e) => setFormData({...formData, status: e.target.value})}
                >
                  <option value="active">Active</option>
                  <option value="completed">Completed</option>
                  <option value="archived">Archived</option>
                </select>
              </div>
              <div className="flex gap-2">
                <button type="submit" className="btn btn-primary">
                  {currentProject ? 'Update' : 'Create'}
                </button>
                <button type="button" onClick={closeModal} className="btn btn-secondary">
                  Cancel
                </button>
              </div>
            </form>
          </div>
        </div>
      )}
    </div>
  );
};

export default Projects;
