import React from 'react';
import ThreatSignalCard from './ThreatSignalCard';
import { useAnalysis } from '../../context/AnalysisContext';
import { Card, CardHeader, CardTitle, CardContent } from '../ui/Card';
import { Search } from 'lucide-react';

const DetectedThreatsSection = () => {
  const { analysisResult: result } = useAnalysis();

  if (!result) return null;

  const riskFactors = result.risk_factors || [];
  const category = result.category || 'Unknown';

  // Convert risk factors to threat objects for display
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

  return (
    <Card className="h-full bg-surface/50 backdrop-blur-xl border-border">
      <CardHeader className="pb-2">
        <div className="flex items-center justify-between">
          <CardTitle className="text-xl font-display flex items-center text-white">
            <Search className="w-5 h-5 text-primary mr-3" />
            Detected Threats
          </CardTitle>
          <div className="text-xs font-mono text-gray-500">
            {new Date(result.created_at || Date.now()).toLocaleTimeString()}
          </div>
        </div>
      </CardHeader>
      <CardContent>
        {threats.length === 0 ? (
          <p className="text-gray-400 text-center py-8 font-mono text-sm">
            No specific threat factors detected in this analysis.
          </p>
        ) : (
          <div className="grid gap-4 mt-2">
            {threats.map((threat) => (
              <ThreatSignalCard key={threat.id} threat={threat} />
            ))}
          </div>
        )}
      </CardContent>
    </Card>
  );
};

export default DetectedThreatsSection;