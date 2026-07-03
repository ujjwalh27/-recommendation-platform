class RecentCategoryManager {

    constructor() {

        this.recentCategories = [];

        this.maxHistory = 5;

    }

    registerCategory(category) {

        this.recentCategories.push(category);

        if (this.recentCategories.length > this.maxHistory) {

            this.recentCategories.shift();

        }

    }

    getPenalty(category) {

        const count =
            this.recentCategories.filter(
                c => c === category
            ).length;

        return count * 10;

    }

    reset() {

        this.recentCategories = [];

    }

}

export default new RecentCategoryManager();