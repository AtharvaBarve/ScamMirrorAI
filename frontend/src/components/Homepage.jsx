import { useState } from 'react';
import useAnalyze from '../hooks/useAnalyze';
import ThreatAssessmentDashboard from './dashboard/ThreatAssessmentDashboard';
import ThreatTrendsSection from './ThreatTrendsSection';

const Homepage = () => {
  const [inputType, setInputType] = useState('message'); // 'message', 'url', 'screenshot'
  const [inputValue, setInputValue] = useState('');
  const [isScreenshotLocked, setIsScreenshotLocked] = useState(true); // Locked unless OCR implemented
  const { data: result, loading, error, execute } = useAnalyze();

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (!inputValue.trim()) return;

    const payload =
      inputType === 'message'
        ? { text: inputValue.trim() }
        : { url: inputValue.trim() };

    await execute(payload);
  };

  const handleExampleClick = (example) => {
    setInputValue(example.text);
    setInputType(example.type);
  };

  const examples = [
    {
      id: 1,
      type: 'message',
      text: 'URGENT: Your SBI account has been blocked. Click here to verify now!',
      label: '🔴 Fake SBI KYC Update'
    },
    {
      id: 2,
      type: 'message',
      text: 'Congratulations! You have won $1,000,000 in the WhatsApp Lucky Draw. Click to claim!',
      label: '🔴 WhatsApp Lottery'
    },
    {
      id: 3,
      type: 'message',
      text: 'Hey John, thanks for meeting yesterday. Let\'s catch up again next week at the same time.',
      label: '🟢 Genuine Meeting Reminder'
    },
    {
      id: 4,
      type: 'message',
      text: 'Your Amazon order #123-4567890 has been refunded. Verify your account details to receive the refund.',
      label: '🟠 Fake Amazon Refund'
    }
  ];

  return (
    <div className='min-h-screen bg-gradient-to-br from-[#09090B] to-[#111113]'>
      {/* Hero Section */}
      <section className='relative pt-20 pb-16'>
        <div className='max-w-4xl mx-auto px-6 lg:px-12 text-center'>
          <h1 className='text-5xl font-bold text-transparent bg-clip-text bg-gradient-to-r from-[#00E5FF] to-[#00BFA6] mb-4'>
            ScamMirror AI
          </h1>
          <p className='text-2xl text-[#00E5FF] mb-6'>
            AI-powered Threat Intelligence Assistant
          </p>
          <p className='text-lg text-gray-300 mb-8 max-w-2xl mx-auto leading-relaxed'>
            Analyze suspicious messages, URLs and screenshots before you trust them.
          </p>
          <div className='flex flex-col sm:flex-row sm:space-x-4 justify-center'>
            <button
              onClick={() => {
                setInputType('message');
                setInputValue(examples[0].text);
              }}
              className='px-6 py-3 bg-[#00E5FF] text-[#09090B] font-semibold rounded-xl hover:bg-[#00CCE5] transition-all duration-300 transform hover:-translate-y-1'
            >
              Try Example
            </button>
            <button
              onClick={() => {
                setInputType('message');
                setInputValue('');
              }}
              className='ml-3 px-6 py-3 border border-[#111113/30] bg-[#111113/50] backdrop-blur-sm text-white font-semibold rounded-xl hover:border-[#00E5FF] hover:bg-[#111113/60] transition-all duration-300'
            >
              Start Analysis
            </button>
          </div>
        </div>
        <div className='absolute bottom-0 left-0 right-0 h-20 bg-gradient-to-t from-[#111113] to-transparent pointer-events-none'></div>
      </section>

      {/* Main Content */}
      <section className='py-16'>
        <div className='max-w-4xl mx-auto px-6 lg:px-12'>
          {/* Analyze Threat Card */}
          <div className='bg-[#111113/50] backdrop-blur-sm rounded-2xl border border-[#111113/30] p-8'>
            <h2 className='text-2xl font-bold text-white mb-6 text-center'>
              Analyze Threat
            </h2>

            <form onSubmit={handleSubmit} className='space-y-6'>
              {/* Input Tabs */}
              <div className='flex border-b border-[#111113/30] pb-2'>
                <button
                  type='button'
                  onClick={() => setInputType('message')}
                  className={`flex-1 px-4 py-3 text-center font-medium transition-all duration-200
                    ${inputType === 'message'
                      ? 'text-white border-b-2 border-[#00E5FF] bg-[#111113/30]'
                      : 'text-gray-400 hover:text-white'}
                  `}
                >
                  Message
                </button>
                <button
                  type='button'
                  onClick={() => setInputType('url')}
                  className={`flex-1 px-4 py-3 text-center font-medium transition-all duration-200
                    ${inputType === 'url'
                      ? 'text-white border-b-2 border-[#00E5FF] bg-[#111113/30]'
                      : 'text-gray-400 hover:text-white'}
                  `}
                >
                  URL
                </button>
                <button
                  type='button'
                  onClick={() => setInputType('screenshot')}
                  disabled={isScreenshotLocked}
                  className={`flex-1 px-4 py-3 text-center font-medium transition-all duration-200
                    ${inputType === 'screenshot'
                      ? 'text-white border-b-2 border-[#00E5FF] bg-[#111113/30]'
                      : 'text-gray-400 hover:text-white opacity-50 cursor-not-allowed'}
                  `}
                >
                  Screenshot
                </button>
              </div>

              {/* Input Field */}
              <div>
                <label className='block text-sm font-medium text-gray-300 mb-2'>
                  {inputType === 'message' ? 'Message or Email' : inputType === 'url' ? 'Website URL' : 'Upload Screenshot'}
                </label>
                {inputType === 'screenshot' && !isScreenshotLocked ? (
                  <div className='mb-4'>
                    <input
                      type='file'
                      accept='image/*'
                      onChange={(e) => {
                        if (e.target.files[0]) {
                          // In a real app, we would process the image here
                          // For now, we'll just simulate with a placeholder
                          setInputValue('screenshot_placeholder');
                        }
                      }}
                      className='mb-2 block w-full text-sm text-gray-500 file:mr-4 file:py-2 file:px-4 file:rounded-md file:border-0 file:text-sm file:font-semibold file:bg-[#00E5FF] file:text-white hover:file:bg-[#00CCE5]'
                    />
                    <p className='text-xs text-gray-400'>
                      Supported formats: JPG, PNG, Max size: 5MB
                    </p>
                  </div>
                ) : (
                  <input
                    type={inputType === 'message' ? 'text' : 'url'}
                    placeholder={
                      inputType === 'message'
                        ? 'Paste a suspicious message or email...'
                        : 'Enter full URL (e.g., https://bit.ly/suspicious-link)'
                    }
                    value={inputValue}
                    onChange={(e) => setInputValue(e.target.value)}
                    className='block w-full rounded-xl border border-[#111113/30] bg-[#111113/20] px-6 py-4 text-white placeholder-gray-400 focus:border-[#00E5FF] focus:ring-2 focus:ring-[#00E5FF/30] transition-all duration-200'
                  />
                )}
              </div>

              {/* Submit Button */}
              <button
                type='submit'
                disabled={loading || !inputValue.trim()}
                className='w-full bg-[#00E5FF] text-[#09090B] font-bold py-3 px-6 rounded-xl hover:bg-[#00CCE5] active:scale-[1.02] transition-all duration-200 disabled:opacity-50 disabled:cursor-not-allowed'
              >
                {loading ? 'Analyzing Threat...' : 'Analyze Threat'}
              </button>
            </form>
          </div>

          {/* Loading/Error States */}
          {error && (
            <div className='mt-6 p-4 bg-[#FF4D6D/20] border border-[#FF4D6D/30] rounded-xl text-red-400'>
              Error: {error}
            </div>
          )}

          {/* Results - Phase 2 Threat Assessment Dashboard */}
          {result || loading ? (
            <ThreatAssessmentDashboard />
          ) : null}
        </div>
      </section>

      {/* Example Analyses Section */}
      <section className='py-16 bg-[#111113/20]'>
        <div className='max-w-4xl mx-auto px-6 lg:px-12'>
          <h2 className='text-2xl font-bold text-white mb-8 text-center'>
            Example Analyses
          </h2>
          <div className='grid gap-6 sm:grid-cols-2 lg:grid-cols-4'>
            {examples.map((example) => (
              <button
                key={example.id}
                onClick={() => handleExampleClick(example)}
                className='group'
              >
                <div className='bg-[#111113/30] border border-[#111113/20] rounded-xl p-6 hover:bg-[#111113/40] hover:border-[#00E5FF/30] transition-all duration-300 transform hover:-translate-y-1'>
                  <div className='flex items-center mb-4'>
                    <span className='text-2xl mr-3'>
                      {example.label.split(' ')[0]} {/* Extract emoji */}
                    </span>
                    <h3 className='text-xl font-bold text-white'>
                      {example.label.split(' ').slice(1).join(' ')} {/* Text without emoji */}
                    </h3>
                  </div>
                  <p className='text-gray-300 text-sm line-clamp-3 flex-1 mb-4'>
                    {example.text}
                  </p>
                  <div className='flex items-center justify-between'>
                    <span className='text-xs text-gray-500'>
                      Click to analyze
                    </span>
                    <span className='text-xs text-[#00E5FF]'>
                      →
                    </span>
                  </div>
                </div>
              </button>
            ))}
          </div>
        </div>
      </section>

      {/* Threat Trends Section */}
      <section className='py-16'>
        <div className='max-w-4xl mx-auto px-6 lg:px-12'>
          <ThreatTrendsSection />
        </div>
      </section>
    </div>
  );
};

export default Homepage;
