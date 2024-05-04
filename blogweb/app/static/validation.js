// Constants
const USERNAME_MIN_LENGTH = 3;
const USERNAME_MAX_LENGTH = 20;
const PASSWORD_MIN_LENGTH = 6;
const PASSWORD_MAX_LENGTH = 20;
const ALERT_COLOR = '#F7B7A6';
const SUCCESS_COLOR = '';

// Variable to keep track of whether specific alert message has been shown
var usernameAlertShown = false;
var usernameExistsAlertShown = false;
var passwordAlertShown = false;

// Selectors
const registerForm = document.getElementById('register-form');
const userNameInput = document.getElementById('register-user-name');
const emailInput = document.getElementById('email-send');
const passwordInput = document.getElementById('register-password');
const confirmPasswordInput = document.getElementById('confirm-password');

// Event listeners
registerForm.addEventListener('submit', validateForm);
userNameInput.addEventListener('focus', showUsernameAlert);
userNameInput.addEventListener('input', validateUsername);
userNameInput.addEventListener('blur', checkUsernameAvailability);
userNameInput.addEventListener('keypress', limitNameLength);
emailInput.addEventListener('input', validateEmail);
emailInput.addEventListener('blur', checkEmailAvailability);
passwordInput.addEventListener('focus', showPasswordAlert);
passwordInput.addEventListener('input', validatePassword);
passwordInput.addEventListener('keypress', limitPasswordLength);
confirmPasswordInput.addEventListener('blur', validateConfirmPassword);

// Functions
// Function to validate the entire form before submission
function validateForm(event) {
  var inputs = registerForm.getElementsByTagName('input');
  var isValid = true;

  for (var i = 0; i < inputs.length; i++) {
    // Check if the value of the input is empty after trimming whitespace
      if (inputs[i].value.trim() === '') {
        isValid = false;
        break;
      }
  }

  if (!isValid) {
    alert('Please fill in all fields.');
    event.preventDefault();
  }
}

// Function to show an alert message for username input
// Make sure the alert message shows only once
function showUsernameAlert() {
  // Check if the username alert has not been shown yet
  if (!usernameAlertShown) {
    alert("Username can only contain numbers or alphabets, and must be between 3 to 20 characters long.");
    usernameAlertShown = true;
  }
}

// Function to validate username input
function validateUsername() {
  let username = userNameInput.value; // Get the value of the username input field

  // Construct the regular expression dynamically using string concatenation
  let regex = new RegExp(`^[a-zA-Z0-9]{${USERNAME_MIN_LENGTH},${USERNAME_MAX_LENGTH}}$`);

  // Test if the username matches the regular expression
  let usernameIsValid = regex.test(username);

  if (!usernameIsValid) {
    userNameInput.style.backgroundColor = ALERT_COLOR;
    nameAlertShown = false;
  } else {
    userNameInput.style.backgroundColor = SUCCESS_COLOR;
    // Update the variable to indicate that the username alert has been shown
    nameAlertShown = true;
  }
}

// Function to check the availability of a username
function checkUsernameAvailability() {
  let username = userNameInput.value; // Get the value of the username input field

  // Check if the username exists alert has not been shown yet
  if (!usernameExistsAlertShown) {
    // Send an AJAX request to check the availability of the username
    $.ajax({
      url: '/check_availability',
      type: 'POST',
      contentType: 'application/json',
      data: JSON.stringify({username: username}),
      success: function(response) {
        if (!response.available) {
          alert('Username already exists.');
          userNameInput.style.backgroundColor = ALERT_COLOR;
          usernameExistsAlertShown = true; 
        } else {
          userNameInput.style.backgroundColor = SUCCESS_COLOR; 
        }
      }
    });
  }
}

// Function to limit username input length
function limitNameLength(event) {

  let username = userNameInput.value;
  if (username.length >= 20) {
    event.preventDefault(); // Prevent further input if maximum length is reached
    alert("Username cannot exceed 20 characters.")
  }
}

// Function to handle email input validation
function validateEmail() {
  let email = emailInput.value;

  let emailIsValid = /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email);
    if (!emailIsValid) {
      emailInput.style.backgroundColor = ALERT_COLOR;
      return; 
    } else {
      emailInput.style.backgroundColor = SUCCESS_COLOR;
    }
}

// Function to check the availability of the email
function checkEmailAvailability() {
  let email = emailInput.value;

  $.ajax({
    url: '/check_availability',
    type: 'POST',
    contentType: 'application/json',
    data: JSON.stringify({email: email}),
    success: function(response) {
      if (!response.available) {
        alert('Email already exists.');
        emailInput.style.backgroundColor = ALERT_COLOR;
      } else {
        emailInput.style.backgroundColor = SUCCESS_COLOR;
      }
    }
  });
}

// Function to show an alert message for password input
// Make sure the alert message shows only once
function showPasswordAlert() {
  if (!passwordAlertShown) {
    alert("Password must contain at least one number, one alphabet character, and be between 6 to 20 characters long.");
    passwordAlertShown = true;
  }
}

// Function to validate password input
function validatePassword() {
  let password = passwordInput.value; // Get the value of the password input field
  
  // Construct the regular expression dynamically using string concatenation
  let regex = new RegExp(`^(?=.*\\d)(?=.*[a-zA-Z])[0-9a-zA-Z]{${PASSWORD_MIN_LENGTH},${PASSWORD_MAX_LENGTH}}$`);
  
  let passwordIsValid = regex.test(password); // Test if the password matches the regular expression
  
  if (!passwordIsValid) {
    passwordInput.style.backgroundColor = ALERT_COLOR;
  } else {
    passwordInput.style.backgroundColor = SUCCESS_COLOR; 
  }
}

// Function to limit password input length
function limitPasswordLength(event) {
  let password = passwordInput.value; 

  if (password.length >= 20) {
    event.preventDefault();
    alert("Password cannot exceed 20 characters.")
  }
}

// Function to validate the confirmation of password input
function validateConfirmPassword() {
  let password = passwordInput.value;
  let confirmPassword = confirmPasswordInput.value;
  let passwordsMatch = password === confirmPassword; // Check if the password and confirm password match
  if (!passwordsMatch) {
    confirmPasswordInput.style.backgroundColor = ALERT_COLOR;
    alert("Password donot match.")
  } else {
    confirmPasswordInput.style.backgroundColor = SUCCESS_COLOR;
  }
}
