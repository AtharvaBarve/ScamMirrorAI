import React, { useState, useEffect } from 'react';
import { Card, CardHeader, CardTitle, CardContent } from '../ui/Card';
import Badge from '../ui/Badge';
import AnimatedPage from '../AnimatedPage';
import { LineChart, TrendingUp, TrendingDown, Minus } from 'lucide-react';
import SkeletonLoader from '../SkeletonLoader';

const ThreatTrendsPage = () => {
  const [trendingThreats, setTrendingThreats] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    // Mock Data for Demo
    const mockData = [
      { id: 1, name: 'Phishing Attack', trend: 'up', change: 23, severity: 'danger' },
      { id: 2, name: 'Fake Invoice Scam', trend: 'up', change: 18, severity: 'warning' },
      { id: 3, name: 'Tech Support Scam', trend: 'down', change: -12, severity: 'success' },
      { id: 4, name: 'Investment Scam', trend: 'up', change: 31, severity: 'danger' },
      { id: 5, name: 'Romance Scam', trend: 'stable', change: 2, severity: 'primary' },
      { id: 6, name: 'Lottery Scam', trend: 'down', change: -8, severity: 'success' },
    ];

    setTimeout(() => {
      setTrendingThreats(mockData);
      setLoading(false);
    }, 800);
  }, []);

  return (
    <AnimatedPage className="max-w-[1600px] mx-auto w-full space-y-6">
      <div className="flex items-center justify-between mb-8 pb-4 border-b border-border/50">
        <div>
          <h1 className="text-2xl font-display font-bold text-white tracking-tight">Global Threat Trends</h1>
          <p className="text-sm text-gray-400 mt-1">Analyzing shifts in social engineering attack vectors.</p>
        </div>
        <Badge variant="warning" className="animate-pulse">DEMO DATA</Badge>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        <Card className="h-full bg-surface/50 backdrop-blur-xl border-border">
          <CardHeader className="pb-2">
            <div className="flex items-center justify-between">
              <CardTitle className="text-xl font-display flex items-center text-white">
                <LineChart className="w-5 h-5 text-primary mr-3" />
                Trending Categories
              </CardTitle>
            </div>
          </CardHeader>
          <CardContent>
            {loading ? (
              <div className="space-y-4 mt-4">
                <SkeletonLoader className="h-16 w-full rounded-lg" />
                <SkeletonLoader className="h-16 w-full rounded-lg" />
                <SkeletonLoader className="h-16 w-full rounded-lg" />
              </div>
            ) : (
              <div className="space-y-4 mt-4">
                {trendingThreats.map((threat) => (
                  <div key={threat.id} className="flex items-center p-4 bg-surface/30 rounded-xl border border-border hover:bg-surface/50 transition-colors">
                    <div className="flex-1">
                      <h4 className="font-semibold text-white mb-1">{threat.name}</h4>
                      <div className="flex items-center text-sm">
                        <span className={`flex items-center mr-3 ${
                          threat.trend === 'up' ? 'text-danger' : 
                          threat.trend === 'down' ? 'text-success' : 'text-primary'
                        }`}>
                          {threat.trend === 'up' ? <TrendingUp className="w-4 h-4 mr-1" /> : 
                           threat.trend === 'down' ? <TrendingDown className="w-4 h-4 mr-1" /> : 
                           <Minus className="w-4 h-4 mr-1" />}
                          {Math.abs(threat.change)}%
                        </span>
                        <span className="text-gray-400">last 24h</span>
                      </div>
                    </div>
                  </div>
                ))}
              </div>
            )}
          </CardContent>
        </Card>
      </div>
    </AnimatedPage>
  );
};

export default ThreatTrendsPage;
