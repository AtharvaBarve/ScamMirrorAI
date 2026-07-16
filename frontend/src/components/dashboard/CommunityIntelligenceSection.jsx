import React from 'react';
import { useAnalysis } from '../../context/AnalysisContext';
import { Card, CardHeader, CardTitle, CardContent } from '../ui/Card';
import { Users, Tag, BarChart2, Clock, Calendar, Hash, ShieldCheck } from 'lucide-react';

const CommunityIntelligenceSection = () => {
  const { analysisResult } = useAnalysis();

  // Extract community intelligence data if available
  const communityIntelligence = analysisResult?.community_intelligence || {};

  // Fallback to category if no community intelligence
  const threatFamily = communityIntelligence.threat_family || analysisResult?.category || 'Unknown';

  // Format dates if available
  const formatDate = (dateString) => {
    if (!dateString) return 'N/A';
    try {
      // Handle ISO string from backend
      const date = new Date(dateString);
      return date.toLocaleDateString(undefined, { year: 'numeric', month: 'short', day: 'numeric' });
    } catch (e) {
      return dateString;
    }
  };

  // Calculate time ago from first seen
  const getTimeAgo = (dateString) => {
    if (!dateString) return 'N/A';
    try {
      const date = new Date(dateString);
      const now = new Date();
      const diffTime = Math.abs(now - date);
      const diffDays = Math.floor(diffTime / (1000 * 60 * 60 * 24));

      if (diffDays === 0) return 'Today';
      if (diffDays === 1) return 'Yesterday';
      if (diffDays < 7) return `${diffDays} days ago`;
      if (diffDays < 30) return `${Math.floor(diffDays / 7)} weeks ago`;
      if (diffDays < 365) return `${Math.floor(diffDays / 12)} months ago`;
      return `${Math.floor(diffDays / 365)} years ago`;
    } catch (e) {
      return 'N/A';
    }
  };

  return (
    <Card className="h-full bg-surface/50 backdrop-blur-xl border-border">
      <CardHeader className="pb-2">
        <div className="flex items-center justify-between">
          <CardTitle className="text-xl font-display flex items-center text-white">
            <Users className="w-5 h-5 text-primary mr-3" />
            Community Intel
          </CardTitle>
          <div className="text-xs font-mono text-gray-500">
            {new Date(analysisResult?.created_at || Date.now()).toLocaleTimeString()}
          </div>
        </div>
      </CardHeader>
      
      <CardContent>
        <div className="space-y-4">
          <div className="flex items-center justify-between p-2 rounded-md hover:bg-surface transition-colors">
            <span className="flex items-center text-gray-400 text-sm">
              <Tag className="w-4 h-4 mr-3" />
              Threat Family
            </span>
            <span className="font-mono text-white text-sm">{threatFamily}</span>
          </div>

          <div className="flex items-center justify-between p-2 rounded-md hover:bg-surface transition-colors">
            <span className="flex items-center text-gray-400 text-sm">
              <BarChart2 className="w-4 h-4 mr-3" />
              Reports
            </span>
            <span className="font-mono text-white text-sm">{communityIntelligence.report_count?.toLocaleString() || '0'}</span>
          </div>

          <div className="flex items-center justify-between p-2 rounded-md hover:bg-surface transition-colors">
            <span className="flex items-center text-gray-400 text-sm">
              <Clock className="w-4 h-4 mr-3" />
              Active For
            </span>
            <span className="font-mono text-white text-sm">{communityIntelligence.first_seen ? getTimeAgo(communityIntelligence.first_seen) : 'N/A'}</span>
          </div>

          <div className="flex items-center justify-between p-2 rounded-md hover:bg-surface transition-colors">
            <span className="flex items-center text-gray-400 text-sm">
              <Calendar className="w-4 h-4 mr-3" />
              First Seen
            </span>
            <span className="font-mono text-gray-300 text-sm">{communityIntelligence.first_seen ? formatDate(communityIntelligence.first_seen) : 'N/A'}</span>
          </div>

          <div className="flex items-center justify-between p-2 rounded-md hover:bg-surface transition-colors">
            <span className="flex items-center text-gray-400 text-sm">
              <Calendar className="w-4 h-4 mr-3" />
              Last Seen
            </span>
            <span className="font-mono text-gray-300 text-sm">{communityIntelligence.last_seen ? formatDate(communityIntelligence.last_seen) : 'N/A'}</span>
          </div>

          <div className="flex items-center justify-between p-2 rounded-md hover:bg-surface transition-colors">
            <span className="flex items-center text-gray-400 text-sm">
              <Hash className="w-4 h-4 mr-3" />
              Threat ID
            </span>
            <span className="font-mono text-white text-sm">{communityIntelligence.threat_id || 'N/A'}</span>
          </div>
        </div>

        <div className="mt-6 pt-4 border-t border-border/50">
          <button className="w-full text-left text-gray-400 hover:text-white rounded-lg transition-colors flex items-center space-x-2 text-sm group">
            <ShieldCheck className="w-4 h-4 group-hover:text-primary transition-colors" />
            <span>Protection Guide</span>
          </button>
        </div>
      </CardContent>
    </Card>
  );
};

export default CommunityIntelligenceSection;