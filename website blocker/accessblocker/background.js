// background.js
const socialMediaSites = ['facebook.com', 'twitter.com', 'instagram.com', 'linkedin.com'];
const dailyLimit = 20;
let accessCount = {};
let lastAccessDate = {};

// Function to check access
function checkAccess(details) {
    const url = new URL(details.url);
    const site = url.hostname;

    if (socialMediaSites.includes(site)) {
        const today = new Date().toISOString().split('T')[0];

        // Initialize access count for the user
        if (!accessCount[site]) {
            accessCount[site] = { count: 0, date: today };
        }

        // Reset count if the day has changed
        if (accessCount[site].date !== today) {
            accessCount[site].count = 0;
            accessCount[site].date = today;
        }

        // Check if the limit has been reached
        if (accessCount[site].count < dailyLimit) {
            accessCount[site].count++;
            return { cancel: false }; // Allow access
        } else {
            return { cancel: true }; // Block access
        }
    }
    return { cancel: false }; // Allow access for non-social media sites
}

// Listen for web requests
chrome.webRequest.onBeforeRequest.addListener(
    checkAccess,
    { urls: ["<all_urls>"] },
    ["blocking"]
);