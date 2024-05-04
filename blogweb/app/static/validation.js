// Function to prevent form submission
document.getElementById('register-form').addEventListener('submit', function(event) {
  event.preventDefault(); // Prevent the form from submitting
});

// Function to handle input validation and alert for username
var userNameInput = document.getElementById('register-user-name');
var alertShownUserName = false;

userNameInput.addEventListener('focus', function() {
  if (!alertShownUserName) {
      showAlert(userNameInput, "Username can only contain numbers or alphabets, and must be between 3 to 20 characters long.");
      alertShownUserName = true;
  }
});

userNameInput.addEventListener('input', function() {
  var username = this.value;

  if (username.length > 20) {
      this.value = username.slice(0, 20); // Truncate input if it exceeds 20 characters
  }

  var usernameIsValid = /^[a-zA-Z0-9]{3,20}$/.test(username);
  if (usernameIsValid && alertShownUserName) {
      resetInput(userNameInput);
      alertShownUserName = false;
  }
});

// Function to handle input validation and alert for password
var passwordInput = document.getElementById('register-password');
var alertShownPassword = false;

passwordInput.addEventListener('focus', function() {
  if (!alertShownPassword) {
      showAlert(passwordInput, "Password must contain at least one number, one alphabet character, and be between 6 to 20 characters long.");
      alertShownPassword = true;
  }
});

passwordInput.addEventListener('input', function() {
  var password = this.value;

  if (password.length > 20) {
      this.value = password.slice(0, 20); // Truncate input if it exceeds 20 characters
  }

  var passwordIsValid = /^(?=.*\d)(?=.*[a-zA-Z])[0-9a-zA-Z]{6,20}$/.test(password);
  if (passwordIsValid && alertShownPassword) {
      resetInput(passwordInput);
      alertShownPassword = false;
  }
});

// Function to handle input length limit
var inputs = [userNameInput, passwordInput];
inputs.forEach(function(input) {
  input.addEventListener('keypress', function(event) {
      if (this.value.length >= 20) {
          event.preventDefault(); // Prevent further input if maximum length is reached
      }
  });
});

// Function to handle confirmation password validation
document.getElementById('confirm-password').addEventListener('input', function() {
  var confirmPassword = this.value;
  var password = passwordInput.value;
  var passwordsMatch = password === confirmPassword;
  if (!passwordsMatch) {
      this.style.backgroundColor = '#F7B7A6';
  } else {
      this.style.backgroundColor = '';
  }
});

// Function to show alert and set background color
function showAlert(element, message) {
  element.style.backgroundColor = '#F7B7A6';
  alert(message);
}

// Function to reset input background color
function resetInput(element) {
  element.style.backgroundColor = '';
}
