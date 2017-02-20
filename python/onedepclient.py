import requests
from requests.packages.urllib3.exceptions import InsecureRequestWarning
import os
import json
from base import URL_BASE, API_BASE

class OnedepAPIClient(object):
    """
    Authenticate against SASBDB and uses JWT tokens to access protected resources from the SASBDB Onedep API
    """

    def __init__(self, verify=True):
        self.verify = verify
        if not verify:
            requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

    """
    Authenticate account against SASBDB and returns a new JWT token
    """
    def new_token(self, username, password):
        try:
            resp = requests.post(os.path.join(URL_BASE, 'api-token-auth/'), data={"username": username, "password": password}, verify=self.verify)
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
    Authenticate account against SASBDB and returns a new JWT token
    """
    def check_JWT_token(self, username, password):
        token = None
        home_dir = os.path.expanduser('~')
        token_dir = os.path.join(home_dir, '.sasbdb_api')
        token_file_path = os.path.join(token_dir, 'sasbdb_onedep_api_token.jwt')
        if not os.path.exists(token_dir):
            os.makedirs(token_dir)

        #If a JWT token file has not been created then create it
        if not os.path.exists(token_file_path):
            try:
                #Authenticate and get a new token
                token = self.new_token(username, password)
                if token:
                    #Write the token to file
                    self.write_file_token(token_file_path, token)
            except:
                pass
        else: #The token file exist
            try:
                #Read the token from file
                file = open(token_file_path, "r")
                token = file.read()
            except IOError as e:
                print "I/O error({0}): {1}".format(e.errno, e.strerror)


        #Check if JWT file token is valid and it is not expired
        if token and not self.verify_token(token):
            try:
                #If token is not valid or expired, then authenticate again and get a new token
                token = self.new_token(username, password)
                if token:
                    #Write the new token to file
                    self.write_file_token(token_file_path, token)
            except:
                pass

        return token

    """
    Writes a JWT token to file
    """
    def write_file_token(self, path, token):
        try:
            file = open(path, "w")
            file.write(token)
            file.close()
        except IOError as e:
            print "I/O error({0}): {1}".format(e.errno, e.strerror)

    """
    Checks for JWT token validity (format, expiration, etc)
    """
    def verify_token(self,token):
        try:
            resp = requests.post(os.path.join(URL_BASE, 'api-token-verify/'), data={'token': token}, verify=self.verify)
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
            resp = requests.post(os.path.join(URL_BASE, 'api-token-refresh/'), data={'token': token}, verify=self.verify)
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
            resp = requests.post(os.path.join(API_BASE, 'deposition/'+onedep_id+"/"), headers=headers, verify=self.verify)
            print "Calling "+resp.url
            if resp.status_code == 200:
                response_content = json.loads(resp.content.decode('utf-8'))
                print response_content
                return response_content
            else:
                print resp.json()