# Import Django modules
from django.contrib.auth import login, authenticate
from django.shortcuts import render, redirect, HttpResponse
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ObjectDoesNotExist
from django.contrib import messages
from django.core.files.base import ContentFile

# Import third party modules
from PIL import Image as PilImage
import pyotp
import qrcode
import io
import vonage
from dotenv import load_dotenv

# Import python standard module
import os

# Import my_mfa modules
from .forms import RegistrationForm
from .models import UserProfile 
from .utils import *  


load_dotenv() # Load the .env file

# # Access the API keys and secrets
# api_key = os.environ.get("API_KEY")
# api_secret = os.environ.get("API_SECRET")

# Create your views here.

# Registration view function
def register_user(request):
    if request.method == "POST":
        form = RegistrationForm(request.POST) # creates an instance of a RegistrationForm
        if form.is_valid():
            user = form.save()
            login(request, user) # Automatically log the user in after registration
            return redirect("mfa") # Redirect to the mfa url
    else:
        form = RegistrationForm()  # IF request is not POST create an instance of the RegistrationForm without any data.
    return render(request, "registration/register.html", {"form": form})


# Defind a view for enabeling MFA
@login_required # Use the login_required decorator to ensure only authenticated users can access this view
def enable_mfa(request):
    try:
        # Retrieve user UserProfile details and if none is found, creates a new one.
        user_profile, created = UserProfile.objects.get_or_create(user=request.user)
        if request.method == "POST":
            # Enable MFA for the user
            user_profile.mfa_enabled = True
            user_profile.save()
            return redirect("mfa-method") # Redirect to the mfa-method url
        # Render the MFA enable form
        return render(request, "registration/enable_mfa.html", {"user_profile": user_profile, "created": created})
    except UserProfile.DoesNotExist:
        # Handle the case where UserProfile does not exist for the user
        return render(request, "registration/user_profile_not_found.html")


# Defind view for setting MFA method
@login_required
def set_mfa_method(request):
    # Retrieve user UserProfile details
    user_profile = UserProfile.objects.get(user=request.user)

    if request.method == "POST":
        # Get the value of the "mfa_method" field from the POST data.
        set_method = request.POST.get("mfa_method")
        # Update the user's MFA method in the UserProfile.
        user_profile.mfa_method = set_method
        user_profile.save()
        return render(request, "registration/mfa_success.html")
    return render(request, "registration/set_mfa_method.html", {"user_profile": user_profile})


# Defind a view for user authentication
def user_authentication(request):
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]

        # Authenticate the user using their username and password
        user = authenticate(request, username=username, password=password)

        if user is not None: # If authentication is succesfull
            user_profile = UserProfile.objects.get(user=user)
            if user_profile.mfa_enabled: # Check if mfa is enable for user
                if user_profile.mfa_method == "TOTP":
                    if not user_profile.totp_secret_key: # If the UserProfile secret_key field is empty
                        return redirect("totp-qr-code") # Redirect to totp-qr-code url
                    else:
                        return redirect("verify-totp") # Redirect to verify-totp url
                elif user_profile.mfa_method == "SMS":
                    if not user_profile.phone_number: # If the UserProfile phone_number field is empty
                        return redirect("send-totp-sms")
                    else:
                        pass
                else:
                    messages.error(request, 'Invalid MFA method.')
                    return HttpResponse("I dont know yet")
            else:
                # MFA is not enabled, log the user in
                login(request, user)
                return HttpResponse("WELCOME TO 909INE")
        else:
            # Authentication failed, show an error message
            messages.error(request, 'Invalid username or password.')
    return render(request, "authentication/login.html") 


