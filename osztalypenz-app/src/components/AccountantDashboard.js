import React from 'react';
import { useNavigate, useParams } from 'react-router-dom';
import '../App.css'; // Import the new CSS file

const AccountantDashboard = () => {
  const navigate = useNavigate();
  const { className } = useParams(); // Get the class name from the URL

  return (
    <div>
      {/* Header Section */}
      <header className="app-header">
        <h1>Osztalype.nz 1.0 Beta</h1>
      </header>
      
      {/* Button Container */}
      <div className="button-container">
        <button className="big-button" onClick={() => navigate(`/${className}/add-money`)}>Befizetés</button>
        <button className="take-money-button" onClick={() => navigate(`/${className}/take-money`)}>Kifizetés</button> {/* Updated class */}
        <button className="small-button" onClick={() => navigate(`/${className}/account-movements`)}>Pénzmozgások</button>
        <button className="small-button" onClick={() => navigate(`/${className}/manage-children`)}>Tanulók</button>
      </div>
    </div>
  );
};

export default AccountantDashboard;
