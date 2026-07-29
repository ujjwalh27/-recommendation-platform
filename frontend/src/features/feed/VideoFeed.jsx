import { useEffect, useState, useRef } from "react";
import { getFeed, getUserProfile } from "../../services/api";
import VideoCard from "./VideoCard";

const ACTIVE_USER_ID = "user_1";

const PERSONA_DESCRIPTIONS = {
    "Automobile Enthusiast": "Fascinated by cars, motorbikes, engines, and racing.",
    "Tech Enthusiast": "Interested in gadgets, computers, programming, and specs.",
    "Food Lover": "Loves recipes, cooking, restaurants, and eating.",
    "Animal Lover": "Enjoys pets, cute animal clips, and wildlife.",
    "Traveler": "Passionate about vacations, nature, and exploring.",
    "Gamer": "Watches gameplay, game highlights, and gaming hacks."
};

function VideoFeed() {
    const [videos, setVideos] = useState([]);
    const [profile, setProfile] = useState(null);
    const [loading, setLoading] = useState(false);
    const [activeIndex, setActiveIndex] = useState(0);
    const [logs, setLogs] = useState([]);
    const consoleRef = useRef(null);

    // Auto scroll the console terminal container internally (prevents page jump scroll)
    useEffect(() => {
        if (consoleRef.current) {
            consoleRef.current.scrollTop = consoleRef.current.scrollHeight;
        }
    }, [logs]);

    // Helper to add terminal console logs
    const addLog = (message, type = "info") => {
        const timestamp = new Date().toLocaleTimeString();
        setLogs(prev => [...prev, { timestamp, message, type }]);
    };

    // Fetch feed and user profile stats on mount
    useEffect(() => {
        async function initLoad() {
            setLoading(true);
            setLogs([]);
            setActiveIndex(0);
            
            addLog(`SESSION_START: Initialized guest session for ${ACTIVE_USER_ID}`, "info");
            
            try {
                // Fetch initial user profile stats
                const profileData = await getUserProfile(ACTIVE_USER_ID);
                setProfile(profileData);
                addLog(`PROFILE_LOADED: Loaded initial interests & creator affinities from backend`, "info");

                // Fetch personalized recommendations feed
                const feedData = await getFeed(ACTIVE_USER_ID);
                setVideos(feedData);
                addLog(`RETRIEVAL: Retrieved ${feedData.length} personalized candidates from FAISS vector search, collaborative filters, and trending pools`, "info");
            } catch (err) {
                console.error(err);
                addLog(`ERROR: Failed to fetch backend data. Verify server status`, "event");
            } finally {
                setLoading(false);
            }
        }
        initLoad();

        const handleCatalogUpdated = async () => {
            try {
                const updatedFeed = await getFeed(ACTIVE_USER_ID);
                setVideos(updatedFeed);
                addLog(`REAL_TIME_SYNC: Live recommendation feed automatically updated with newly processed content!`, "info");
            } catch (err) {
                console.error("Failed to auto-refresh catalog feed:", err);
            }
        };

        window.addEventListener("catalog_updated", handleCatalogUpdated);
        return () => window.removeEventListener("catalog_updated", handleCatalogUpdated);
    }, []);

    // Callback when feedback is successfully posted to backend
    const handleFeedbackSubmitted = async (res) => {
        try {
            // Re-load profile stats
            const profileData = await getUserProfile(ACTIVE_USER_ID);
            setProfile(profileData);

            // Re-load feed dynamically to see re-ranking
            const feedData = await getFeed(ACTIVE_USER_ID);
            
            // Preserve all videos up to the current activeIndex (so the active video doesn't change)
            // And merge the new recommended videos (filtering out duplicates of already watched ones)
            setVideos(prevVideos => {
                const watched = prevVideos.slice(0, activeIndex + 1);
                const lastCategory = watched[watched.length - 1]?.category;
                const watchedIds = new Set(watched.map(v => v.video_id));
                
                // Filter out watched IDs
                let newCands = feedData.filter(v => !watchedIds.has(v.video_id));
                
                // Enforce category alternation at the boundary
                if (newCands.length > 0 && newCands[0].category === lastCategory && lastCategory) {
                    const diffCatIdx = newCands.findIndex(v => v.category !== lastCategory);
                    if (diffCatIdx !== -1) {
                        const [item] = newCands.splice(diffCatIdx, 1);
                        newCands.unshift(item);
                    }
                }
                
                return [...watched, ...newCands];
            });
            
            addLog(`RE-RANKING: Recommender weights updated. Next videos in feed adjusted in real-time!`, "info");
        } catch (err) {
            console.error("Reload after feedback failed:", err);
        }
    };

    // Navigate slides in Reels mode
    const handleNextSlide = () => {
        if (activeIndex < videos.length - 1) {
            setActiveIndex(prev => prev + 1);
        }
    };

    const handlePrevSlide = () => {
        if (activeIndex > 0) {
            setActiveIndex(prev => prev - 1);
        }
    };

    // Active video details for scoring breakdown
    const activeVideo = videos[activeIndex];

    return (
        <div className="dashboard-container">
            {/* Left Panel: Immersive Reels Player Column */}
            <div className="feed-column">
                <div className="feed-header-row">
                    <div className="feed-title">
                        <h1>Daiv Clips Feed</h1>
                        <p>Personalized Recommendations Playground (MSR-VTT Dataset)</p>
                    </div>
                </div>

                {loading ? (
                    <div className="loading-state">
                        <div style={{ fontSize: "24px", marginBottom: "10px" }}>⚡</div>
                        Running candidate generation and multi-objective ranking...
                    </div>
                ) : videos.length === 0 ? (
                    <div className="loading-state">No videos found.</div>
                ) : (
                    <div className="reels-wrapper">
                        {/* Floating live event logs on the left of the player mockup */}
                        <div className="floating-console-widget">
                            <h3 style={{ display: "flex", alignItems: "center", margin: "0 0 10px 0", fontSize: "13px", color: "var(--accent)" }}>
                                <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2.5" strokeLinecap="round" strokeLinejoin="round" style={{ width: "15px", height: "15px", marginRight: "6px" }}><polyline points="4 17 10 11 4 5" /><line x1="12" y1="19" x2="20" y2="19" /></svg>
                                Real-Time Pipeline Logs
                            </h3>
                            <div className="floating-console-box" ref={consoleRef}>
                                {logs.length === 0 ? (
                                    <div className="empty-console">Terminal active. Awaiting logs...</div>
                                ) : (
                                    logs.map((log, index) => (
                                        <div key={index} className="console-line">
                                            <span className="console-time">[{log.timestamp}]</span>
                                            {log.type === "event" && <span className="console-tag-event" style={{ color: "#c084fc", marginRight: "4px" }}>[EVENT]</span>}
                                            {log.type === "feedback" && <span className="console-tag-feedback" style={{ color: "#34d399", marginRight: "4px" }}>[FEEDBACK]</span>}
                                            {log.type === "info" && <span className="console-tag-info" style={{ color: "#60a5fa", marginRight: "4px" }}>[SYSTEM]</span>}
                                            <span style={{ color: log.type === "feedback" ? "#34d399" : log.type === "event" ? "#c084fc" : "#e2e8f0" }}>{log.message}</span>
                                        </div>
                                    ))
                                )}
                            </div>
                        </div>

                        {/* Up button */}
                        {activeIndex > 0 && (
                            <button className="reels-nav-btn reels-nav-up" onClick={handlePrevSlide}>
                                ▲
                            </button>
                        )}

                        <div className="reels-viewport">
                            {videos.map((vid, idx) => (
                                <div 
                                    key={vid.video_id} 
                                    className="reels-slide"
                                    style={{ display: idx === activeIndex ? "block" : "none" }}
                                >
                                    <VideoCard
                                        video={vid}
                                        isActive={idx === activeIndex}
                                        layoutMode="reels"
                                        userId={ACTIVE_USER_ID}
                                        onFeedbackSubmitted={handleFeedbackSubmitted}
                                        addLog={addLog}
                                    />
                                </div>
                            ))}
                        </div>

                        {/* Down button */}
                        {activeIndex < videos.length - 1 && (
                            <button className="reels-nav-btn reels-nav-down" onClick={handleNextSlide}>
                                ▼
                            </button>
                        )}
                    </div>
                )}
            </div>

            {/* Right Panel: Algorithmic Dashboard */}
            <div className="dashboard-column">
                <div style={{ textAlign: "left" }}>
                    <h2 style={{ color: "var(--accent)", display: "flex", alignItems: "center" }}>
                        <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2.5" strokeLinecap="round" strokeLinejoin="round" style={{ width: "24px", height: "24px", marginRight: "8px", color: "var(--accent)" }}>
                            <path d="M9.5 2A2.5 2.5 0 0 1 12 4.5v15a2.5 2.5 0 0 1-4.96-.44 2.5 2.5 0 0 1 0-3.12 3 3 0 0 1 0-3.88 2.5 2.5 0 0 1 0-3.12A2.5 2.5 0 0 1 9.5 2Z" />
                            <path d="M14.5 2A2.5 2.5 0 0 0 12 4.5v15a2.5 2.5 0 0 0 4.96-.44 2.5 2.5 0 0 0 0-3.12 3 3 0 0 0 0-3.88 2.5 2.5 0 0 0 0-3.12A2.5 2.5 0 0 0 14.5 2Z" />
                        </svg>
                        Recommender Dashboard
                    </h2>
                    <span style={{ fontSize: "12px", color: "#8b9bb4" }}>Real-Time Personalization Stats</span>
                </div>

                <div className="divider"></div>

                {/* User Stats Card */}
                {profile && (
                    <div className="dashboard-widget-card">
                        <h3 style={{ display: "flex", alignItems: "center" }}>
                            <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round" style={{ width: "16px", height: "16px", marginRight: "6px", color: "var(--accent)" }}>
                                <path d="M19 21v-2a4 4 0 0 0-4-4H9a4 4 0 0 0-4 4v2" />
                                <circle cx="12" cy="7" r="4" />
                            </svg>
                            Session Profile
                        </h3>
                        <div style={{ fontSize: "13px", display: "flex", flexDirection: "column", gap: "6px" }}>
                            <div><strong>Username:</strong> {profile.username}</div>
                            <div><strong>User ID:</strong> {profile.user_id}</div>
                            <div>
                                <strong>Active Persona:</strong>{" "}
                                <span style={{ 
                                    background: "rgba(56, 189, 248, 0.15)", 
                                    color: "#38bdf8", 
                                    padding: "2px 8px", 
                                    borderRadius: "4px", 
                                    fontSize: "11px",
                                    fontWeight: "bold",
                                    marginLeft: "4px",
                                    display: "inline-block"
                                }}>
                                    {profile.persona || "Standard"}
                                </span>
                            </div>
                            {profile.persona && PERSONA_DESCRIPTIONS[profile.persona] && (
                                <div style={{ 
                                    marginTop: "4px", 
                                    fontSize: "11px", 
                                    color: "#94a3b8", 
                                    background: "rgba(255,255,255,0.02)", 
                                    padding: "6px 8px", 
                                    borderRadius: "6px", 
                                    borderLeft: "2px solid #38bdf8",
                                    fontStyle: "italic",
                                    lineHeight: "1.4"
                                }}>
                                    {PERSONA_DESCRIPTIONS[profile.persona]}
                                </div>
                            )}
                            <div style={{ marginTop: "4px" }}><strong>Watched Count:</strong> {profile.total_watched} clips</div>
                        </div>
                    </div>
                )}

                {/* Interest Profile Card */}
                {profile && (
                    <div className="dashboard-widget-card">
                        <h3 style={{ display: "flex", alignItems: "center" }}>
                            <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round" style={{ width: "16px", height: "16px", marginRight: "6px", color: "var(--accent)" }}>
                                <line x1="18" y1="20" x2="18" y2="10" />
                                <line x1="12" y1="20" x2="12" y2="4" />
                                <line x1="6" y1="20" x2="6" y2="14" />
                            </svg>
                            Interest Profile Vector
                        </h3>
                        <div style={{ display: "flex", flexDirection: "column" }}>
                            {Object.entries(profile.interests).length === 0 ? (
                                <span style={{ fontSize: "12px", fontStyle: "italic", color: "#64748b" }}>Empty vector (Cold Start)</span>
                            ) : (
                                Object.entries(profile.interests)
                                    .sort((a,b) => b[1] - a[1])
                                    .map(([cat, pct]) => (
                                        <div key={cat} className="interest-row">
                                            <div className="interest-info">
                                                <span>{cat}</span>
                                                <span>{pct}%</span>
                                            </div>
                                            <div className="bar-bg">
                                                <div 
                                                    className="bar-fill" 
                                                    style={{ 
                                                        width: `${pct}%`, 
                                                        background: cat === "Automobile" || cat === "Auto" ? "#ff3b5c" : 
                                                                    cat === "Tech" || cat === "Science" ? "#00e676" : 
                                                                    cat === "Food" ? "#ffeb3b" : 
                                                                    cat === "Travel" ? "#38bdf8" : 
                                                                    cat === "Animal" ? "#ec4899" : "#bb86fc"
                                                    }}
                                                ></div>
                                            </div>
                                        </div>
                                    ))
                            )}
                        </div>
                    </div>
                )}

                {/* Creator Affinity Card */}
                {profile && (
                    <div className="dashboard-widget-card">
                        <h3 style={{ display: "flex", alignItems: "center" }}>
                            <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round" style={{ width: "16px", height: "16px", marginRight: "6px", color: "var(--accent)" }}>
                                <polygon points="12 2 15.09 8.26 22 9.27 17 14.14 18.18 21.02 12 17.77 5.82 21.02 7 14.14 2 9.27 8.91 8.26 12 2" />
                            </svg>
                            Creator Affinity Index
                        </h3>
                        <div className="affinity-list">
                            {Object.entries(profile.creator_affinities).length === 0 ? (
                                <span style={{ fontSize: "12px", fontStyle: "italic", color: "#64748b", padding: "10px 0" }}>No creator interaction data</span>
                            ) : (
                                Object.entries(profile.creator_affinities)
                                    .sort((a,b) => b[1] - a[1])
                                    .map(([creator, score]) => (
                                        <div key={creator} className="affinity-item">
                                            <span className="affinity-creator">@{creator}</span>
                                            <span className="affinity-score">Affinity: {score.toFixed(0)}</span>
                                        </div>
                                    ))
                            )}
                        </div>
                    </div>
                )}

                {/* Algorithmic Score Breakdown Card */}
                {activeVideo && activeVideo.score_breakdown && (
                    <div className="dashboard-widget-card">
                        <h3 style={{ display: "flex", alignItems: "center" }}>
                            <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round" style={{ width: "16px", height: "16px", marginRight: "6px", color: "var(--accent)" }}>
                                <circle cx="12" cy="12" r="10" />
                                <circle cx="12" cy="12" r="6" />
                                <circle cx="12" cy="12" r="2" />
                            </svg>
                            Explanation & Ranking Breakdown
                        </h3>
                        
                        <div style={{ fontSize: "12px", background: "rgba(255,255,255,0.03)", padding: "10px", borderRadius: "10px", border: "1px solid rgba(255,255,255,0.05)", marginBottom: "14px", lineHeight: "1.4" }}>
                            <strong>Decision:</strong> "{activeVideo.explanation}"
                        </div>
                        
                        <div style={{ display: "flex", flexDirection: "column" }}>
                            {/* Interest match (Weight: 35%) */}
                            <div className="breakdown-row">
                                <span className="breakdown-label">
                                    <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round" style={{ width: "13px", height: "13px", marginRight: "5px", display: "inline-block", verticalAlign: "middle" }}><path d="M4 20h16a2 2 0 0 0 2-2V8a2 2 0 0 0-2-2h-7.93a2 2 0 0 1-1.66-.9l-.82-1.2A2 2 0 0 0 7.93 3H4a2 2 0 0 0-2 2v13a2 2 0 0 0 2 2Z" /></svg>
                                    Category Interest <span style={{ color: "#64748b" }}>(35%)</span>
                                </span>
                                <div style={{ display: "flex", alignItems: "center", gap: "8px" }}>
                                    <div className="breakdown-bar-bg">
                                        <div className="breakdown-bar-fill" style={{ width: `${activeVideo.score_breakdown.interest * 100}%` }}></div>
                                    </div>
                                    <span className="breakdown-value">{(activeVideo.score_breakdown.interest * 100).toFixed(0)}%</span>
                                </div>
                            </div>

                            {/* Creator Affinity (Weight: 20%) */}
                            <div className="breakdown-row">
                                <span className="breakdown-label">
                                    <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round" style={{ width: "13px", height: "13px", marginRight: "5px", display: "inline-block", verticalAlign: "middle" }}><path d="M19 21v-2a4 4 0 0 0-4-4H9a4 4 0 0 0-4 4v2" /><circle cx="12" cy="7" r="4" /></svg>
                                    Creator Affinity <span style={{ color: "#64748b" }}>(20%)</span>
                                </span>
                                <div style={{ display: "flex", alignItems: "center", gap: "8px" }}>
                                    <div className="breakdown-bar-bg">
                                        <div className="breakdown-bar-fill" style={{ width: `${activeVideo.score_breakdown.creator_affinity * 100}%` }}></div>
                                    </div>
                                    <span className="breakdown-value">{(activeVideo.score_breakdown.creator_affinity * 100).toFixed(0)}%</span>
                                </div>
                            </div>

                            {/* Vector Similarity (Weight: 15%) */}
                            <div className="breakdown-row">
                                <span className="breakdown-label">
                                    <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round" style={{ width: "13px", height: "13px", marginRight: "5px", display: "inline-block", verticalAlign: "middle" }}><circle cx="18" cy="5" r="3" /><circle cx="6" cy="12" r="3" /><circle cx="18" cy="19" r="3" /><line x1="8.59" y1="13.51" x2="15.42" y2="17.49" /><line x1="15.41" y1="6.51" x2="8.59" y2="10.49" /></svg>
                                    Vector Similarity <span style={{ color: "#64748b" }}>(15%)</span>
                                </span>
                                <div style={{ display: "flex", alignItems: "center", gap: "8px" }}>
                                    <div className="breakdown-bar-bg">
                                        <div className="breakdown-bar-fill" style={{ width: `${activeVideo.score_breakdown.similarity * 100}%` }}></div>
                                    </div>
                                    <span className="breakdown-value">{(activeVideo.score_breakdown.similarity * 100).toFixed(0)}%</span>
                                </div>
                            </div>

                            {/* Collaborative filtering (Weight: 10%) */}
                            <div className="breakdown-row">
                                <span className="breakdown-label">
                                    <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round" style={{ width: "13px", height: "13px", marginRight: "5px", display: "inline-block", verticalAlign: "middle" }}><path d="M16 21v-2a4 4 0 0 0-4-4H6a4 4 0 0 0-4 4v2" /><circle cx="9" cy="7" r="4" /><path d="M22 21v-2a4 4 0 0 0-3-3.87" /><path d="M16 3.13a4 4 0 0 1 0 7.75" /></svg>
                                    Taste Similarity <span style={{ color: "#64748b" }}>(10%)</span>
                                </span>
                                <div style={{ display: "flex", alignItems: "center", gap: "8px" }}>
                                    <div className="breakdown-bar-bg">
                                        <div className="breakdown-bar-fill" style={{ width: `${activeVideo.score_breakdown.collaborative_filtering * 100}%` }}></div>
                                    </div>
                                    <span className="breakdown-value">{(activeVideo.score_breakdown.collaborative_filtering * 100).toFixed(0)}%</span>
                                </div>
                            </div>

                            {/* Popularity (Weight: 10%) */}
                            <div className="breakdown-row">
                                <span className="breakdown-label">
                                    <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round" style={{ width: "13px", height: "13px", marginRight: "5px", display: "inline-block", verticalAlign: "middle" }}><polyline points="22 7 13.5 15.5 8.5 10.5 2 17" /><polyline points="16 7 22 7 22 13" /></svg>
                                    Popularity / Views <span style={{ color: "#64748b" }}>(10%)</span>
                                </span>
                                <div style={{ display: "flex", alignItems: "center", gap: "8px" }}>
                                    <div className="breakdown-bar-bg">
                                        <div className="breakdown-bar-fill" style={{ width: `${activeVideo.score_breakdown.popularity * 100}%` }}></div>
                                    </div>
                                    <span className="breakdown-value">{(activeVideo.score_breakdown.popularity * 100).toFixed(0)}%</span>
                                </div>
                            </div>

                            {/* Freshness (Weight: 5%) */}
                            <div className="breakdown-row">
                                <span className="breakdown-label">
                                    <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round" style={{ width: "13px", height: "13px", marginRight: "5px", display: "inline-block", verticalAlign: "middle" }}><path d="m12 3-1.912 5.813a2 2 0 0 1-1.275 1.275L3 12l5.813 1.912a2 2 0 0 1 1.275 1.275L12 21l1.912-5.813a2 2 0 0 1 1.275-1.275L21 12l-5.813-1.912a2 2 0 0 1-1.275-1.275L12 3Z" /></svg>
                                    Content Freshness <span style={{ color: "#64748b" }}>(5%)</span>
                                </span>
                                <div style={{ display: "flex", alignItems: "center", gap: "8px" }}>
                                    <div className="breakdown-bar-bg">
                                        <div className="breakdown-bar-fill" style={{ width: `${activeVideo.score_breakdown.freshness * 100}%` }}></div>
                                    </div>
                                    <span className="breakdown-value">{(activeVideo.score_breakdown.freshness * 100).toFixed(0)}%</span>
                                </div>
                            </div>

                            {/* Exploration (Weight: 5%) */}
                            <div className="breakdown-row">
                                <span className="breakdown-label">
                                    <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round" style={{ width: "13px", height: "13px", marginRight: "5px", display: "inline-block", verticalAlign: "middle" }}><circle cx="12" cy="12" r="10" /><polygon points="16.24 7.76 14.12 14.12 7.76 16.24 9.88 9.88 16.24 7.76" /></svg>
                                    Exploration Bonus <span style={{ color: "#64748b" }}>(5%)</span>
                                </span>
                                <div style={{ display: "flex", alignItems: "center", gap: "8px" }}>
                                    <div className="breakdown-bar-bg">
                                        <div className="breakdown-bar-fill" style={{ width: `${activeVideo.score_breakdown.exploration * 100}%` }}></div>
                                    </div>
                                    <span className="breakdown-value">{(activeVideo.score_breakdown.exploration * 100).toFixed(0)}%</span>
                                </div>
                            </div>

                            <div className="divider" style={{ margin: "10px 0" }}></div>

                            <div style={{ display: "flex", justifyContent: "space-between", alignItems: "center", fontWeight: "700" }}>
                                <span style={{ color: "var(--text-bright)" }}>Final Matching Score</span>
                                <span style={{ color: "var(--success)", fontSize: "16px" }}>{(activeVideo.score * 100).toFixed(1)}% Match</span>
                            </div>
                        </div>
                    </div>
                )}


            </div>
        </div>
    );
}

export default VideoFeed;