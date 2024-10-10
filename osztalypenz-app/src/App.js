import React from 'react';
import { BrowserRouter as Router, Route, Routes, Navigate } from 'react-router-dom';
// import PinLogin from './components/Login'; // Correct path to Login component
import Dashboard from './components/AccountantDashboard'; // Correct path to AccountantDashboard component
import AddMoney from './components/AddMoney'; // Import AddMoney component
import TakeMoney from './components/TakeMoney'; // Import TakeMoney component
import AccountMovements from './components/AccountMovements'; // Import AccountMovements component
import ManageChildren from './components/ManageChildren'; // Import ManageChildren component
import AddClass from './components/AddClass'; // Import AddClass component
import NotFoundPage from './components/NotFoundPage'; 
import Login from './components/Login';
import StudentAccountMovements from './components/StudentAccountMovements';
import Pay from './components/Pay';
import ChildLogin from './components/ChildLogin';


const App = () => {
  return (
    <Router>
      <Routes>
        <Route path="/" element={<Dashboard />} />
         <Route path="/:className/login" element={<Login />} />
        <Route path="/add-class" element={<AddClass />} /> {/* Route for adding a new class */}
        <Route path="/:className/student/:studentId" element={<StudentAccountMovements />} />
        <Route path="/404" element={<NotFoundPage />} />
        {/*  <Route path="*" element={<NotFoundPage />} /> {/* Catch-all route for non-existing URLs */}
        <Route path="/:className/dashboard" element={<Dashboard />} />
        <Route path="/:className" element={<Navigate to={`/${window.location.pathname.split('/')[1]}/dashboard`} replace />} />
        <Route path="/:className/manage-children" element={<ManageChildren />} />
        
        <Route path="/:className/account-movements" element={<AccountMovements isStudentView={false} />} />
        <Route path="/:className/:childName" element={<AccountMovements isStudentView={true} />} />
        
        <Route path="/:className/add-money" element={<AddMoney />} />
        <Route path="/:className/take-money" element={<TakeMoney />} />
        
        <Route path="/:className/:childName/login" element={<ChildLogin />} />


        
        <Route path="/befizetes" element={<Pay />} /> {/* New route for the Pay page */}
      </Routes>
    </Router>
  );
};

export default App;
