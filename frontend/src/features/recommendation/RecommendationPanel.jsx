import ContextManager from "./ContextManager";

function RecommendationPanel({ rankedVideos }) {

  if (!rankedVideos || rankedVideos.length === 0) {

    return (

      <div
        style={{
          width: 320,
          height: "90vh",
          background: "#121212",
          color: "white",
          display: "flex",
          justifyContent: "center",
          alignItems: "center",
          borderRadius: "10px"
        }}
      >
        Loading Recommendations...
      </div>

    );

  }

  const topVideo = rankedVideos[0];

  return (

    <div
      style={{
        width: 320,
        height: "90vh",
        background: "#121212",
        color: "white",
        padding: "20px",
        borderRadius: "10px",
        overflowY: "auto"
      }}
    >

      <h2>🎯 Recommendation</h2>

      <hr />

      <p>
        <strong>Time Context</strong>
        <br />
        {ContextManager.getTimeContext()}
      </p>

      <hr />

      <p>
        <strong>Video</strong>
        <br />
        {topVideo.title}
      </p>

      <p>
        <strong>Category</strong>
        <br />
        {topVideo.category}
      </p>

      <hr />

      <p>
        Interest
        <br />
        {topVideo.interest}
      </p>

      <p>
        Freshness
        <br />
        {topVideo.freshness}
      </p>

      <p>
        Popularity
        <br />
        {topVideo.popularity}
      </p>

      <p>
        Creator Score
        <br />
        {topVideo.creatorScore}
      </p>

      <p>
        Exploration
        <br />
        {topVideo.exploration}
      </p>

      <p>
        Context
        <br />
        {topVideo.context}
      </p>

      <p>
        Session
        <br />
        {topVideo.session}
      </p>

      <p>
        Recent Penalty
        <br />
        {topVideo.recentPenalty}
      </p>

      <p>
        Diversity Penalty
        <br />
        {topVideo.diversityPenalty}
      </p>

      <hr />

      <h2>Final Score</h2>

      <h1>
        {topVideo.recommendationScore}
      </h1>

    </div>

  );

}

export default RecommendationPanel;