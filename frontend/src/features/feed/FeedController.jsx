import { useEffect, useState, useRef } from "react";
import { Search, User, X } from "lucide-react";

import VideoCard from "./VideoCard";

import {
  getFeed,
  getRecommendations
} from "../../services/api";

function FeedController({ onFeedUpdated }) {

  const [feed, setFeed] = useState([]);
  const [currentIndex, setCurrentIndex] = useState(0);

  const [isGlobalMuted, setIsGlobalMuted] = useState(true);

  const [isLoadingMore, setIsLoadingMore] = useState(false);

  const [activeModal, setActiveModal] = useState(null);

  const [searchQuery, setSearchQuery] = useState("");

  const onFeedUpdatedRef = useRef(onFeedUpdated);

  useEffect(() => {

    onFeedUpdatedRef.current = onFeedUpdated;

  }, [onFeedUpdated]);

  // ----------------------------
  // Initial Feed Load
  // ----------------------------

  useEffect(() => {

    loadFeed();

  }, []);

  const loadFeed = async () => {

    try {

      console.log("Loading Feed...");

      const data = await getFeed();

      console.log(data);

      setFeed(data);

      if (onFeedUpdatedRef.current) {

        onFeedUpdatedRef.current(data);

      }

    } catch (err) {

      console.error(err);

    }

  };

  // ----------------------------
  // Infinite Recommendations
  // ----------------------------

  useEffect(() => {

    if (feed.length === 0) return;

    if (currentIndex >= feed.length - 2) {

      loadMoreRecommendations();

    }

  }, [currentIndex]);

  const loadMoreRecommendations = async () => {

    if (isLoadingMore) return;

    setIsLoadingMore(true);

    try {

      const currentVideo = feed[currentIndex];

      if (!currentVideo) {

        setIsLoadingMore(false);

        return;

      }

      const recommendations =
        await getRecommendations(
          currentVideo.video_id
        );

      if (
        recommendations &&
        !recommendations.error &&
        recommendations.length > 0
      ) {

        setFeed(previous => [

          ...previous,

          ...recommendations

        ]);

      }

    } catch (err) {

      console.error(err);

    }

    setIsLoadingMore(false);

  };

  // ----------------------------
  // Scroll
  // ----------------------------

  const handleScroll = (e) => {

    const {

      scrollTop,

      clientHeight

    } = e.currentTarget;

    if (clientHeight === 0) return;

    const index = Math.round(

      scrollTop /

      clientHeight

    );

    if (

      index >= 0 &&

      index < feed.length

    ) {

      setCurrentIndex(index);

    }

  };

  // ----------------------------
  // Search
  // ----------------------------

  const filteredFeed =

    searchQuery.trim() === ""

      ? feed

      : feed.filter(video => {

          const query =

            searchQuery.toLowerCase();

          return (

            (video.title || "")
              .toLowerCase()
              .includes(query)

            ||

            (video.creator || "")
              .toLowerCase()
              .includes(query)

            ||

            (video.description || "")
              .toLowerCase()
              .includes(query)

            ||

            (video.music || "")
              .toLowerCase()
              .includes(query)

          );

        });

  // ----------------------------
  // Mute
  // ----------------------------

  const handleMuteToggle = () => {

    setIsGlobalMuted(

      previous => !previous

    );

  };

  if (feed.length === 0) {

    return (

      <div className="loading-container">

        <div className="spinner"></div>

        <p>

          Loading Feed...

        </p>

      </div>

    );

  }

    return (

    <div className="app-container">

      {/* Header */}

      <div className="app-header">

        <div className="logo-text">

          AI Reels

        </div>

        <div className="header-actions">

          <button
            className="icon-btn"
            onClick={() =>
              setActiveModal(
                activeModal === "search"
                  ? null
                  : "search"
              )
            }
          >

            <Search size={18} />

          </button>

          <button
            className="icon-btn"
            onClick={() =>
              setActiveModal(
                activeModal === "profile"
                  ? null
                  : "profile"
              )
            }
          >

            <User size={18} />

          </button>

        </div>

      </div>

      {/* Feed */}

      <div
        className="feed-container no-scrollbar"
        onScroll={handleScroll}
      >

        {

          filteredFeed.map((video, index) => (

            <VideoCard

              key={video.video_id}

              video={video}

              isActive={
                index === currentIndex
              }

              isGlobalMuted={
                isGlobalMuted
              }

              onMuteToggle={
                handleMuteToggle
              }

            />

          ))

        }

        {

          isLoadingMore && (

            <div
              style={{
                height: 80,
                display: "flex",
                alignItems: "center",
                justifyContent: "center"
              }}
            >

              <div className="spinner" />

            </div>

          )

        }

      </div>

      {/* Search */}

      {

        activeModal === "search" && (

          <div
            style={modalOverlayStyle}
            onClick={() =>
              setActiveModal(null)
            }
          >

            <div
              style={modalContentStyle}
              onClick={(e) =>
                e.stopPropagation()
              }
            >

              <div
                style={{
                  display: "flex",
                  justifyContent:
                    "space-between",
                  width: "100%",
                  marginBottom: 15
                }}
              >

                <h3>

                  Search

                </h3>

                <button
                  className="icon-btn"
                  onClick={() =>
                    setActiveModal(null)
                  }
                >

                  <X size={16} />

                </button>

              </div>

              <input

                value={searchQuery}

                onChange={(e) =>
                  setSearchQuery(
                    e.target.value
                  )
                }

                placeholder="Search..."

                style={inputStyle}

              />

            </div>

          </div>

        )

      }

      {/* Profile */}

      {

        activeModal === "profile" && (

          <div
            style={modalOverlayStyle}
            onClick={() =>
              setActiveModal(null)
            }
          >

            <div
              style={modalContentStyle}
              onClick={(e) =>
                e.stopPropagation()
              }
            >

              <div
                style={{
                  display: "flex",
                  justifyContent:
                    "space-between",
                  width: "100%",
                  marginBottom: 15
                }}
              >

                <h3>

                  My Profile

                </h3>

                <button
                  className="icon-btn"
                  onClick={() =>
                    setActiveModal(null)
                  }
                >

                  <X size={16} />

                </button>

              </div>

              <div style={avatarStyle}>

                V

              </div>

              <h4>

                @you_viewer

              </h4>

              <p>

                Videos Loaded :

                {" "}

                {feed.length}

              </p>

              <p>

                Current Video :

                {" "}

                {currentIndex + 1}

              </p>

            </div>

          </div>

        )

      }

    </div>

  );

}

const modalOverlayStyle = {

  position: "absolute",

  inset: 0,

  background: "rgba(0,0,0,.8)",

  display: "flex",

  alignItems: "center",

  justifyContent: "center",

  zIndex: 20

};

const modalContentStyle = {

  background: "#121214",

  padding: 20,

  borderRadius: 12,

  width: 340,

  display: "flex",

  flexDirection: "column",

  alignItems: "center"

};

const inputStyle = {

  width: "100%",

  padding: 10,

  borderRadius: 8,

  background: "#222",

  color: "#fff",

  border: "1px solid #333"

};

const avatarStyle = {

  width: 60,

  height: 60,

  borderRadius: "50%",

  display: "flex",

  alignItems: "center",

  justifyContent: "center",

  background: "#ff3366",

  color: "#fff",

  fontWeight: "bold",

  fontSize: 22,

  marginBottom: 15

};

export default FeedController;