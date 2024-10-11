import React, { useState } from 'react';
import { useNavigate, useParams } from 'react-router-dom';
import '../App.css'; // Ensure that the CSS file is imported

const ChildLogin = () => {
  const { className, childName } = useParams();
  const [pinCode, setPinCode] = useState('');
  const [message, setMessage] = useState('');
  const navigate = useNavigate();

  const apiUrl = process.env.REACT_APP_API_URL || `${window.location.protocol}//${window.location.hostname}${window.location.port ? ':' + window.location.port : ''}/auth`;

  const handleLogin = async (e) => {
    e.preventDefault(); // Prevent the default form submission
    setMessage(''); // Reset the message

    try {
      const response = await fetch(`${apiUrl}/${className}/${childName}/verify-pin`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ pin_code: pinCode }),
        credentials: 'include' // Include session cookie
      });

      if (response.ok) {
        localStorage.setItem(`${className}_${childName}_authenticated`, 'true');
        navigate(`/${className}/${childName}`);
      } else {
        const data = await response.json();
        setMessage(data.error || 'Invalid PIN');
      }
    } catch (error) {
      console.error('Error verifying PIN:', error);
      setMessage('Something went wrong, please try again.');
    }
  };

  return (
    <div className="login-container">
      <h1>Belépés</h1>
      <form onSubmit={handleLogin} className="login-form">
        <input
          type="password"
          value={pinCode}
          onChange={(e) => setPinCode(e.target.value)}
          maxLength="4"
          placeholder="PIN kód"
          className="pin-input"
          required
        />
        <button type="submit" className="login-button">Gyerünk!</button>
      </form>
      {message && <p className="error-message">{message}</p>}
    </div>
  );
};

export default ChildLogin;
