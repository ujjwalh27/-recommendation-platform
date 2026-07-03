import FeedbackManager from "../recommendation/FeedbackManager";

class WatchSessionManager {

  constructor() {
    this.session = null;
    this.listeners = [];
  }

  // --------------------------
  // Observer Pattern
  // --------------------------

  subscribe(listener) {
    this.listeners.push(listener);
  }

  unsubscribe(listener) {
    this.listeners = this.listeners.filter(
      (l) => l !== listener
    );
  }

  notify() {
    this.listeners.forEach((listener) => {
      listener(this.session);
    });
  }

  // --------------------------
  // Session Management
  // --------------------------

  start(userId, video) {

    if (this.session) return;

    this.session = {

      sessionId: crypto.randomUUID(),

      userId,

      videoId: video.id,
      title: video.title,
      creator: video.creator,
      category: video.category,

      duration: 0,

      state: "PLAYING",

      startedAt: new Date(),
      endedAt: null,

      watchTime: 0,
      completion: 0,

      playCount: 1,
      pauseCount: 0,
      seekCount: 0,
      replayCount: 0,

      liked: false,
      saved: false,
      shared: false,
      commented: false,

      events: []

    };

    console.log("🟢 Session Started");
    console.table(this.session);

    this.notify();

  }

  processEvent(event) {

    if (!this.session) return;

    this.session.events.push(event);

    switch (event.event) {

      case "PLAY":
        this.session.state = "PLAYING";
        this.session.playCount++;
        break;

      case "PAUSE":
        this.session.state = "PAUSED";
        this.session.pauseCount++;
        break;

      case "SEEKING":
        this.session.seekCount++;
        break;

      case "WATCH_PROGRESS":
        this.session.watchTime = event.currentTime;
        this.session.completion = event.percentage;
        break;

      case "ENDED":
        this.end();
        return;

      default:
        break;
    }

    this.notify();

  }

  // --------------------------
  // User Actions
  // --------------------------

  like() {

    if (!this.session) return;

    this.session.liked = true;

    console.log("❤️ Liked");

    this.notify();

  }

  unlike() {

    if (!this.session) return;

    this.session.liked = false;

    console.log("💔 Unliked");

    this.notify();

  }

  save() {

    if (!this.session) return;

    this.session.saved = true;

    console.log("💾 Saved");

    this.notify();

  }

  unsave() {

    if (!this.session) return;

    this.session.saved = false;

    console.log("🗑️ Unsaved");

    this.notify();

  }

  share() {

    if (!this.session) return;

    this.session.shared = true;

    console.log("📤 Shared");

    this.notify();

  }

  comment() {

    if (!this.session) return;

    this.session.commented = true;

    console.log("💬 Commented");

    this.notify();

  }

  replay() {

    if (!this.session) return;

    this.session.replayCount++;

    console.log(
      "🔁 Replay Count:",
      this.session.replayCount
    );

    this.notify();

  }

  // --------------------------
  // End Session
  // --------------------------

  end() {

    if (!this.session) return;

    this.session.state = "ENDED";
    this.session.endedAt = new Date();

    console.log("🏁 Session Finished");
    console.table(this.session);

    // Process the entire session
    FeedbackManager.process(this.session);

    this.notify();

    this.session = null;

  }

  // --------------------------
  // Getter
  // --------------------------

  getSession() {
    return this.session;
  }

}

export default new WatchSessionManager();