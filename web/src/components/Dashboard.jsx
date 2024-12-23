import { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { Bar, Pie } from 'react-chartjs-2';
import axios from 'axios';

import { Chart as ChartJS, CategoryScale, LinearScale, BarElement, Title, Tooltip, Legend, ArcElement } from 'chart.js';

// Register the necessary components
ChartJS.register(CategoryScale, LinearScale, BarElement, ArcElement, Title, Tooltip, Legend);


const Dashboard = () => {
  const [file, setFile] = useState(null);
  const [results, setResults] = useState(null);
  const [errorMessage, setErrorMessage] = useState(null);  // State for error messages
  const [isAuthenticated, setIsAuthenticated] = useState(false);  // State to track authentication status
  const [chartType, setChartType] = useState('bar'); // State for chart type ('bar' or 'pie')
  const navigate = useNavigate();

  useEffect(() => {
    // Check if the user is logged in, if not redirect to login page
    if (!localStorage.getItem('access_token')) {
      setIsAuthenticated(false);
      navigate('/');  // Redirect to login page if not logged in
    } else {
      setIsAuthenticated(true);
    }
  }, [navigate]);

  const handleFileChange = (e) => {
    setFile(e.target.files[0]);
  };

  const handleUpload = async () => {
    if (!file) {
      setErrorMessage('Please upload a file.');
      return;
    }
    
    const formData = new FormData();
    formData.append('file', file);

    try {
      // Make the POST request for sentiment analysis
      const response = await axios.post(
        'http://localhost:8000/sentiment/analyze', // Update with your backend endpoint
        formData,
        {
          headers: {
            'Authorization': `Bearer ${localStorage.getItem('access_token')}`, // Pass JWT token in the header
          },
        }
      );

      // Set the results from the response
      setResults(response.data.results);
      setErrorMessage(null); // Clear error message if successful
    } catch (error) {
      console.error('Error uploading file:', error);
      setErrorMessage('Error uploading file or performing sentiment analysis.');
    }
  };

  const handleLogout = () => {
    localStorage.removeItem('access_token');  // Remove the access token
    setIsAuthenticated(false);  // Update state to reflect the user is logged out
    navigate('/');  // Redirect to the home page (login page)
  };

  // Calculate sentiment counts
  const sentimentCounts = results
    ? results.reduce(
        (acc, { sentiment }) => {
          acc[sentiment] = (acc[sentiment] || 0) + 1;
          return acc;
        },
        { positive: 0, neutral: 0, negative: 0 }
      )
    : {};

  // Prepare chart data
  const chartData = {
    labels: ['Positive', 'Neutral', 'Negative'], // Correctly label the sentiment categories
    datasets: [
      {
        label: 'Sentiment Analysis', // Update to match the sentiment categories
        data: [sentimentCounts.positive, sentimentCounts.neutral, sentimentCounts.negative],
        backgroundColor: ['#4CAF50', '#FFC107', '#F44336'],
      },
    ],
  };
  

  return (
    <div>
      <h2>Dashboard</h2>
      
      {isAuthenticated ? (
        <>
          <button onClick={handleLogout}>Logout</button> {/* Logout Button */}
          <input type="file" onChange={handleFileChange} />
          <button onClick={handleUpload}>Upload CSV</button>

          {errorMessage && <p style={{ color: 'red' }}>{errorMessage}</p>} {/* Error message */}
          
          {/* Chart Type Toggle Button */}
          <div>
            <button onClick={() => setChartType('bar')}>Bar Chart</button>
            <button onClick={() => setChartType('pie')}>Pie Chart</button>
          </div>

          {results && (
            <div>
              {/* Render the selected chart type */}
              {chartType === 'bar' ? (
                <Bar data={chartData} />
              ) : (
                <Pie data={chartData} />
              )}

            <table>
              <thead>
                <tr>
                  <th>Text</th>
                  <th>Sentiment</th>
                  <th>Timestamp</th>
                </tr>
              </thead>
              <tbody>
                {results.map((item) => (
                  <tr key={item.id}>
                    <td>{item.text}</td>
                    <td>{item.sentiment}</td>
                    <td>{item.timestamp ? item.timestamp : 'N/A'}</td> {/* Display 'N/A' if no timestamp */}
                  </tr>
                ))}
              </tbody>
            </table>

            </div>
          )}
        </>
      ) : (
        <p>Please log in to access the dashboard.</p> // If not authenticated, show a message
      )}
    </div>
  );
};

export default Dashboard;
