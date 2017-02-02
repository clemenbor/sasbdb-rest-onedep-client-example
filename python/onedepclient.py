import requests
import os
import json
from base import URL_BASE, API_BASE

class OnedepAPIClient():
    """
    Authenticate against SASBDB and gets a fresh token to access protected resources from the SASBDB Onedep API
    """
    def new_token(self, username, password):
        try:
            resp = requests.post(os.path.join(URL_BASE, 'api-token-auth/'), data={"username": username, "password": password}, verify=False)
            if resp.status_code == 200:
                # Authentication ok. Get token
                print resp.json()
                response_content = json.loads(resp.content.decode('utf-8'))
                token = response_content["token"]
                return token
            else:
                # Unable to login with credentials
                print resp.json()
        except requests.exceptions.HTTPError:
            resp.raise_for_status()
        return None

    """
    Checks for JWT token validity (format, expiration, etc)
    """
    def verify_token(self,token):
        try:
            resp = requests.post(os.path.join(URL_BASE, 'api-token-verify/'), data={'token': token}, verify=False)
            if resp.status_code == 200:
                #Token is valid
                return True
            else:
                #Token is invalid or it's expired
                print resp.json()
                return False
        except:
            resp.raise_for_status()
        return False

    """
    Refresh JWT token.
    Refresh with tokens can be repeated if submitted token is still valid (token1 -> token2 -> token3)
    By default, this can be done up to 7 days
    """
    def refresh_token(self, token):
        try:
            resp = requests.post(os.path.join(URL_BASE, 'api-token-refresh/'), data={'token': token}, verify=False)
            if resp.status_code == 200:
                response_content = json.loads(resp.content.decode('utf-8'))
                refreshed_token = response_content["token"]
                return refreshed_token
            else:
                # Token is invalid or it's expired
                print resp.json()
                return False
        except:
            resp.raise_for_status()
        return False

    """
    Get SASBDB entry status given a onedep_id and a valid token
    """
    def deposition_status(self, token, onedep_id):

            headers = {'Authorization': 'JWT '+token}
            resp = requests.post(os.path.join(API_BASE, 'deposition/'+onedep_id+"/"), headers=headers, verify=False)
            print "Calling "+resp.url
            if resp.status_code == 200:
                response_content = json.loads(resp.content.decode('utf-8'))
                print response_content
                return response_content
            else:
                print resp.json()


def main():
    username = "example@example.org"  # SASBDB account username/e-mail
    password = "XXYYZZ"  # SASBDB account password

    client = OnedepAPIClient()
    #Authenticate and get a new token.
    token = client.new_token(username, password)

    onedep_id = "D_1200003133" #Onedep ID example to request to SASBDB

    if token:
        print "User is authenticated and token is valid"
        json_data = client.deposition_status(token, onedep_id)

if __name__ == "__main__":
    main()