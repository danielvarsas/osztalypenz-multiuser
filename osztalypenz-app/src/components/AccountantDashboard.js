import React, { useState, useEffect } from 'react';
import { useParams, useNavigate } from 'react-router-dom'; // Import useNavigate
import axios from 'axios';
import '../App.css';

const AccountantDashboard = () => {
  const { className } = useParams(); // Get the class name from the URL
  const [data, setData] = useState(null); // State to hold data
  const [error, setError] = useState(null); // State to hold errors
  const navigate = useNavigate(); // Use navigate to redirect

  const apiUrl = process.env.REACT_APP_API_URL || `${window.location.protocol}//${window.location.hostname}:5000`;

useEffect(() => {
  const fetchData = async () => {
    try {
      // Example API request to validate if the class exists
      const response = await axios.get(`${apiUrl}/${className}/account-movements`);
      setData(response.data);
    } catch (error) {
      // Check if the error is a 500 (internal server error) or 404
      if (error.response) {
        if (error.response.status === 500 || error.response.status === 404) {
          navigate('/404'); // Redirect to the 404 page on either 500 or 404 error
        } else {
          setError('An error occurred. Please try again.');
        }
      } else {
        setError('An error occurred. Please try again.');
      }
    }
  };

  fetchData();
}, [className, navigate, apiUrl]);

  if (error) {
    return <p>{error}</p>;
  }

  return (
    <div>
      {/* Header Section */}
      <header className="app-header">
        <h1>{className} Dashboard</h1>
      </header>

      {/* Render class data or some UI */}
      {data ? (
        <div className="button-container">
          <button className="big-button" onClick={() => navigate(`/${className}/add-money`)}>Befizetés</button>
          <button className="take-money-button" onClick={() => navigate(`/${className}/take-money`)}>Kifizetés</button>
          <button className="small-button" onClick={() => navigate(`/${className}/account-movements`)}>Pénzmozgások</button>
          <button className="small-button" onClick={() => navigate(`/${className}/manage-children`)}>Tanulók</button>
        </div>
      ) : (
        <p>Loading...</p> // Show a loading message while data is being fetched
      )}
    </div>
  );
};

export default AccountantDashboard;
