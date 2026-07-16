import React from 'react';
import { useAnalysis } from '../../context/AnalysisContext';
import { Card, CardHeader, CardTitle, CardContent } from '../ui/Card';
import { BrainCircuit, Info } from 'lucide-react';

const ExplanationSection = () => {
  const { analysisResult: result } = useAnalysis();

  if (!result) return null;

  return (
    <Card className="h-full bg-surface/50 backdrop-blur-xl border-border">
      <CardHeader className="pb-2">
        <div className="flex items-center justify-between">
          <CardTitle className="text-xl font-display flex items-center text-white">
            <BrainCircuit className="w-5 h-5 text-primary mr-3" />
            AI Explanation
          </CardTitle>
          <div className="text-xs font-mono text-gray-500">
            {new Date(result.created_at || Date.now()).toLocaleTimeString()}
          </div>
        </div>
      </CardHeader>
      <CardContent>
        <p className="text-gray-300 leading-relaxed font-sans text-sm">
          {result.explanation}
        </p>

        {result.confidence < 0.9 && (
          <div className="mt-6 pt-4 border-t border-border/50">
            <button className="w-full text-left text-gray-400 hover:text-white rounded-lg transition-colors flex items-center space-x-2 text-sm group">
              <Info className="w-4 h-4 group-hover:text-primary transition-colors" />
              <span>How this assessment was made</span>
            </button>
          </div>
        )}
      </CardContent>
    </Card>
  );
};

export default ExplanationSection;