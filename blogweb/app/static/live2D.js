
L2Dwidget
  .on('*', (name) => {
    console.log('%c EVENT ' + '%c -> ' + name, 'background: #222; color: yellow', 'background: #fff; color: #000')
  })
  .init({
    "model": {
      "jsonPath": "https://unpkg.com/live2d-widget-model-hijiki@1.0.5/assets/hijiki.model.json",
      "scale": 1
    },
    "display": {
      "position": "right",
      "width": 300,
      "height": 400,
      "hOffset": 0,
      "vOffset": -20
    },
    "dialog": {
      "enable": true,
      "script": {
        'tap body': '害羞/(/ ⁄•/ω/•/ /)/',
        'tap face': '~~'
      }
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

