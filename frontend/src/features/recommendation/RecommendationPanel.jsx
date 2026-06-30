import RecommendationEngine from "./RecommendationEngine";
import videos from "../../data/videos";

function RecommendationPanel() {

  const rankedVideos =
    RecommendationEngine.rankVideos(videos);

  const topVideo =
    rankedVideos[0];

  return (

    <div
      style={{
        width:320,
        height:"90vh",
        background:"#121212",
        color:"white",
        padding:"20px",
        borderRadius:"10px",
        overflowY:"auto"
      }}
    >

      <h2>🎯 Recommendation</h2>

      <hr/>

      <p>

        <strong>Video</strong>

        <br/>

        {topVideo.title}

      </p>

      <p>

        <strong>Category</strong>

        <br/>

        {topVideo.category}

      </p>

      <hr/>

      <p>

        Interest

        <br/>

        {topVideo.interest}

      </p>

      <p>

        Freshness

        <br/>

        {topVideo.freshness}

      </p>

      <p>

        Popularity

        <br/>

        {topVideo.popularity}

      </p>

      <p>

        Creator

        <br/>

        {topVideo.creator}

      </p>

      <p>

        Exploration

        <br/>

        {topVideo.exploration}

      </p>

      <hr/>

      <h2>

        Final Score

      </h2>

      <h1>

        {topVideo.recommendationScore}

      </h1>

    </div>

  );

}

export default RecommendationPanel;