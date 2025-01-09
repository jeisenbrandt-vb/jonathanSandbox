#this code comes from here https://medium.com/@flaviohenriquepereiraoliveira/how-to-use-digikey-api-for-product-detail-c7d262cad14
#that medium article was my saving grace


import requests
import json
import time
import sys
from urllib.parse import quote

#filename is needed to store login information in a JSON file
#auth_code will be received code from the request link below...
code = 'y0PWpSG3'
token_filename = 'digikey_token.json'

def get_access_token(auth_code, filename):
    token = load_token_from_file(filename)
    url = 'https://api.digikey.com/v1/oauth2/token'
    url_data = {
        'code': auth_code,
        'client_id': token['client_id'],
        'client_secret': token['client_secret'],
        'redirect_uri': 'https://localhost',
        'grant_type': 'authorization_code'
    }
    response = requests.post(url, data=url_data)
    if response.status_code == 200:
        print('\033[32mAccess Token get SUCCESS\033[0m')
        response_data = response.json()
        token['access_token'] = response_data['access_token']
        token['refresh_token'] = response_data['refresh_token']
        token['expires_in'] = response_data['expires_in']
        token['refresh_token_expires_in'] = response_data['refresh_token_expires_in']
        token['token_type'] = response_data['token_type']

    with open(filename, "w") as arquivo:
        json.dump(token, arquivo)

    return(response.json())

def load_token_from_file(filename):
    with open(filename, 'r') as arquivo:
        token = json.load(arquivo)

    if token != False:
        print('\033[32mToken load SUCCESS.\033[0m')
    else:
        print('\033[31m\033[1mToken load FAILED.\033[0m')
    return token

def get_product_details(partnumber, token):
    partnumber = quote(partnumber) #it replaces invalid characters in the partnumber
    url = f'https://api.digikey.com/Search/v3/Products/{partnumber}'

    print(url)

    url_header = {
        'x-digikey-locale': 'pt',
        'X-DIGIKEY-Locale-Site': 'US',
        'X-DIGIKEY-Locale-Currency': 'USD',
        'Authorization': f"{token['token_type']} {token['access_token']}",
        'X-DIGIKEY-Client-Id': token['client_id']
    }

    #print(f'URL {url}\nHeaders: {url_header}\n')
    response = requests.get(url, headers=url_header)

    if response.status_code == 200:
        response_dict = response.json()
        print(f'\033[32mGot information for {partnumber}\033[0m')
        print(response.json())
        return response_dict
    else:
        print(f'\033[31mFailed to get information for {partnumber}\033[0m')
        print(response.status_code, response.reason)
        return False
    
get_product_details("36-117-ND", load_token_from_file(token_filename))

# get_access_token(code, token_filename)