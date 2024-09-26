import React from 'react';

const NotFoundPage = () => {
  return (
    <div style={{ textAlign: 'center', marginTop: '50px' }}>
      <h1>404 - Class Not Found</h1>
      <p>Oops! The class you're looking for doesn't exist.</p>
      <a href="/">Go back to home</a>
    </div>
  );
};

export default NotFoundPage;
