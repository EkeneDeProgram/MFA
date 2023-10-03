function togglePhoneNumberInput() {
    var phoneInput = document.getElementById('phone_number_input');
    var smsRadio = document.querySelector('input[name="mfa_method"][value="SMS"]');
    if (smsRadio.checked) {
        phoneInput.style.display = 'block';
    } else {
        phoneInput.style.display = 'none';
    }
}