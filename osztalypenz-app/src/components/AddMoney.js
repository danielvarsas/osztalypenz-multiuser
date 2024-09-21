import React, { useState, useEffect } from 'react';
import { useParams, useNavigate } from 'react-router-dom'; // Import useParams and useNavigate
import axios from 'axios';
import '../App.css'; // Import the updated CSS file

const AddMoney = () => {
  const { className } = useParams(); // Get the class name from the URL
  const navigate = useNavigate(); // Use navigate to handle redirection
  const [childId, setChildId] = useState('');
  const [amount, setAmount] = useState('');
  const [message, setMessage] = useState(''); // State to store the message
  const [children, setChildren] = useState([]);
  const apiUrl = process.env.REACT_APP_API_URL || `${window.location.protocol}//${window.location.hostname}:5000`;

  useEffect(() => {
    const fetchChildren = async () => {
      try {
        const response = await axios.get(`${apiUrl}/${className}/children`);

        // Filter out the soft-deleted children (isDeleted = true) and child with ID 1
        const filteredChildren = response.data.filter(
          (child) => child.id !== 1 && !child.isDeleted
        );

        setChildren(filteredChildren);
      } catch (error) {
        console.error('Error fetching children:', error);
      }
    };

    fetchChildren();
  }, [className]); // Add className as a dependency to re-run when it changes

  const handleAddMoney = async () => {
    setMessage(''); // Clear the message

    if (!childId || !amount) {
      setMessage('Child and amount are required.');
      return;
    }

    try {
      // Send request to backend with dynamic URL
      const response = await axios.post(`http://127.0.0.1:5000/${className}/add-money`, { child_id: childId, amount: amount });

      // Set the message dynamically from the backend response
      setMessage(response.data.message);

      // Reset the form fields after successful addition
      setChildId(''); // Reset child selection to default
      setAmount(''); // Clear amount input field
    } catch (error) {
      setMessage('Error adding money');
    }
  };

  const handleBackToDashboard = () => {
    navigate(`/${className}/dashboard`); // Navigate back to the dashboard
  };

  return (
    <div className="money-container">
      <h2>Befizetés</h2>
      <div className="dropdown-container">
        <select
          value={childId}
          onChange={(e) => setChildId(e.target.value)}
          className="add-money-dropdown-button"
        >
          <option value="">Tanuló kiválasztása</option>
          {children.map((child) => (
            <option key={child.id} value={child.id}>
              {child.name}
            </option>
          ))}
        </select>
      </div>
      <div className="input-container">
        <input
          type="number"
          placeholder="Összeg"
          value={amount}
          onChange={(e) => setAmount(e.target.value)}
          className="amount-input"
        />
        <span className="currency-inside">Ft</span>
      </div>
      <button className="add-button" onClick={handleAddMoney}>
        Befizetés
      </button>
      {message && <p>{message}</p>} {/* Display the message dynamically */}
      <button 
        className="back-to-dashboard-button" 
        onClick={handleBackToDashboard}
      >
        Vissza a menübe
      </button>
    </div>
  );
};

export default AddMoney;
