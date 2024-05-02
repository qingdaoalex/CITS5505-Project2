document.addEventListener("DOMContentLoaded", function() {
  // Load the loading page
  var loadingFrame = document.createElement("iframe");
  loadingFrame.style.cssText = "position: fixed; top: 0; left: 0; width: 100%; height: 100%; border: none; z-index: 9999;";
  loadingFrame.src = "loading.html";
  
  // Append the loading page iframe to the body
  document.body.appendChild(loadingFrame);
});

window.addEventListener("load", function() {
  // Hide the loading page when all resources (including images, scripts, etc.) are loaded
  var loadingFrame = document.querySelector("iframe[src='loading.html']");
  if (loadingFrame) {
    loadingFrame.style.display = "none";
  }
});
