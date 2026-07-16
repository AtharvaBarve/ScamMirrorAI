import React from 'react';
import HeroSection from './HeroSection';
import SocialProofSection from './SocialProofSection';
import StatsSection from './StatsSection';
import FeaturesSection from './FeaturesSection';
import TimelineSection from './TimelineSection';
import ThreatFeedSection from './ThreatFeedSection';
import FAQSection from './FAQSection';
import AnimatedPage from '../AnimatedPage';

const LandingPage = () => {
  return (
    <AnimatedPage className="bg-background min-h-screen text-white selection:bg-primary/30">
      <HeroSection />
      <SocialProofSection />
      <StatsSection />
      <FeaturesSection />
      <TimelineSection />
      <ThreatFeedSection />
      <FAQSection /> 
    </AnimatedPage>
  );
};

export default LandingPage;
