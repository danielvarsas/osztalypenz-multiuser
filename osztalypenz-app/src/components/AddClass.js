import React, { useState } from 'react';
import axios from 'axios';

const AddClass = () => {
  const [className, setClassName] = useState('');  // State to store the class name
  const [message, setMessage] = useState('');      // State to store success/error messages

  // Function to handle the form submission
  const handleAddClass = () => {
    if (!className) {
      setMessage('Class name is required.');
      return;
    }

    // Make a POST request to the backend to create a new class
    axios.post('http://127.0.0.1:5000/create-class', { class_name: className })
      .then((response) => {
        setMessage(response.data.message || 'Class created successfully!');
      })
      .catch((error) => {
        console.error('Error creating class:', error);
        setMessage('Error creating class. Please try again.');
      });
  };

  return (
    <div>
      <h1>Add a New Class</h1>
      <input
        type="text"
        placeholder="Enter class name"
        value={className}
        onChange={(e) => setClassName(e.target.value)} // Update className state on input change
      />
      <button onClick={handleAddClass}>Create Class</button>
      {message && <p>{message}</p>}  {/* Display success/error messages */}
    </div>
  );
};

export default AddClass;
