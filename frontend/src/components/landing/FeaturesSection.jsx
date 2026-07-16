import React from 'react';
import { motion } from 'framer-motion';
import { Card, CardContent } from '../ui/Card';
import { ShieldAlert, Link, Users, FileText, Cpu, Lock } from 'lucide-react';

const FeaturesSection = () => {
  const features = [
    {
      title: 'Hybrid AI Engine',
      description: 'Combines heuristic rule-based detection with local Large Language Models (LLaMA 3) to analyze text semantics and intent.',
      icon: <Cpu className="w-8 h-8 text-primary" />
    },
    {
      title: 'Real-time URL Analysis',
      description: 'Deep scan suspicious links to extract hidden structures and identify zero-day phishing sites before they are reported.',
      icon: <Link className="w-8 h-8 text-primary" />
    },
    {
      title: 'Community Intelligence',
      description: 'Opt-in crowdsourced threat data. Share anonymized threat hashes so when one user is protected, the whole network learns.',
      icon: <Users className="w-8 h-8 text-primary" />
    },
    {
      title: 'Explainable Detection',
      description: 'AI that explains its reasoning. ScamMirror identifies the exact risk factors in a message (urgency, spoofing, authority).',
      icon: <ShieldAlert className="w-8 h-8 text-primary" />
    },
    {
      title: 'Exportable Reports',
      description: 'Generate standardized JSON and HTML threat reports for incident response or personal record keeping.',
      icon: <FileText className="w-8 h-8 text-primary" />
    },
    {
      title: 'Zero Data Logged',
      description: 'All analysis is processed statelessly. Your private texts, emails, and browsing history are never stored on our servers.',
      icon: <Lock className="w-8 h-8 text-primary" />
    }
  ];

  return (
    <section id="features" className="py-24 bg-surface/20">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="text-center mb-16">
          <h2 className="text-3xl md:text-5xl font-display font-bold text-white mb-6">
            Core Platform Capabilities
          </h2>
          <p className="text-gray-400 max-w-2xl mx-auto text-lg">
            ScamMirror AI integrates multiple defense mechanisms into a single, privacy-focused open-source tool.
          </p>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8">
          {features.map((feature, idx) => (
            <motion.div
              key={idx}
              initial={{ opacity: 0, y: 20 }}
              whileInView={{ opacity: 1, y: 0 }}
              viewport={{ once: true }}
              transition={{ delay: idx * 0.1, duration: 0.5 }}
            >
              <Card className="h-full hover:border-primary/50 transition-colors group">
                <CardContent className="p-8">
                  <div className="mb-6 p-4 bg-background rounded-lg inline-block group-hover:scale-110 transition-transform duration-300">
                    {feature.icon}
                  </div>
                  <h3 className="text-xl font-display font-bold text-white mb-3">
                    {feature.title}
                  </h3>
                  <p className="text-gray-400 leading-relaxed">
                    {feature.description}
                  </p>
                </CardContent>
              </Card>
            </motion.div>
          ))}
        </div>
      </div>
    </section>
  );
};

export default FeaturesSection;
