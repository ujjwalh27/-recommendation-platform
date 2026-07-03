import InterestProfileManager from "./InterestProfileManager";
import CreatorAffinityManager from "./CreatorAffinityManager";
import EngagementScorer from "./EngagementScorer";
import EventBus from "../event/EventBus";

class FeedbackManager {

    process(session) {

        console.log("📩 Processing User Session");

        // --------------------------
        // Calculate Engagement Score
        // --------------------------

        const engagementScore =
            EngagementScorer.calculate(session);

        console.log(
            "⭐ Engagement Score:",
            engagementScore
        );

        // --------------------------
        // Update Interest Profile
        // --------------------------

        if (engagementScore >= 80) {

            InterestProfileManager.updateInterest(
                session.category,
                15
            );

        }
        else if (engagementScore >= 60) {

            InterestProfileManager.updateInterest(
                session.category,
                10
            );

        }
        else if (engagementScore >= 30) {

            InterestProfileManager.updateInterest(
                session.category,
                5
            );

        }
        else if (engagementScore > 0) {

            InterestProfileManager.updateInterest(
                session.category,
                2
            );

        }
        else {

            InterestProfileManager.decreaseInterest(
                session.category,
                5
            );

        }

        // --------------------------
        // Update Creator Affinity
        // --------------------------

        CreatorAffinityManager.updateCreatorAffinity(
            session,
            engagementScore
        );

        // --------------------------
        // Debug Logs
        // --------------------------

        console.log("📈 Interest Profile");
        console.table(
            InterestProfileManager.getProfile()
        );

        console.log("👤 Creator Affinity");
        console.table(
            CreatorAffinityManager.getAllCreatorAffinities()
        );

        // --------------------------
        // Notify Recommendation Engine
        // --------------------------

        EventBus.publish(
            "PROFILE_UPDATED",
            {

                engagementScore,

                session,

                interests:
                    InterestProfileManager.getProfile(),

                creators:
                    CreatorAffinityManager.getAllCreatorAffinities()

            }
        );

    }

}

export default new FeedbackManager();