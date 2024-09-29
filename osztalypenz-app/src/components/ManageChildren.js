import React, { useState, useEffect } from 'react';
import { useParams } from 'react-router-dom';
import axios from 'axios';
import './ManageChildren.css'; 

const ManageChildren = () => {
  const { className } = useParams();
  const [children, setChildren] = useState([]);
  const [newChildName, setNewChildName] = useState('');
  const [newChildEmail, setNewChildEmail] = useState('');  // New state for email
  const [editingChild, setEditingChild] = useState(null);
  const [message, setMessage] = useState('');
  //const apiUrl = process.env.REACT_APP_API_URL || `${window.location.protocol}//${window.location.hostname}`;
  const apiUrl = process.env.REACT_APP_API_URL || `${window.location.protocol}//${window.location.hostname}${window.location.port ? ':' + window.location.port : ''}/api`;


  useEffect(() => {
    const fetchChildren = async () => {
      try {
        const response = await axios.get(`${apiUrl}/${className}/children`);
        const filteredChildren = response.data.filter((child) => child.id !== 1 && !child.isDeleted);
        setChildren(filteredChildren);
      } catch (error) {
        console.error('Error fetching children:', error);
        setMessage('Error fetching children.');
      }
    };

    fetchChildren();
  }, [className]);

  const handleAddChild = async () => {
    if (!newChildName || !newChildEmail) {
      setMessage('Child name and email are required.');
      return;
    }

    try {
      const response = await axios.post(`${apiUrl}/${className}/children`, { name: newChildName, email: newChildEmail });
      setChildren([...children, { id: response.data.id, name: newChildName, email: newChildEmail, isDeleted: false }]);
      setNewChildName('');
      setNewChildEmail('');  // Clear email input after adding
      setMessage('Child added successfully!');
    } catch (error) {
      console.error('Error adding child:', error);
      setMessage('Error adding child.');
    }
  };

  const handleDeleteChild = async (childId) => {
    try {
      await axios.delete(`${apiUrl}/${className}/children/${childId}`);
      setChildren(children.filter((child) => child.id !== childId));
      setMessage('Child deleted successfully!');
    } catch (error) {
      console.error('Error deleting child:', error);
      setMessage('Error deleting child.');
    }
  };

  const handleModifyChild = async (child) => {
    if (!editingChild || editingChild.name.trim() === '' || editingChild.email.trim() === '') {
      setMessage('Child name and email are required.');
      return;
    }

    try {
      await axios.put(`${apiUrl}/${className}/children/${child.id}`, { name: editingChild.name, email: editingChild.email });
      setChildren(children.map((c) => (c.id === child.id ? { ...c, name: editingChild.name, email: editingChild.email } : c)));
      setEditingChild(null);
      setMessage('Child modified successfully!');
    } catch (error) {
      console.error('Error modifying child:', error);
      setMessage('Error modifying child.');
    }
  };

  const handleEditClick = (child) => {
    setEditingChild(child);
    setMessage('');
  };

  return (
    <div className="manage-children-container">
      <h1>Tanulók</h1>
      {message && <p className="message">{message}</p>}
      
      <ul className="children-list">
        {children.map((child) => (
          <li key={child.id} className="child-item">
            {editingChild && editingChild.id === child.id ? (
              <>
                <input
                  type="text"
                  className="child-input"
                  value={editingChild.name}
                  onChange={(e) => setEditingChild({ ...editingChild, name: e.target.value })}
                />
                <input
                  type="email"
                  className="child-input"
                  value={editingChild.email}
                  onChange={(e) => setEditingChild({ ...editingChild, email: e.target.value })}
                />
              </>
            ) : (
              <>
                <span className="child-name">{child.name}</span>
                <span className="child-email">{child.email}</span>
              </>
            )}
            {editingChild && editingChild.id === child.id ? (
              <button className="btn save-btn" onClick={() => handleModifyChild(child)}>Mentés</button>
            ) : (
              <>
                <button className="btn modify-btn" onClick={() => handleEditClick(child)}>Módosítás</button>
                <button className="btn delete-btn" onClick={() => handleDeleteChild(child.id)}>Törlés</button>
              </>
            )}
          </li>
        ))}
      </ul>

      <div className="add-child-section">
        <input
          type="text"
          placeholder="Tanuló neve"
          value={newChildName}
          className="new-child-input"
          onChange={(e) => setNewChildName(e.target.value)}
        />
        <input
          type="email"
          placeholder="Tanuló email"
          value={newChildEmail}
          className="new-child-input"
          onChange={(e) => setNewChildEmail(e.target.value)}
        />
        <button className="btn add-btn" onClick={handleAddChild}>Hozzáadás</button>
      </div>
    </div>
  );
};

export default ManageChildren;
