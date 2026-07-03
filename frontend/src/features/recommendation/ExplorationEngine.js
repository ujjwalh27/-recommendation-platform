class ExplorationEngine {

    constructor() {
        this.exploredCategories = new Set();
    }

    reset() {
        this.exploredCategories.clear();
    }

    getBonus(category) {

        if (!this.exploredCategories.has(category)) {
            return 20;
        }

        return 0;
    }

    registerRecommendation(category) {
        this.exploredCategories.add(category);
    }

    getStats() {
        return [...this.exploredCategories];
    }

}

export default new ExplorationEngine();