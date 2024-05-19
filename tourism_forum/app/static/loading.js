// Function to load the loading page
function loadLoadingPage() {
    // Create a new iframe element for the loading page
    var loadingFrame = document.createElement("iframe");
    loadingFrame.style.cssText = "position: fixed; top: 0; left: 0; width: 100%; height: 100%; border: none; z-index: 9999;";
    loadingFrame.src = "loading.html";
    
    // Append the iframe to the body
    document.body.appendChild(loadingFrame);
  }
  
  // Function to check if the main content is fully loaded
  function checkMainContentLoaded() {
    // Check if the document and all external resources are fully loaded
    if (document.readyState === "complete") {
      // Hide the loading page if the main content is fully loaded
      var loadingPage = document.getElementById("loading-page");
      if (loadingPage) {
        loadingPage.style.display = "none";
      }
    } else {
      // Load the loading page if the main content is not fully loaded
      loadLoadingPage();
    }
  }
  
  // Event listener for DOMContentLoaded event
  document.addEventListener("DOMContentLoaded", function() {
    checkMainContentLoaded();
  });
  
  // Event listener for load event
  window.addEventListener("load", function() {
    checkMainContentLoaded();
  });
  