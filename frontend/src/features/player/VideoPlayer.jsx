import BehaviourTracker from "../analytics/BehaviourTracker";
import WatchSessionManager from "../session/WatchSessionManager";

function VideoPlayer({ video }) {

  const track = (eventName, currentTime = 0, percentage = 0) => {

    const event = {
      event: eventName,
      currentTime,
      percentage,
      time: new Date().toLocaleTimeString(),
    };

    BehaviourTracker.record(event);

    WatchSessionManager.processEvent(event);
  };

  return (

    <video
      src={video.video_url}
      controls
      autoPlay
      muted
      playsInline
      width="100%"
      height="100%"
      style={{
        background: "black",
        objectFit: "cover",
      }}

      onLoadedMetadata={(e) => {
        track("LOADED", e.target.duration);
      }}

      onPlay={(e) => {

        if (!WatchSessionManager.getSession()) {
          WatchSessionManager.start(1, video);
        }

        track("PLAY", e.target.currentTime);

      }}

      onPause={(e) => {
        track("PAUSE", e.target.currentTime);
      }}

      onSeeking={(e) => {
        track("SEEKING", e.target.currentTime);
      }}

      onSeeked={(e) => {
        track("SEEKED", e.target.currentTime);
      }}

      onEnded={(e) => {
        track("ENDED", e.target.currentTime);
      }}

      onTimeUpdate={(e) => {

        const percentage =
          (e.target.currentTime / e.target.duration) * 100;

        track(
          "WATCH_PROGRESS",
          e.target.currentTime,
          percentage
        );

      }}

    />

  );

}

export default VideoPlayer;