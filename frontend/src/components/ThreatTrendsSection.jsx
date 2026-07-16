import React, { useState, useEffect } from 'react';

const ThreatTrendsSection = () => {
  const [trendingThreats, setTrendingThreats] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    // Simulate fetching trending threats from backend
    // In a real app, this would be an API call to /api/v1/threats/trending
    const mockData = [
      { id: 1, name: 'Phishing Attack', trend: 'up', change: 23, color: '#ff6b6b' },
      { id: 2, name: 'Fake Invoice Scam', trend: 'up', change: 18, color: '#ffd93d' },
      { id: 3, name: 'Tech Support Scam', trend: 'down', change: -12, color: '#6bcb77' },
      { id: 4, name: 'Investment Scam', trend: 'up', change: 31, color: '#4d96ff' },
      { id: 5, name: 'Romance Scam', trend: 'stable', change: 2, color: '#a29bfe' },
      { id: 6, name: 'Lottery Scam', trend: 'down', change: -8, color: '#fd79a8' },
    ];

    // Simulate network delay
    setTimeout(() => {
      setTrendingThreats(mockData);
      setLoading(false);
    }, 800);
  }, []);

  if (loading) {
    return (
      <div className='text-center py-12'>
        <div className='flex justify-center space-x-3'>
          <div className='h-4 w-4 bg-gray-400 rounded-full animate-pulse'></div>
          <div className='h-4 w-4 bg-gray-400 rounded-full animate-pulse'></div>
          <div className='h-4 w-4 bg-gray-400 rounded-full animate-pulse'></div>
        </div>
        <p className='mt-4 text-gray-400'>Loading threat trends...</p>
      </div>
    );
  }

  return (
    <div className='bg-[#111113/50] backdrop-blur-sm rounded-2xl border border-[#111113/30] p-6'>
      <h3 className='text-xl font-bold text-white flex items-center mb-6'>
        <span className='mr-2'>📈</span>
        Threat Trends
      </h3>

      <p className='text-gray-300 mb-6'>
        Current trending scam categories in our threat intelligence network
      </p>

      <div className='space-y-4'>
        {trendingThreats.map((threat) => (
          <div key={threat.id} className='flex items-center p-4 bg-[#111113/30] rounded-xl transition-all duration-300 hover:bg-[#111113/40]'>
            <div className='flex-shrink-0'>
              <div className={`w-8 h-8 flex items-center justify-center rounded-full bg-[#111113/40] ${threat.color}20`}>
                <span className='text-xs font-bold'>{threat.name.charAt(0)}</span>
              </div>
            </div>
            <div className='flex-1 ml-4'>
              <h4 className='font-semibold text-white mb-1'>{threat.name}</h4>
              <div className='flex items-center text-sm'>
                <span className={`flex-items-center mr-3 ${threat.trend === 'up' ? 'text-red-400' : threat.trend === 'down' ? 'text-green-400' : 'text-yellow-400'}`}>
                  {threat.trend === 'up' ? '▲' : threat.trend === 'down' ? '▼' : '→'}
                  {Math.abs(threat.change)}%
                </span>
                <span className='text-gray-400'>last 24h</span>
              </div>
            </div>
            <div className='flex-shrink-0'>
              <div className={`w-2 h-2 rounded-full ${threat.color}`} />
            </div>
          </div>
        ))}
      </div>

      <div className='mt-6 pt-4 border-t border-[#111113/20] text-sm text-gray-400'>
        <p>
          <span className='text-red-400'>▲</span> Increasing threat |
          <span className='text-green-400'>▼</span> Decreasing threat |
          <span className='text-yellow-400'>→</span> Stable threat
        </p>
      </div>
    </div>
  );
};

export default ThreatTrendsSection;
