const togglePassword = document.getElementById('togglePassword');
const password = document.getElementById('password');

function togglePasswordVisibility() {
    if (password.type === 'password') {
        password.type = 'text';
        togglePassword.src = '/static/images/close-eye.svg';
    } else {
        password.type = 'password';
        togglePassword.src = '/static/images/open-eye.svg';
    }
}

function submitResponse() {
    grecaptcha.ready(function () {
      grecaptcha
        .execute("6LfTQOgnAAAAAPUKwxk5C_ZQNIi__k7HGTzbi3Yw", { action: "submit" })
        .then(function (token) {
          const alertText = document.getElementById("alert-text");
  
          var email = document.getElementById("email").value;
          var password = document.getElementById("password").value;
  
          if (email == "" || password == "") {
            alertText.classList.add("error-text");
            alertText.innerHTML = "Email adress or password is missing";
            return;
          }
  
          if (!email.includes("@") || !email.includes(".")) {
            alertText.classList.add("error-text");
            alertText.innerHTML = "Email adress is not valid";
            return;
          }
  
  
          if (password.length < 8) {
            alertText.classList.add("error-text");
            alertText.innerHTML = "Password must be at least 8 characters long";
            return;
          }
  
          var data = {
            email: email,
            password: password,
            recaptcha_token: token,
          };
  
          const submitButton = document.getElementById("submit-button");
          const submitButtonText = submitButton.innerHTML;
  
          submitButton.innerHTML = "Loading...";
          submitButton.disabled = true;
  
          fetch('/auth/api/v2/sign-in', {
            method: "POST",
            headers: {
              "Content-Type": "application/json",
            },
            body: JSON.stringify(data),
          })
            .then(function (response) {
              if (response.status == 500) {
                alertText.classList.add("error-text");
                alertText.innerHTML = "Our services are currently facing some issues, please try again later";
                return;
              }
              return response.json();
            }).then(function (data) {
              if (data.status == 'error') {
                alertText.classList.add("error-text");
                alertText.innerHTML = data.message;
                return;
              }
              if (data.status == 'success') {
                alertText.classList.add("success-text");
                alertText.innerHTML = data.message;
                window.location.href = data.redirect + "/dashboard";
              }
            })
            .catch(function (error) {;
              alertText.classList.add("error-text");
              alertText.innerHTML = "An unexpected error occured, please try again later";
            })
            .finally(function () {
              submitButton.innerHTML = submitButtonText;
              submitButton.disabled = false;
            });
        });
    });
  }
  