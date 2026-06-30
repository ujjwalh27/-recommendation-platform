import VideoPlayer from "../player/VideoPlayer";
import VideoInfo from "../player/VideoInfo";
import ActionButtons from "../player/ActionButtons";

function VideoCard({ video }) {
  return (
    <div
      style={{
        width: "400px",
        height: "700px",
        background: "#222",
        color: "white",
        display: "flex",
        flexDirection: "column",
      }}
    >
      <div
        style={{
          flex: 1,
          display: "flex",
          justifyContent: "center",
          alignItems: "center",
        }}
      >
        {/* Pass video to VideoPlayer */}
        <VideoPlayer video={video} />
      </div>

      <VideoInfo video={video} />

      <ActionButtons />
    </div>
  );
}

export default VideoCard;