import { useMemo, useState } from "react";
import videos from "../../data/videos";
import RecommendationEngine from "../recommendation/RecommendationEngine";
import VideoCard from "./VideoCard";

function FeedController() {
  const [currentIndex, setCurrentIndex] = useState(0);

  // Rank videos whenever this component renders
  const rankedVideos = useMemo(() => {
    return RecommendationEngine.rankVideos(videos);
  }, []);

  const nextVideo = () => {
    if (currentIndex < rankedVideos.length - 1) {
      setCurrentIndex(currentIndex + 1);
    }
  };

  const previousVideo = () => {
    if (currentIndex > 0) {
      setCurrentIndex(currentIndex - 1);
    }
  };

  return (
    <div>
      <VideoCard video={rankedVideos[currentIndex]} />

      <div
        style={{
          marginTop: 20,
          display: "flex",
          justifyContent: "space-between",
        }}
      >
        <button onClick={previousVideo}>⬅ Previous</button>

        <span>
          {currentIndex + 1} / {rankedVideos.length}
        </span>

        <button onClick={nextVideo}>Next ➡</button>
      </div>
    </div>
  );
}

export default FeedController;