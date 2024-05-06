// Constants
const USERNAME_MIN_LENGTH = 3;
const USERNAME_MAX_LENGTH = 20;
const ALERT_COLOR = '#F7B7A6';
const FORBIDDEN_COLOR = 'red';
const SUCCESS_COLOR = '';

// Variable to keep track of whether specific alert message has been shown
var usernameAlertShown = false;
var usernameExistsAlertShown = false;
var emailExistsAlertShown = false;

// Selectors
const editForm = document.getElementById('editForm');
const userNameInput = document.getElementById('reset-username');
const emailInput = document.getElementById('reset-email');
const aboutMe = document.getElementById('about-me')

// Event listeners
editForm.addEventListener('submit', validateForm);
userNameInput.addEventListener('focus', showUsernameAlert);
userNameInput.addEventListener('input', validateUsername);
userNameInput.addEventListener('blur', checkUsernameAvailability);
userNameInput.addEventListener('keypress', limitNameLength);
emailInput.addEventListener('input', validateEmail);
emailInput.addEventListener('blur', checkEmailAvailability);

// Function to validate the entire form before submission
function validateForm(event) {
  // Validate username
  if (!validateUsername()) {
    alert("Please enter a valid username.");
    event.preventDefault(); 
    return;
  }
  
  // Validate email
  if (!validateEmail()) {
    alert("Please enter a valid email address.");
    event.preventDefault();
    return;
  }

  if(!validateAboutMe()) {
    event.preventDefault(); 
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
  let email = emailInput.value.trim(); // Trim whitespace from input

  let emailIsValid = /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email);
    if (!emailIsValid || email.includes(' ')) {
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

// Function to validate the aboutMe field (allows it to be empty, but cannot exceed 140 characters if not empty)
function validateAboutMe() {
  let aboutMeValue = aboutMe.value.trim();
  
  if (aboutMeValue === '') {
    return true; // Field is empty, so it's valid
  } else if (aboutMeValue.length > 140) {
    alert("About Me cannot exceed 140 characters.");
    return false; // Field exceeds 140 characters, so it's invalid
  }

  return true; // Field is not empty and within character limit, so it's valid
}
