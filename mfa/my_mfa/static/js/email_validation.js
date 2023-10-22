$(document).ready(function() {
    $('#id_email').on('input', function() {
        var email = $(this).val();
        $.ajax({
            url: '{% url "check_email_availability" %}',
            data: {
                'email': email
            },
            dataType: 'json',
            success: function(data) {
                if (data.is_taken) {
                    $('#email-error').text('This email address is already registered.');
                } else {
                    $('#email-error').text('');
                }
            }
        });
    });
});





