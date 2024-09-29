import React, { useEffect, useState } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import '../App.css';

const AccountantDashboard = () => {
  const { className } = useParams(); 
  const navigate = useNavigate(); 
  const [classExists, setClassExists] = useState(null); // null: loading, true: exists, false: doesn't exist
  const apiUrl = process.env.REACT_APP_API_URL || `${window.location.protocol}//${window.location.hostname}${window.location.port ? ':' + window.location.port : ''}/api`;

  // Function to check if class exists
  const checkClassExists = async () => {
    try {
      const response = await fetch(`${apiUrl}/classes/${className}`); // Make API request to check class existence
      if (response.status === 200) {
        setClassExists(true);  // Class exists
      } else {
        setClassExists(false); // Class doesn't exist
      }
    } catch (error) {
      console.error('Error checking class existence:', error);
      setClassExists(false);  // On error, assume class doesn't exist
    }
  };

  // useEffect hook to check if the class exists when the component mounts
  useEffect(() => {
    checkClassExists();
  }, [className]);

  // Show loading state while checking
  if (classExists === null) {
    return <div>Loading...</div>;
  }

  // If class doesn't exist, redirect to a "Not Found" page or show an error
  if (!classExists) {
    return <div>Class not found. Redirecting...</div>; // Show a message
    // Optionally, redirect:
    // useNavigate('/not-found');
  }

  // If class exists, render the dashboard
  return (
    <div>
      {/* Header Section */}
      <header className="app-header">
        <h1>{className} Dashboard</h1>
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
