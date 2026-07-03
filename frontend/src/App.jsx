import { useEffect, useState } from "react";
import { getFeed } from "./services/api";

function App() {

    const [videos, setVideos] = useState([]);

    useEffect(() => {

        async function load() {

            const data = await getFeed();

            console.log(data[0]);

            setVideos(data);

        }

        load();

    }, []);

    return (

        <div style={{padding:20}}>

            <h1 style={{color:"white"}}>
                Recommendation Engine
            </h1>

            {videos.map(video => (

                <div
                    key={video.video_id}
                    style={{
                        marginBottom:30,
                        color:"white",
                        border:"1px solid gray",
                        padding:10
                    }}
                >

                    <img
                        src={video.thumbnail_url}
                        width="200"
                    />

                    <h3>{video.title}</h3>

                    <video
                        controls
                        width="300"
                        src={video.video_url}
                    />

                </div>

            ))}

        </div>

    );

}

export default App;