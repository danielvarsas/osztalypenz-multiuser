import React, { useState, useEffect } from 'react';
import { useParams, useNavigate } from 'react-router-dom'; // Import useNavigate for redirection
import axios from 'axios';
import '../App.css'; // Import the new CSS file

const AccountMovements = ({ isStudentView }) => {
  const { className, childName } = useParams();
  const navigate = useNavigate();
  const [movements, setMovements] = useState([]);
  const [balance, setBalance] = useState(0);

  // Check if the child is authenticated (only for student view)
  useEffect(() => {
    if (isStudentView) {
      const isAuthenticated = localStorage.getItem(`${className}_${childName}_authenticated`);
      if (!isAuthenticated) {
        navigate(`/${className}/${childName}/login`);
      }
    }
  }, [className, childName, navigate, isStudentView]);

  const apiUrl = process.env.REACT_APP_API_URL || `${window.location.protocol}//${window.location.hostname}${window.location.port ? ':' + window.location.port : ''}/api`;

  useEffect(() => {
    const fetchMovements = async () => {
      try {
        const endpoint = isStudentView 
          ? `${apiUrl}/${className}/${childName}/account-movements`
          : `${apiUrl}/${className}/account-movements`;
        const response = await axios.get(endpoint);
        setMovements(response.data);

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
  }, [className, childName, isStudentView]);

  const getRowStyle = (reason) => {
    return reason === 'Befizetés' ? { backgroundColor: '#4297a0' } : { backgroundColor: '#e57f84' };
  };

  const formatAmount = (amount) => {
    return `${Math.round(amount)} Ft`;
  };
  
  const formatDate = (dateString) => {
    const date = new Date(dateString);
    const year = date.getFullYear();
    const month = String(date.getMonth() + 1).padStart(2, '0');
    const day = String(date.getDate()).padStart(2, '0');
    return `${year}.${month}.${day}`;
  };
  
  return (
    <section>
       <h1>{isStudentView ? `${childName} - Pénzmozgások` : `${className} - Pénzmozgások`}</h1>
      <h2 style={{ textAlign: 'center', color: 'black', margin: '20px 0' }}>Egyenleg: {formatAmount(balance)}</h2>
      <div className="tbl-content">
        <table>
          <thead>
            <tr>
              {isStudentView ? (
                <>
                  <th>Befizetés / Kivét</th>
                  <th>Összeg</th>
                  <th>Ok</th>
                  <th>Dátum</th>
                </>
              ) : (
                <>
                  <th>Gyermek neve</th>
                  <th>Befizetés / Kivét</th>
                  <th>Összeg</th>
                  <th>Ok</th>
                  <th>Dátum</th>
                </>
              )}
            </tr>
          </thead>
          <tbody>
            {movements.map((movement, index) => (
              <tr key={index} style={getRowStyle(movement.reason || 'Befizetés')}>
                {!isStudentView && <td>{movement.child_name}</td>}
                <td>{movement.type === 'add' ? 'Befizetés' : 'Kivét'}</td>
                <td>{formatAmount(movement.amount)}</td>
                <td>{movement.reason || 'Befizetés'}</td>
                <td>{formatDate(movement.created_at)}</td>
              </tr>
            ))}
          </tbody>
        </table>
        
      </div>
      {/* Add "Befizetés" button for student view */}
      {isStudentView && (
        <div style={{ textAlign: 'center', marginTop: '20px' }}>
          <button className="big-button" onClick={() => navigate('/befizetes')}>Befizetés</button>
        </div>
      )}
       {!isStudentView && (
        <div style={{ textAlign: 'center', marginTop: '20px' }}>
          <button className="back-to-dashboard-button" style={{ width: '100%' }} onClick={() => navigate(`/${className}/dashboard`)}>Vissza a menübe</button>
        </div>
      )}
    </section>
  );
};

export default AccountMovements;
