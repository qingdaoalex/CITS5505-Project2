// Constants
const USERNAME_MIN_LENGTH = 3;
const USERNAME_MAX_LENGTH = 20;
const PASSWORD_MIN_LENGTH = 6;
const PASSWORD_MAX_LENGTH = 20;
const ALERT_COLOR = '#F7B7A6';
const SUCCESS_COLOR = '';

// Selectors
const editForm = document.getElementById('editForm');
const userNameInput = document.getElementById('reset-username');
const emailInput = document.getElementById('reset-email');

// Event listeners
editForm.addEventListener('submit', validateForm);
userNameInput.addEventListener('input', validateUsername);
userNameInput.addEventListener('keypress', limitNameLength);
emailInput.addEventListener('input', validateEmail);

function validateForm(event) {
  var isValid = true;

  // Validate username
  if (!validateUsername()) {
    isValid = false;
  }
  // Validate email
  if (!validateEmail()) {
    isValid = false;
  }

  // Check if all fields are valid before allowing form submission
  if (userNameInput.style.backgroundColor === ALERT_COLOR || userNameInput.value.trim() === '' ||
      emailInput.style.backgroundColor === ALERT_COLOR || emailInput.value.trim() === '') {
    isValid = false;
  }

  if (!isValid) {
    alert('Please correct the errors.');
    event.preventDefault(); // Prevent form submission
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
  } else {
    userNameInput.style.backgroundColor = SUCCESS_COLOR;
  }
}

// Function to limit username input length
function limitNameLength(event) {
  let username = userNameInput.value;
  if (username.length >= 20) {
    event.preventDefault(); // Prevent further input if maximum length is reached
  }
}

// Function to handle email input validation
function validateEmail() {
  let email = emailInput.value.trim(); // Trim whitespace from input

  let emailIsValid = /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email);
    if (!emailIsValid || email.includes(' ')) {
      emailInput.style.backgroundColor = ALERT_COLOR;
    } else {
      emailInput.style.backgroundColor = SUCCESS_COLOR;
    }
}
