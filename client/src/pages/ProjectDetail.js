import React, { useState, useEffect } from 'react';
import { useParams, useNavigate } from 'react-router-dom';

const ProjectDetail = () => {
  const { id } = useParams();
  const navigate = useNavigate();
  const [project, setProject] = useState(null);
  const [tasks, setTasks] = useState([]);
  const [loading, setLoading] = useState(true);
  const [showModal, setShowModal] = useState(false);
  const [currentTask, setCurrentTask] = useState(null);
  const [formData, setFormData] = useState({
    title: '',
    description: '',
    status: 'todo',
    priority: 'medium',
    due_date: ''
  });
  const [error, setError] = useState('');
  const [aiLoading, setAiLoading] = useState(false);

  useEffect(() => {
    fetchProject();
    fetchTasks();
  }, [id]);

  const fetchProject = async () => {
    try {
      const response = await fetch(`/api/projects/${id}`, {
        credentials: 'include'
      });
      if (response.ok) {
        const data = await response.json();
        setProject(data);
      } else {
        navigate('/projects');
      }
    } catch (error) {
      console.error('Failed to fetch project:', error);
    }
  };

  const fetchTasks = async () => {
    try {
      const response = await fetch(`/api/projects/${id}/tasks`, {
        credentials: 'include'
      });
      if (response.ok) {
        const data = await response.json();
        setTasks(data.tasks);
      }
    } catch (error) {
      console.error('Failed to fetch tasks:', error);
    } finally {
      setLoading(false);
    }
  };

  const openModal = (task = null) => {
    if (task) {
      setCurrentTask(task);
      setFormData({
        title: task.title,
        description: task.description || '',
        status: task.status,
        priority: task.priority,
        due_date: task.due_date ? task.due_date.split('T')[0] : ''
      });
    } else {
      setCurrentTask(null);
      setFormData({
        title: '',
        description: '',
        status: 'todo',
        priority: 'medium',
        due_date: ''
      });
    }
    setShowModal(true);
    setError('');
  };

  const closeModal = () => {
    setShowModal(false);
    setCurrentTask(null);
    setFormData({
      title: '',
      description: '',
      status: 'todo',
      priority: 'medium',
      due_date: ''
    });
    setError('');
  };

  const generateDescription = async () => {
    if (!formData.title) {
      setError('Please enter a task title first');
      return;
    }

    setAiLoading(true);
    setError('');

    try {
      const response = await fetch('/api/ai/generate-task-description', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        credentials: 'include',
        body: JSON.stringify({ title: formData.title })
      });

      if (response.ok) {
        const data = await response.json();
        setFormData({ ...formData, description: data.description });
      } else {
        const errorData = await response.json();
        setError(errorData.error || 'AI generation is not available');
      }
    } catch (err) {
      setError('Failed to generate description');
    } finally {
      setAiLoading(false);
    }
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError('');

    try {
      const url = currentTask 
        ? `/api/tasks/${currentTask.id}`
        : `/api/projects/${id}/tasks`;
      const method = currentTask ? 'PATCH' : 'POST';

      const response = await fetch(url, {
        method,
        headers: { 'Content-Type': 'application/json' },
        credentials: 'include',
        body: JSON.stringify(formData)
      });

      if (!response.ok) {
        const errorData = await response.json();
        throw new Error(errorData.error || 'Failed to save task');
      }

      closeModal();
      fetchTasks();
    } catch (err) {
      setError(err.message);
    }
  };

  const handleDelete = async (taskId) => {
    if (!window.confirm('Are you sure you want to delete this task?')) {
      return;
    }

    try {
      const response = await fetch(`/api/tasks/${taskId}`, {
        method: 'DELETE',
        credentials: 'include'
      });

      if (response.ok) {
        fetchTasks();
      }
    } catch (error) {
      console.error('Failed to delete task:', error);
    }
  };

  if (loading || !project) {
    return <div className="loading">Loading...</div>;
  }

  const tasksByStatus = {
    todo: tasks.filter(t => t.status === 'todo'),
    in_progress: tasks.filter(t => t.status === 'in_progress'),
    completed: tasks.filter(t => t.status === 'completed')
  };

  return (
    <div className="container">
      <div className="mb-3">
        <button onClick={() => navigate('/projects')} className="btn btn-secondary">
          ← Back to Projects
        </button>
      </div>

      <div className="flex justify-between align-center mb-3">
        <div>
          <h1>{project.name}</h1>
          <p style={{color: '#666', marginTop: '0.5rem'}}>{project.description}</p>
        </div>
        <button onClick={() => openModal()} className="btn btn-primary">
          + New Task
        </button>
      </div>

      <div style={{display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(300px, 1fr))', gap: '1.5rem'}}>
        <div>
          <h3 className="mb-2">To Do ({tasksByStatus.todo.length})</h3>
          {tasksByStatus.todo.map(task => (
            <TaskCard key={task.id} task={task} onEdit={openModal} onDelete={handleDelete} />
          ))}
        </div>
        <div>
          <h3 className="mb-2">In Progress ({tasksByStatus.in_progress.length})</h3>
          {tasksByStatus.in_progress.map(task => (
            <TaskCard key={task.id} task={task} onEdit={openModal} onDelete={handleDelete} />
          ))}
        </div>
        <div>
          <h3 className="mb-2">Completed ({tasksByStatus.completed.length})</h3>
          {tasksByStatus.completed.map(task => (
            <TaskCard key={task.id} task={task} onEdit={openModal} onDelete={handleDelete} />
          ))}
        </div>
      </div>

      {showModal && (
        <div className="modal-overlay" onClick={closeModal}>
          <div className="modal-content" onClick={(e) => e.stopPropagation()}>
            <div className="modal-header">
              <h2 className="modal-title">
                {currentTask ? 'Edit Task' : 'New Task'}
              </h2>
              <button className="modal-close" onClick={closeModal}>&times;</button>
            </div>
            {error && <div className="alert alert-error">{error}</div>}
            <form onSubmit={handleSubmit}>
              <div className="form-group">
                <label className="form-label">Task Title</label>
                <input
                  type="text"
                  className="form-input"
                  value={formData.title}
                  onChange={(e) => setFormData({...formData, title: e.target.value})}
                  required
                />
              </div>
              <div className="form-group">
                <div className="flex justify-between align-center mb-1">
                  <label className="form-label">Description</label>
                  <button
                    type="button"
                    onClick={generateDescription}
                    className="btn btn-outline"
                    style={{padding: '0.25rem 0.75rem', fontSize: '0.875rem'}}
                    disabled={aiLoading}
                  >
                    {aiLoading ? '🤖 Generating...' : '🤖 AI Generate'}
                  </button>
                </div>
                <textarea
                  className="form-textarea"
                  value={formData.description}
                  onChange={(e) => setFormData({...formData, description: e.target.value})}
                />
              </div>
              <div className="grid grid-2 gap-2">
                <div className="form-group">
                  <label className="form-label">Status</label>
                  <select
                    className="form-select"
                    value={formData.status}
                    onChange={(e) => setFormData({...formData, status: e.target.value})}
                  >
                    <option value="todo">To Do</option>
                    <option value="in_progress">In Progress</option>
                    <option value="completed">Completed</option>
                  </select>
                </div>
                <div className="form-group">
                  <label className="form-label">Priority</label>
                  <select
                    className="form-select"
                    value={formData.priority}
                    onChange={(e) => setFormData({...formData, priority: e.target.value})}
                  >
                    <option value="low">Low</option>
                    <option value="medium">Medium</option>
                    <option value="high">High</option>
                  </select>
                </div>
              </div>
              <div className="form-group">
                <label className="form-label">Due Date</label>
                <input
                  type="date"
                  className="form-input"
                  value={formData.due_date}
                  onChange={(e) => setFormData({...formData, due_date: e.target.value})}
                />
              </div>
              <div className="flex gap-2">
                <button type="submit" className="btn btn-primary">
                  {currentTask ? 'Update' : 'Create'}
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

const TaskCard = ({ task, onEdit, onDelete }) => {
  return (
    <div className="card" style={{marginBottom: '1rem'}}>
      <div style={{marginBottom: '0.75rem'}}>
        <h4 style={{marginBottom: '0.5rem'}}>{task.title}</h4>
        <p style={{fontSize: '0.875rem', color: '#666', marginBottom: '0.5rem'}}>
          {task.description || 'No description'}
        </p>
        <div style={{display: 'flex', gap: '0.5rem', flexWrap: 'wrap'}}>
          <span className={`badge badge-${task.priority}`}>{task.priority}</span>
          {task.due_date && (
            <span className="badge" style={{background: '#e9ecef', color: '#495057'}}>
              Due: {new Date(task.due_date).toLocaleDateString()}
            </span>
          )}
        </div>
      </div>
      <div style={{display: 'flex', gap: '0.5rem'}}>
        <button onClick={() => onEdit(task)} className="btn btn-secondary" style={{flex: 1}}>
          Edit
        </button>
        <button onClick={() => onDelete(task.id)} className="btn btn-danger" style={{flex: 1}}>
          Delete
        </button>
      </div>
    </div>
  );
};

export default ProjectDetail;
