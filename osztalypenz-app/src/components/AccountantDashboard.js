import React, { useEffect, useState } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import '../App.css';

const AccountantDashboard = () => {
  const { className } = useParams(); 
  const navigate = useNavigate(); 
  const [classExists, setClassExists] = useState(null); // null: loading, true: exists, false: doesn't exist
  const [authorized, setAuthorized] = useState(false); // To track if the user is authorized
  const apiUrl = process.env.REACT_APP_API_URL || `${window.location.protocol}//${window.location.hostname}${window.location.port ? ':' + window.location.port : ''}/api`;

  // Function to check if class exists
  const checkClassExists = async () => {
    try {
      const response = await fetch(`${apiUrl}/classes/${className}`);
      if (response.status === 200) {
        setClassExists(true);
      } else {
        setClassExists(false);
      }
    } catch (error) {
      console.error('Error checking class existence:', error);
      setClassExists(false);
    }
  };

  // Function to check if the user is authenticated
  const checkAuthorization = async () => {
    try {
      const response = await fetch(`${apiUrl}/${className}/dashboard`, {
        method: 'GET',
        credentials: 'include', // Include the session cookie
      });

      if (response.status === 403) {
        // Not authorized, redirect to login page
        navigate(`/${className}/login`);
      } else {
        setAuthorized(true); // User is authorized
      }
    } catch (error) {
      console.error('Error checking authorization:', error);
      navigate(`/${className}/login`);
    }
  };

  // Check if the class exists and if the user is authorized
  useEffect(() => {
    checkClassExists();
    checkAuthorization(); // Check authorization after checking class existence
  }, [className]);

  // Show loading state while checking class and authorization
  if (classExists === null || !authorized) {
    return <div>Loading...</div>;
  }

  // If class doesn't exist, redirect to a "Not Found" page or show an error
  if (!classExists) {
    return <div>Class not found. Redirecting...</div>;
  }

  // If class exists and user is authorized, render the dashboard
  return (
    <div>
      {/* Header Section */}
      <header className="app-header">
        <h1>Osztálypénz - {className}</h1>
      </header>

      {/* Render buttons for navigation */}
      <div className="button-container">
        <button className="big-button" onClick={() => navigate(`/${className}/add-money`)}>Befizetés</button>
        <button className="take-money-button" onClick={() => navigate(`/${className}/take-money`)}>Kifizetés</button>
        <button className="small-button" onClick={() => navigate(`/${className}/account-movements`)}>Pénzmozgások</button>
        <button className="small-button" onClick={() => navigate(`/${className}/manage-children`)}>Tanulók</button>
      </div>
    </div>
  );
};

export default AccountantDashboard;
