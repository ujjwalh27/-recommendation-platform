import InterestProfileManager from "../recommendation/InterestProfileManager";
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

      events: [],
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

  end() {
  if (!this.session) return;

  this.session.state = "ENDED";
  this.session.endedAt = new Date();

  console.log("🏁 Session Finished");
  console.log(this.session);

  // --------------------------
  // Update Interest Profile
  // --------------------------

  const completion = this.session.completion;

  if (completion >= 80) {
    InterestProfileManager.updateInterest(
      this.session.category,
      10
    );
  } else if (completion >= 50) {
    InterestProfileManager.updateInterest(
      this.session.category,
      5
    );
  } else if (completion >= 20) {
    InterestProfileManager.updateInterest(
      this.session.category,
      2
    );
  } else {
    InterestProfileManager.decreaseInterest(
      this.session.category,
      2
    );
  }

  console.log("📈 Interest Profile");
  console.table(
    InterestProfileManager.getProfile()
  );

  this.notify();
}
}