import { useState } from 'react';
import useAnalyze from '../hooks/useAnalyze';
import Spinner from './Spinner';
import ResultCard from './ResultCard';

const Analyzer = () => {
  const [inputType, setInputType] = useState('text'); // 'text' or 'url'
  const [inputValue, setInputValue] = useState('');
  const { data: result, loading, error, execute } = useAnalyze();

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (!inputValue.trim()) return;

    const payload =
      inputType === 'text'
        ? { text: inputValue.trim() }
        : { url: inputValue.trim() };

    await execute(payload);
  };

  return (
    <div className='bg-white rounded-xl shadow-md p-6 space-y-5 w-full max-w-xl'>
      <form onSubmit={handleSubmit} className='space-y-4'>
        <div>
          <label className='block text-sm font-medium text-gray-700'>
            What do you want to check?
          </label>
          <div className='flex space-x-2 mt-1'>
            <label className='inline-flex items-center'>
              <input
                type='radio'
                name='type'
                value='text'
                checked={inputType === 'text'}
                onChange={(e) => setInputType(e.target.value)}
                className='h-4 w-4 text-indigo-600'
              />
              <span className='ml-2'>Text / Message</span>
            </label>
            <label className='inline-flex items-center ml-4'>
              <input
                type='radio'
                name='type'
                value='url'
                checked={inputType === 'url'}
                onChange={(e) => setInputType(e.target.value)}
                className='h-4 w-4 text-indigo-600'
              />
              <span className='ml-2'>URL / Website</span>
            </label>
          </div>
        </div>

        <div>
          <label className='block text-sm font-medium text-gray-700 mb-1'>
            {inputType === 'text' ? 'Message' : 'URL'}
          </label>
          <input
            type={inputType === 'text' ? 'text' : 'url'}
            placeholder={
              inputType === 'text'
                ? 'Paste a message…'
                : 'Enter full URL (e.g., https://example.com)'
            }
            value={inputValue}
            onChange={(e) => setInputValue(e.target.value)}
            className='block w-full rounded-md border-gray-300 shadow-sm focus:border-indigo-500 focus:ring-indigo-500 sm:text-sm'
          />
        </div>

        <button
          type='submit'
          disabled={loading || !inputValue.trim()}
          className='w-full justify-center py-2 px-4 border border-transparent rounded-md shadow-sm text-sm font-medium text-white bg-indigo-600 hover:bg-indigo-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500 disabled:opacity-50'
        >
          {loading ? 'Analyzing…' : 'Analyze'}
        </button>
      </form>

      {error && (
        <p className='text-sm text-red-600'>
          Error: {error}
        </p>
      )}

      {result && (
        <div className='border-t pt-4'>
          <h2 className='text-lg font-semibold text-gray-900 mb-2'>
            Result
          </h2>
          <ResultCard result={{ verdict: result.verdict, explanation: result.explanation, confidence: result.confidence }} />
        </div>
      )}
    </div>
  );
};

export default Analyzer;