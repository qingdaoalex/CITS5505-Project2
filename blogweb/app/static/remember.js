const rmCheck = document.getElementById("login-check");
const nameInput = document.getElementById("login-user-name");

// Check if there's a saved username in local storage
if (localStorage.username && localStorage.checkbox === "checked") {
    rmCheck.checked = true;
    nameInput.value = localStorage.username;
} else {
    rmCheck.checked = false;
    nameInput.value = "";
}

// Function to update local storage when checkbox state changes
function lsRememberMe() {
    if (rmCheck.checked && nameInput.value !== "") {
        localStorage.username = nameInput.value;
        localStorage.checkbox = "checked"; // Store the checked status
    } else {
        localStorage.username = "";
        localStorage.checkbox = ""; // Clear the checkbox status
    }
}
// Call lsRememberMe function when checkbox state changes
rmCheck.addEventListener("change", lsRememberMe);