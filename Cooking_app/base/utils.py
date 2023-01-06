import random
import string


from django.core.mail import send_mail

def generate_verification_code():
    # generate a random string of length 6
    code = ''.join(random.choices(string.ascii_letters + string.digits, k=6))
    return code

def send_verification_code(to_email, code):
    subject = 'COOKERY BOOK - Verification code'
    message = f'Your verification code is: {code}'
    try:
        send_mail(
            subject=subject,
            message=message,
            from_email=None,
            recipient_list=[to_email],
        )
    except Exception as e:
        return str(e)