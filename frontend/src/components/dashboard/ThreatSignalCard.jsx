import React from 'react';
import Badge from '../ui/Badge';
import { AlertTriangle, Zap, Search } from 'lucide-react';

const ThreatSignalCard = ({ threat }) => {
  const severityLabels = {
    HIGH: 'High Risk',
    MEDIUM: 'Medium Risk',
    LOW: 'Low Risk'
  };

  const severityIcons = {
    HIGH: <AlertTriangle className="w-6 h-6 text-danger" />,
    MEDIUM: <Zap className="w-6 h-6 text-warning" />,
    LOW: <Search className="w-6 h-6 text-success" />
  };

  const badgeVariant = {
    HIGH: 'danger',
    MEDIUM: 'warning',
    LOW: 'success'
  };

  const severity = threat.severity || 'MEDIUM';

  return (
    <div className="bg-surface border border-border rounded-lg p-4 hover:border-primary/50 hover:bg-surface/80 transition-all duration-300">
      <div className="flex items-start space-x-3">
        <div className="flex-shrink-0 mt-1">
          {severityIcons[severity] || <Search className="w-6 h-6 text-primary" />}
        </div>
        <div className="flex-1">
          <div className="flex items-start justify-between">
            <h4 className="font-display font-semibold text-white mb-1">
              {threat.name || 'Threat Detected'}
            </h4>
            <Badge variant={badgeVariant[severity]}>
              {severityLabels[severity]}
            </Badge>
          </div>
          <p className="text-gray-400 text-sm mt-1 mb-3 line-clamp-2">
            {threat.description || 'Suspicious pattern detected in the input.'}
          </p>
          {threat.evidence && (
            <div className="mt-2 pt-2 border-t border-border/50">
              <span className="text-xs text-gray-500 font-mono italic">
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