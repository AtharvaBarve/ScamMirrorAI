import { useState } from 'react';

const ResultCard = ({ result }) => {
  const [copied, setCopied] = useState(false);

  const copyToClipboard = () => {
    const text = [
      `Verdict: ${result.verdict}`,
      `Confidence: ${Math.round(result.confidence * 100)}%`,
      `Category: ${result.category}`,
      `Risk Factors: ${result.risk_factors.length > 0 ? result.risk_factors.join(', ') : 'None'}`,
      `Recommended Actions: ${result.recommended_actions.length > 0 ? result.recommended_actions.join(', ') : 'None'}`,
      `Explanation: ${result.explanation}`,
      `Processing Time: ${result.processing_time.toFixed(2)} seconds`,
    ].join('\n');
    navigator.clipboard.writeText(text).then(() => {
      setCopied(true);
      setTimeout(() => setCopied(false), 2000);
    });
  };

  const getVerdictClass = (verdict) => {
    const lower = verdict.toLowerCase();
    if (lower.includes('scam')) return 'text-red-600';
    if (lower.includes('safe')) return 'text-green-600';
    return 'text-gray-600';
  };

  return (
    <div className='space-y-4'>
      <div className='flex items-center'>
        <span className='font-medium mr-2'>Verdict:</span>
        <span className={`${getVerdictClass(result.verdict)} font-bold`}>
          {result.verdict}
        </span>
      </div>

      <div>
        <span className='block text-sm font-medium text-gray-700 mb-1'>
          Confidence:
        </span>
        <div className='w-full bg-gray-200 rounded-full h-2.5'>
          <div
            className={`bg-indigo-600 h-2.5 rounded-full`}
            style={{ width: `${result.confidence * 100}%` }}
          ></div>
        </div>
        <div className='text-right text-sm text-gray-600 mt-1'>
          {Math.round(result.confidence * 100)}%
        </div>
      </div>

      <div className='border-t pt-3'>
        <span className='block text-sm font-medium text-gray-700 mb-1'>
          Category:
        </span>
        <span className='text-gray-700'>{result.category}</span>
      </div>

      <div className='border-t pt-3'>
        <span className='block text-sm font-medium text-gray-700 mb-1'>
          Risk Factors:
        </span>
        <span className='text-gray-700'>
          {result.risk_factors.length > 0 ? result.risk_factors.map((f, i) => (
            <span key={i} className='bg-gray-100 px-2 py-1 rounded text-sm mr-1 mb-1 inline-block'>
              {f}
            </span>
          )) : 'None'}
        </span>
      </div>

      <div className='border-t pt-3'>
        <span className='block text-sm font-medium text-gray-700 mb-1'>
          Recommended Actions:
        </span>
        <span className='text-gray-700'>
          {result.recommended_actions.length > 0 ? result.recommended_actions.map((a, i) => (
            <span key={i} className='bg-gray-100 px-2 py-1 rounded text-sm mr-1 mb-1 inline-block'>
              {a}
            </span>
          )) : 'None'}
        </span>
      </div>

      <div className='border-t pt-3'>
        <span className='block text-sm font-medium text-gray-700 mb-1'>
          Explanation:
        </span>
        <p className='text-gray-700 leading-relaxed'>{result.explanation}</p>
      </div>

      <div className='border-t pt-3'>
        <span className='block text-sm font-medium text-gray-700 mb-1'>
          Processing Time:
        </span>
        <span className='text-gray-700'>
          {result.processing_time.toFixed(2)} seconds
        </span>
      </div>

      <div className='mt-4 flex justify-end space-x-2'>
        <button
          onClick={copyToClipboard}
          className='flex items-center px-3 py-1.5 text-sm font-medium text-center text-white bg-indigo-600 border border-transparent rounded-lg hover:bg-indigo-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500 disabled:opacity-50'
        >
          {copied ? 'Copied!' : 'Copy Result'}
        </button>
      </div>
    </div>
  );
};

export default ResultCard;