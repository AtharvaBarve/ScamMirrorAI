import { useState } from 'react';
import axios from 'axios';

// Configure base URL for production deployment
if (import.meta.env.VITE_API_URL) {
  axios.defaults.baseURL = import.meta.env.VITE_API_URL;
}
import { useAnalysis } from '../context/AnalysisContext';

/**
 * Hook to send analysis request to backend.
 * Returns { data, loading, error, execute }
 * Also updates the global AnalysisContext
 */
const useAnalyze = () => {
  const { setAnalysis, setIsLoading } = useAnalysis();
  const [data, setData] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  const execute = async (payload) => {
    setError(null);
    setLoading(true);
    setIsLoading(true);
    try {
      const response = await axios.post('/api/v1/analyze', payload);
      // Update both local state and global context
      setData(response.data);
      setAnalysis(response.data);
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
      // Set local state to null on error
      setData(null);
      setAnalysis(null);
      return null;
    } finally {
      setLoading(false);
      setIsLoading(false);
    }
  };

  return { data, loading, error, execute };
};

export default useAnalyze;
