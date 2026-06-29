function VideoInfo({ video }) {
  return (
    <div
      style={{
        padding: "20px",
        color: "white",
      }}
    >
      <h2>{video.title}</h2>

      <p>{video.creator}</p>

      <p>{video.category}</p>

      <p>{video.description}</p>
    </div>
  );
}

export default VideoInfo;