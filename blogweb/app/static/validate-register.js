// Constants
const USERNAME_MIN_LENGTH = 3;
const USERNAME_MAX_LENGTH = 20;
const PASSWORD_MIN_LENGTH = 6;
const PASSWORD_MAX_LENGTH = 20;
const ALERT_COLOR = '#F7B7A6';
const FORBIDDEN_COLOR = 'red';
const SUCCESS_COLOR = '';

// Variable to keep track of whether specific alert message has been shown
var usernameAlertShown = false;
var usernameExistsAlertShown = false;
var emailExistsAlertShown = false;
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
confirmPasswordInput.addEventListener('input', validateConfirmPassword);

// Functions
// Function to validate the entire form before submission
function validateForm(event) {
  // Validate username
  if (!validateUsername()) {
    alert("Please enter a valid username.");
    event.preventDefault(); // Prevent form submission
    return;
  }
  
  // Validate email
  if (!validateEmail()) {
    alert("Please enter a valid email address.");
    event.preventDefault(); // Prevent form submission
    return;
  }

  // Validate password
  if (!validatePassword()) {
    alert("Please enter a valid password.");
    event.preventDefault(); // Prevent form submission
    return;
  }

  // Validate confirm password
  if (!validateConfirmPassword()) {
    alert("Passwords do not match.");
    event.preventDefault(); // Prevent form submission
    return;
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
  let username = userNameInput.value.trim();
  let regex = new RegExp(`^[a-zA-Z0-9]{${USERNAME_MIN_LENGTH},${USERNAME_MAX_LENGTH}}$`);
  let usernameIsValid = regex.test(username);

  if (!usernameIsValid) {
    userNameInput.style.backgroundColor = ALERT_COLOR;
    usernameAlertShown = false;
    return false;
  } else {
    userNameInput.style.backgroundColor = SUCCESS_COLOR;
    usernameAlertShown = true;
    return true;
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
        if (!response.username_available) {
          if (!response.current_username_available) {
            alert('Username already exists.');
            userNameInput.style.backgroundColor = FORBIDDEN_COLOR;
            usernameExistsAlertShown = true; 
          }
        } else {
          usernameExistsAlertShown = false;
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
  let email = emailInput.value.trim();
  let emailIsValid = /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email);

  if (!emailIsValid) {
    emailInput.style.backgroundColor = ALERT_COLOR;
    return false;
  } else {
    emailInput.style.backgroundColor = SUCCESS_COLOR;
    return true;
  }
}

// Function to check the availability of the email
function checkEmailAvailability() {
  let email = emailInput.value;

  if (!emailExistsAlertShown) {
    $.ajax({
      url: '/check_availability',
      type: 'POST',
      contentType: 'application/json',
      data: JSON.stringify({email: email}),
      success: function(response) {
        if (!response.email_available) {
          if (!response.current_email_available) {
            alert('Email already exists.');
            emailInput.style.backgroundColor = FORBIDDEN_COLOR;
            emailExistsAlertShown = true; 
          }
        } else {
          emailExistsAlertShown = false;
        }
      } 
    });
  }
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
  let password = passwordInput.value.trim();
  let regex = new RegExp(`^(?=.*\\d)(?=.*[a-zA-Z])[a-zA-Z0-9]{${PASSWORD_MIN_LENGTH},${PASSWORD_MAX_LENGTH}}$`);
  let passwordIsValid = regex.test(password);

  if (!passwordIsValid) {
    passwordInput.style.backgroundColor = ALERT_COLOR;
    return false;
  } else {
    passwordInput.style.backgroundColor = SUCCESS_COLOR;
    return true;
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
  let password = passwordInput.value.trim();
  let confirmPassword = confirmPasswordInput.value.trim();
  let passwordsMatch = password === confirmPassword;

  if (!passwordsMatch) {
    confirmPasswordInput.style.backgroundColor = ALERT_COLOR;
    return false;
  } else {
    confirmPasswordInput.style.backgroundColor = SUCCESS_COLOR;
    return true;
  }
}
