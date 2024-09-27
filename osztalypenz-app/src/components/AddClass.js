import React, { useState, useEffect } from 'react';
import axios from 'axios';

const AddClass = () => {
  const [className, setClassName] = useState(''); // State to store the class name
  const [adminEmail, setAdminEmail] = useState(''); // State to store the admin email
  const [pin_code, setPin] = useState(''); // State to store the PIN
  const [message, setMessage] = useState(''); // State to store success/error messages
  const [classes, setClasses] = useState([]); // State to store class list
  const [editingClass, setEditingClass] = useState(null); // State to store the class being edited
  const [newEmail, setNewEmail] = useState(''); // State to store the new email being edited
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
  if (!className || !adminEmail || !pin_code) {
    setMessage('Class name, email, and PIN are required.');
    return;
  }

  // Make a POST request to the backend to create a new class
  axios
    .post(`${apiUrl}/create-class`, {
      class_name: className,
      admin_email: adminEmail,
      pin_code: pin_code,
    })
    .then((response) => {
      setMessage(response.data.message || 'Class created successfully!');
      setClassName(''); // Clear the input fields after adding
      setAdminEmail('');
      setPin('');
      setClasses([...classes, { class_name: className, admin_email: adminEmail }]); // Add the new class to the list
    })
    .catch((error) => {
      // Check if the response has a specific error message
      if (error.response && error.response.data && error.response.data.error) {
        setMessage(error.response.data.error); // Display backend error message
      } else {
        setMessage('Error creating class. Please try again.'); // Fallback message
      }
    });
};


  // Function to handle deleting a class
  const handleDeleteClass = (classNameToDelete) => {
    if (window.confirm(`Are you sure you want to delete the class: ${classNameToDelete}?`)) {
      // Add the API call to delete the class
      axios
        .delete(`${apiUrl}/classes/${classNameToDelete}`)
        .then(() => {
          setMessage(`Class '${classNameToDelete}' deleted successfully.`);
          setClasses(classes.filter((cls) => cls.class_name !== classNameToDelete)); // Remove the deleted class from the list
        })
        .catch((error) => {
          console.error('Error deleting class:', error);
          setMessage('Error deleting class. Please try again.');
        });
    }
  };

  // Function to handle modifying the admin email
  const handleEditClass = (className, adminEmail) => {
    setEditingClass(className);
    setNewEmail(adminEmail);
  };

  // Function to save the updated email
  const handleSaveEmail = (className) => {
    if (!newEmail) {
      setMessage('Email is required.');
      return;
    }

    axios
      .put(`${apiUrl}/update-class-admin`, { class_name: className, admin_email: newEmail })
      .then((response) => {
        setMessage(response.data.message);
        setEditingClass(null); // Reset the editing state
        setClasses(
          classes.map((cls) =>
            cls.class_name === className ? { ...cls, admin_email: newEmail } : cls
          )
        ); // Update the email in the list
      })
      .catch((error) => {
        console.error('Error updating email:', error);
        setMessage('Error updating email. Please try again.');
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
      <input
        type="text"
        placeholder="Enter admin email"
        value={adminEmail}
        onChange={(e) => setAdminEmail(e.target.value)} // Update adminEmail state on input change
      />
      <input
        type="password"
        placeholder="Enter PIN"
        value={pin_code}
        onChange={(e) => setPin(e.target.value)} // Update PIN state on input change
      />
      <button onClick={handleAddClass}>Create Class</button>
      {message && <p>{message}</p>} {/* Display success/error messages */}

      <h2>Existing Classes</h2>
      <ul>
        {classes.map((cls) => (
          <li key={cls.class_name}>
            <span>{cls.class_name}</span>
            {editingClass === cls.class_name ? (
              <>
                <input
                  type="text"
                  value={newEmail}
                  onChange={(e) => setNewEmail(e.target.value)}
                  placeholder="Enter new email"
                />
                <button onClick={() => handleSaveEmail(cls.class_name)}>Save</button>
                <button onClick={() => setEditingClass(null)}>Cancel</button>
              </>
            ) : (
              <>
                <span> | Admin Email: {cls.admin_email || 'No email'}</span>
                <button onClick={() => handleEditClass(cls.class_name, cls.admin_email)}>Edit Email</button>
                <button onClick={() => handleDeleteClass(cls.class_name)}>Delete</button>
              </>
            )}
          </li>
        ))}
      </ul>
    </div>
  );
};

export default AddClass;
