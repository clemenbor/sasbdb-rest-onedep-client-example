# sasbdb-rest-onedep-client-example
This repository contains example scripts to access information from SASBDB by
using the SASBDB Onedep REST API.

### Example
1) A sasbdb account with access to the API will be provided by SASBDB.<br />
2) Configure this account in the file base.py (API_USERNAME and API_PASSWORD properties).<br />
3) Run the following example:

```
python example1.py
```
The script will do the following:
+ Authenticate the account against SASBDB
+ Create a JWT token for API access valid for 30 days in local storage. It will renew the token automatically when it is expired.
+ Call the API method deposition_status using a onedep_id as a parameter (and a valid token for access).