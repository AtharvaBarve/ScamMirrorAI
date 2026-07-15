import React from 'react';
import SkeletonLoader from '../../SkeletonLoader';
import ThreatLevelSection from './ThreatLevelSection';
import ExplanationSection from './ExplanationSection';
import DetectedThreatsSection from './DetectedThreatsSection';
import CommunityIntelligenceSection from './CommunityIntelligenceSection';
import ProtectOthersSection from './ProtectOthersSection';
import ThreatReportSection from './ThreatReportSection';

const ThreatAssessmentDashboard = ({ result, loading = false }) => {
  if (loading && !result) {
    // Show skeleton loaders when loading and no result yet
    return (
      <div className='space-y-8'>
        <div className='grid grid-cols-1 lg:grid-cols-3 gap-6'>
          <div className='lg:col-span-1'>
            {/* Threat Level Section Skeleton */}
            <div className='bg-[#111113/50] backdrop-blur-sm rounded-2xl border border-[#111113/30] p-6'>
              <h3 className='text-xl font-bold text-white flex items-center mb-4'>
                <span className='mr-2'>🎯</span>
                Threat Level
              </h3>
              <SkeletonLoader className='mb-4' />
              <p className='text-gray-300'>Analyzing threat level...</p>
            </div>

            {/* Community Intelligence Section Skeleton */}
            <div className='bg-[#111113/50] backdrop-blur-sm rounded-2xl border border-[#111113/30] p-6 mt-6'>
              <h3 className='text-xl font-bold text-white flex items-center mb-4'>
                <span className='mr-2'>👥</span>
                Community Intel
              </h3>
              <SkeletonLoader className='mb-4' />
              <p className='text-gray-300'>Loading community data...</p>
            </div>

            {/* Protect Others Section Skeleton */}
            <div className='bg-[#111113/50] backdrop-blur-sm rounded-2xl border border-[#111113/30] p-6 mt-6'>
              <h3 className='text-xl font-bold text-white flex items-center mb-4'>
                <span className='mr-2'>🛡️</span>
                Protect Others
              </h3>
              <SkeletonLoader className='mb-4' />
              <p className='text-gray-300'>Preparing protection features...</p>
            </div>
          </div>
          <div className='lg:col-span-2'>
            {/* Explanation Section Skeleton */}
            <div className='bg-[#111113/50] backdrop-blur-sm rounded-2xl border border-[#111113/30] p-6'>
              <h3 className='text-xl font-bold text-white flex items-center mb-4'>
                <span className='mr-2'>📝</span>
                Explanation
              </h3>
              <SkeletonLoader className='mb-4' />
              <SkeletonLoader className='mb-2' style={{ width: '80%' }} />
              <SkeletonLoader className='mb-2' style={{ width: '60%' }} />
              <p className='text-gray-300'>Generating explanation...</p>
            </div>

            {/* Detected Threats Section Skeleton */}
            <div className='bg-[#111113/50] backdrop-blur-sm rounded-2xl border border-[#111113/30] p-6 mt-6'>
              <h3 className='text-xl font-bold text-white flex items-center mb-4'>
                <span className='mr-2'>⚠️</span>
                Detected Threats
              </h3>
              <SkeletonLoader className='mb-2' />
              <SkeletonLoader className='mb-2' />
              <SkeletonLoader className='mb-2' />
              <p className='text-gray-300'>Analyzing threat signals...</p>
            </div>

            {/* Threat Report Section Skeleton */}
            <div className='bg-[#111113/50] backdrop-blur-sm rounded-2xl border border-[#111113/30] p-6 mt-6'>
              <h3 className='text-xl font-bold text-white flex items-center mb-4'>
                <span className='mr-2'>📄</span>
                Threat Report
              </h3>
              <SkeletonLoader className='mb-4' />
              <p className='text-gray-300'>Preparing report generation...</p>
            </div>
          </div>
        </div>
      </div>
    );
  }

  if (!result) return null;

  return (
    <div className='space-y-8'>
      <div className='grid grid-cols-1 lg:grid-cols-3 gap-6'>
        <div className='lg:col-span-1'>
          <ThreatLevelSection result={result} />
          <CommunityIntelligenceSection result={result} />
          <ProtectOthersSection result={result} />
        </div>
        <div className='lg:col-span-2'>
          <ExplanationSection result={result} />
          <DetectedThreatsSection result={result} />
          <ThreatReportSection result={result} />
        </div>
      </div>
    </div>
  );
};

export default ThreatAssessmentDashboard;