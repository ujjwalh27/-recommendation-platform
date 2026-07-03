import WatchSessionManager from "../session/WatchSessionManager";

function ActionButtons() {

  return (

    <div
      style={{
        display: "flex",
        justifyContent: "space-evenly",
        alignItems: "center",
        padding: "20px",
        borderTop: "1px solid #444",
        fontSize: "28px"
      }}
    >

      <button
        style={buttonStyle}
        onClick={() => {

          console.log("❤️ Like");

          WatchSessionManager.like();

        }}
      >
        ❤️
      </button>

      <button
        style={buttonStyle}
        onClick={() => {

          console.log("💬 Comment");

          WatchSessionManager.comment();

        }}
      >
        💬
      </button>

      <button
        style={buttonStyle}
        onClick={() => {

          console.log("💾 Save");

          WatchSessionManager.save();

        }}
      >
        💾
      </button>

      <button
        style={buttonStyle}
        onClick={() => {

          console.log("📤 Share");

          WatchSessionManager.share();

        }}
      >
        ↗️
      </button>

    </div>

  );

}

const buttonStyle = {

  background: "transparent",
  border: "none",
  color: "white",
  cursor: "pointer",
  fontSize: "28px"

};

export default ActionButtons;