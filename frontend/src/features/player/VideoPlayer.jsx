import { useEffect, useRef } from "react";
import BehaviourTracker from "../analytics/BehaviourTracker";
import WatchSessionManager from "../session/WatchSessionManager";

function VideoPlayer({
  video,
  isActive,
  isMuted,
  onProgress,
  onWaiting,
  onPlaying,
  videoRef,
}) {
  const localRef = useRef(null);
  const playerRef = videoRef || localRef;

  const track = (event, currentTime = 0, percentage = 0) => {
    const behaviour = {
      event,
      currentTime,
      percentage,
      time: new Date().toLocaleTimeString(),
    };

    BehaviourTracker.record(behaviour);
    WatchSessionManager.processEvent(behaviour);
  };

  // Handle active video
  useEffect(() => {
    const player = playerRef.current;

    if (!player) return;

    if (isActive) {
      if (!WatchSessionManager.getSession()) {
        WatchSessionManager.start(1, video);
      }

      player
        .play()
        .then(() => {
          track("PLAY", player.currentTime);
        })
        .catch((err) => {
          console.warn("Autoplay blocked:", err);
        });
    } else {
      player.pause();
      player.currentTime = 0;

      const session = WatchSessionManager.getSession();

      if (
        session &&
        session.videoId === video.video_id
      ) {
        WatchSessionManager.end();
      }
    }
  }, [isActive]);

  // Handle mute
  useEffect(() => {
    if (playerRef.current) {
      playerRef.current.muted = isMuted;
    }
  }, [isMuted]);

  return (
    <video
      ref={playerRef}
      src={video.video_url}
      className="video-element"
      playsInline
      loop
      preload="metadata"

      onWaiting={() => {
        if (onWaiting) onWaiting();
      }}

      onPlaying={() => {
        if (onPlaying) onPlaying();
      }}

      onLoadedMetadata={(e) => {
        track(
          "LOADED",
          e.target.duration
        );
      }}

      onPause={(e) => {
        track(
          "PAUSE",
          e.target.currentTime
        );
      }}

      onSeeking={(e) => {
        track(
          "SEEKING",
          e.target.currentTime
        );
      }}

      onSeeked={(e) => {
        track(
          "SEEKED",
          e.target.currentTime
        );
      }}

      onEnded={(e) => {
        track(
          "ENDED",
          e.target.currentTime,
          100
        );
      }}

      onTimeUpdate={(e) => {
        const duration = e.target.duration;

        const percent =
          duration > 0
            ? (e.target.currentTime / duration) * 100
            : 0;

        if (onProgress) {
          onProgress(percent);
        }

        track(
          "WATCH_PROGRESS",
          e.target.currentTime,
          percent
        );
      }}
    />
  );
}

export default VideoPlayer;