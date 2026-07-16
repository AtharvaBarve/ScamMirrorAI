import React from 'react';
import { useAnalysis } from '../../context/AnalysisContext';

const CommunityIntelligenceSection = () => {
  const { analysisResult } = useAnalysis();

  // Extract community intelligence data if available
  const communityIntelligence = analysisResult?.community_intelligence || {};

  // Fallback to category if no community intelligence
  const threatFamily = communityIntelligence.threat_family || analysisResult?.category || 'Unknown';

  // Format dates if available
  const formatDate = (dateString) => {
    if (!dateString) return 'N/A';
    try {
      // Handle ISO string from backend
      const date = new Date(dateString);
      return date.toLocaleDateString(undefined, { year: 'numeric', month: 'short', day: 'numeric' });
    } catch (e) {
      return dateString;
    }
  };

  // Calculate time ago from first seen
  const getTimeAgo = (dateString) => {
    if (!dateString) return 'N/A';
    try {
      const date = new Date(dateString);
      const now = new Date();
      const diffTime = Math.abs(now - date);
      const diffDays = Math.floor(diffTime / (1000 * 60 * 60 * 24));

      if (diffDays === 0) return 'Today';
      if (diffDays === 1) return 'Yesterday';
      if (diffDays < 7) return `${diffDays} days ago`;
      if (diffDays < 30) return `${Math.floor(diffDays / 7)} weeks ago`;
      if (diffDays < 365) return `${Math.floor(diffDays / 12)} months ago`;
      return `${Math.floor(diffDays / 365)} years ago`;
    } catch (e) {
      return 'N/A';
    }
  };

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
          <span>Total Reports</span>
          <span className='font-semibold text-white'>{communityIntelligence.report_count ? communityIntelligence.report_count.toLocaleString() : '0'}</span>
        </div>

        <div className='flex items-center justify-between text-gray-300'>
          <span>Days Active</span>
          <span className='font-semibold text-white'>{communityIntelligence.first_seen ? getTimeAgo(communityIntelligence.first_seen) : 'N/A'}</span>
        </div>

        <div className='flex items-center justify-between text-gray-300 text-sm'>
          <span>First Seen</span>
          <span>{communityIntelligence.first_seen ? formatDate(communityIntelligence.first_seen) : 'N/A'}</span>
        </div>

        <div className='flex items-center justify-between text-gray-300 text-sm'>
          <span>Last Seen</span>
          <span>{communityIntelligence.last_seen ? formatDate(communityIntelligence.last_seen) : 'N/A'}</span>
        </div>

        <div className='flex items-center justify-between text-gray-300'>
          <span>Threat ID</span>
          <span className='font-semibold text-white'>{communityIntelligence.threat_id || 'N/A'}</span>
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
