import React from 'react';
import ThreatSignalCard from './ThreatSignalCard';

const DetectedThreatsSection = ({ result }) => {
  const riskFactors = result.risk_factors || [];
  const category = result.category || 'Unknown';

  // Convert risk factors to threat objects for display
  // In a real implementation with future backend endpoints,
  # this would come from GET /community/threats or similar
  const threats = riskFactors.map((factor, index) => {
    // Map common risk factors to appropriate threat types and severities
    const threatMap = {
      'Urgency': {
        name: 'Urgency Tactics',
        description: 'Creates false sense of urgency to pressure quick action',
        severity: 'HIGH',
        evidence: `Urgency language detected: "${factor}"`
      },
      'Unsolicited offer': {
        name: 'Unsolicited Offer',
        description: 'Unexpected offers or prizes used to lure victims',
        severity: 'HIGH',
        evidence: `Unsolicited offer detected: "${factor}"`
      },
      'Financial scam': {
        name: 'Financial Scam Pattern',
        description: 'Requests for money, gift cards, or financial information',
        severity: 'HIGH',
        evidence: `Financial scam indicators: "${factor}"`
      },
      'Impersonation': {
        name: 'Impersonation Attempt',
        description: 'Attempts to mimic legitimate organizations or people',
        severity: 'HIGH',
        evidence: `Impersonation indicators: "${factor}"`
      },
      'Phishing link': {
        name: 'Phishing Link',
        description: 'Contains links to fraudulent websites',
        severity: 'HIGH',
        evidence: `Suspicious link detected: "${factor}"`
      },
      'Personal information request': {
        name: 'Personal Information Request',
        description: 'Attempts to collect sensitive personal data',
        severity: 'HIGH',
        evidence: `PII request detected: "${factor}"`
      }
    };

    const threatData = threatMap[factor] || threatMap[factor.toLowerCase()] || {
      name: factor,
      description: `Suspicious factor detected: ${factor}`,
      severity: 'MEDIUM',
      evidence: `Risk factor: "${factor}"`
    };

    return {
      id: index,
      ...threatData
    };
  });

  // If no risk factors but we have a category, create a generic threat
  if (threats.length === 0 && category && category !== 'Unknown') {
    threats.push({
      id: 0,
      name: `${category} Pattern`,
      description: `Patterns consistent with ${category} detected`,
      severity: 'MEDIUM',
      evidence: `Threat category identified: ${category}`
    });
  }

  // If still no threats, show a message
  if (threats.length === 0) {
    return (
      <div className='bg-[#111113/50] backdrop-blur-sm rounded-2xl border border-[#111113/30] p-6'>
        <h3 className='text-xl font-bold text-white flex items-center mb-4'>
          <span className='mr-2'>🔍</span>
          Detected Threats
        </h3>
        <p className='text-gray-400 text-center py-8'>
          No specific threat factors detected in this analysis.
        </p>
      </div>
    );
  }

  return (
    <div className='bg-[#111113/50] backdrop-blur-sm rounded-2xl border border-[#111113/30] p-6'>
      <h3 className='text-xl font-bold text-white flex items-center mb-4'>
        <span className='mr-2'>🔍</span>
        Detected Threats
      </h3>

      <div className='grid gap-4 sm:grid-cols-2 lg:grid-cols-3'>
        {threats.map((threat) => (
          <ThreatSignalCard key={threat.id} threat={threat} />
        ))}
      </div>
    </div>
  );
};

export default DetectedThreatsSection;