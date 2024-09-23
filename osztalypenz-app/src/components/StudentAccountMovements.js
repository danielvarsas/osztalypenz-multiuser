import React, { useState, useEffect } from 'react';
import { useParams } from 'react-router-dom';
import axios from 'axios';
import '../App.css';

const StudentAccountMovements = () => {
  const { className, studentId } = useParams(); // Get className and studentId from URL
  const [movements, setMovements] = useState([]);
  const [balance, setBalance] = useState(0); // State to store the balance

  const apiUrl = process.env.REACT_APP_API_URL || `${window.location.protocol}//${window.location.hostname}:5000`;

  useEffect(() => {
    const fetchMovements = async () => {
      try {
        // Fetch movements for a specific student
        const response = await axios.get(`${apiUrl}/${className}/student/${studentId}/account-movements`);
        setMovements(response.data);

        // Calculate the balance for this student
        const calculatedBalance = response.data.reduce((acc, movement) => {
          const amount = parseFloat(movement.amount) || 0;
          return movement.type === 'add' ? acc + amount : acc - amount;
        }, 0);

        setBalance(calculatedBalance); // Update the balance state
      } catch (error) {
        console.error('Error fetching account movements:', error);
      }
    };

    fetchMovements();
  }, [className, studentId]); // Re-run when className or studentId changes

  const getRowStyle = (reason) => {
    return reason === 'Befizetés' ? { backgroundColor: '#4297a0' } : { backgroundColor: '#e57f84' };
  };

  const formatAmount = (amount) => {
    return `${Math.round(amount)} Ft`;
  };

  return (
    <section>
      <h1>Pénzmozgások a diák részére</h1>
      {/* Display the balance for the student */}
      <h2 style={{ textAlign: 'center', color: 'black', margin: '20px 0' }}>Diák egyenleg: {formatAmount(balance)}</h2>
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
