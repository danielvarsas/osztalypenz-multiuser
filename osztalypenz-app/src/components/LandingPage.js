import React from 'react';
import '../App.css'; // Import your CSS file for styling

const LandingPage = () => {
  return (
    <div className="landing-page" style={{ textAlign: 'center' }}>
      <h1>Ezen még dolgozok</h1>
      <img 
        src="https://media.istockphoto.com/id/1217429917/photo/do-it-yourself-home-renovation-concept-with-dog-in-hardhat-holding-hummer-in-mouth-against.jpg?s=612x612&w=0&k=20&c=lNH3LcPZ2guYBWUSM0-XjuIX9LqiFsDiOLZeT1RTlCM=" 
        alt="Dog with hardhat holding hammer"
        className="landing-image"
      />
    </div>
  );
};

export default LandingPage;