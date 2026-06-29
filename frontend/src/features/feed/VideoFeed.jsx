import videos from "../../data/videos";
import VideoCard from "./VideoCard";
import AnalyticsPanel from "../analytics/AnalyticsPanel";

function VideoFeed() {
  return (
    <div
      style={{
        display: "flex",
        justifyContent: "center",
        alignItems: "center",
        gap: "30px",
        height: "100vh",
        background: "#000",
      }}
    >
      <VideoCard video={videos[0]} />

      <AnalyticsPanel />
    </div>
  );
}

export default VideoFeed;