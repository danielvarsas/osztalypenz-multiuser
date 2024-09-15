import React from 'react';
import { BrowserRouter as Router, Route, Routes } from 'react-router-dom';
// import PinLogin from './components/Login'; // Correct path to Login component
import Dashboard from './components/AccountantDashboard'; // Correct path to AccountantDashboard component
import AddMoney from './components/AddMoney'; // Import AddMoney component
import TakeMoney from './components/TakeMoney'; // Import TakeMoney component
import AccountMovements from './components/AccountMovements'; // Import AccountMovements component
import ManageChildren from './components/ManageChildren'; // Import ManageChildren component
import AddClass from './components/AddClass'; // Import AddClass component

const App = () => {
  return (
    <Router>
      <Routes>
        <Route path="/" element={<Dashboard />} />
        <Route path="/add-class" element={<AddClass />} /> {/* Route for adding a new class */}

        <Route path="/:className/dashboard" element={<Dashboard />} />
        <Route path="/:className/manage-children" element={<ManageChildren />} />
        <Route path="/:className/account-movements" element={<AccountMovements />} />
        <Route path="/:className/add-money" element={<AddMoney />} />
        <Route path="/:className/take-money" element={<TakeMoney />} />
      </Routes>
    </Router>
  );
};

export default App;
