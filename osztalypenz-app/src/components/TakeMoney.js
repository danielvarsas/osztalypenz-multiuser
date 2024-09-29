import React, { useState, useEffect } from 'react';
import { useParams, useNavigate } from 'react-router-dom'; // Import useParams to get className from URL
import axios from 'axios';
import '../App.css'; // Import the updated CSS file

const TakeMoney = () => {
  const { className } = useParams(); // Get the class name from the URL
  const [amount, setAmount] = useState('');
  const [reason, setReason] = useState('');
  const [message, setMessage] = useState('');
  const navigate = useNavigate(); // Use navigate to handle redirection
  //const apiUrl = process.env.REACT_APP_API_URL || `${window.location.protocol}//${window.location.hostname}:5000`;
  const apiUrl = process.env.REACT_APP_API_URL || `${window.location.protocol}//${window.location.hostname}${window.location.port ? ':' + window.location.port : ''}/api`;

  const handleTakeMoney = async () => {
    setMessage('');

    if (!amount || !reason) {
      setMessage('Amount and reason are required.');
      return;
    }

    try {
      // Send request to backend with dynamic URL
      const response = await axios.post(`${apiUrl}/${className}/take-money`, { amount: amount, reason: reason });
      setMessage(response.data.message);
    } catch (error) {
      setMessage('Error taking money');
    }
  };

 const handleBackToDashboard = () => {
    navigate(`/${className}/dashboard`); // Navigate back to the dashboard
  };


  return (
    <div className="money-container">
      <h2>Kivétel</h2>
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
      <div className="reason-container">
        <input
          type="text"
          placeholder="Mire lesz kivéve?"
          value={reason}
          onChange={(e) => setReason(e.target.value)}
          className="reason-input"
        />
      </div>
      <button className="take-button" onClick={handleTakeMoney}>
        Kivét
      </button>
      {message && <p>{message}</p>}
      <button 
        className="back-to-dashboard-button" 
        onClick={handleBackToDashboard}
      >
        Vissza a menübe
      </button>

    </div>
  );
};

export default TakeMoney;
