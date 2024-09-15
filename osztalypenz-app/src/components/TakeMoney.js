import React, { useState } from 'react';
import axios from 'axios';
import '../App.css'; // Import the updated CSS file

const TakeMoney = () => {
  const [amount, setAmount] = useState('');
  const [reason, setReason] = useState('');
  const [message, setMessage] = useState('');

  const handleTakeMoney = async () => {
    setMessage('');

    if (!amount || !reason) {
      setMessage('Amount and reason are required.');
      return;
    }

    try {
      const response = await axios.post('http://127.0.0.1:5000/take-money', { amount: amount, reason: reason });
      setMessage(response.data.message);
    } catch (error) {
      setMessage('Error taking money');
    }
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
    </div>
  );
};

export default TakeMoney;
