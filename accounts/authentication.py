
import requests
from django.contrib.auth import get_user_model
User = get_user_model()

import logging

PERSONA_VERIFY_URL = 'https://verifier.login.persona.org/verify'
DOMAIN = 'localhost'

class PersonaAuthenticationBackend(object):

    def authenticate(self, assertion):

        logging.warning('entering authenticate function')

        response = requests.post(
            PERSONA_VERIFY_URL,
            data={'assertion': assertion, 'audience': DOMAIN}
        )

        logging.warning('got response from persona')
        logging.warning(response.content.decode())

        if response.ok and response.json()['status'] == 'okay':
            email=response.json()['email']
            try:
                return User.objects.get(email=email)
            except User.DoesNotExist:
                return User.objects.create(email=email)

    def get_user(self,email):
        try:
            return User.objects.get(email=email)
        except User.DoesNotExist:
            return None