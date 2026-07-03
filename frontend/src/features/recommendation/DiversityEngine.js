class DiversityEngine {

    constructor() {
        this.categoryCount = {};
    }

    reset() {
        this.categoryCount = {};
    }

    getPenalty(category) {
        const count = this.categoryCount[category] || 0;
        return count * 10;
    }

    registerRecommendation(category) {
        if (!this.categoryCount[category]) {
            this.categoryCount[category] = 0;
        }

        this.categoryCount[category]++;
    }

    getStats() {
        return this.categoryCount;
    }

}

export default new DiversityEngine();