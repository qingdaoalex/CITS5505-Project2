// Create a new script element
var script = document.createElement('script');

// Set the source attribute to the URL of the JavaScript file you want to load
script.src = 'https://l2dwidget.js.org/lib/L2Dwidget.min.js';

// Define a callback function to execute once the script has loaded
script.onload = function() {
  // Code to execute after the script has loaded
  L2Dwidget.init({
    "model": {
      "jsonPath": "https://unpkg.com/live2d-widget-model-hijiki@1.0.5/assets/hijiki.model.json",
      "scale": 0.8,
    },
    "display": {
      "position":"left",
      "width": 220,
      "height": 280,
      "hOffset": 0,
      "vOffset": -20
    },
    "mobile": {
      "show": true,
      "scale": 0.4,
      "motion": true
    },
    "react": {
      "opacityDefault": 0.8,
      "opacityOnHover": 0.1
    },
    "name": {
      "canvas": "live2dcanvas",
      "div": "live2d-widget",
    }
  });
};

// Append the script element to the document's head to start loading the script
document.head.appendChild(script);
