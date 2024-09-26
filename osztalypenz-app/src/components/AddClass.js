import React, { useState, useEffect } from 'react';
import axios from 'axios';

const AddClass = () => {
  const [className, setClassName] = useState(''); // State to store the class name
  const [message, setMessage] = useState(''); // State to store success/error messages
  const [classes, setClasses] = useState([]); // State to store class list
  const apiUrl = process.env.REACT_APP_API_URL || `${window.location.protocol}//${window.location.hostname}:5000`;

  // Fetch classes when the component mounts
  useEffect(() => {
    const fetchClasses = async () => {
      try {
        const response = await axios.get(`${apiUrl}/classes`);
        setClasses(response.data); // Set fetched classes
      } catch (error) {
        console.error('Error fetching classes:', error);
        setMessage('Error fetching classes.');
      }
    };

    fetchClasses();
  }, [apiUrl]);

  // Function to handle adding a new class
  const handleAddClass = () => {
    if (!className) {
      setMessage('Class name is required.');
      return;
    }

    // Make a POST request to the backend to create a new class
    axios.post(`${apiUrl}/create-class`, { class_name: className })
      .then((response) => {
        setMessage(response.data.message || 'Class created successfully!');
        setClassName(''); // Clear the input field after adding
        setClasses([...classes, className]); // Add the new class to the list
      })
      .catch((error) => {
        console.error('Error creating class:', error);
        setMessage('Error creating class. Please try again.');
      });
  };

  // Function to handle deleting a class
  const handleDeleteClass = (classNameToDelete) => {
    if (window.confirm(`Are you sure you want to delete the class: ${classNameToDelete}?`)) {
      // Add the API call to delete the class (you will need to create the endpoint for this)
      axios.delete(`${apiUrl}/classes/${classNameToDelete}`)
        .then(() => {
          setMessage(`Class '${classNameToDelete}' deleted successfully.`);
          setClasses(classes.filter((cls) => cls !== classNameToDelete)); // Remove the deleted class from the list
        })
        .catch((error) => {
          console.error('Error deleting class:', error);
          setMessage('Error deleting class. Please try again.');
        });
    }
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

      <h2>Existing Classes</h2>
      <ul>
        {classes.map((cls) => (
          <li key={cls}>
            {cls} <button onClick={() => handleDeleteClass(cls)}>Delete</button>
          </li>
        ))}
      </ul>
    </div>
  );
};

export default AddClass;
