class CandidateGenerator {

    generate(videos, profile) {

        if (!profile || Object.keys(profile).length === 0) {
            return videos;
        }

        const candidates = videos.map(video => {

            const interestScore =
                profile[video.category] || 0;

            return {
                ...video,
                candidateScore: interestScore
            };

        });

        candidates.sort(
            (a, b) => b.candidateScore - a.candidateScore
        );

        return candidates;
    }

}

export default new CandidateGenerator();