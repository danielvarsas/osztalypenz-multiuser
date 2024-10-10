import React, { useState, useEffect } from 'react';
import { useParams, useNavigate } from 'react-router-dom'; // Import useNavigate for redirection
import axios from 'axios';
import '../App.css'; // Import the new CSS file

const StudentAccountMovements = () => {
  const { className, childName } = useParams();
  const navigate = useNavigate();
  const [movements, setMovements] = useState([]);
  const [balance, setBalance] = useState(0);

  // Check if the child is authenticated
  useEffect(() => {
    const isAuthenticated = localStorage.getItem(`${className}_${childName}_authenticated`);
    if (!isAuthenticated) {
      navigate(`/${className}/${childName}/login`);
    }
  }, [className, childName, navigate]);

  const apiUrl = process.env.REACT_APP_API_URL || `${window.location.protocol}//${window.location.hostname}${window.location.port ? ':' + window.location.port : ''}/api`;

  useEffect(() => {
    const fetchMovements = async () => {
      try {
        const response = await axios.get(`${apiUrl}/${className}/${childName}/account-movements`);
        setMovements(response.data);

        // Calculate the balance for the child
        const calculatedBalance = response.data.reduce((acc, movement) => {
          const amount = parseFloat(movement.amount) || 0;
          return movement.type === 'add' ? acc + amount : acc - amount;
        }, 0);

        setBalance(calculatedBalance);
      } catch (error) {
        console.error('Error fetching account movements:', error);
      }
    };

    fetchMovements();
  }, [className, childName]);

  const getRowStyle = (reason) => {
    return reason === 'Befizetés' ? { backgroundColor: '#4297a0' } : { backgroundColor: '#e57f84' };
  };

  const formatAmount = (amount) => {
    return `${Math.round(amount)} Ft`; // Rounds to the nearest integer and adds "Ft"
  };

  return (
    <section>
      <h1>Pénzmozgások</h1>
      {/* Display the balance */}
      <h2 style={{ textAlign: 'center', color: 'black', margin: '20px 0' }}>Egyenleg: {formatAmount(balance)}</h2>
      <div className="tbl-header">
        <table>
          <thead>
            <tr>
              <th>Befizetés / Kivét</th>
              <th>Összeg</th>
              <th>Ok</th>
            </tr>
          </thead>
        </table>
      </div>
      <div className="tbl-content">
        <table>
          <tbody>
            {movements.map((movement, index) => (
              <tr key={index} style={getRowStyle(movement.reason || 'Befizetés')}>
                <td>{movement.type === 'add' ? 'Befizetés' : 'Kivét'}</td>
                <td>{formatAmount(movement.amount)}</td>
                <td>{movement.reason || 'Befizetés'}</td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </section>
  );
};

export default StudentAccountMovements;
