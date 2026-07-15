import React from 'react';

const ThreatSignalCard = ({ threat }) => {
  const severityColors = {
    HIGH: '#FF4D6D',    // Red
    MEDIUM: '#FFB703',  // Amber
    LOW: '#22C55E'      // Green
  };

  const severityLabels = {
    HIGH: 'High Risk',
    MEDIUM: 'Medium Risk',
    LOW: 'Low Risk'
  };

  const severityIcons = {
    HIGH: '⚠️',
    MEDIUM: '⚡',
    LOW: '🔍'
  };

  const severity = threat.severity || 'MEDIUM';

  return (
    <div className='bg-[#111113/30] backdrop-blur-sm rounded-xl border border-[#111113/20] p-4 hover:bg-[#111113/40] transition-colors duration-200'>
      <div className='flex items-start space-x-3'>
        <div className='flex-shrink-0 text-2xl'>
          {severityIcons[severity] || '🔍'}
        </div>
        <div className='flex-1'>
          <h4 className='font-semibold text-white mb-1'>
            {threat.name || 'Threat Detected'}
          </h4>
          <div className='flex items-center space-x-2 mb-2'>
            <span className={`px-2 py-0.5 text-xs font-medium rounded-full
              ${severity === 'HIGH' ? 'bg-red-500/20 text-red-400' :
                severity === 'MEDIUM' ? 'bg-amber-500/20 text-amber-400' :
                'bg-green-500/20 text-green-400'}`}>
              {severityLabels[severity]}
            </span>
          </div>
          <p className='text-gray-300 text-sm line-clamp-2'>
            {threat.description || 'Suspicious pattern detected in the input.'}
          </p>
          {threat.evidence && (
            <div className='mt-2 pt-2 border-t border-[#111113/20]'>
              <span className='text-xs text-gray-400 font-mono'>
                "{threat.evidence}"
              </span>
            </div>
          )}
        </div>
      </div>
    </div>
  );
};

export default ThreatSignalCard;