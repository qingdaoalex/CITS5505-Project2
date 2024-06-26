
$(document).ready(function() {
  // Function to read and display the selected image before uploading
  function readURL(input) {
    if (input.files && input.files[0]) {
      var reader = new FileReader();
      reader.onload = function(e) {
        $('#user-avatar').attr('src', e.target.result);
      }
      reader.readAsDataURL(input.files[0]);
    }
  }

  // Function to handle changes in the image upload input
  $("#image-upload").change(function() {
    var file = this.files[0];
    var maxSize = 500 * 1024; // 500 KB

    if (file.size > maxSize) {
      alert('File size exceeds the limit of 500 KB.');
      this.value = ''; // Clear the input
      return;
    }

    readURL(this);
  });

  // Prevent the default form submission
  $('#avatar-form').submit(function(event) {
    event.preventDefault();
  });

  // Function to handle clicking on the image button
  $("#image-button").click(function() {
      var formData = new FormData($('#avatar-form')[0]); // Collect form data
      // AJAX request to upload the avatar
      $.ajax({
        type: 'POST',
        url: '/upload_avatar',
        data: formData,
        contentType: false,
        processData: false,
        success: function(response) {
          // Check if the response contains a redirect URL
          if (response.redirect_url) {
            // Redirect to the specified URL
            window.location.href = response.redirect_url;
          } else {
            alert('Avatar uploaded successfully!');
            location.reload();
          }
        },
        error: function(_, _, error) {
          // Alert if there's an error during upload
          alert('Error uploading avatar: ' + error);
        }
      });
    });
  });

// Function to handle clicking on the default button
$("#image-default").click(function() {
  // AJAX request to set avatar path to NULL
  $.ajax({
    type: 'POST',
    url: '/set_default_avatar', // Route to handle setting default avatar
    success: function(response) {
      // Check if the response contains a redirect URL
      if (response.redirect_url) {
        // Redirect to the specified URL
        window.location.href = response.redirect_url;
      } else {
        // For example, you might display a success message
        alert('Default avatar set successfully!');
        location.reload();
      }
    },
    error: function(_, _, error) {
      // Alert if there's an error during the request
      alert('Error setting default avatar: ' + error);
    }
  });
});
