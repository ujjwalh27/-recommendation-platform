function ActionButtons() {
  return (
    <div
      style={{
        display: "flex",
        justifyContent: "space-evenly",
        alignItems: "center",
        padding: "20px",
        borderTop: "1px solid #444",
        fontSize: "28px",
      }}
    >
      <button style={buttonStyle}>❤️</button>
      <button style={buttonStyle}>💬</button>
      <button style={buttonStyle}>💾</button>
      <button style={buttonStyle}>↗️</button>
    </div>
  );
}

const buttonStyle = {
  background: "transparent",
  border: "none",
  color: "white",
  cursor: "pointer",
  fontSize: "28px",
};

export default ActionButtons;