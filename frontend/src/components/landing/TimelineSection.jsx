import React from 'react';
import { motion } from 'framer-motion';
import { MessageSquare, ShieldCheck, Database, BrainCircuit, Share2 } from 'lucide-react';

const TimelineSection = () => {
  const steps = [
    {
      title: 'User Input',
      description: 'User submits a suspicious URL, email, or SMS.',
      icon: <MessageSquare className="w-6 h-6 text-white" />
    },
    {
      title: 'Rule Engine',
      description: 'Fast heuristics catch known patterns instantly.',
      icon: <ShieldCheck className="w-6 h-6 text-white" />
    },
    {
      title: 'Hybrid AI Analysis',
      description: 'NVIDIA NIM powered LLMs analyze semantic intent.',
      icon: <BrainCircuit className="w-6 h-6 text-white" />
    },
    {
      title: 'Community Check',
      description: 'Cross-referenced with global threat intelligence.',
      icon: <Database className="w-6 h-6 text-white" />
    },
    {
      title: 'Threat Report',
      description: 'Actionable verdict and explanation delivered.',
      icon: <Share2 className="w-6 h-6 text-white" />
    }
  ];

  return (
    <section className="py-24 relative overflow-hidden">
      <div className="absolute top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2 w-[1000px] h-[500px] bg-primary/5 blur-[120px] rounded-full pointer-events-none" />
      
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 relative z-10">
        <div className="text-center mb-16">
          <h2 className="text-3xl md:text-5xl font-display font-bold text-white mb-6">
            How ScamMirror Secures Your Business
          </h2>
          <p className="text-gray-400 max-w-2xl mx-auto text-lg">
            Our multi-stage pipeline ensures zero-day threats are caught before they reach your employees.
          </p>
        </div>

        <div className="relative max-w-4xl mx-auto">
          {/* Vertical Line for Mobile */}
          <div className="hidden md:block absolute top-1/2 left-0 right-0 h-0.5 bg-border -translate-y-1/2 z-0" />
          
          <div className="flex flex-col md:flex-row justify-between items-center gap-8 md:gap-4 relative z-10">
            {steps.map((step, idx) => (
              <motion.div 
                key={idx}
                className="flex flex-col items-center text-center w-full md:w-1/5"
                initial={{ opacity: 0, y: 20 }}
                whileInView={{ opacity: 1, y: 0 }}
                viewport={{ once: true }}
                transition={{ delay: idx * 0.15, duration: 0.5 }}
              >
                <div className="w-16 h-16 rounded-full bg-surface border border-primary/30 flex items-center justify-center mb-4 shadow-glow relative">
                  {step.icon}
                  {/* Connectors for desktop */}
                  {idx < steps.length - 1 && (
                    <div className="hidden md:block absolute top-1/2 left-full w-full h-[2px] bg-gradient-to-r from-primary/50 to-transparent -translate-y-1/2 z-[-1]" />
                  )}
                </div>
                <h3 className="text-lg font-display font-bold text-white mb-2">{step.title}</h3>
                <p className="text-sm text-gray-400">{step.description}</p>
              </motion.div>
            ))}
          </div>
        </div>
      </div>
    </section>
  );
};

export default TimelineSection;