# Defind a view to generate totp_qr_code
@login_required
def generate_totp_qr_code(request):
    # Generate secret key in base32 format
    secret_key = pyotp.random_base32()
    # Specify the time step (in seconds)
    time_step = 30
    
    # Retrieve user UserProfile details
    user_profile = UserProfile.objects.get(user=request.user)
    username = user_profile.user.username # Get user name from django in-built User models

    # Update UserProfile details
    user_profile.totp_secret_key = secret_key
    user_profile.save()
   
    # Create a TOTP object with the specified time step
    totp = pyotp.TOTP(user_profile.totp_secret_key, interval=time_step)
    # Generate the current TOTP value
    totp_value = totp.now()
    # Create a TOTP provisioning URL
    totp_url = totp.provisioning_uri(username, issuer_name="909ine MFA System")
    # Generate a QR code for the TOTP URL
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
        #image_factory=PilImage,
    )
    qr.add_data(totp_url)
    qr.make(fit=True)
    qr_code_image = qr.make_image(fill_color="black", back_color="white")

    # Convert the QR code image to a specific format (e.g., PNG) using Pillow
    image_io = io.BytesIO()
    qr_code_image.save(image_io, format="PNG")
    image_io.seek(0)

    # Save the QR code image to the model
    user_profile.name = "QR Code"
    #user_profile.image.save("qr_code.png", qr_code_image)
    user_profile.image.save("qr_code.png", ContentFile(image_io.read()))

    qr_code = user_profile.image.url
    
    # Pass the TOTP URL, QR code image, secret key, and TOTP value to the template
    context = {
        "totp_url": totp_url,
        "qr_code": qr_code,
        "totp_value": totp_value,
        "username": username,
    }

    return render(request, "authentication/generate_totp.html",context)



# Defind view to verify totp
@login_required
def verify_totp(request):
    if request.method == "POST":
        # Get the TOTP code entered by the user
        user_input_totp = request.POST.get("totp_code")

        # Get user's profile
        user_profile = UserProfile.objects.get(user=request.user)

        if user_profile.mfa_method == "TOTP":
            if not user_profile.totp_secret_key:
                messages.error(request, f"No TOTP secret key found for this user: {user_profile.user.username}")
            # Verify the TOTP code
            totp = pyotp.TOTP(user_profile.totp_secret_key)
            generated_totp_code = totp.now()  # Generate the TOTP code for comparison
            if totp.verify(user_input_totp):
                messages.success(request, "TOTP code is valid.")
            else:
                messages.error(request, "Invalid TOTP code.") 
        else:
            messages.error(request, 'MFA method is not TOTP.')
    return render(request, "authentication/verify_totp.html")


# Defind view to send totp code via SMS
@login_required 
def send_totp_sms(request):
    user_profile = UserProfile.objects.get(user=request.user)
    if request.method == "POST":
        # Retrieve the phone_number submitted in the form data
        user_phone_number = request.POST.get("phone_number")
        # Update UserProfile model
        user_profile.phone_number = user_phone_number
        user_profile.save()
        # Generate a Time-Based One-Time Password (TOTP) code.
        totp_code = generate_totp_code()
        # Initialize the Vonage API client with API key and API secret
        api_key = os.environ.get("API_KEY") # Access the API keys and secrets
        api_secret = os.environ.get("API_SECRET")
        client = vonage.Client(key=api_key, secret=api_secret)
        sms = vonage.Sms(client)

        # Send the TOTP code via SMS
        try:
            sms_response = sms.send_message({
                "from": "909ine MFA System",
                "to": user_profile.phone_number,
                "text": f"Your TOTP code: {totp_code} Valid for 1 minute"
            })

            if sms_response["messages"][0]["status"] == "0":
                messages.success(request, "TOTP code sent via SMS. Check your phone for the code.")
                print(f"{user_profile.phone_number}")
            else:
                messages.error(request, f"Error: {sms_response['messages'][0]['error-text']}")
        except Exception as e:
            return HttpResponse(f'Error: {str(e)}')
        
        #return HttpResponse("TOTP code sent successfully.")
    return render(request, "authentication/send_totp_sms.html")


# Define a view for updating user MFA status
@login_required 
def update_mfa_status(request):
    user_profile = UserProfile.objects.get(user=request.user)
    if request.method == "POST":
        try:
            user_profile.mfa_enabled = not user_profile.mfa_enabled # Toggle the MFA status
            user_profile.save()
            return HttpResponse("Successfull")
        except UserProfile.DoesNotExist:
            return render(request, "registration/user_profile_not_found.html") 
    return render(request, "registration/update_mfa_status.html", {"user_profile": user_profile})

