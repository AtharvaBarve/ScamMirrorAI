import React, { useContext } from 'react';
import { useAnalysis } from '../../context/AnalysisContext';

const ThreatLevelSection = () => {
  const { analysisResult: result } = useAnalysis();

  if (!result) return null;

  const getThreatLevelColor = (verdict) => {
    const lower = verdict.toLowerCase();
    if (lower.includes('scam')) return '#FF4D6D'; // Danger/Red
    if (lower.includes('safe')) return '#22C55E'; // Success/Green
    return '#FFB703'; // Warning/Amber
  };

  const getThreatLevelLabel = (verdict) => {
    const lower = verdict.toLowerCase();
    if (lower.includes('scam')) return 'HIGH';
    if (lower.includes('safe')) return 'LOW';
    return 'MEDIUM';
  };

  return (
    <div className='bg-[#111113/50] backdrop-blur-sm rounded-2xl border border-[#111113/30] p-6'>
      <div className='space-y-5'>
        <h3 className='text-xl font-bold text-white flex items-center'>
          <span className='mr-2'>🛡️</span>
          Threat Assessment
        </h3>

        <div className='flex items-center space-x-4'>
          <div className='flex-shrink-0 w-12 h-12 flex items-center justify-center'>
            <span className={`text-2xl font-bold`} style={{ color: getThreatLevelColor(result.verdict) }}>
              {getThreatLevelLabel(result.verdict)}
            </span>
          </div>
          <div>
            <p className='text-2xl font-bold text-white'>
              {result.verdict}
            </p>
            <p className='text-gray-300'>
              Threat Level
            </p>
          </div>
        </div>

        <div className='relative h-8'>
          <div className='absolute inset-0 bg-[#111113/20] rounded-full'></div>
          <div
            className='absolute inset-0'
            style={{
              background: `conic-gradient(
                ${getThreatLevelColor(result.verdict)} 0% ${result.confidence * 360}deg,
                #111113 ${result.confidence * 360}deg 360deg
              )`,
              WebkitMask: `conic-gradient(#000 0% ${result.confidence * 100}%, transparent ${result.confidence * 100}% 100%)`,
              mask: `conic-gradient(#000 0% ${result.confidence * 100}%, transparent ${result.confidence * 100}% 100%)`
            }}
          ></div>
        </div>

        <div className='flex justify-between text-sm text-gray-400'>
          <span>0%</span>
          <span>{Math.round(result.confidence * 100)}%</span>
          <span>100%</span>
        </div>
      </div>
    </div>
  );
};

export default ThreatLevelSection;