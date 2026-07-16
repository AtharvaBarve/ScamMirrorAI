import { useState } from 'react';
import useAnalyze from '../hooks/useAnalyze';
import ThreatAssessmentDashboard from './dashboard/ThreatAssessmentDashboard';
import ThreatTrendsSection from './ThreatTrendsSection';
import { Lightbulb, AlertCircle, CheckCircle, AlertTriangle, ArrowRight, ShieldAlert, Link as LinkIcon, Image as ImageIcon } from 'lucide-react';
import Button from './ui/Button';
import Input from './ui/Input';
import { Card, CardContent } from './ui/Card';

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

  const getExampleIcon = (type) => {
    switch(type) {
      case 'danger': return <AlertCircle className="w-5 h-5 text-red-500" />;
      case 'success': return <CheckCircle className="w-5 h-5 text-green-500" />;
      case 'warning': return <AlertTriangle className="w-5 h-5 text-yellow-500" />;
      default: return <AlertCircle className="w-5 h-5 text-gray-500" />;
    }
  };

  const examples = [
    {
      id: 1,
      type: 'message',
      text: 'URGENT: Your SBI account has been blocked. Click here to verify now!',
      label: 'Fake SBI KYC Update',
      iconType: 'danger'
    },
    {
      id: 2,
      type: 'message',
      text: 'Congratulations! You have won $1,000,000 in the WhatsApp Lucky Draw. Click to claim!',
      label: 'WhatsApp Lottery',
      iconType: 'danger'
    },
    {
      id: 3,
      type: 'message',
      text: 'Hey John, thanks for meeting yesterday. Let\'s catch up again next week at the same time.',
      label: 'Genuine Meeting Reminder',
      iconType: 'success'
    },
    {
      id: 4,
      type: 'message',
      text: 'Your Amazon order #123-4567890 has been refunded. Verify your account details to receive the refund.',
      label: 'Fake Amazon Refund',
      iconType: 'warning'
    }
  ];

  return (
    <div className='py-8'>
      {/* Main Content */}
      <div className='max-w-7xl mx-auto px-4 sm:px-6 lg:px-8'>
        {/* Responsive Grid: 2 columns on lg+, 1 column below */}
        <div className='grid gap-8 lg:grid-cols-[1fr_300px]'>
          {/* Main Analyze Card - Takes 1fr on lg+, full width below */}
          <div className='lg:col-span-1'>
            <Card className='border-border/50'>
              <CardContent className="p-8">
                <h2 className='text-2xl font-bold text-white mb-6 text-center'>
                  Analyze Threat
                </h2>

                <form onSubmit={handleSubmit} className='space-y-6'>
                  {/* Input Tabs */}
                  <div className='flex border-b border-border pb-2'>
                    <button
                      type='button'
                      onClick={() => setInputType('message')}
                      className={`flex-1 px-4 py-3 text-center font-medium transition-all duration-200 flex items-center justify-center
                        ${inputType === 'message'
                          ? 'text-white border-b-2 border-primary bg-surface/50'
                          : 'text-gray-400 hover:text-white hover:bg-surface/30'}
                      `}
                    >
                      <ShieldAlert className="w-4 h-4 mr-2" />
                      Message
                    </button>
                    <button
                      type='button'
                      onClick={() => setInputType('url')}
                      className={`flex-1 px-4 py-3 text-center font-medium transition-all duration-200 flex items-center justify-center
                        ${inputType === 'url'
                          ? 'text-white border-b-2 border-primary bg-surface/50'
                          : 'text-gray-400 hover:text-white hover:bg-surface/30'}
                      `}
                    >
                      <LinkIcon className="w-4 h-4 mr-2" />
                      URL
                    </button>
                    <button
                      type='button'
                      onClick={() => setInputType('screenshot')}
                      disabled={isScreenshotLocked}
                      className={`flex-1 px-4 py-3 text-center font-medium transition-all duration-200 flex items-center justify-center
                        ${inputType === 'screenshot'
                          ? 'text-white border-b-2 border-primary bg-surface/50'
                          : 'text-gray-400 hover:text-white opacity-50 cursor-not-allowed'}
                      `}
                    >
                      <ImageIcon className="w-4 h-4 mr-2" />
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
                              setInputValue('screenshot_placeholder');
                            }
                          }}
                          className='mb-2 block w-full text-sm text-gray-500 file:mr-4 file:py-2 file:px-4 file:rounded-md file:border-0 file:text-sm file:font-semibold file:bg-primary file:text-background hover:file:bg-primary-hover'
                        />
                        <p className='text-xs text-gray-400'>
                          Supported formats: JPG, PNG, Max size: 5MB
                        </p>
                      </div>
                    ) : (
                      <Input
                        type={inputType === 'message' ? 'text' : 'url'}
                        placeholder={
                          inputType === 'message'
                            ? 'Paste a suspicious message or email...'
                            : 'Enter full URL (e.g., https://bit.ly/suspicious-link)'
                        }
                        value={inputValue}
                        onChange={(e) => setInputValue(e.target.value)}
                      />
                    )}
                  </div>

                  {/* Submit Button */}
                  <Button
                    type='submit'
                    disabled={loading || !inputValue.trim()}
                    className='w-full'
                    size='lg'
                  >
                    {loading ? 'Analyzing Threat...' : 'Analyze Threat'}
                  </Button>
                </form>
              </CardContent>
            </Card>

            {/* Loading/Error States */}
            {error && (
              <div className='mt-6 p-4 bg-red-500/10 border border-red-500/20 rounded-xl text-red-400'>
                Error: {error}
              </div>
            )}

            {/* Results */}
            {result || loading ? (
              <ThreatAssessmentDashboard />
            ) : null}
          </div>

          {/* Sidebar - Examples and Trends */}
          <aside className='lg:col-span-1 space-y-6'>
            {/* Example Analyses */}
            <section>
              <h3 className='text-xl font-bold text-white mb-4 flex items-center'>
                <Lightbulb className='w-5 h-5 text-primary mr-2' />
                Example Analyses
              </h3>
              <div className='grid gap-4 sm:grid-cols-2 lg:grid-cols-1'>
                {examples.map((example) => (
                  <button
                    key={example.id}
                    onClick={() => handleExampleClick(example)}
                    className='group text-left'
                  >
                    <div className='bg-surface/30 border border-border rounded-xl p-4 hover:bg-surface/50 hover:border-primary/30 transition-all duration-300 transform hover:-translate-y-1'>
                      <div className='flex items-center mb-2'>
                        <span className='mr-2'>
                          {getExampleIcon(example.iconType)}
                        </span>
                        <h4 className='font-semibold text-white'>
                          {example.label}
                        </h4>
                      </div>
                      <p className='text-gray-400 text-xs line-clamp-2'>
                        {example.text}
                      </p>
                      <div className='flex items-center justify-between mt-3'>
                        <span className='text-xs text-gray-500'>
                          Click to analyze
                        </span>
                        <ArrowRight className='w-4 h-4 text-primary opacity-0 group-hover:opacity-100 transition-opacity' />
                      </div>
                    </div>
                  </button>
                ))}
              </div>
            </section>

            {/* Threat Trends Section */}
            <section>
              <ThreatTrendsSection />
            </section>
          </aside>
        </div>
      </div>
    </div>
  );
};

export default Homepage;