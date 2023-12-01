import os
import numpy as np
import json
import http.client
import urllib.parse


def search_product(query: str, max_items: int=4, rapidAPI_key_index: int=0):
    fname_rapidAPI_keys = 'RAPIDAPI_KEYS.txt'
    RAPID_API_KEYS = []
    if os.path.isfile(fname_rapidAPI_keys):
        with open(fname_rapidAPI_keys, 'r') as fh:
            for key in fh:
                RAPID_API_KEYS.append(key.strip())
    else:
        print('Error: RAPIDAPI_KEYS.txt file not found')
    
    if rapidAPI_key_index >= len(RAPID_API_KEYS):
        print('Error: Too many shopping requests been made. Please wait for a while.')
        return None
    
    RapidAPI_host = "real-time-product-search.p.rapidapi.com"
    conn = http.client.HTTPSConnection(RapidAPI_host)

    headers = {
        'X-RapidAPI-Key': RAPID_API_KEYS[rapidAPI_key_index],
        'X-RapidAPI-Host': RapidAPI_host
    }

    formatted_query = urllib.parse.quote(query)
    conn.request("GET", f"/search?q={formatted_query}&country=ch&language=en", headers=headers)

    res = conn.getresponse()
    


    data = res.read().decode("utf-8")
    query_result = json.loads(data)

    if 'status' in query_result:
        if query_result['status'] == 'ERROR':
            return search_product(query, max_items, rapidAPI_key_index=rapidAPI_key_index+1)

    if 'message' in query_result:
        if query_result['message'][:len('You have exceeded')] == 'You have exceeded':
            return search_product(query, max_items, rapidAPI_key_index=rapidAPI_key_index+1)
    
    if 'data' not in query_result:
        print('Something went wrong in shopping API!')
        return None
    thumbnails = [query_result['data'][i]['product_photos'][0] for i in range(np.min((max_items, len(query_result['data']))))]
    links = [query_result['data'][i]['offer']['offer_page_url'] for i in range(np.min((max_items, len(query_result['data']))))]
    prices = [query_result['data'][i]['offer']['price'] for i in range(np.min((max_items, len(query_result['data']))))]
    return {'thumbnails': thumbnails, 'links': links, 'prices': prices}