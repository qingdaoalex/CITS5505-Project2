document.addEventListener("DOMContentLoaded", function() {
  var interactionContainer = document.querySelector(".interaction-container");
  var dialogContainer = document.getElementById("dialog");
  var map = document.getElementById("map"); 

  var dialogs = [
      "Would you like to explore with a map? <a href='#' class='response' data-choice='yes'>Yes</a> / <a href='#' class='response' data-choice='no'>No</a>",
      "Great! Let's start."
  ];
  var currentDialogIndex = 0;

  // Function to update the dialog
  function updateDialog() {
      if (currentDialogIndex < dialogs.length) {
          dialogContainer.innerHTML = "<p>" + dialogs[currentDialogIndex] + "</p>";
          currentDialogIndex++;
      } else {
          interactionContainer.style.display = "none"; // Hide interaction container if no more dialogs
      }
  }

  // Function to hide the live2d-widget
  function hideLive2DWidget() {
      var live2d = document.getElementById("live2d-widget");
      if (live2d) {
          live2d.style.visibility = "hidden"; // Hide live2d-widget
      }
  }

  // Add click event listener to the dialog container
  dialogContainer.addEventListener("click", function(e) {
      var target = e.target;
      if (target.classList.contains("response")) {
          var choice = target.getAttribute("data-choice");
          if (choice === "yes") {
              updateDialog(); // Display next dialog for "Yes" choice
              map.style.visibility = "visible"; // Show the map
          } else if (choice === "no") {
              dialogContainer.innerHTML = "<p>Bye~</p>"; // Display "bye~" message
              setTimeout(function() {
                  interactionContainer.style.display = "none"; // Hide interaction container for "No" choice after delay
                  hideLive2DWidget(); // Hide live2d-widget for "No" choice
              }, 1000); // Delay before hiding interaction container and live2d-widget (1 second)
          }
      }
  });

  // Initial dialog display
  updateDialog();
});
