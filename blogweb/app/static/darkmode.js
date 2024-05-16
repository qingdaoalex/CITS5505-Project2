function addDarkmodeWidget() {
  new Darkmode().showWidget();
}
window.addEventListener('load', addDarkmodeWidget);

const options = {
  bottom: '64px', // default: '32px'
  right: 'unset', // default: '32px'
  left: '32px', // default: 'unset'
  time: '0.5s', // default: '0.3s'
  backgroundColor: '#fff',  // default: '#fff'
  buttonColorDark: '#fff',  // default: '#100f2c'
  buttonColorLight: '#100f2c', // default: '#fff'
  saveInCookies: true, // default: true,
  label: '🌓', // default: ''
  autoMatchOsTheme: false // default: true
}

const darkmode = new Darkmode(options);
darkmode.showWidget();
