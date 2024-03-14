container = document.querySelector(".container"),
pwShowHide = document.querySelectorAll(".showHidePw"),
pwFields = document.querySelectorAll(".password"),
signUp = document.querySelector(".signup-link"),
login = document.querySelector(".login-link"),
termsCheckbox = document.getElementById("termCon"),
termsLink = document.querySelector(".terms-link"),
termsPopup = document.getElementById("termsPopup"),
forms = document.querySelectorAll('form');

pwShowHide.forEach(eyeIcon => {
    eyeIcon.addEventListener("click", () => {
        pwFields.forEach(pwField => {
            if (pwField.type === "password") {
                pwField.type = "text";

                pwShowHide.forEach(icon => {
                    icon.classList.replace("uil-eye-slash", "uil-eye");
                })
            } else {
                pwField.type = "password";

                pwShowHide.forEach(icon => {
                    icon.classList.replace("uil-eye", "uil-eye-slash");
                })
            }
        })
    })
});

// Add an event listener to form submissions
forms.forEach(form => {
    form.addEventListener('submit', (event) => {
        if (form.contains(termsCheckbox) && !termsCheckbox.checked) {
            event.preventDefault();
            alert('Please accept the terms and conditions.');
        } else if (form.id === "registerForm" && !validatePasswords()) {
            event.preventDefault();
        }
    });
});

signUp.addEventListener("click", () => {
    container.classList.add("active");
});

login.addEventListener("click", () => {
    container.classList.remove("active");
});

function validatePasswords() {
    var password = document.getElementById("password").value;
    var confirmPassword = document.getElementById("confirm_password").value;
    var passwordMatchMsg = document.getElementById("passwordMatchMsg");

    if (password !== confirmPassword) {
        passwordMatchMsg.innerHTML = "*Passwords don't match";
        return false;
    } else {
        passwordMatchMsg.innerHTML = "";
        return true;
    }
}
