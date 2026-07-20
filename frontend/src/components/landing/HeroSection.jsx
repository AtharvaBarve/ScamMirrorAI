import React from 'react';
import { motion } from 'framer-motion';
import Button from '../ui/Button';
import { Shield, ChevronRight } from 'lucide-react';
import { useNavigate } from 'react-router-dom';

const HeroSection = () => {
  const navigate = useNavigate();

  return (
    <section className="relative pt-32 pb-20 lg:pt-48 lg:pb-32 overflow-hidden">
      {/* Subtle Tech Background */}
      <div className="absolute inset-0 bg-background pointer-events-none opacity-40">
        <div className="absolute inset-0" style={{
          backgroundImage: `radial-gradient(#1f2937 1px, transparent 1px)`,
          backgroundSize: '32px 32px',
          maskImage: 'linear-gradient(to bottom, black, transparent)'
        }} />
        <div className="absolute inset-0 bg-gradient-to-b from-primary/5 to-transparent" />
      </div>

      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 relative z-10 text-center">
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.6 }}
        >
          <div className="inline-flex items-center px-4 py-2 rounded-full bg-surface/80 backdrop-blur border border-border mb-8 shadow-card">
            <Shield className="w-5 h-5 text-primary mr-2" />
            <span className="text-sm font-mono font-medium text-gray-300 tracking-wide">ET AI Hackathon Prototype</span>
          </div>
        </motion.div>

        <motion.h1 
          className="text-5xl md:text-7xl font-display font-bold text-white mb-8 leading-tight tracking-tight max-w-5xl mx-auto"
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.6, delay: 0.1 }}
        >
          AI-Powered Scam Detection <span className="text-primary">Engine</span>
        </motion.h1>

        <motion.p 
          className="text-lg md:text-xl text-gray-400 mb-12 max-w-3xl mx-auto font-sans leading-relaxed"
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.6, delay: 0.2 }}
        >
          Instantly analyze suspicious texts, emails, and URLs. ScamMirror AI combines a fine-tuned DeBERTa classifier with a ChromaDB RAG pipeline and NVIDIA NIM to intercept social engineering attacks before they compromise your data.
        </motion.p>

        <motion.div 
          className="flex flex-col sm:flex-row items-center justify-center gap-4"
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.6, delay: 0.3 }}
        >
          <Button size="lg" className="w-full sm:w-auto px-8 py-4 text-lg" onClick={() => navigate('/login')}>
            Try the Dashboard
          </Button>
          <a href="#/features" onClick={(e) => {
                  if (window.location.hash !== '#/') {
                      e.preventDefault();
                      navigate('/');
                      setTimeout(() => document.getElementById('features')?.scrollIntoView(), 100);
                  }
              }}>
            <Button variant="secondary" size="lg" className="w-full sm:w-auto px-8 py-4 text-lg group bg-surface/50 border-border hover:bg-surface">
              Explore Features
              <ChevronRight className="w-5 h-5 ml-2 text-gray-400 group-hover:text-white transition-colors" />
            </Button>
          </a>
        </motion.div>
      </div>
    </section>
  );
};

export default HeroSection;
