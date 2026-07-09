import { useState, useEffect, useRef } from "react";
import { submitFeedback, videoUrl, thumbnailUrl } from "../../services/api";

function VideoCard({ video, isActive, layoutMode, userId, onFeedbackSubmitted, onSelect, addLog }) {
    const videoRef = useRef(null);
    const [liked, setLiked] = useState(false);
    const [saved, setSaved] = useState(false);
    const [commented, setCommented] = useState(false);
    const [isPlaying, setIsPlaying] = useState(false);
    const [showIndicator, setShowIndicator] = useState(null); // 'play' or 'pause'
    const [progress, setProgress] = useState(0);
    
    // Watch statistics refs to avoid React re-render loops during continuous updates
    const watchStartTimeRef = useRef(null);
    const totalWatchTimeRef = useRef(0);
    const replayCountRef = useRef(0);
    const durationRef = useRef(video.duration || 15.0);

    // Sync state if video model already has engagement (or defaults)
    useEffect(() => {
        setLiked(video.is_liked || false);
        setSaved(video.is_saved || false);
        setCommented(video.is_commented || false);
        totalWatchTimeRef.current = 0;
        replayCountRef.current = 0;
        setProgress(0);
    }, [video, userId]);

    // Handle Reels Play/Pause auto trigger
    useEffect(() => {
        if (!videoRef.current) return;

        const videoEl = videoRef.current;
        if (isActive) {
            videoEl.currentTime = 0;
            videoEl.play()
                .then(() => {
                    setIsPlaying(true);
                    watchStartTimeRef.current = Date.now();
                    addLog(`PLAY: Started playing clip ${video.video_id}`, "event");
                })
                .catch(err => console.log("Play interrupted:", err));
        } else {
            videoEl.pause();
            setIsPlaying(false);
            submitSessionFeedback();
        }

        return () => {
            // Submit session on cleanup (when active changes or component unmounts)
            if (isActive) {
                submitSessionFeedback();
            }
        };
    }, [isActive, userId]);

    const submitSessionFeedback = () => {
        if (watchStartTimeRef.current === null) return;

        const sessionTime = (Date.now() - watchStartTimeRef.current) / 1000.0;
        totalWatchTimeRef.current += sessionTime;
        watchStartTimeRef.current = null;

        const duration = durationRef.current || 15.0;
        const watchCompletionRate = Math.min(2.0, totalWatchTimeRef.current / duration);

        if (totalWatchTimeRef.current < 0.5) {
            // Ignore accidental quick scrolls
            return;
        }

        const engagement = {
            watchCompletionRate: Number(watchCompletionRate.toFixed(2)),
            watchTimeSeconds: Number(totalWatchTimeRef.current.toFixed(2)),
            replayCount: replayCountRef.current,
            isLiked: liked,
            isSaved: saved,
            isShared: false,
            isCommented: commented
        };

        addLog(`SESSION_END: Finished watching clip ${video.video_id} (Watch Time: ${engagement.watchTimeSeconds}s, Completion: ${Math.round(engagement.watchCompletionRate * 100)}%, Replays: ${engagement.replayCount})`, "feedback");

        submitFeedback(userId, video.video_id, engagement)
            .then(res => {
                if (res.status === "success") {
                    addLog(`MODEL_TRAINED: Recalculated interests for ${userId}. Dynamic re-ranking updated!`, "info");
                    if (onFeedbackSubmitted) {
                        onFeedbackSubmitted(res);
                    }
                }
            })
            .catch(err => {
                console.error("Feedback submit failed:", err);
            });
    };

    const handleVideoClick = () => {
        if (!videoRef.current) return;
        const videoEl = videoRef.current;
        if (videoEl.paused) {
            videoEl.play();
            setIsPlaying(true);
            watchStartTimeRef.current = Date.now();
            setShowIndicator("play");
            addLog(`PLAY: Resumed clip ${video.video_id}`, "event");
        } else {
            videoEl.pause();
            setIsPlaying(false);
            if (watchStartTimeRef.current) {
                totalWatchTimeRef.current += (Date.now() - watchStartTimeRef.current) / 1000.0;
                watchStartTimeRef.current = null;
            }
            setShowIndicator("pause");
            addLog(`PAUSE: Paused clip ${video.video_id}`, "event");
        }
        setTimeout(() => setShowIndicator(null), 800);
    };

    const handleTimeUpdate = (e) => {
        const videoEl = e.target;
        if (videoEl.duration) {
            durationRef.current = videoEl.duration;
            setProgress((videoEl.currentTime / videoEl.duration) * 100);
        }
    };

    const handleVideoEnded = (e) => {
        replayCountRef.current += 1;
        addLog(`LOOP: Clip ${video.video_id} replayed (${replayCountRef.current}x)`, "event");
        
        // Accumulate watch time for the full loop
        if (watchStartTimeRef.current) {
            totalWatchTimeRef.current += (Date.now() - watchStartTimeRef.current) / 1000.0;
            watchStartTimeRef.current = Date.now(); // reset start time for next loop
        }
        
        const videoEl = e.target;
        videoEl.currentTime = 0;
        videoEl.play().catch(err => console.log(err));
    };

    const handleLikeClick = (e) => {
        e.stopPropagation();
        const nextLiked = !liked;
        setLiked(nextLiked);
        addLog(`LIKE: ${nextLiked ? "Liked" : "Unliked"} clip ${video.video_id}`, "event");
        
        // Send immediate interactive update to backend
        const duration = durationRef.current || 15.0;
        const currentSessionTime = watchStartTimeRef.current ? (Date.now() - watchStartTimeRef.current) / 1000.0 : 0;
        const totalTime = totalWatchTimeRef.current + currentSessionTime;
        
        submitFeedback(userId, video.video_id, {
            watchCompletionRate: Number((totalTime / duration).toFixed(2)),
            watchTimeSeconds: Number(totalTime.toFixed(2)),
            replayCount: replayCountRef.current,
            isLiked: nextLiked,
            isSaved: saved,
            isCommented: commented
        }).then(res => {
            if (res.status === "success" && onFeedbackSubmitted) {
                onFeedbackSubmitted(res);
            }
        });
    };

    const handleSaveClick = (e) => {
        e.stopPropagation();
        const nextSaved = !saved;
        setSaved(nextSaved);
        addLog(`SAVE: ${nextSaved ? "Saved" : "Unsaved"} clip ${video.video_id}`, "event");

        const duration = durationRef.current || 15.0;
        const currentSessionTime = watchStartTimeRef.current ? (Date.now() - watchStartTimeRef.current) / 1000.0 : 0;
        const totalTime = totalWatchTimeRef.current + currentSessionTime;

        submitFeedback(userId, video.video_id, {
            watchCompletionRate: Number((totalTime / duration).toFixed(2)),
            watchTimeSeconds: Number(totalTime.toFixed(2)),
            replayCount: replayCountRef.current,
            isLiked: liked,
            isSaved: nextSaved,
            isCommented: commented
        }).then(res => {
            if (res.status === "success" && onFeedbackSubmitted) {
                onFeedbackSubmitted(res);
            }
        });
    };

    const handleCommentClick = (e) => {
        e.stopPropagation();
        const commentText = prompt("Add a comment to this clip:");
        if (commentText === null) return; // User cancelled
        
        const text = commentText.trim() || "Awesome clip!";
        setCommented(true);
        addLog(`COMMENT: Posted comment "${text}" on clip ${video.video_id}`, "event");

        const duration = durationRef.current || 15.0;
        const currentSessionTime = watchStartTimeRef.current ? (Date.now() - watchStartTimeRef.current) / 1000.0 : 0;
        const totalTime = totalWatchTimeRef.current + currentSessionTime;

        submitFeedback(userId, video.video_id, {
            watchCompletionRate: Number((totalTime / duration).toFixed(2)),
            watchTimeSeconds: Number(totalTime.toFixed(2)),
            replayCount: replayCountRef.current,
            isLiked: liked,
            isSaved: saved,
            isCommented: true
        }).then(res => {
            if (res.status === "success" && onFeedbackSubmitted) {
                onFeedbackSubmitted(res);
            }
        });
    };

    const handleShareClick = (e) => {
        e.stopPropagation();
        addLog(`SHARE: Shared clip ${video.video_id}`, "event");
        
        // Share has +10 score weight
        const duration = durationRef.current || 15.0;
        const currentSessionTime = watchStartTimeRef.current ? (Date.now() - watchStartTimeRef.current) / 1000.0 : 0;
        const totalTime = totalWatchTimeRef.current + currentSessionTime;

        submitFeedback(userId, video.video_id, {
            watchCompletionRate: Number((totalTime / duration).toFixed(2)),
            watchTimeSeconds: Number(totalTime.toFixed(2)),
            replayCount: replayCountRef.current,
            isLiked: liked,
            isSaved: saved,
            isShared: true,
            isCommented: commented
        }).then(res => {
            if (res.status === "success" && onFeedbackSubmitted) {
                onFeedbackSubmitted(res);
            }
        });
    };

    // Reels view Layout
    const matchPercentage = Math.round(video.score * 100);
    return (
        <div className="video-card-reels" onClick={handleVideoClick}>
            <video
                ref={videoRef}
                src={video.video_url}
                controls={false}
                muted={false} // Unmute in reels mode so they can hear audio
                playsInline
                onTimeUpdate={handleTimeUpdate}
                onEnded={handleVideoEnded}
            />

            {/* Custom Interactive Indicator overlay */}
            {showIndicator && (
                <div className="video-custom-controls">
                    <div className="play-pause-indicator">
                        {showIndicator === "play" ? "▶" : "⏸"}
                    </div>
                </div>
            )}

            {/* Reels action sidebar */}
            <div className="reels-sidebar">
                <div className="reels-action-item" onClick={handleLikeClick}>
                    <button className={`reels-action-btn ${liked ? "active-like" : ""}`}>
                        ❤
                    </button>
                    <span className="reels-action-label">{liked ? "Liked" : "Like"}</span>
                </div>

                <div className="reels-action-item" onClick={handleSaveClick}>
                    <button className={`reels-action-btn ${saved ? "active-save" : ""}`}>
                        ★
                    </button>
                    <span className="reels-action-label">{saved ? "Saved" : "Save"}</span>
                </div>

                <div className="reels-action-item" onClick={handleCommentClick}>
                    <button className={`reels-action-btn ${commented ? "active-save" : ""}`} style={{ color: commented ? "#38bdf8" : "#ffffff" }}>
                        💬
                    </button>
                    <span className="reels-action-label">{commented ? "Commented" : "Comment"}</span>
                </div>

                <div className="reels-action-item" onClick={handleShareClick}>
                    <button className="reels-action-btn">
                        📤
                    </button>
                    <span className="reels-action-label">Share</span>
                </div>
            </div>

            {/* Bottom info banner */}
            <div className="reels-overlay-bottom">
                <div style={{ display: "flex", gap: "8px", alignItems: "center" }}>
                    <div className="reels-creator-avatar">
                        {(video.title[0] || "@").toUpperCase()}
                    </div>
                    <span className="category-tag">{video.category}</span>
                    <span className="match-badge">{matchPercentage}% Match</span>
                    {video.retrieval_sources && video.retrieval_sources.includes("freshness") && (
                        <span className="badge-retrieval badge-fresh">✨ Fresh</span>
                    )}
                    {video.retrieval_sources && video.retrieval_sources.includes("exploration") && (
                        <span className="badge-retrieval badge-explore">🎲 Explore</span>
                    )}
                    {video.retrieval_sources && (
                        video.retrieval_sources.includes("similarity") ||
                        video.retrieval_sources.includes("creator_affinity") ||
                        video.retrieval_sources.includes("collaborative_filtering") ||
                        video.retrieval_sources.includes("category")
                    ) && (
                        <span className="badge-retrieval badge-personal">❤️ Personal</span>
                    )}
                </div>

                <p className="reels-caption">{video.title}</p>
                
                {video.explanation && (
                    <div className="explanation-banner">
                        ✨ {video.explanation}
                    </div>
                )}
            </div>

            {/* Progress bar line at the bottom */}
            <div className="reels-progress-bar">
                <div className="reels-progress-fill" style={{ width: `${progress}%` }}></div>
            </div>
        </div>
    );
}

export default VideoCard;