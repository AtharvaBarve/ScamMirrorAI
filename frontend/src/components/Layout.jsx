import { Outlet, useNavigate } from 'react-router-dom';
import { Moon, Globe, Mail, Code, Shield, ShieldCheck } from 'lucide-react';
import Button from './ui/Button';

const Layout = () => {
  const navigate = useNavigate();

  return (
    <div className="flex flex-col min-h-screen bg-background">
      {/* Premium Navbar */}
      <header className="bg-background/80 backdrop-blur-xl border-b border-border sticky top-0 z-50">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex justify-between items-center h-20">
            {/* Logo */}
            <div className="flex-shrink-0 flex items-center group cursor-pointer" onClick={() => navigate('/')}>
              <div className="relative">
                <Shield className="w-8 h-8 text-primary mr-3 group-hover:scale-110 transition-transform duration-300 relative z-10" />
                <div className="absolute inset-0 bg-primary blur-md opacity-20 group-hover:opacity-50 transition-opacity" />
              </div>
              <span className="text-2xl font-display font-bold text-white tracking-tight">
                ScamMirror
              </span>
            </div>
            
            {/* Main Links */}
            <nav className="hidden lg:flex items-center space-x-8">
              <a href="#/features" onClick={(e) => {
                  if (window.location.hash !== '#/') {
                      e.preventDefault();
                      navigate('/');
                      setTimeout(() => document.getElementById('features')?.scrollIntoView(), 100);
                  }
              }} className="text-sm font-medium text-gray-300 hover:text-white transition-colors duration-200">How it Works</a>
              
              <a href="#/tech" onClick={(e) => {
                  if (window.location.hash !== '#/') {
                      e.preventDefault();
                      navigate('/');
                      setTimeout(() => document.getElementById('tech')?.scrollIntoView(), 100);
                  }
              }} className="text-sm font-medium text-gray-300 hover:text-white transition-colors duration-200">Tech Stack</a>
              
              <a href="#/faq" onClick={(e) => {
                  if (window.location.hash !== '#/') {
                      e.preventDefault();
                      navigate('/');
                      setTimeout(() => document.getElementById('faq')?.scrollIntoView(), 100);
                  }
              }} className="text-sm font-medium text-gray-300 hover:text-white transition-colors duration-200">FAQ</a>
            </nav>

            {/* Right Actions */}
            <div className="hidden md:flex items-center space-x-4">
              <button className="p-2 text-gray-400 hover:text-white transition-colors">
                <Globe className="w-5 h-5" />
              </button>
              <button className="p-2 text-gray-400 hover:text-white transition-colors">
                <Moon className="w-5 h-5" />
              </button>
              <div className="w-px h-6 bg-border mx-2" />
              <Button size="sm" onClick={() => navigate('/login')}>Open Dashboard</Button>
            </div>
          </div>
        </div>
      </header>

      {/* Main Content */}
      <main className="flex-grow">
        <Outlet />
      </main>

      {/* Footer */}
      <footer className="bg-surface border-t border-border mt-auto relative overflow-hidden">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-12">
          <div className="flex flex-col md:flex-row justify-between items-start md:items-center gap-8">
            <div className="max-w-sm">
              <div className="flex items-center mb-4">
                <ShieldCheck className="w-6 h-6 text-primary mr-3" />
                <h3 className="text-white font-display font-bold text-xl">ScamMirror AI</h3>
              </div>
              <p className="text-gray-400 text-sm leading-relaxed mb-6">
                An open-source Hybrid AI threat detection engine built for the ET AI Hackathon 2026. Designed to intercept social engineering attacks locally.
              </p>
              <div className="flex space-x-4">
                <a href="https://github.com/ScamMirrorAI" target="_blank" rel="noopener noreferrer" className="w-10 h-10 rounded-full bg-background border border-border flex items-center justify-center hover:border-primary/50 text-gray-400 hover:text-white transition-all">
                  <Code className="w-5 h-5" />
                </a>
                <a href="mailto:contact@scammirror.ai" className="w-10 h-10 rounded-full bg-background border border-border flex items-center justify-center hover:border-primary/50 text-gray-400 hover:text-white transition-all">
                  <Mail className="w-5 h-5" />
                </a>
              </div>
            </div>
            
            <div className="flex flex-col md:items-end space-y-4">
              <div className="flex items-center text-sm text-gray-400 font-mono">
                <span className="w-2 h-2 rounded-full bg-success mr-2"></span>
                Local Inference Online
              </div>
              <p className="text-sm text-gray-500 font-mono text-left md:text-right">
                &copy; 2026 ET AI Hackathon Prototype.<br />
                Powered by NVIDIA NIM & FastAPI.
              </p>
            </div>
          </div>
        </div>
      </footer>
    </div>
  );
};

export default Layout;