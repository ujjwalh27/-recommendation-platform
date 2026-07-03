const BASE_URL = "http://127.0.0.1:8000";

export async function getFeed() {
    const response = await fetch(`${BASE_URL}/feed`);
    return await response.json();
}

export async function getRecommendations(videoId) {
    const response = await fetch(
        `${BASE_URL}/recommend/${videoId}`
    );

    return await response.json();
}

export function videoUrl(videoId) {
    return `${BASE_URL}/videos/${videoId}.mp4`;
}

export function thumbnailUrl(videoId) {
    return `${BASE_URL}/thumbnails/${videoId}.jpg`;
}