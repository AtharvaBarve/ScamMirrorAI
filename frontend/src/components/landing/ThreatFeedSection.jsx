import React from 'react';
import { motion } from 'framer-motion';
import { Card, CardContent } from '../ui/Card';
import Badge from '../ui/Badge';
import { AlertCircle, Clock } from 'lucide-react';

const ThreatFeedSection = () => {
  const threats = [
    { type: 'Financial Scam', severity: 'danger', time: '2 mins ago', family: 'Crypto/Web3', status: 'Blocked' },
    { type: 'Deepfake Voice', severity: 'danger', time: '15 mins ago', family: 'CEO Fraud', status: 'Blocked' },
    { type: 'Fake Invoice', severity: 'warning', time: '1 hr ago', family: 'Vendor Fraud', status: 'Flagged' },
    { type: 'OTP Scam', severity: 'danger', time: '2 hrs ago', family: 'Account Takeover', status: 'Blocked' },
    { type: 'Police Impersonation', severity: 'warning', time: '5 hrs ago', family: 'Social Engineering', status: 'Flagged' },
  ];

  return (
    <section className="py-24 bg-surface/20 border-y border-border">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="flex flex-col lg:flex-row gap-16 items-center">
          
          <div className="w-full lg:w-1/2">
            <h2 className="text-3xl md:text-5xl font-display font-bold text-white mb-6">
              Live Threat Intelligence
            </h2>
            <p className="text-gray-400 text-lg mb-8 leading-relaxed">
              Our community intelligence network intercepts and analyzes thousands of novel threats daily. When one organization identifies a new phishing vector, the entire network is instantly immunized.
            </p>
            <ul className="space-y-4 mb-8">
              <li className="flex items-center text-gray-300">
                <AlertCircle className="w-5 h-5 text-primary mr-3" />
                Real-time signature sharing
              </li>
              <li className="flex items-center text-gray-300">
                <AlertCircle className="w-5 h-5 text-primary mr-3" />
                Cross-organization threat correlation
              </li>
              <li className="flex items-center text-gray-300">
                <AlertCircle className="w-5 h-5 text-primary mr-3" />
                Automated indicator of compromise (IOC) extraction
              </li>
            </ul>
          </div>

          <div className="w-full lg:w-1/2">
            <Card className="border-border/50 bg-background/50">
              <CardContent className="p-0">
                <div className="p-4 border-b border-border flex justify-between items-center bg-surface/50">
                  <h3 className="font-mono text-sm text-gray-300 flex items-center">
                    <span className="w-2 h-2 rounded-full bg-danger mr-2 animate-pulse" />
                    LIVE INTERCEPTS
                  </h3>
                  <span className="font-mono text-xs text-gray-500 flex items-center">
                    <Clock className="w-3 h-3 mr-1" />
                    Updating
                  </span>
                </div>
                <div className="divide-y divide-border/50 h-[400px] overflow-hidden relative">
                  {/* Subtle fade at bottom */}
                  <div className="absolute bottom-0 left-0 right-0 h-20 bg-gradient-to-t from-background to-transparent z-10 pointer-events-none" />
                  
                  {threats.map((threat, idx) => (
                    <motion.div 
                      key={idx}
                      className="p-4 flex items-center justify-between hover:bg-surface/30 transition-colors"
                      initial={{ opacity: 0, x: 20 }}
                      whileInView={{ opacity: 1, x: 0 }}
                      viewport={{ once: true }}
                      transition={{ delay: idx * 0.1 }}
                    >
                      <div>
                        <div className="flex items-center gap-3 mb-1">
                          <span className="font-display font-semibold text-white">{threat.type}</span>
                          <Badge variant={threat.severity}>{threat.severity.toUpperCase()}</Badge>
                        </div>
                        <div className="text-xs text-gray-500 font-mono">
                          Family: {threat.family} | {threat.time}
                        </div>
                      </div>
                      <div>
                        <span className={`text-xs font-mono px-2 py-1 rounded border ${threat.status === 'Blocked' ? 'border-danger/30 text-danger' : 'border-warning/30 text-warning'}`}>
                          {threat.status}
                        </span>
                      </div>
                    </motion.div>
                  ))}
                </div>
              </CardContent>
            </Card>
          </div>

        </div>
      </div>
    </section>
  );
};

export default ThreatFeedSection;
