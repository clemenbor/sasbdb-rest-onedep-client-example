from onedepclient import OnedepAPIClient
from base import API_USERNAME, API_PASSWORD

def main():

    client = OnedepAPIClient(False)

    #Create and store JWT token in local storage and checks for validity
    token = client.check_JWT_token(API_USERNAME, API_PASSWORD)

    if token:
        onedep_id = "D_1200003131"  # Onedep ID example to request to SASBDB
        json_data = client.deposition_status(token, onedep_id)
        #json_data contains the result, now you can parse it as you want
        try:
            print json_data["onedep_id"]
        except:
            pass

if __name__ == "__main__":
    main()