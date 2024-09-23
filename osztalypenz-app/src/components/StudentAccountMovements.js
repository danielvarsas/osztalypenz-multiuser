import React, { useState, useEffect } from 'react';
import { useParams } from 'react-router-dom';
import axios from 'axios';
import '../App.css'; // Import the new CSS file

const StudentAccountMovements = () => {
  const { className, url_name } = useParams(); // Get both className and url_name from the URL
  const [movements, setMovements] = useState([]);
  const [totalPayments, setTotalPayments] = useState(0);

  const apiUrl = process.env.REACT_APP_API_URL || `${window.location.protocol}//${window.location.hostname}:5000`;

  useEffect(() => {
    const fetchMovements = async () => {
      try {
        // Fetch movements using className and url_name
        const response = await axios.get(`${apiUrl}/${className}/${url_name}/account-movements`);
        setMovements(response.data);

        // Calculate the total payments for the student
        const total = response.data.reduce((acc, movement) => {
          const amount = parseFloat(movement.amount) || 0;
          return movement.type === 'add' ? acc + amount : acc;
        }, 0);
        setTotalPayments(total);
      } catch (error) {
        console.error('Error fetching account movements:', error);
      }
    };

    fetchMovements();
  }, [className, url_name, apiUrl]);

  // Function to determine the row background color
  const getRowStyle = (reason) => {
    return reason === 'Befizetés' ? { backgroundColor: '#4297a0' } : { backgroundColor: '#e57f84' };
  };

  // Function to format the amount without decimals
  const formatAmount = (amount) => {
    return `${Math.round(amount)} Ft`; // Rounds to the nearest integer and adds "Ft"
  };

  return (
    <section>
      <h1>Pénzmozgások: {url_name}</h1>
      {/* Display the total payments */}
      <h2 style={{ textAlign: 'center', color: 'black', margin: '20px 0' }}>Teljes befizetés: {formatAmount(totalPayments)}</h2>
      <div className="tbl-header">
        <table>
          <thead>
            <tr>
              <th>Befizetés / Kivét</th>
              <th>Összeg</th>
              <th>Ok</th>
              <th>Dátum</th>
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
                <td>{new Date(movement.created_at).toLocaleDateString()}</td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </section>
  );
};

export default StudentAccountMovements;
