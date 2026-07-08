import { useEffect, useState } from "react";

import { getFeed, getRecommendations } from "../../services/api";

import VideoCard from "./VideoCard";

function FeedController({ onFeedUpdated }) {

  const [feed, setFeed] = useState([]);
  const [currentIndex, setCurrentIndex] = useState(0);
  const [loading, setLoading] = useState(true);

  // --------------------------
  // Initial Feed
  // --------------------------

  useEffect(() => {

    async function loadFeed() {

      try {

        const data = await getFeed();

        setFeed(data);

        if (onFeedUpdated) {
          onFeedUpdated(data);
        }

      } catch (err) {

        console.error(err);

      } finally {

        setLoading(false);

      }

    }

    loadFeed();

  }, []);

  // --------------------------
  // Navigation
  // --------------------------

  const nextVideo = async () => {

    if (feed.length === 0) return;

    // Normal next video
    if (currentIndex < feed.length - 1) {

      setCurrentIndex(currentIndex + 1);

      return;

    }

    // End of feed
    console.log("Loading more recommendations...");

    try {

      const currentVideo = feed[currentIndex];

      const recommendations =
        await getRecommendations(currentVideo.video_id);

      if (recommendations.length > 0) {

        const updatedFeed = [

          ...feed,

          ...recommendations

        ];

        setFeed(updatedFeed);

        if (onFeedUpdated) {
          onFeedUpdated(updatedFeed);
        }

        setCurrentIndex(currentIndex + 1);

      }

    } catch (err) {

      console.error(err);

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

  if (loading) {

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
        Loading Feed...
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

          {currentIndex + 1} / {feed.length}

        </span>

        <button onClick={nextVideo}>
          Next ➡
        </button>

      </div>

    </div>

  );

}

export default FeedController;