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
      "scale": 1
    },
    "display": {
      "position":"right",
      "width": 300,
      "height": 400,
      "hOffset": 0,
      "vOffset": -20
    },
    "mobile": {
      "show": true,
      "scale": 0.5
    },
    "react": {
      "opacityDefault": 0.8,
      "opacityOnHover": 0.1
    }
  });
};

// Append the script element to the document's head to start loading the script
document.head.appendChild(script);
