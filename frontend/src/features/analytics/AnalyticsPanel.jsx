import { useEffect, useState } from "react";
import BehaviourTracker from "./BehaviourTracker";
import WatchSessionManager from "../session/WatchSessionManager";

function AnalyticsPanel() {
  const [events, setEvents] = useState([]);
  const [session, setSession] = useState(null);

  useEffect(() => {
    // Listen for behaviour events
    const eventListener = (updatedEvents) => {
      setEvents([...updatedEvents]);
    };

    // Listen for watch session updates
    const sessionListener = (updatedSession) => {
      setSession(updatedSession);
    };

    BehaviourTracker.subscribe(eventListener);
    WatchSessionManager.subscribe(sessionListener);

    // Load current session if available
    setSession(WatchSessionManager.getSession());

    return () => {
      BehaviourTracker.unsubscribe(eventListener);
      WatchSessionManager.unsubscribe(sessionListener);
    };
  }, []);

  return (
    <div
      style={{
        width: 340,
        height: "90vh",
        background: "#181818",
        color: "white",
        padding: "20px",
        overflowY: "auto",
        borderRadius: "10px",
      }}
    >
      <h2>📊 Live Session</h2>

      {!session ? (
        <p>No Active Session</p>
      ) : (
        <>
          <hr />

          <p><strong>🎬 Video</strong><br />{session.title}</p>

          <p><strong>👤 Creator</strong><br />{session.creator}</p>

          <p><strong>📂 Category</strong><br />{session.category}</p>

          <p><strong>📍 Status</strong><br />{session.state}</p>

          <p><strong>⏱ Watch Time</strong><br />
            {Number(session.watchTime).toFixed(2)} sec
          </p>

          <p><strong>📈 Completion</strong><br />
            {Number(session.completion).toFixed(2)}%
          </p>

          <p><strong>▶ Play Count</strong><br />{session.playCount}</p>

          <p><strong>⏸ Pause Count</strong><br />{session.pauseCount}</p>

          <p><strong>⏩ Seek Count</strong><br />{session.seekCount}</p>

          <p><strong>🔁 Replay Count</strong><br />{session.replayCount}</p>

          <p><strong>❤️ Liked</strong><br />
            {session.liked ? "Yes" : "No"}
          </p>

          <p><strong>💾 Saved</strong><br />
            {session.saved ? "Yes" : "No"}
          </p>

          <p><strong>📤 Shared</strong><br />
            {session.shared ? "Yes" : "No"}
          </p>

          <p><strong>📋 Total Events</strong><br />
            {session.events.length}
          </p>
        </>
      )}

      <hr style={{ margin: "25px 0" }} />

      <h3>📝 Latest Events</h3>

      {events.length === 0 ? (
        <p>No Events Yet</p>
      ) : (
        [...events].reverse().map((event, index) => (
          <div
            key={index}
            style={{
              marginBottom: "12px",
              padding: "10px",
              border: "1px solid #444",
              borderRadius: "8px",
              background: "#252525",
            }}
          >
            <strong>{event.event}</strong>

            <br />

            {event.time}

            {event.currentTime !== undefined && (
              <>
                <br />
                {Number(event.currentTime).toFixed(2)} sec
              </>
            )}
          </div>
        ))
      )}
    </div>
  );
}

export default AnalyticsPanel;