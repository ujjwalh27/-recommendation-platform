const BASE_URL = "http://127.0.0.1:8000";

export async function getFeed(userId = "user_1") {
    const response = await fetch(`${BASE_URL}/feed?user_id=${userId}`);
    return await response.json();
}

export async function getRecommendations(videoId) {
    const response = await fetch(`${BASE_URL}/recommend/${videoId}`);
    return await response.json();
}

export async function submitFeedback(userId, videoId, engagement) {
    const response = await fetch(`${BASE_URL}/feedback`, {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify({
            user_id: userId,
            video_id: videoId,
            watch_completion_rate: engagement.watchCompletionRate,
            watch_time_seconds: engagement.watchTimeSeconds || 0.0,
            replay_count: engagement.replayCount || 0,
            is_liked: engagement.isLiked || false,
            is_saved: engagement.isSaved || false,
            is_shared: engagement.isShared || false,
            is_commented: engagement.isCommented || false,
            is_final: engagement.isFinal || false
        })
    });
    return await response.json();
}

export async function getUserProfile(userId) {
    const response = await fetch(`${BASE_URL}/profile/${userId}`);
    return await response.json();
}

export function videoUrl(videoId) {
    return `${BASE_URL}/videos/${videoId}.mp4`;
}

export function thumbnailUrl(videoId) {
    return `${BASE_URL}/thumbnails/${videoId}.jpg`;
}