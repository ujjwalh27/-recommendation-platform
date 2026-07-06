import EngagementScorer from "./EngagementScorer";

class FeedbackManager {

    process(session) {

        console.log("📩 Processing User Session");

        const engagementScore =
            EngagementScorer.calculate(session);

        console.log(
            "⭐ Engagement Score:",
            engagementScore
        );

        console.log("📊 Session Summary");

        console.table({

            Video: session.title,

            Creator: session.creator,

            Category: session.category,

            WatchTime: session.watchTime,

            Completion:
                `${session.completion.toFixed(1)} %`,

            Liked: session.liked,

            Saved: session.saved,

            Shared: session.shared,

            Commented: session.commented,

            Replay: session.replayCount,

            Score: engagementScore

        });

        // -------------------------
        // Future
        // -------------------------
        //
        // POST /events
        //
        // fetch(...)
        //
        // -------------------------

        return engagementScore;

    }

}

export default new FeedbackManager();