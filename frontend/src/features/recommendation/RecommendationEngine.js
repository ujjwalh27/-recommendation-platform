import InterestProfileManager from "./InterestProfileManager";

class RecommendationEngine {

  calculateFreshness(uploadAge) {
    return Math.max(0, 100 - uploadAge);
  }

  calculatePopularity(popularity) {
    return popularity;
  }

  calculateCreatorScore() {
    // Placeholder
    return 50;
  }

  calculateExplorationBonus() {
    // Placeholder
    return 20;
  }

  scoreVideo(video) {

    const profile =
      InterestProfileManager.getProfile();

    const interest =
      profile[video.category] || 0;

    const freshness =
      this.calculateFreshness(video.uploadAge);

    const popularity =
      this.calculatePopularity(video.popularity);

    const creator =
      this.calculateCreatorScore(video.creator);

    const exploration =
      this.calculateExplorationBonus();

    const score =

      interest * 0.40 +

      freshness * 0.10 +

      popularity * 0.10 +

      creator * 0.15 +

      exploration * 0.05;

    return {

      ...video,

      interest,

      freshness,

      popularity,

      creator,

      exploration,

      recommendationScore: Number(score.toFixed(2))

    };

  }

  rankVideos(videos) {

    return videos

      .map(video => this.scoreVideo(video))

      .sort(

        (a,b)=>

          b.recommendationScore -

          a.recommendationScore

      );

  }

}

export default new RecommendationEngine();