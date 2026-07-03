class CreatorAffinityManager {

    constructor() {

        this.creatorAffinity = {};

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
            this.listeners.filter(
                l => l !== listener
            );

    }

    notify() {

        this.listeners.forEach(listener =>
            listener(this.creatorAffinity)
        );

    }

    // --------------------------
    // Creator Affinity
    // --------------------------

    updateCreatorAffinity(session, engagementScore) {

        const creator = session.creator;

        if (!creator) {
            return;
        }

        if (!this.creatorAffinity[creator]) {

            this.creatorAffinity[creator] = 0;

        }

        // --------------------------
        // Update based on Engagement
        // --------------------------

        if (engagementScore >= 80) {

            this.creatorAffinity[creator] += 20;

        }
        else if (engagementScore >= 60) {

            this.creatorAffinity[creator] += 15;

        }
        else if (engagementScore >= 30) {

            this.creatorAffinity[creator] += 10;

        }
        else if (engagementScore > 0) {

            this.creatorAffinity[creator] += 5;

        }
        else {

            this.creatorAffinity[creator] -= 5;

        }

        // Prevent negative affinity

        if (this.creatorAffinity[creator] < 0) {

            this.creatorAffinity[creator] = 0;

        }

        console.log("👤 Creator Affinity Updated");
        console.table(this.creatorAffinity);

        this.notify();

    }

    // --------------------------
    // Getters
    // --------------------------

    getCreatorScore(creator) {

        return this.creatorAffinity[creator] || 0;

    }

    getAffinity(creator) {

        return this.getCreatorScore(creator);

    }

    getAllCreatorAffinities() {

        return this.creatorAffinity;

    }

    // --------------------------
    // Reset
    // --------------------------

    reset() {

        this.creatorAffinity = {};

        this.notify();

    }

}

export default new CreatorAffinityManager();