class InterestProfileManager {
  constructor() {
    this.profile = {};

    this.listeners = [];
  }

  // --------------------------
  // Observer Pattern
  // --------------------------

  subscribe(listener) {
    this.listeners.push(listener);
  }

  unsubscribe(listener) {
    this.listeners =
      this.listeners.filter(l => l !== listener);
  }

  notify() {
    this.listeners.forEach(listener =>
      listener(this.profile)
    );
  }

  // --------------------------
  // Interest Management
  // --------------------------

  updateInterest(category, score) {

    if (!this.profile[category]) {
      this.profile[category] = 0;
    }

    this.profile[category] += score;

    this.notify();
  }

  decreaseInterest(category, score) {

    if (!this.profile[category]) {
      this.profile[category] = 0;
    }

    this.profile[category] -= score;

    if (this.profile[category] < 0) {
      this.profile[category] = 0;
    }

    this.notify();
  }

  getProfile() {
    return this.profile;
  }

  reset() {
    this.profile = {};
    this.notify();
  }
}

export default new InterestProfileManager();