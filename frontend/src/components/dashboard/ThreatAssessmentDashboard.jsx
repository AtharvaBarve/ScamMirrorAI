import React, { useState } from 'react';
import { useAnalysis } from '../../context/AnalysisContext';
import useAnalyze from '../../hooks/useAnalyze';
import SkeletonLoader from '../SkeletonLoader';
import ThreatLevelSection from './ThreatLevelSection';
import ExplanationSection from './ExplanationSection';
import DetectedThreatsSection from './DetectedThreatsSection';
import CommunityIntelligenceSection from './CommunityIntelligenceSection';
import ProtectOthersSection from './ProtectOthersSection';
import ThreatReportSection from './ThreatReportSection';
import AnimatedPage from '../AnimatedPage';
import { Card, CardContent } from '../ui/Card';
import Button from '../ui/Button';
import Input from '../ui/Input';
import { ShieldAlert, Link as LinkIcon, Image as ImageIcon } from 'lucide-react';

const ThreatAssessmentDashboard = () => {
  const { analysisResult: result, loading, setAnalysis } = useAnalysis();
  const { execute, error } = useAnalyze();
  
  const [inputType, setInputType] = useState('message');
  const [inputValue, setInputValue] = useState('');

  const handleAnalyze = async (e) => {
    e.preventDefault();
    if (!inputValue.trim()) return;

    const payload = inputType === 'message'
      ? { text: inputValue.trim() }
      : { url: inputValue.trim() };

    await execute(payload);
  };

  if (loading && !result) {
    // Show skeleton loaders in the new enterprise grid layout
    return (
      <div className="max-w-[1600px] mx-auto w-full space-y-6">
        <div className="flex items-center justify-between mb-8">
          <div>
            <h1 className="text-2xl font-display font-bold text-white tracking-tight">Threat Assessment</h1>
            <p className="text-sm text-gray-400 mt-1">Analyzing incoming signals and correlating with global intelligence...</p>
          </div>
          <SkeletonLoader className="h-10 w-32 rounded-lg" />
        </div>

        <div className="grid grid-cols-1 lg:grid-cols-12 gap-6">
          {/* Top Row */}
          <div className="lg:col-span-4 bg-surface/50 backdrop-blur-sm rounded-xl border border-border p-6 shadow-card">
            <h3 className="text-lg font-display font-semibold text-white mb-4">Threat Level</h3>
            <SkeletonLoader className="h-16 w-16 mx-auto rounded-full mb-4" />
            <SkeletonLoader className="h-4 w-3/4 mx-auto mb-2" />
            <SkeletonLoader className="h-4 w-1/2 mx-auto" />
          </div>

          <div className="lg:col-span-8 bg-surface/50 backdrop-blur-sm rounded-xl border border-border p-6 shadow-card">
            <h3 className="text-lg font-display font-semibold text-white mb-4">AI Explanation</h3>
            <SkeletonLoader className="h-4 w-full mb-3" />
            <SkeletonLoader className="h-4 w-full mb-3" />
            <SkeletonLoader className="h-4 w-5/6 mb-3" />
            <SkeletonLoader className="h-4 w-4/6" />
          </div>

          {/* Middle Row */}
          <div className="lg:col-span-6 bg-surface/50 backdrop-blur-sm rounded-xl border border-border p-6 shadow-card">
            <h3 className="text-lg font-display font-semibold text-white mb-4">Detected Threats</h3>
            <div className="space-y-3">
              <SkeletonLoader className="h-12 w-full rounded-lg" />
              <SkeletonLoader className="h-12 w-full rounded-lg" />
              <SkeletonLoader className="h-12 w-full rounded-lg" />
            </div>
          </div>

          <div className="lg:col-span-6 bg-surface/50 backdrop-blur-sm rounded-xl border border-border p-6 shadow-card">
            <h3 className="text-lg font-display font-semibold text-white mb-4">Community Intelligence</h3>
            <div className="space-y-4">
              <SkeletonLoader className="h-20 w-full rounded-lg" />
              <SkeletonLoader className="h-20 w-full rounded-lg" />
            </div>
          </div>

          {/* Bottom Row */}
          <div className="lg:col-span-4 bg-surface/50 backdrop-blur-sm rounded-xl border border-border p-6 shadow-card">
            <h3 className="text-lg font-display font-semibold text-white mb-4">Protection & Actions</h3>
            <div className="space-y-3">
              <SkeletonLoader className="h-10 w-full rounded-lg" />
              <SkeletonLoader className="h-10 w-full rounded-lg" />
            </div>
          </div>

          <div className="lg:col-span-8 bg-surface/50 backdrop-blur-sm rounded-xl border border-border p-6 shadow-card">
            <h3 className="text-lg font-display font-semibold text-white mb-4">Incident Report</h3>
            <div className="flex justify-between items-center mb-4">
              <SkeletonLoader className="h-8 w-40 rounded" />
              <SkeletonLoader className="h-8 w-24 rounded" />
            </div>
            <SkeletonLoader className="h-32 w-full rounded-lg" />
          </div>
        </div>
      </div>
    );
  }

  if (!result) {
    return (
      <AnimatedPage className="max-w-4xl mx-auto w-full pt-12">
        <div className="text-center mb-10">
          <h1 className="text-3xl font-display font-bold text-white tracking-tight mb-3">Analyze New Threat</h1>
          <p className="text-gray-400">Enter a suspicious message, email, or URL to perform a deep heuristic and semantic analysis.</p>
        </div>

        <Card className="border-border bg-surface/50 backdrop-blur-xl shadow-2xl">
          <CardContent className="p-8">
            <form onSubmit={handleAnalyze} className="space-y-6">
              {/* Input Tabs */}
              <div className="flex border-b border-border pb-2">
                <button
                  type="button"
                  onClick={() => setInputType('message')}
                  className={`flex-1 px-4 py-3 text-center font-medium transition-all duration-200 flex items-center justify-center
                    ${inputType === 'message'
                      ? 'text-white border-b-2 border-primary bg-surface/30'
                      : 'text-gray-400 hover:text-white hover:bg-surface/20'}
                  `}
                >
                  <ShieldAlert className="w-4 h-4 mr-2" />
                  Text / Email
                </button>
                <button
                  type="button"
                  onClick={() => setInputType('url')}
                  className={`flex-1 px-4 py-3 text-center font-medium transition-all duration-200 flex items-center justify-center
                    ${inputType === 'url'
                      ? 'text-white border-b-2 border-primary bg-surface/30'
                      : 'text-gray-400 hover:text-white hover:bg-surface/20'}
                  `}
                >
                  <LinkIcon className="w-4 h-4 mr-2" />
                  Website URL
                </button>
                <button
                  type="button"
                  disabled
                  className="flex-1 px-4 py-3 text-center font-medium transition-all duration-200 flex items-center justify-center text-gray-500 cursor-not-allowed"
                >
                  <ImageIcon className="w-4 h-4 mr-2" />
                  Image (Soon)
                </button>
              </div>

              {/* Input Field */}
              <div>
                <label className="block text-sm font-medium text-gray-300 mb-2">
                  {inputType === 'message' ? 'Paste Suspicious Text' : 'Enter Website URL'}
                </label>
                <Input
                  type={inputType === 'message' ? 'text' : 'url'}
                  placeholder={
                    inputType === 'message'
                      ? 'e.g. URGENT: Your account has been locked. Click here...'
                      : 'e.g. https://bit.ly/secure-login-123'
                  }
                  value={inputValue}
                  onChange={(e) => setInputValue(e.target.value)}
                  className="bg-background/50 border-border h-14"
                />
              </div>

              {/* Error Display */}
              {error && (
                <div className="p-4 bg-danger/10 border border-danger/20 rounded-lg text-danger text-sm font-medium flex items-center">
                  <ShieldAlert className="w-5 h-5 mr-2" />
                  {error}
                </div>
              )}

              {/* Submit Button */}
              <Button
                type="submit"
                disabled={loading || !inputValue.trim()}
                className="w-full h-14 text-lg"
                size="lg"
              >
                Start Analysis
              </Button>
            </form>
          </CardContent>
        </Card>
      </AnimatedPage>
    );
  }

  const handleNewThreat = () => {
    setAnalysis(null);
  };

  return (
    <AnimatedPage className="max-w-[1600px] mx-auto w-full space-y-6">
      <div className="flex flex-col md:flex-row md:items-center justify-between gap-4 mb-8 pb-4 border-b border-border/50">
        <div>
          <h1 className="text-2xl font-display font-bold text-white tracking-tight">Threat Assessment</h1>
          <p className="text-sm text-gray-400 mt-1 font-mono">ID: {result.id || `EVT-${Date.now().toString().slice(-6)}`} | Timestamp: {new Date().toISOString()}</p>
        </div>
        <Button variant="secondary" onClick={handleNewThreat}>
          Analyze New Threat
        </Button>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-12 gap-6">
        <div className="lg:col-span-4">
          <ThreatLevelSection result={result} />
        </div>
        <div className="lg:col-span-8">
          <ExplanationSection result={result} />
        </div>
        <div className="lg:col-span-6">
          <DetectedThreatsSection result={result} />
        </div>
        <div className="lg:col-span-6">
          <CommunityIntelligenceSection result={result} />
        </div>
        <div className="lg:col-span-4">
          <ProtectOthersSection result={result} />
        </div>
        <div className="lg:col-span-8">
          <ThreatReportSection result={result} />
        </div>
      </div>
    </AnimatedPage>
  );
};

export default ThreatAssessmentDashboard;