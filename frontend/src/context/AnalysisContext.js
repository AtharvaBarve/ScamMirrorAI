import React, { createContext, useContext, useState, useEffect } from 'react';
import { get, set } from '../services/cache_service';

const AnalysisContext = createContext();

// Custom hook to use the analysis context
export const useAnalysis = () => {
  const context = useContext(AnalysisContext);
  if (!context) {
    throw new Error('useAnalysis must be used within an AnalysisProvider');
  }
  return context;
};

// Provider component
export const AnalysisProvider = ({ children }) => {
  const [analysisResult, setAnalysisResult] = useState(null);
  const [loading, setLoading] = useState(false);

  // Function to set analysis result from anywhere in the app
  const setAnalysis = (result) => {
    setAnalysisResult(result);
    // Also cache it for potential reuse
    // Note: In a real app, we'd have a proper cache key based on input
    set('latest_analysis', result);
  };

  // Function to get current analysis
  const getAnalysis = () => analysisResult;

  // Function to set loading state
  const setIsLoading = (isLoading) => {
    setLoading(isLoading);
  };

  // Function to get loading state
  const getIsLoading = () => loading;

  // Attempt to load cached analysis on startup
  useEffect(() => {
    const cached = get('latest_analysis');
    if (cached) {
      setAnalysisResult(cached);
    }
  }, []);

  const contextValue = {
    analysisResult,
    setAnalysis,
    getAnalysis,
    loading,
    setIsLoading,
    getIsLoading
  };

  return React.createElement(
    AnalysisContext.Provider,
    { value: contextValue },
    children
  );
};
