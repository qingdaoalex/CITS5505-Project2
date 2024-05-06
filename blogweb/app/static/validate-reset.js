	// Constants
  const PASSWORD_MIN_LENGTH = 6;
  const PASSWORD_MAX_LENGTH = 20;
  const ALERT_COLOR = '#F7B7A6';
  const SUCCESS_COLOR = '';

  // Variable to keep track of whether specific alert message has been shown
  var passwordAlertShown = false;

  // Selectors
  const resetForm = document.getElementById('reset-form');
  const passwordInput = document.getElementById('reset-password');
  const confirmPasswordInput = document.getElementById('reset-confirm');

  // Event listeners
  resetForm.addEventListener('submit', validateForm);
  passwordInput.addEventListener('focus', showPasswordAlert);
  passwordInput.addEventListener('input', validatePassword);
  passwordInput.addEventListener('keypress', limitPasswordLength);
  confirmPasswordInput.addEventListener('blur', validateConfirmPassword);

  // Functions
  // Function to validate the entire form before submission
  function validateForm(event) {
  
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
