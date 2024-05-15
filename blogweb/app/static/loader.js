// Function to check if all scripts are loaded
function allScriptsLoaded() {
    const scripts = document.querySelectorAll('script[defer]');
    return Array.from(scripts).every(script => script.loaded);
}

// Function to hide loader
function hideLoader() {
    if (allScriptsLoaded()) {
        document.body.classList.add('loaded');
    }
}

// Add listener to load.js to execute hideLoader function
document.querySelector('script[src="load.js"]').addEventListener('load', hideLoader);

// Event listener for each script to mark it as loaded
document.addEventListener('readystatechange', hideLoader);
document.addEventListener('DOMContentLoaded', hideLoader);
window.addEventListener('load', hideLoader);