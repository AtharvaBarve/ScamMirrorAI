import React from 'react';

const SocialProofSection = () => {
  const technologies = [
    'NVIDIA NIM',
    'FastAPI',
    'React',
    'Tailwind CSS',
    'Framer Motion',
    'LLaMA 3'
  ];

  return (
    <section id="tech" className="py-12 border-y border-border bg-background">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 text-center">
        <p className="text-sm font-mono text-gray-500 mb-8 uppercase tracking-widest">Built with Modern Architecture</p>
        <div className="flex flex-wrap justify-center items-center gap-6 md:gap-12">
          {technologies.map((tech, idx) => (
            <div key={idx} className="px-4 py-2 rounded-full border border-border/50 bg-surface/50 text-sm font-mono text-gray-300 tracking-wide hover:border-primary/50 transition-colors">
              {tech}
            </div>
          ))}
        </div>
      </div>
    </section>
  );
};

export default SocialProofSection;
