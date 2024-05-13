function addDarkmodeWidget() {
  new Darkmode().showWidget();
}
window.addEventListener('load', addDarkmodeWidget);

const darkmode =  new Darkmode();
darkmode.toggle();
