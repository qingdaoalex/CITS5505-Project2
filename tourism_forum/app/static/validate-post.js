// Constants
const CONTENT_MIN_LENGTH = 1;
const CONTENT_MAX_LENGTH= 200;

const postForm = document.getElementById('postForm');

// Selectors
const postContent = document.getElementById('post-contnet');

// Event listeners
postForm.addEventListener('submit', validateForm);


// Function to validate the post before submission
function validateForm(event) {
  if(!validatePostContent()) {
    event.preventDefault(); 
    return;
  }
}


// Function to validate the aboutMe field (allows it to be empty, but cannot exceed 140 characters if not empty)
function validatePostContent() {
  let postContentData = postContent.value.trim();
  
  if (postContentData == '') {
    alert("Question content is empty.");
    return false; // Field is empty, so it's valid
  } else if (postContentData.length > CONTENT_MAX_LENGTH) {
    alert("Question content cannot exceed 200 characters.");
    return false;
  }

  return true; 
}
