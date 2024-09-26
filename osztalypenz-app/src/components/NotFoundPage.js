import React from 'react';

const NotFoundPage = () => {
  return (
    <div style={{ textAlign: 'center', marginTop: '50px' }}>
      <h1 style={{ fontSize: '2.5rem', color: '#333' }}>A manóba... Ez az osztály nem létezik!</h1>
      <p style={{ fontSize: '1.2rem', color: '#666' }}>
        Sajnos nem találtuk meg az osztályt, amit keresel. Lehet, hogy elírtad?
      </p>
      <img 
        src="https://i.etsystatic.com/18020299/r/il/97214c/5476508908/il_570xN.5476508908_g8ne.jpg" 
        alt="Funny Not Found" 
        style={{ width: '300px', margin: '20px auto', display: 'block' }} 
      />
      <a href="/" style={{ fontSize: '1.2rem', color: '#007BFF', textDecoration: 'none' }}>
        Vissza a főoldalra
      </a>
    </div>
  );
};

export default NotFoundPage;
