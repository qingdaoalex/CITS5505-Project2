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

