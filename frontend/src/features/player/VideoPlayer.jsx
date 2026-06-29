import BehaviourTracker from "../analytics/BehaviourTracker";
import WatchSessionManager from "../session/WatchSessionManager";

const USER_ID = 1;

const VIDEO = {
  id: 1,
  title: "Morning Yoga",
  creator: "DAIV Health",
  category: "Health",
};

function VideoPlayer() {
  /**
   * Sends an event to the BehaviourTracker
   * and WatchSessionManager
   */
  const track = (eventName, currentTime = 0, extra = {}) => {
    const event = {
      event: eventName,
      currentTime: Number(currentTime.toFixed(2)),
      time: new Date().toLocaleTimeString(),
      ...extra,
    };

    BehaviourTracker.record(event);
    WatchSessionManager.processEvent(event);
  };

  return (
    <video
      src="/videos/sample.mp4"
      controls
      width="100%"
      height="100%"
      style={{
        background: "black",
        objectFit: "cover",
      }}

      /* -------------------------------
         Video Loaded
      -------------------------------- */
      onLoadedMetadata={(e) => {
        track("LOADED", 0, {
          duration: Number(e.target.duration.toFixed(2)),
        });
      }}

      /* -------------------------------
         Play
      -------------------------------- */
      onPlay={(e) => {
        if (!WatchSessionManager.getSession()) {
          WatchSessionManager.start(USER_ID, VIDEO);
        }

        track("PLAY", e.target.currentTime);
      }}

      /* -------------------------------
         Pause
      -------------------------------- */
      onPause={(e) => {
        track("PAUSE", e.target.currentTime);
      }}

      /* -------------------------------
         User Starts Seeking
      -------------------------------- */
      onSeeking={(e) => {
        track("SEEKING", e.target.currentTime);
      }}

      /* -------------------------------
         User Finished Seeking
      -------------------------------- */
      onSeeked={(e) => {
        track("SEEKED", e.target.currentTime);
      }}

      /* -------------------------------
         Video Progress
      -------------------------------- */
      onTimeUpdate={(e) => {
        if (!e.target.duration) return;

        const percentage =
          (e.target.currentTime / e.target.duration) * 100;

        track(
          "WATCH_PROGRESS",
          e.target.currentTime,
          {
            percentage: Number(percentage.toFixed(1)),
          }
        );
      }}

      /* -------------------------------
         Video Finished
      -------------------------------- */
      onEnded={(e) => {
        track("ENDED", e.target.currentTime);
      }}
    />
  );
}

export default VideoPlayer;