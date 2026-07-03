import InterestProfileManager from "./InterestProfileManager";
import CreatorAffinityManager from "./CreatorAffinityManager";
import ContextManager from "./ContextManager";
import SessionManager from "./SessionManager";
import RecentCategoryManager from "./RecentCategoryManager";

function DebugDashboard({ rankedVideos }) {

    const profile =
        InterestProfileManager.getProfile();

    return (

        <div
            style={{
                width: 420,
                height: "90vh",
                overflowY: "auto",
                background: "#181818",
                color: "white",
                padding: 20,
                borderRadius: 10
            }}
        >

            <h2>Recommendation Debug Dashboard</h2>

            <hr />

            <h3>Current Context</h3>

            <p>
                Time :
                {" "}
                {ContextManager.getTimeContext()}
            </p>

            <p>
                Session Videos :
                {" "}
                {SessionManager.getSessionCount()}
            </p>

            <hr />

            <h3>Interest Profile</h3>

            <pre>
                {JSON.stringify(profile, null, 2)}
            </pre>

            <hr />

            <h3>Ranked Videos</h3>

            {
                rankedVideos.map(video => (

                    <div
                        key={video.id}
                        style={{
                            marginBottom:20,
                            borderBottom:"1px solid gray",
                            paddingBottom:10
                        }}
                    >

                        <b>{video.title}</b>

                        <br/>

                        Category :
                        {" "}
                        {video.category}

                        <br/>

                        Score :
                        {" "}
                        {video.recommendationScore}

                    </div>

                ))
            }

        </div>

    );

}

export default DebugDashboard;