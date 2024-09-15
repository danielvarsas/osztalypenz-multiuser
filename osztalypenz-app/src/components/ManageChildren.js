import React, { useState, useEffect } from 'react';
import axios from 'axios';
import './ManageChildren.css'; // Import a CSS file for styles

const ManageChildren = () => {
  const [children, setChildren] = useState([]);
  const [newChildName, setNewChildName] = useState('');
  const [editingChild, setEditingChild] = useState(null);
  const [message, setMessage] = useState('');

  // Fetch the children data from the backend
  useEffect(() => {
    const fetchChildren = async () => {
      try {
        const response = await axios.get('http://127.0.0.1:5000/children');
        setChildren(response.data);
      } catch (error) {
        console.error('Error fetching children:', error);
        setMessage('Error fetching children.');
      }
    };

    fetchChildren();
  }, []);

  // Function to handle adding a child
  const handleAddChild = async () => {
    if (!newChildName) {
      setMessage('Child name is required.');
      return;
    }

    try {
      const response = await axios.post('http://127.0.0.1:5000/children', { name: newChildName });
      setChildren([...children, { id: response.data.id, name: newChildName }]); // Append the new child to the list
      setNewChildName('');
      setMessage('Child added successfully!');
    } catch (error) {
      console.error('Error adding child:', error);
      setMessage('Error adding child.');
    }
  };

  // Function to handle deleting a child
  const handleDeleteChild = async (childId) => {
    try {
      await axios.delete(`http://127.0.0.1:5000/children/${childId}`);
      setChildren(children.filter((child) => child.id !== childId)); // Remove the child from the list
      setMessage('Child deleted successfully!');
    } catch (error) {
      console.error('Error deleting child:', error);
      setMessage('Error deleting child.');
    }
  };

  // Function to handle modifying a child
  const handleModifyChild = async (child) => {
    if (!editingChild || editingChild.name.trim() === '') {
      setMessage('Child name is required.');
      return;
    }

    try {
      await axios.put(`http://127.0.0.1:5000/children/${child.id}`, { name: editingChild.name });
      setChildren(children.map((c) => (c.id === child.id ? { ...c, name: editingChild.name } : c))); // Update the modified child in the list
      setEditingChild(null);
      setMessage('Child modified successfully!');
    } catch (error) {
      console.error('Error modifying child:', error);
      setMessage('Error modifying child.');
    }
  };

  // Function to handle clicking on the "Modify" button
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
              <input
                type="text"
                className="child-input"
                value={editingChild.name}
                onChange={(e) => setEditingChild({ ...editingChild, name: e.target.value })}
              />
            ) : (
              <span className="child-name">{child.name}</span>
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

      {/* Add new child section */}
      <div className="add-child-section">
        <input
          type="text"
          placeholder="Tanuló neve"
          value={newChildName}
          className="new-child-input"
          onChange={(e) => setNewChildName(e.target.value)}
        />
        <button className="btn add-btn" onClick={handleAddChild}>Hozzáadás</button>
      </div>
    </div>
  );
};

export default ManageChildren;
