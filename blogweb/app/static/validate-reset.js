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
    var isValid = true;
  
    // Validate password
    if (!validatePassword()) {
      isValid = false;
    }
    // Validate confirm password
    if (!validateConfirmPassword()) {
      isValid = false;
    }
  
    // Check if all fields are valid before allowing form submission
    if (passwordInput.style.backgroundColor === ALERT_COLOR || passwordInput.value.trim() === '' ||
        confirmPasswordInput.style.backgroundColor === ALERT_COLOR || confirmPasswordInput.value.trim() === '') {
      isValid = false;
    }
  
    if (!isValid) {
      alert('Please fill in all fields and correct the errors.');
      event.preventDefault(); // Prevent form submission
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
  let password = passwordInput.value; // Get the value of the password input field
  
  // Construct the regular expression dynamically using string concatenation
  let regex = new RegExp(`^(?=.*\\d)(?=.*[a-zA-Z])[a-zA-Z0-9]{${PASSWORD_MIN_LENGTH},${PASSWORD_MAX_LENGTH}}$`);
  
  let passwordIsValid = regex.test(password); // Test if the password matches the regular expression
  
  if (password.length < PASSWORD_MIN_LENGTH || password.length > PASSWORD_MAX_LENGTH || !passwordIsValid) {
    passwordInput.style.backgroundColor = ALERT_COLOR;
    passwordIsValid = false; // Set the flag to false if the password doesn't meet the criteria
  } else {
    passwordInput.style.backgroundColor = SUCCESS_COLOR; 
  }

  return passwordIsValid; // Return the flag indicating password validity
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
