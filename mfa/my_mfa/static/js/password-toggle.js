document.addEventListener('DOMContentLoaded', function () {
    const passwordFields = document.querySelectorAll('.password-field');
    const showPasswordCheckbox = document.querySelector('.show-password-checkbox');

    showPasswordCheckbox.addEventListener('change', function () {
        if (showPasswordCheckbox.checked) {
            passwordFields.forEach(function (field) {
                field.type = 'text'; // Show the password
            });
        } else {
            passwordFields.forEach(function (field) {
                field.type = 'password'; // Hide the password
            });
        }
    });

});