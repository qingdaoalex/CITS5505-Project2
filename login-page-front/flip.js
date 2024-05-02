document.addEventListener("DOMContentLoaded", function() {
    var toRegister = document.getElementById("to-register");
    var toLogin_1 = document.getElementById("to-login-1");
    var toLogin_2 = document.getElementById("to-login-2");
    var toReset = document.getElementById("to-reset");

    toRegister.onclick = function(){
        document.querySelector("#flipper").classList.toggle("flip");
        document.querySelector(".reset").style.visibility = "hidden";
        document.querySelector(".register").style.visibility = "visible";
        document.querySelector(".register").style.pointerEvents = "auto";
        document.querySelector(".login").style.visibility = "hidden";
        document.querySelector(".login").style.pointerEvents = "none";
    };
    // Check if the URL contains "#register" and trigger the click event on toRegister
    if (window.location.hash === "#register") {
        toRegister.onclick();
    }
    toLogin_1.onclick = function(){
        document.querySelector("#flipper").classList.toggle("flip");
        document.querySelector(".reset").style.visibility = "hidden";
        document.querySelector(".register").style.visibility = "hidden";
        document.querySelector(".register").style.pointerEvents = "none";
        document.querySelector(".login").style.visibility = "visible";
        document.querySelector(".login").style.pointerEvents = "auto";
    };
    toReset.onclick = function(){
        document.querySelector("#flipper").classList.toggle("flip");
        document.querySelector(".register").style.visibility = "hidden";
        document.querySelector(".reset").style.visibility = "visible";
        document.querySelector(".reset").style.pointerEvents = "auto";
        document.querySelector(".login").style.visibility = "hidden";
        document.querySelector(".login").style.pointerEvents = "none";
    }
    toLogin_2.onclick = function(){
        document.querySelector("#flipper").classList.toggle("flip");
        document.querySelector(".reset").style.visibility = "hidden";
        document.querySelector(".register").style.visibility = "hidden";
        document.querySelector(".register").style.pointerEvents = "none";
        document.querySelector(".login").style.visibility = "visible";
        document.querySelector(".login").style.pointerEvents = "auto";
    };
});
