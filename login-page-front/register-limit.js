// Function to validate Name
function validateName() {
    const nameInput = document.getElementById('register-user-name');

    if (nameInput.validity.patternMismatch) {
        alert("Only alphabets, numbers, and underscore '_' are allowed.");
    } else if (nameInput.value.length >= 20) {
        alert("Name must be at most 20 characters long.");
    }
}

// Function to validate password
function validatePassword() {
    const passwordInput = document.getElementById('register-password');

    if (passwordInput.value.length >= 20) {
        alert("Password must be at most 20 characters long.");
    }
}

// Function to validate security answer
function validateAnswer() {
    const answerInput = document.getElementById('validate-question');

    if (answerInput.value.length >= 20) {
        alert("Answer must be at most 20 characters long.");
    }
}

// Event listeners for input fields
document.getElementById('register-user-name').addEventListener('input', validateName);
document.getElementById('register-password').addEventListener('input', validatePassword);
document.getElementById('validate-question').addEventListener('input', validateAnswer);
