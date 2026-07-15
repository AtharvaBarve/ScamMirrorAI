import React, { useState } from 'react';

const CommunityIntelligenceSection = ({ result }) => {
  // Mock data for demonstration - would come from backend in real implementation
  const threatFamily = result.category || 'Financial Scam';
  const reportedCount = Math.floor(Math.random() * 1247) + 850; // Mock data
  const trend = Math.random() > 0.5 ? 'up' : 'down';
  const trendPercent = Math.floor(Math.random() * 15) + 2;
  const firstSeen = '2024-03-15';
  const lastSeen = new Date().toISOString().split('T')[0];

  // Determine threat campaign status based on trend and severity
  const getThreatStatus = () => {
    if (trend === 'up' && trendPercent > 20) return { text: 'RAPIDLY GROWING', color: '#FF4D6D' };
    if (trend === 'up' && trendPercent > 10) return { text: 'GROWING', color: '#FFB703' };
    if (trend === 'down' && trendPercent > 15) return { text: 'DECLINING', color: '#22C55E' };
    if (trend === 'up') return { text: 'STEADY GROWTH', color: '#FFB703' };
    return { text: 'STABLE', color: '#22C55E' };
  };

  const threatStatus = getThreatStatus();

  return (
    <div className='bg-[#111113/50] backdrop-blur-sm rounded-2xl border border-[#111113/30] p-6'>
      <h3 className='text-xl font-bold text-white flex items-center mb-4'>
        <span className='mr-2'>👥</span>
        Community Threat Intelligence
      </h3>

      <div className='space-y-4'>
        <div className='flex items-center justify-between text-gray-300'>
          <span>Threat Family</span>
          <span className='font-semibold text-white'>{threatFamily}</span>
        </div>

        <div className='flex items-center justify-between text-gray-300'>
          <span>Reported Cases</span>
          <span className='font-semibold text-white'>{reportedCount.toLocaleString()}+</span>
        </div>

        <div className='flex items-center justify-between text-gray-300'>
          <span>Trend (30d)</span>
          <span className={`font-semibold text-white flex items-center space-x-1`}>
            {trend === 'up' ? '📈' : '📉'}
            {trend === 'up' ? `+${trendPercent}%` : `-${trendPercent}%`}
          </span>
        </div>

        <div className='flex items-center justify-between text-gray-300 text-sm'>
          <span>First Seen</span>
          <span>{firstSeen}</span>
        </div>

        <div className='flex items-center justify-between text-gray-300 text-sm'>
          <span>Last Seen</span>
          <span>{lastSeen}</span>
        </div>

        <div className='flex items-center justify-between text-gray-300'>
          <span>Threat Campaign Status</span>
          <span className={`font-semibold text-white flex items-center space-x-1`}>
            <span className={`text-[${threatStatus.color}]`}>
              {threatStatus.text}
            </span>
          </span>
        </div>
      </div>

      <div className='mt-4 pt-3 border-t border-[#111113/20]'>
        <button className='w-full text-left text-gray-300 hover:text-white hover:bg-[#111113/20] rounded-lg px-4 py-2 transition-colors flex items-center space-x-2'>
          <span className='mr-2'>🛡️</span>
          <span>Learn how to protect against this threat</span>
        </button>
      </div>
    </div>
  );
};

export default CommunityIntelligenceSection;