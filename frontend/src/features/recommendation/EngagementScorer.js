class EngagementScorer {

    calculate(session) {

        let score = 0;

        // --------------------------
        // Watch Completion
        // --------------------------

        if (session.completion >= 80) {

            score += 40;

        } else if (session.completion >= 50) {

            score += 20;

        } else if (session.completion >= 20) {

            score += 5;

        } else {

            score -= 10;

        }

        // --------------------------
        // Like
        // --------------------------

        if (session.liked) {

            score += 25;

        }

        // --------------------------
        // Save
        // --------------------------

        if (session.saved) {

            score += 20;

        }

        // --------------------------
        // Share
        // --------------------------

        if (session.shared) {

            score += 20;

        }

        // --------------------------
        // Comment
        // --------------------------

        if (session.commented) {

            score += 15;

        }

        // --------------------------
        // Replay
        // Give diminishing returns
        // --------------------------

        if (session.replayCount > 0) {

            score += Math.min(
                session.replayCount * 5,
                15
            );

        }

        // --------------------------
        // Too many pauses
        // --------------------------

        if (session.pauseCount >= 5) {

            score -= 10;

        }

        // --------------------------
        // Skip
        // --------------------------

        if (session.completion < 10) {

            score -= 30;

        }

        // --------------------------
        // Clamp Score
        // --------------------------

        score = Math.max(
            -50,
            Math.min(score, 100)
        );

        return score;

    }

}

export default new EngagementScorer();