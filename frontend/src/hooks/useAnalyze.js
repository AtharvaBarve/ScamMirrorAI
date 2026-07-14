import { useState } from 'react';
import axios from 'axios';

/**
 * Hook to send analysis request to backend.
 * Returns { data, loading, error, execute }
 */
const useAnalyze = () => {
  const [data, setData] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  const execute = async (payload) => {
    setLoading(true);
    setError(null);
    try {
      const response = await axios.post('/api/v1/analyze', payload);
      setData(response.data);
      return response.data;
    } catch (err) {
      // Axios error
      if (err.response) {
        // Server responded with error status
        setError(
          err.response.data?.detail ||
            err.response.statusText ||
            'An error occurred'
        );
      } else if (err.request) {
        // No response received
        setError('Network error – cannot reach server');
      } else {
        // Other error
        setError(err.message);
      }
      return null;
    } finally {
      setLoading(false);
    }
  };

  return { data, loading, error, execute };
};

export default useAnalyze;