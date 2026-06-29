import { useEffect, useState } from "react";
import BehaviourTracker from "./BehaviourTracker";

function AnalyticsPanel() {

  const [events,setEvents] = useState([]);

  useEffect(() => {

    const listener = (updatedEvents) => {

      setEvents(updatedEvents);

    };

    BehaviourTracker.subscribe(listener);

    return () => BehaviourTracker.unsubscribe(listener);

  }, []);

  return (

    <div
      style={{
        width:320,
        height:"90vh",
        background:"#181818",
        color:"white",
        padding:"20px",
        overflowY:"auto"
      }}
    >

      <h2>📊 Live Analytics</h2>

      {events.length===0 &&

        <p>No Events Yet</p>

      }

      {

        events.map((event,index)=>(

          <div
            key={index}
            style={{
              marginBottom:"15px",
              padding:"10px",
              border:"1px solid #444",
              borderRadius:"8px"
            }}
          >

            <strong>{event.event}</strong>

            <br/>

            {event.time}

          </div>

        ))

      }

    </div>

  );

}

export default AnalyticsPanel;