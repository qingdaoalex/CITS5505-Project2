document.addEventListener("DOMContentLoaded", function() {
    var toRegister = document.getElementById("to-register");
    var toLogin_1 = document.getElementById("to-login-1");
    var toLogin_2 = document.getElementById("to-login-2");
    var toReset = document.getElementById("to-reset");

    toRegister.onclick = function(){
        document.querySelector("#flipper").classList.toggle("flip");
        document.querySelector("#reset").classList.add("invisible");
    };
    toLogin_1.onclick = function(){
        document.querySelector("#flipper").classList.toggle("flip");
        document.querySelector("#reset").classList.remove("invisible");
    };
    toLogin_2.onclick = function(){
        document.querySelector("#flipper").classList.toggle("flip");
        document.querySelector("#register").classList.remove("invisible");
    };
    toReset.onclick = function(){
        document.querySelector("#flipper").classList.toggle("flip");
        document.querySelector("#register").classList.add("invisible");
    }
});