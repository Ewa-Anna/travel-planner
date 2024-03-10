import random
import string

from django_rest_passwordreset.models import ResetPasswordToken


class CustomTokenGenerator:

    def __init__(self, token_length=30):
        self.token_length = token_length

    def generate_token(self):
        characters = string.ascii_letters + string.digits

        token = "".join(random.choice(characters) for _ in range(self.token_length))

        return token


def get_user_from_token(token_key):
    try:
        token = ResetPasswordToken.objects.get(key=token_key)
        return token.user
    except ResetPasswordToken.DoesNotExist:
        return None
