import React, { useState } from 'react';
import { useNavigate, useParams } from 'react-router-dom';
import '../App.css';

const Login = () => {
  const [pin, setPin] = useState('');
  const [error, setError] = useState('');
  const navigate = useNavigate();
  const { className } = useParams(); // Get the class name from the URL
  const apiUrl = process.env.REACT_APP_API_URL || `${window.location.protocol}//${window.location.hostname}${window.location.port ? ':' + window.location.port : ''}/auth`;

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError(''); // Reset the error before starting

    try {
      const response = await fetch(`${apiUrl}/${className}/verify-pin`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ pin_code: pin }),
        credentials: 'include' // Make sure the session cookie is included
      });

      const data = await response.json();
      if (response.ok) {
        navigate(`/${className}/dashboard`); // Redirect to the dashboard if login is successful
      } else {
        setError(data.error || 'PIN verification failed.');
      }
    } catch (error) {
      setError('Something went wrong, please try again.');
    }
  };

  return (
    <div className="login-container">
      <h1>Belépés</h1>
      <form onSubmit={handleSubmit}>
        <input
          type="password"
          value={pin}
          onChange={(e) => setPin(e.target.value)}
          maxLength="4"
          placeholder="PIN kód"
          className="pin-input"
          required
        />
        <button type="submit" className="login-button">Gyerünk!</button>
      </form>
      {error && <p className="error-message">{error}</p>}
    </div>
  );
};

export default Login;
