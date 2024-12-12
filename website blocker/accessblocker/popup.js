// popup.js

// Function to reset access counts for all allowed sites
document.getElementById('reset-button').addEventListener('click', async () => {
    const allowedSites = ['facebook.com', 'twitter.com', 'instagram.com', 'linkedin.com'];
    
    // Reset access count for each allowed site
    for (const site of allowedSites) {
        await chrome.storage.local.set({ [site]: { count: 0, date: new Date().toISOString().split('T')[0] } });
    }
    
    // Notify the user that the access count has been reset
    alert('Access count has been reset for all sites.');
});

// Placeholder for settings button functionality
document.getElementById('settings-button').addEventListener('click', () => {
    alert('Settings functionality is not yet implemented.');
});

// Optional: Function to display current access counts (if needed)
async function displayAccessCounts() {
    const allowedSites = ['facebook.com', 'twitter.com', 'instagram.com', 'linkedin.com'];
    let message = 'Current Access Counts:\n';

    for (const site of allowedSites) {
        const data = await chrome.storage.local.get(site);
        const count = data[site] ? data[site].count : 0;
        message += `${site}: ${count} accesses\n`;
    }

    alert(message);
}

// Uncomment the following line to display access counts when the popup opens
// displayAccessCounts();
