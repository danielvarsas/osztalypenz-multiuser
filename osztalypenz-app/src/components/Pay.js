import React from 'react';
import '../App.css'; // Import the new CSS file

const PaymentPage = () => {
  const copyToClipboard = (text) => {
    navigator.clipboard.writeText(text).then(() => {
      alert('Copied to clipboard!');
    });
  };

  return (
    <section className="payment-container" style={{ textAlign: 'left' }}>
      <h1>Fizetési lehetőségek</h1>

      {/* Bank Transfer Section */}
      <div className="payment-section" style={{ marginBottom: '20px', width: '100%' }}>
        <h2>Banki Átutalás</h2>
        <div className="payment-row">
          <span>Számlatulajdonos neve: Varsás Dániel</span>
          <button className="btn copy-btn" style={{ marginLeft: '10px' }} onClick={() => copyToClipboard('Varsás Dániel')}>Másolás</button>
        </div>
        <div className="payment-row">
          <span>Számlaszám: 11600006-00000000-97461704</span>
          <button className="btn copy-btn" style={{ marginLeft: '10px' }} onClick={() => copyToClipboard('11600006 00000000 97461704')}>Másolás</button>
        </div>
      </div>

      {/* Revolut Section */}
      <div className="payment-section" style={{ width: '100%' }}>
        <h2>Revolut </h2>
        <div className="payment-row">
          <span>Kattints az alábbi linkre a fizetéshez:</span>
          </div>
          
        <div className="payment-row">
          <a href="https://revolut.me/varsas" target="_blank" rel="noopener noreferrer" className="revolut-link">Fizetés Revoluton keresztül</a>
        </div>
        <div className="payment-row">
          <span>(Revolut számla nélkül, akár bankkártyával)</span>
        </div>
        <div className="payment-row">
          <button className="btn copy-btn" style={{ marginTop: '10px' }} onClick={() => window.open('https://revolut.com/referral/?referral-code=dnielyvaa!OCT1-24-AR-L1', '_blank')}>Revolut számlát nyitok</button>
        </div>
      </div>
    </section>
  );
};

export default PaymentPage;
