document.addEventListener("DOMContentLoaded", function() {
    var flipButtons = document.getElementsByClassName("flipbutton");

    for (var i = 0; i < flipButtons.length; i++) {
        flipButtons[i].onclick = function(){
            var flipper = document.querySelector("#flipper");
            flipper.classList.toggle("flip");
            waitForTransitionAndNavigate(this.href);
            return false; // Prevent default anchor behavior
        };
    }

    function waitForTransitionAndNavigate(url) {
        var flipper = document.querySelector("#flipper");
        // Listen for the 'transitionend' event
        flipper.addEventListener('transitionend', function() {
            // Once the transition ends, navigate to the specified URL
            window.location.href = url;
        }, { once: true }); // Use { once: true } to ensure the event listener is triggered only once
    }
});
