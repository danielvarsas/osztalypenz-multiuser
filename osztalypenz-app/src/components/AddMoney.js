import React, { useState, useEffect } from 'react';
import axios from 'axios';
import '../App.css'; // Import the updated CSS file

const AddMoney = () => {
  const [childId, setChildId] = useState('');
  const [amount, setAmount] = useState('');
  const [message, setMessage] = useState(''); // State to store the message
  const [children, setChildren] = useState([]);

  useEffect(() => {
    const fetchChildren = async () => {
      try {
        const response = await axios.get('http://127.0.0.1:5000/children');

        // Filter out the child with ID 1
        const filteredChildren = response.data.filter((child) => child.id !== 1);

        setChildren(filteredChildren);
      } catch (error) {
        console.error('Error fetching children:', error);
      }
    };

    fetchChildren();
  }, []);

  const handleAddMoney = async () => {
    setMessage(''); // Clear the message

    if (!childId || !amount) {
      setMessage('Child and amount are required.');
      return;
    }

    try {
      // Send request to backend
      const response = await axios.post('http://127.0.0.1:5000/add-money', { child_id: childId, amount: amount });

      // Set the message dynamically from the backend response
      setMessage(response.data.message);
    } catch (error) {
      setMessage('Error adding money');
    }
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
    </div>
  );
};

export default AddMoney;
