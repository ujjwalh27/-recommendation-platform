
import RecommendationPanel from "../recommendation/RecommendationPanel";
import FeedController from "./FeedController";
import AnalyticsPanel from "../analytics/AnalyticsPanel";

function VideoFeed() {

  const rankedVideos =
    RecommendationEngine.rankVideos(videos);

  return (

    <div
      style={{
        display:"flex",
        justifyContent:"center",
        alignItems:"center",
        gap:"30px",
        height:"100vh",
        background:"#000"
      }}
    >

      <FeedController />

      <AnalyticsPanel />

      <RecommendationPanel />

    </div>

  );

}

export default VideoFeed;