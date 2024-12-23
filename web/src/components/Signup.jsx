import { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import axios from 'axios';


const Signup = () => {
  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');
  const [errorMessage, setErrorMessage] = useState(null); // State for error messages
  const navigate = useNavigate();

  const handleSignup = async (e) => {
    e.preventDefault();

    // Check if both username and password are provided
    if (!username || !password) {
      setErrorMessage('Both username and password are required.');
      return;
    }

    const formData = new FormData();
    formData.append('username', username);
    formData.append('password', password);

    try {
      // Send signup request to the backend using FormData
      await axios.post('https://hanabi-backend-ltfq.onrender.com/auth/signup', formData, {
        headers: {
          'Content-Type': 'multipart/form-data', // Set proper content type for form data
        },
      });

      // Redirect to login page after successful signup
      navigate('/login');
      setErrorMessage(null); // Clear error message if successful
    } catch (error) {
      console.error('Error signing up:', error);
      // Check if it's a field-related error and provide a specific message
      if (error.response && error.response.data && error.response.data.detail) {
        const fieldErrors = error.response.data.detail.map((err) => err.msg).join(', ');
        setErrorMessage(`Error: ${fieldErrors}`);
      } else {
        setErrorMessage('An unexpected error occurred. Please try again.');
      }
    }
  };

  return (
    <div>
      <h2>Signup</h2>
      {errorMessage && <p style={{ color: 'red' }}>{errorMessage}</p>} {/* Error message */}
      <form onSubmit={handleSignup}>
        <input
          type="text"
          placeholder="Username"
          value={username}
          onChange={(e) => setUsername(e.target.value)}
        />
        <input
          type="password"
          placeholder="Password"
          value={password}
          onChange={(e) => setPassword(e.target.value)}
        />
        <button type="submit">Signup</button>
      </form>
    </div>
  );
};

export default Signup;
