import React from 'react';
import { useAnalysis } from '../../context/AnalysisContext';
import { Card, CardHeader, CardTitle, CardContent } from '../ui/Card';
import { Target } from 'lucide-react';

const ThreatLevelSection = () => {
  const { analysisResult: result } = useAnalysis();

  if (!result) return null;

  const getThreatLevelColor = (verdict) => {
    const lower = verdict.toLowerCase();
    if (lower.includes('scam')) return '#FF3366'; // Tailwind Danger
    if (lower.includes('safe')) return '#00E676'; // Tailwind Success
    return '#FFB300'; // Tailwind Warning
  };

  return (
    <Card className="h-full bg-surface/50 backdrop-blur-xl border-border">
      <CardHeader className="pb-2">
        <div className="flex items-center justify-between">
          <CardTitle className="text-xl font-display flex items-center text-white">
            <Target className="w-5 h-5 text-primary mr-3" />
            Threat Level
          </CardTitle>
          <div className="text-xs font-mono text-gray-500">
            {new Date(result.created_at || Date.now()).toLocaleTimeString()}
          </div>
        </div>
      </CardHeader>
      
      <CardContent>
        <div className="relative h-14 w-full mt-4">
          <div className="absolute inset-0 bg-background/50 rounded-full border border-border"></div>
          <div
            className="absolute inset-0 rounded-full transition-all duration-1000 ease-out"
            style={{
              background: `conic-gradient(
                ${getThreatLevelColor(result.verdict)} 0% ${result.confidence * 360}deg,
                transparent ${result.confidence * 360}deg 360deg
              )`,
              WebkitMask: `conic-gradient(#000 0% ${result.confidence * 100}%, transparent ${result.confidence * 100}% 100%)`,
              mask: `conic-gradient(#000 0% ${result.confidence * 100}%, transparent ${result.confidence * 100}% 100%)`
            }}
          ></div>
          <div className="absolute inset-[4px] bg-surface rounded-full shadow-inner flex items-center justify-center">
            <span className="font-mono font-bold text-lg text-white">
              {Math.round(result.confidence * 100)}%
            </span>
          </div>
        </div>

        <div className="flex items-center justify-between text-xs font-mono mt-3 text-gray-500">
          <span>0%</span>
          <span>100%</span>
        </div>

        <div className="mt-6 text-center border-t border-border/50 pt-4">
          <p className="text-2xl font-display font-bold uppercase tracking-widest" style={{ color: getThreatLevelColor(result.verdict) }}>
            {result.verdict}
          </p>
          <p className="text-gray-400 text-xs font-mono mt-1 uppercase">
            Confidence Interval
          </p>
        </div>
      </CardContent>
    </Card>
  );
};

export default ThreatLevelSection;