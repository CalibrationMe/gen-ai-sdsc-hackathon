## some utility functions

import requests

def shorten_url(long_url):
    api_url = f"https://tinyurl.com/api-create.php?url={long_url}"
    response = requests.get(api_url)
    return response.text
