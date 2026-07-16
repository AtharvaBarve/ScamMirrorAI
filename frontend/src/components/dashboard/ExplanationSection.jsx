import React, { useContext } from 'react';
import { useAnalysis } from '../../context/AnalysisContext';

const ExplanationSection = () => {
  const { analysisResult: result } = useAnalysis();

  if (!result) return null;

  return (
    <div className='bg-[#111113/50] backdrop-blur-sm rounded-2xl border border-[#111113/30] p-6'>
      <div className='space-y-4'>
        <h3 className='text-xl font-bold text-white flex items-center'>
          <span className='mr-2'>💡</span>
          Why We Flagged This
        </h3>

        <p className='text-gray-300 leading-relaxed'>
          {result.explanation}
        </p>
      </div>
    </div>
  );
};

export default ExplanationSection;