import React from 'react';
import { useRouteError, Link } from 'react-router-dom';
import { AlertOctagon, ArrowLeft } from 'lucide-react';
import Button from './ui/Button';

const ErrorPage = () => {
  const error = useRouteError();
  console.error("React Router caught an error:", error);

  return (
    <div className="min-h-screen bg-background flex flex-col items-center justify-center relative overflow-hidden p-4">
      {/* Background Effects */}
      <div className="absolute top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2 w-[800px] h-[800px] bg-danger/5 blur-[120px] rounded-full pointer-events-none" />
      
      <div className="z-10 text-center max-w-lg mx-auto bg-surface/50 backdrop-blur-xl border border-border p-8 rounded-2xl shadow-card">
        <div className="inline-flex items-center justify-center w-16 h-16 rounded-full bg-danger/20 text-danger mb-6">
          <AlertOctagon className="w-8 h-8" />
        </div>
        
        <h1 className="text-4xl font-display font-bold text-white mb-4">
          404 Not Found
        </h1>
        
        <p className="text-gray-400 mb-8 leading-relaxed font-sans">
          The intelligence sector you are trying to access does not exist or has been heavily redacted. Please verify your clearance level or return to the main dashboard.
        </p>

        {error && error.statusText && (
          <div className="mb-8 p-4 bg-background/50 rounded-lg border border-danger/20 font-mono text-sm text-danger/80">
            [SYS_ERR]: {error.statusText || error.message}
          </div>
        )}

        <div className="flex justify-center">
          <Link to="/">
            <Button size="lg" className="group">
              <ArrowLeft className="w-5 h-5 mr-2 group-hover:-translate-x-1 transition-transform" />
              Return to Safety
            </Button>
          </Link>
        </div>
      </div>
    </div>
  );
};

export default ErrorPage;
