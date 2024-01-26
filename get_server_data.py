import requests
import time

server_a_url = 'https://test.pierceaero.space/remote-id/v1.0.0/events'
client_id = "O6PaSAflzYZ2gT1WgvlQKWCBJi2zmTdY"
client_secret = "NvDrUWkWTrJL71-myJfdqmUD6fWH2-utcDVAaZfKYrgZrOWTWbQCoNDLv70l51SE"
audience = "https://api.pierceaero.space"

def get_oauth_token(client_id, client_secret, audience):
    token_url = "https://dev-xm6pb748e4rijx6t.us.auth0.com/oauth/token"
    token_data = {
        "grant_type": "client_credentials",
        "client_id": client_id,
        "client_secret": client_secret,
        "audience": audience,
    }    # Make the token request
    response = requests.post(token_url, data=token_data)
    if response.status_code == 200:
        # Parse the JSON response and extract the token
        token = response.json().get("access_token")
        return token
    else:
        raise Exception(f"Failed to get OAuth token. Status code: {response.status_code}")


def make_request(url, token):
    headers = {"Authorization": f"Bearer {token}"}
    response = requests.get(url, headers=headers)
    status_code = response.status_code
    data = response.text  # Assuming the response is a string; adjust accordingly    # Print status code and data
    print(f"Server A Status Code: {status_code}")
    print(f"Server A Data: {data}")
    return status_code

def make_post(url, token, data):
    headers = {"Authorization": f"Bearer {token}"}
    response = requests.post(url, json=data, headers=headers)
    if response.status_code == 200:
        print('POST request successful')
    else:
        print(f'Error: {response.status_code} - {response.text}')

def main():
    try:
        # Get OAuth token at the beginning of the program
        oauth_token = get_oauth_token(client_id, client_secret, audience)
        while True:
            # Make requests to Server A
            status_code_a = make_request(server_a_url, oauth_token)

            time.sleep(2)
    except Exception as e:
        print(f"Error: {e}")


if __name__ == "__main__":
    main()