const BASE_URL = "http://127.0.0.1:8000";

async function request(url) {
    const response = await fetch(url);

    if (!response.ok) {
        throw new Error(
            `HTTP ${response.status}`
        );
    }

    return response.json();
}

export async function getFeed() {
    return request(`${BASE_URL}/feed`);
}

export async function getRecommendations(videoId) {
    return request(
        `${BASE_URL}/recommend/${videoId}`
    );
}

export function getVideoUrl(videoId) {
    return `${BASE_URL}/videos/${videoId}.mp4`;
}

export function getThumbnailUrl(videoId) {
    return `${BASE_URL}/thumbnails/${videoId}.jpg`;
}