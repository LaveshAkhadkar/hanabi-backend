import { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import axios from 'axios';


const Login = () => {
  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');
  const [errorMessage, setErrorMessage] = useState(null);  // State for error messages
  const navigate = useNavigate();

  const handleLogin = async (e) => {
    e.preventDefault();
    
    const formData = new FormData();
    formData.append('username', username);
    formData.append('password', password);

    try {
      // Send login request to the backend with FormData
      const response = await axios.post('http://localhost:8000/auth/login', formData);

      // Save the access token in localStorage
      localStorage.setItem('access_token', response.data.access_token);

      // Redirect to the dashboard
      navigate('/dashboard');
      setErrorMessage(null); // Clear error message if successful
    } catch (error) {
      console.error('Error logging in:', error);
      setErrorMessage('Invalid username or password.');
    }
  };

  return (
    <div className="login-container">
      <div className="login-form">
        <h2>Login</h2>
        {errorMessage && <p className="error-message">{errorMessage}</p>} {/* Error message */}
        <form onSubmit={handleLogin}>
          <input
            type="text"
            placeholder="Username"
            value={username}
            onChange={(e) => setUsername(e.target.value)}
            className="input-field"
          />
          <input
            type="password"
            placeholder="Password"
            value={password}
            onChange={(e) => setPassword(e.target.value)}
            className="input-field"
          />
          <button type="submit" className="submit-button">Login</button>
        </form>
      </div>
    </div>
  );
};

export default Login;
