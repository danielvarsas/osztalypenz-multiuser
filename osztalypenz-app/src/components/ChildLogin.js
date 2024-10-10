import React, { useState } from 'react';
import { useNavigate, useParams } from 'react-router-dom';
import axios from 'axios';

const ChildLogin = () => {
  const { className, childName } = useParams();
  const [pinCode, setPinCode] = useState('');
  const [message, setMessage] = useState('');
  const navigate = useNavigate();

  const apiUrl = process.env.REACT_APP_API_URL || `${window.location.protocol}//${window.location.hostname}${window.location.port ? ':' + window.location.port : ''}/auth`;

  const handleLogin = async () => {
    try {
      const response = await axios.post(`${apiUrl}/${className}/${childName}/verify-pin`, { pin_code: pinCode });
      console.log("Constructed URL:", `${apiUrl}/${className}/${childName}/verify-pin`);
      
      if (response.status === 200) {
        // Assuming successful verification, store auth info
        localStorage.setItem(`${className}_${childName}_authenticated`, 'true');
        navigate(`/${className}/${childName}`);
      } else {
        setMessage('Invalid PIN');
      }
    } catch (error) {
      console.error('Error verifying PIN:', error);
      setMessage('Something went wrong, please try again.');
    }
  };

  return (
    <div>
      <h1>Login to Access Your Account</h1>
      <input
        type="password"
        value={pinCode}
        onChange={(e) => setPinCode(e.target.value)}
        placeholder="Enter your PIN"
      />
      <button onClick={handleLogin}>Login</button>
      {message && <p>{message}</p>}
    </div>
  );
};

export default ChildLogin;
