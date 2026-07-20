import React from 'react';
import { motion } from 'framer-motion';

const StatsSection = () => {
  const stats = [
    { value: '34', label: 'Data Logged' },
    { value: 'Local', label: 'AI Inference' },
    { value: '<1s', label: 'Analysis Time' },
    { value: 'Hybrid', label: 'Detection Engine' }
  ];

  return (
    <section className="py-24 relative border-y border-border/50 bg-background/50">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 relative z-10">
        <div className="grid grid-cols-2 lg:grid-cols-4 gap-8">
          {stats.map((stat, idx) => (
            <motion.div 
              key={idx}
              className="text-center"
              initial={{ opacity: 0, y: 20 }}
              whileInView={{ opacity: 1, y: 0 }}
              viewport={{ once: true }}
              transition={{ delay: idx * 0.1, duration: 0.5 }}
            >
              <div className="text-4xl md:text-5xl lg:text-6xl font-mono font-bold text-white mb-2 shadow-primary/20 drop-shadow-[0_0_15px_rgba(255,255,255,0.1)]">
                {stat.value}
              </div>
              <div className="text-primary font-sans text-sm md:text-base font-medium tracking-widest uppercase">
                {stat.label}
              </div>
            </motion.div>
          ))}
        </div>
      </div>
    </section>
  );
};

export default StatsSection;
