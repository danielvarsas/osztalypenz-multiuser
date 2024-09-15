import React from 'react';
import { useNavigate } from 'react-router-dom';
import '../App.css'; // Import the new CSS file

const AccountantDashboard = () => {
  const navigate = useNavigate();

  return (
    <div>
      {/* Header Section */}
      <header className="app-header">
        <h1>Osztalype.nz 1.0 Beta</h1>
      </header>
      
      {/* Button Container */}
      <div className="button-container">
        <button className="big-button" onClick={() => navigate('/add-money')}>Befizetés</button>
        <button className="take-money-button" onClick={() => navigate('/take-money')}>Kifizetés</button> {/* Updated class */}
        <button className="small-button" onClick={() => navigate('/account-movements')}>Pénzmozgások</button>
        <button className="small-button" onClick={() => navigate('/manage-children')}>Tanulók</button>
      </div>
    </div>
  );
};

export default AccountantDashboard;
