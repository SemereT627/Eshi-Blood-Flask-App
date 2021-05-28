from werkzeug.security import safe_str_cmp
from eshiBlood.models.models import UserCredential

def authenticate(email, password):
    user = UserCredential.find_by_email(email)
    if user and safe_str_cmp(user.Password, password):
        return user


def identity(payload):
    user_id = payload['identity']
    return UserCredential.find_by_id(user_id)
