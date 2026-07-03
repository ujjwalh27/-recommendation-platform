class FeedRefreshManager {

    constructor() {
        this.feed = [];
    }

    initialize(videos) {
        this.feed = [...videos];
    }

    getFeed() {
        return this.feed;
    }

    consumeVideo(videoId) {

        this.feed = this.feed.filter(
            video => video.id !== videoId
        );

    }

    appendRecommendations(videos) {

        videos.forEach(video => {

            const exists = this.feed.some(
                item => item.id === video.id
            );

            if (!exists) {
                this.feed.push(video);
            }

        });

    }

}

export default new FeedRefreshManager();