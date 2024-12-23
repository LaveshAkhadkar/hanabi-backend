import { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';

const Home = () => {
  const [isLoggedIn, setIsLoggedIn] = useState(false);
  const navigate = useNavigate();

  useEffect(() => {
    // Check if the user is logged in by checking the access token in localStorage
    if (localStorage.getItem('access_token')) {
      setIsLoggedIn(true);
    }
  }, []);

  const handleLogout = () => {
    // Remove the access token and logout the user
    localStorage.removeItem('access_token');
    setIsLoggedIn(false);
    navigate('/'); // Redirect to the home page
  };

  return (
    <div>
      <h2>Home</h2>
      {!isLoggedIn ? (
        <div>
          <button onClick={() => navigate('/login')}>Login</button>
          <button onClick={() => navigate('/signup')}>Signup</button>
        </div>
      ) : (
        <div>
          <button onClick={() => navigate('/dashboard')}>Dashboard</button>
          <button onClick={handleLogout}>Logout</button>
        </div>
      )}
    </div>
  );
};

export default Home;
