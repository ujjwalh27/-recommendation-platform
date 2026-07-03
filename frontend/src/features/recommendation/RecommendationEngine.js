import DiversityEngine from "./DiversityEngine";
import CreatorAffinityManager from "./CreatorAffinityManager";
import InterestProfileManager from "./InterestProfileManager";
import ExplorationEngine from "./ExplorationEngine";
import CandidateGenerator from "./CandidateGenerator";
import FeedRefreshManager from "./FeedRefreshManager";
import ContextManager from "./ContextManager";
import SessionManager from "./SessionManager";
import RecentCategoryManager from "./RecentCategoryManager";

class RecommendationEngine {

  calculateFreshness(uploadAge) {
    return Math.max(0, 100 - uploadAge);
  }

  calculatePopularity(popularity) {
    return popularity;
  }

  calculateCreatorScore(creator) {
    return CreatorAffinityManager.getCreatorScore(creator);
  }

  calculateExplorationBonus(category) {
    return ExplorationEngine.getBonus(category);
}

calculateSessionScore() {
    return SessionManager.getSessionScore();
}

calculateRecentCategoryPenalty(category) {

    return RecentCategoryManager.getPenalty(category);

}

calculateContextScore(category) {
  return ContextManager.calculateContextScore(category);
}
  scoreVideo(video) {

    const profile = InterestProfileManager.getProfile();

    const context =
  this.calculateContextScore(video.category);

  const session =
    this.calculateSessionScore();

    const recentPenalty =
    this.calculateRecentCategoryPenalty(
        video.category
    );

    const interest =
      profile[video.category] || 0;

    const freshness =
      this.calculateFreshness(video.uploadAge);

    const popularity =
      this.calculatePopularity(video.popularity);

    const creatorScore =
    this.calculateCreatorScore(video.creator);

    const exploration =
    this.calculateExplorationBonus(
        video.category
    );

    const diversityPenalty =
    DiversityEngine.getPenalty(video.category);  

   const score =

  interest * 0.35 +

  freshness * 0.10 +

  popularity * 0.10 +

  creatorScore * 0.15 +

  exploration * 0.05 +

  context * 0.15 +

  session * 0.10 -

  recentPenalty;
    return {

    ...video,

    interest,

    freshness,

    popularity,

    creatorScore,

    exploration,

    context,

    session,

    recentPenalty,

    diversityPenalty,

    recommendationScore:
        Number(score.toFixed(2))

};
  }

  rankVideos(videos) {

   DiversityEngine.reset();
ExplorationEngine.reset();
RecentCategoryManager.reset();

    const profile =
        InterestProfileManager.getProfile();

    const candidates =
        CandidateGenerator.generate(
            videos,
            profile
        );

    const ranked = candidates
        .map(video => this.scoreVideo(video))
        .sort(
            (a, b) =>
                b.recommendationScore -
                a.recommendationScore
        );

    ranked.forEach(video => {

    DiversityEngine.registerRecommendation(
        video.category
    );

    ExplorationEngine.registerRecommendation(
        video.category
    );

    RecentCategoryManager.registerCategory(
        video.category
    );

});

    FeedRefreshManager.initialize(ranked);

return FeedRefreshManager.getFeed();

}
refreshFeed(watchedVideoId, videos) {

    FeedRefreshManager.consumeVideo(
        watchedVideoId
    );

    const refreshed =
        this.rankVideos(videos);

    FeedRefreshManager.appendRecommendations(
        refreshed
    );

    return FeedRefreshManager.getFeed();

}

  }


export default new RecommendationEngine();