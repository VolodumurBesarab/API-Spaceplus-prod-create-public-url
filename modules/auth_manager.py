import json
from msal import ConfidentialClientApplication

class AuthManager:
    def __init__(self):
        with open("secrets.json") as secrets:
            secrets = json.load(secrets)

        self.application_id = secrets.get("VLAD_APPLICATION_ID")
        self.client_secret = secrets.get("VLAD_CLIENT_SECRET")
        self.authority_url = secrets.get("authority_url")
        self.default_scope = ['https://graph.microsoft.com/.default']
        self.base_url = "https://graph.microsoft.com/v1.0/"
        self.endpoint = self.base_url + "users/andrzej.besarab@spacelpus.onmicrosoft.com/"
        self.client = ConfidentialClientApplication(
            client_id=self.application_id,
            client_credential=self.client_secret,
            authority=self.authority_url
        )

    def get_endpoint(self) -> str:
        return self.endpoint

    def base_url(self) -> str:
        return self.base_url

    def get_access_token_default_scopes(self) -> str:
        access_token = None
        token_result = self.client.acquire_token_silent(self.default_scope, account=None)
        # If the token is available in cache, save it to a variable
        if token_result:
            access_token = 'Bearer ' + token_result['access_token']
            print('Access token was loaded from cache')

        # If the token is not available in cache, acquire a new one from Azure AD and save it to a variable
        if not token_result:
            token_result = self.client.acquire_token_for_client(scopes=self.default_scope)
            access_token = 'Bearer ' + token_result['access_token']
            print('New access token was acquired from Azure AD')
        return access_token

    def get_access_token(self, scopes) -> str:
        access_token = None
        token_result = self.client.acquire_token_silent(scopes, account=None)

        # If the token is available in cache, save it to a variable
        if token_result:
            access_token = 'Bearer ' + token_result['access_token']
            print('Access token was loaded from cache')

        # If the token is not available in cache, acquire a new one from Azure AD and save it to a variable
        if not token_result:
            token_result = self.client.acquire_token_for_client(scopes=scopes)
            access_token = 'Bearer ' + token_result['access_token']
            print('New access token was acquired from Azure AD')
        return access_token

    def get_default_header(self, access_token):
        return {'Authorization': access_token}
