import { useState, useCallback } from "react";
import RecommendationPanel from "../recommendation/RecommendationPanel";
import FeedController from "./FeedController";
import AnalyticsPanel from "../analytics/AnalyticsPanel";

function VideoFeed() {
  const [rankedVideos, setRankedVideos] = useState([]);

  const handleFeedUpdated = useCallback((updatedFeed) => {
    setRankedVideos(updatedFeed);
  }, []);

  return (
    <div className="layout-container">
      {/* Main Reels Swiper Feed */}
      <FeedController onFeedUpdated={handleFeedUpdated} />

      {/* Real-time Recommendation & Analytics Sidebars (hidden on mobile/tablet) */}
      <div className="debug-panel" style={{ display: 'flex', gap: '20px', height: '90vh', alignItems: 'center' }}>
        <AnalyticsPanel />
        <RecommendationPanel rankedVideos={rankedVideos} />
      </div>
    </div>
  );
}

export default VideoFeed;