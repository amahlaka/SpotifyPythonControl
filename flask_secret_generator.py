import random
import string
def generate_activation_token():
    secret = ''.join(random.SystemRandom().choice(string.ascii_letters + string.digits) for _ in range(64))
    print(secret)
generate_activation_token()