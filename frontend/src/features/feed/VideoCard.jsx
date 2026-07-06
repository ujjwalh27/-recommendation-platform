import React, { useState, useRef } from "react";
import {
  Heart,
  MessageCircle,
  Send,
  Bookmark,
  Volume2,
  VolumeX,
  Music,
} from "lucide-react";

import VideoPlayer from "../player/VideoPlayer";
import WatchSessionManager from "../session/WatchSessionManager";
import CommentsDrawer from "./CommentsDrawer";

function VideoCard({

  video,

  isActive,

  isGlobalMuted,

  onMuteToggle,

}) {

  const [liked, setLiked] = useState(false);

  const [saved, setSaved] = useState(false);

  const [likesCount, setLikesCount] =
    useState(video.likes || 0);

  const [savesCount, setSavesCount] =
    useState(video.saves || 0);

  const [progress, setProgress] =
    useState(0);

  const [isLoading, setIsLoading] =
    useState(true);

  const [showHeartPop, setShowHeartPop] =
    useState(false);

  const [isCommentsOpen, setIsCommentsOpen] =
    useState(false);

  const clickTimeout = useRef(null);

  const videoRef = useRef(null);

  const handleLikeToggle = () => {

    const next = !liked;

    setLiked(next);

    setLikesCount(previous =>
      previous + (next ? 1 : -1)
    );

    next
      ? WatchSessionManager.like()
      : WatchSessionManager.unlike();

  };

  const handleSaveToggle = () => {

    const next = !saved;

    setSaved(next);

    setSavesCount(previous =>
      previous + (next ? 1 : -1)
    );

    next
      ? WatchSessionManager.save()
      : WatchSessionManager.unsave();

  };

  const handleShare = () => {

    navigator.clipboard.writeText(
      window.location.href
    );

    WatchSessionManager.share();

  };

  const handleVideoClick = () => {

    if (clickTimeout.current) {

      clearTimeout(clickTimeout.current);

      clickTimeout.current = null;

      if (!liked) {

        handleLikeToggle();

      }

      setShowHeartPop(true);

      setTimeout(() => {

        setShowHeartPop(false);

      }, 700);

      return;

    }

    clickTimeout.current = setTimeout(() => {

      clickTimeout.current = null;

      if (!videoRef.current) return;

      if (videoRef.current.paused) {

        videoRef.current.play();

      } else {

        videoRef.current.pause();

      }

    }, 250);

  };

  const format = count => {

    if (count >= 1000000)
      return (count / 1000000).toFixed(1) + "M";

    if (count >= 1000)
      return (count / 1000).toFixed(1) + "K";

    return count;

  };

  return (

    <div className="video-card-container">

      <div
        className="video-player-wrapper"
        onClick={handleVideoClick}
      >

        <VideoPlayer

          videoRef={videoRef}

          video={video}

          isActive={isActive}

          isMuted={isGlobalMuted}

          onWaiting={() =>
            setIsLoading(true)
          }

          onPlaying={() =>
            setIsLoading(false)
          }

          onProgress={setProgress}

        />

        {isLoading && (

          <div className="player-spinner">

            <div className="spinner"></div>

          </div>

        )}

        {showHeartPop && (

          <div className="heart-pop">

            <Heart
              size={80}
              fill="red"
              stroke="none"
            />

          </div>

        )}

        <button

          className="icon-btn"

          style={{
            position: "absolute",
            top: 20,
            right: 20,
            zIndex: 20,
          }}

          onClick={e => {

            e.stopPropagation();

            onMuteToggle();

          }}

        >

          {isGlobalMuted
            ? <VolumeX size={18} />
            : <Volume2 size={18} />}

        </button>

        <div
          className="video-overlay-right"
          onClick={e => e.stopPropagation()}
        >

          <div
            className="overlay-action"
            onClick={handleLikeToggle}
          >

            <Heart
              size={22}
              fill={liked ? "currentColor" : "none"}
            />

            <span>

              {format(likesCount)}

            </span>

          </div>

          <div
            className="overlay-action"
            onClick={() =>
              setIsCommentsOpen(true)
            }
          >

            <MessageCircle size={22} />

            <span>

              {format(video.comments)}

            </span>

          </div>

          <div
            className="overlay-action"
            onClick={handleShare}
          >

            <Send size={22} />

            <span>

              {format(video.shares)}

            </span>

          </div>

          <div
            className="overlay-action"
            onClick={handleSaveToggle}
          >

            <Bookmark
              size={22}
              fill={saved ? "currentColor" : "none"}
            />

            <span>

              {format(savesCount)}

            </span>

          </div>

        </div>

        <div className="video-overlay-bottom">

          <div className="creator-header">

            <div className="creator-avatar">

              {(video.display_name || video.creator || "U")
                .charAt(0)
                .toUpperCase()}

            </div>

            <span>

              {video.display_name || video.creator}

            </span>

          </div>

          <p className="video-caption">

            {video.title}

          </p>

          <div className="music-ticker-container">

            <Music size={11} />

            <span>

              {video.music || "Original Audio"}

            </span>

          </div>

        </div>

      </div>

      <CommentsDrawer

        videoId={video.video_id}

        creator={
          video.display_name || video.creator
        }

        isOpen={isCommentsOpen}

        onClose={() =>
          setIsCommentsOpen(false)
        }

      />

    </div>

  );

}

export default VideoCard;