import React from 'react';
import { BrowserRouter as Router, Route, Routes } from 'react-router-dom';
// import PinLogin from './components/Login'; // Correct path to Login component
import Dashboard from './components/AccountantDashboard'; // Correct path to AccountantDashboard component
import AddMoney from './components/AddMoney'; // Import AddMoney component
import TakeMoney from './components/TakeMoney'; // Import TakeMoney component
import AccountMovements from './components/AccountMovements'; // Import AccountMovements component
import ManageChildren from './components/ManageChildren'; // Import ManageChildren component

const App = () => {
  return (
    <Router>
      <Routes>
        <Route path="/" element={<Dashboard />} />
        <Route path="/dashboard" element={<Dashboard />} />
        <Route path="/add-money" element={<AddMoney />} />
        <Route path="/take-money" element={<TakeMoney />} />
        <Route path="/account-movements" element={<AccountMovements />} />
        <Route path="/manage-children" element={<ManageChildren />} />
      </Routes>
    </Router>
  );
};

export default App;
