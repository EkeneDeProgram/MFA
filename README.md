# Multifactor Authentication System (MFA)
### Video Demo:

### Description: 
This repository contains the source code and documentation for a multifactor authentication system designed to enhance the security of your applications and systems. Multifactor authentication (MFA) adds an additional layer of protection to your accounts by requiring users to provide multiple forms of verification.

### Tech Stack:
- Python 
- Django
- SQLite
- HTML
- CSS
- JavaScript

### Features:
- **Multiple Authentication Factors**: Our MFA system supports a variety of authentication factors, including:
    - Something you know (e.g., password)
    - Something you have (e.g., one-time password from a mobile app)
- **User-Friendly**: The MFA process is designed to be user-friendly, with step-by-step instructions for setting up and using MFA.

### Getting Started
#### Prerequisites
Before you get started, make sure you have the following:
- Python 3.x 
- A compatible database (e.g., SQLite3, MySQL, PostgreSQL)

#### Installation
1. Clone the repository to your local machine:
    <pre>
    git clone https://github.com/EkeneDeProgram/MFA.git
    </pre>

2. Set up a virtual environment (recommended):
    <pre>
    python3 -m venv env
    source env/bin/activate
    </pre>

3. Install dependencies:
    <pre>
    pip install -r requirements.txt
    <pre>

4. Configure the application settings by modifying settings.py. Make sure to set database credentials and other relevant configurations.

5. Initialize the database:
    <pre>
    python manage.py makemigrations
    python manage.py migrate
    <pre>

6. Run the application:
    <pre>
    python manage.py runserver
    <pre>

### Usage
1. Access the MFA system via the provided URL.
2. Register your account and configure MFA settings.
3. Log in with MFA.
4. Enjoy enhanced security for your account.

### Security Considerations
It's important to consider and implement security best practices when using the MFA system. Please refer to our Security Guidelines for information on how to secure your system and protect user data.




