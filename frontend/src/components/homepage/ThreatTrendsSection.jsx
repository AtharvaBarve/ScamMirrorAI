import React from 'react';

const ThreatTrendsSection = () => {
  // Mock data for trending scam categories - would come from GET /community/trends endpoint
  const trendingCategories = [
    { name: 'AI Voice Scams', change: +45, isPositive: false },
    { name: 'Cryptocurrency Giveaways', change: +32, isPositive: false },
    { name: 'Fake Job Offers', change: +28, isPositive: false },
    { name: 'Romance Scams', change: +15, isPositive: false },
    { name: 'Tech Support Scams', change: -8, isPositive: true },
    { name: 'IRS/Tax Scams', change: -12, isPositive: true },
    { name: 'Lottery/Prize Scams', change: -5, isPositive: true },
    { name: 'Charity Fraud', change: +22, isPositive: false }
  ];

  return (
    <section className='py-16 bg-[#111113/20]'>
      <div className='max-w-4xl mx-auto px-6 lg:px-12'>
        <h2 className='text-2xl font-bold text-white mb-8 text-center'>
          Threat Trends
        </h2>
        <p className='text-center text-gray-400 mb-10 max-w-2xl mx-auto'>
          Stay informed about the latest scam trends targeting our community
        </p>

        <div className='grid gap-6 sm:grid-cols-2 lg:grid-cols-4'>
          {trendingCategories.map((category, index) => (
            <div key={index} className='bg-[#111113/30] border border-[#111113/20] rounded-xl p-4 text-center'>
              <div className='flex items-center justify-content mb-3'>
                <span className='text-2xl mr-2'>
                  {category.isPositive ? '📉' : '📈'}
                </span>
                <span className={`font-semibold text-${category.isPositive ? '#22C55E' : '#FF4D6D'}`}>
                  {Math.abs(category.change)}%
                </span>
              </div>
              <h3 className='font-bold text-white mb-2'>
                {category.name}
              </h3>
              <p className='text-gray-400 text-sm'>
                {category.isPositive ? 'Decreasing' : 'Increasing'} threat
              </p>
            </div>
          ))}
        </div>
      </div>
    </section>
  );
};

export default ThreatTrendsSection;