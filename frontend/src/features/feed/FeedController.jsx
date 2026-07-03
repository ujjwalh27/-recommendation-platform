import { useEffect, useState } from "react";

import videos from "../../data/videos";

import RecommendationEngine from "../recommendation/RecommendationEngine";
import InterestProfileManager from "../recommendation/InterestProfileManager";
import CreatorAffinityManager from "../recommendation/CreatorAffinityManager";
import SessionManager from "../recommendation/SessionManager";

import VideoCard from "./VideoCard";

function FeedController({ onFeedUpdated }) {

  const [feed, setFeed] = useState([]);
  const [currentIndex, setCurrentIndex] = useState(0);

  useEffect(() => {

    const refreshFeed = () => {

      console.log("🔄 Recommendation Refresh Triggered");

      const rankedFeed =
        RecommendationEngine.rankVideos(videos);

      console.log("🆕 New Ranking");
      console.table(
        rankedFeed.map(video => ({
          Title: video.title,
          Score: video.recommendationScore
        }))
      );

      setFeed(rankedFeed);

      // Notify parent (App.jsx)
      if (onFeedUpdated) {
        onFeedUpdated(rankedFeed);
      }

      // If current index becomes invalid after refresh
      setCurrentIndex(prev =>
        prev >= rankedFeed.length ? 0 : prev
      );

    };

    // Initial recommendation generation
    refreshFeed();

    // Subscribe for live updates
    InterestProfileManager.subscribe(
      refreshFeed
    );

    CreatorAffinityManager.subscribe(
      refreshFeed
    );

    return () => {

      InterestProfileManager.unsubscribe(
        refreshFeed
      );

      CreatorAffinityManager.unsubscribe(
        refreshFeed
      );

    };

  }, [onFeedUpdated]);

  // --------------------------
  // Navigation
  // --------------------------

  const nextVideo = () => {

    if (feed.length === 0) return;

    SessionManager.incrementSession();

    if (currentIndex < feed.length - 1) {

      setCurrentIndex(currentIndex + 1);

    } else {

      console.log("📺 End of Feed");

    }

  };

  const previousVideo = () => {

    if (currentIndex > 0) {

      setCurrentIndex(currentIndex - 1);

    }

  };

  // --------------------------
  // Loading
  // --------------------------

  if (feed.length === 0) {

    return (

      <div
        style={{
          width: 400,
          height: "90vh",
          display: "flex",
          justifyContent: "center",
          alignItems: "center",
          fontSize: 20
        }}
      >
        Loading Recommendations...
      </div>

    );

  }

  // --------------------------
  // UI
  // --------------------------

  return (

    <div>

      <VideoCard
        video={feed[currentIndex]}
      />

      <div
        style={{
          marginTop: 20,
          display: "flex",
          justifyContent: "space-between",
          alignItems: "center"
        }}
      >

        <button onClick={previousVideo}>
          ⬅ Previous
        </button>

        <span>

          {currentIndex + 1}

          {" / "}

          {feed.length}

        </span>

        <button onClick={nextVideo}>
          Next ➡
        </button>

      </div>

    </div>

  );

}

export default FeedController;