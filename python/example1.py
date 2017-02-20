from onedepclient import OnedepAPIClient

def main():

    username = "example@sasbdb.org"  # SASBDB account username/e-mail
    password = "XXYYZZ"  # SASBDB account password
    onedep_id = "D_1200003131"  # Onedep ID example to request to SASBDB

    client = OnedepAPIClient(False)

    # Create and store JWT token in local storage and checks for validity
    token = client.check_JWT_token(username, password)

    if token:
        json_data = client.deposition_status(token, onedep_id)
        #json_data contains the result, now you can parse it as you want
        try:
            print json_data["onedep_id"]
        except:
            pass

if __name__ == "__main__":
    main()