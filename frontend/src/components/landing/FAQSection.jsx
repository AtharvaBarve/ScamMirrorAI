import React, { useState } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { ChevronDown } from 'lucide-react';

const FAQItem = ({ question, answer }) => {
  const [isOpen, setIsOpen] = useState(false);

  return (
    <div className="border-b border-border">
      <button
        onClick={() => setIsOpen(!isOpen)}
        className="flex w-full items-center justify-between py-6 text-left focus:outline-none"
      >
        <span className="font-display text-lg font-semibold text-white">{question}</span>
        <ChevronDown 
          className={`w-5 h-5 text-gray-400 transition-transform duration-300 ${isOpen ? 'rotate-180' : ''}`} 
        />
      </button>
      <AnimatePresence>
        {isOpen && (
          <motion.div
            initial={{ height: 0, opacity: 0 }}
            animate={{ height: 'auto', opacity: 1 }}
            exit={{ height: 0, opacity: 0 }}
            transition={{ duration: 0.3 }}
            className="overflow-hidden"
          >
            <p className="pb-6 text-gray-400 leading-relaxed">
              {answer}
            </p>
          </motion.div>
        )}
      </AnimatePresence>
    </div>
  );
};

const FAQSection = () => {
  const faqs = [
    {
      question: 'How is ScamMirror different from standard antivirus?',
      answer: 'Standard antivirus relies heavily on known signatures and hashes. ScamMirror uses a Hybrid AI engine to understand the semantic intent of messages, catching zero-day social engineering and deepfake scams that bypass traditional filters.'
    },
    {
      question: 'Is my data kept private?',
      answer: 'Yes. ScamMirror operates on a stateless architecture. We analyze the text or URL for threats and immediately discard the payload. We do not store your private messages or emails in our databases.'
    },
    {
      question: 'Is ScamMirror open source?',
      answer: 'Yes! ScamMirror is built as a prototype for the ET AI Hackathon 2026. The entire frontend (React) and backend (FastAPI) can be run locally on your own hardware for maximum privacy.'
    },
    {
      question: 'Can I integrate ScamMirror into my own apps?',
      answer: 'Absolutely. The core threat detection engine is exposed via a standard REST API built with FastAPI, making it easy to plug into your own Slack bots, Discord servers, or email filters.'
    }
  ];

  return (
    <section id="faq" className="py-24">
      <div className="max-w-3xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="text-center mb-16">
          <h2 className="text-3xl md:text-5xl font-display font-bold text-white mb-6">
            Frequently Asked Questions
          </h2>
        </div>
        <div className="bg-surface/30 backdrop-blur-md rounded-2xl border border-border p-8">
          {faqs.map((faq, idx) => (
            <FAQItem key={idx} question={faq.question} answer={faq.answer} />
          ))}
        </div>
      </div>
    </section>
  );
};

export default FAQSection;
