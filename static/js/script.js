function validateForm() { /* pas nécéssaire pour le moment*/
    let isValid = true;

    const username = document.getElementById("username").value.trim();
    const password = document.getElementById("password").value.trim();
    const usernameError = document.getElementById("username-error");
    const passwordError = document.getElementById("password-error");

    usernameError.textContent = "";
    passwordError.textContent = "";

    if (!username) {
        usernameError.textContent = "Pseudo ne peut pas être vide";
        isValid = false;
    }

    if (!password) {
        passwordError.textContent = "Mot de passe ne peut pas être vide";
        isValid = false;
    }

    return isValid;
}