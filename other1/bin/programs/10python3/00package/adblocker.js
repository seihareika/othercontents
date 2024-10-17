// adblocker.js
const adSelectors = [
    '[id^="ad-"]',
    '[class*="ad-"]',
    'iframe[src*="ads"]',
    'iframe[src*="doubleclick"]',
    'iframe[src*="googlesyndication"]',
    'iframe[src*="adservice"]'
];

function removeAds() {
    adSelectors.forEach(selector => {
        document.querySelectorAll(selector).forEach(ad => ad.remove());
    });
}

window.onload = () => {
    removeAds();
    new MutationObserver(removeAds).observe(document.body, { childList: true, subtree: true });
};
