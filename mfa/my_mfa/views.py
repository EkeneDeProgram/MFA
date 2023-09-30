from django.contrib.auth import login
from django.shortcuts import render, redirect, HttpResponse
from .forms import RegistrationForm

# Create your views here.

# Registration view function
def register_user(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            # Check if passwords match
            # password = form.cleaned_data['password']
            # confirm_password = form.cleaned_data['confirm_password']
            # if password == confirm_password:
                user = form.save()
                return HttpResponse('home')
            # else:
            #      form.add_error('confirm_password', 'Passwords do not match.')
    else:
        form = RegistrationForm()  
    return render(request, 'registration/register.html', {'form': form})


def user_authentication(request):
    pass


def mfa_status(request):
    pass


def mfa_verification(request):
    pass