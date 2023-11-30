import http.client
import urllib.parse
import json

def search_product(query):
    conn = http.client.HTTPSConnection("real-time-product-search.p.rapidapi.com")

    headers = {
        'X-RapidAPI-Key': "a6045d240bmsha035283f32634a5p17b44ejsna905ccfe27ae",
        'X-RapidAPI-Host': "real-time-product-search.p.rapidapi.com"
    }

    formatted_query = urllib.parse.quote(query)
    conn.request("GET", f"/search?q={formatted_query}&country=ch&language=en", headers=headers)

    res = conn.getresponse()
    
    
 ######### custom output #########      
 #################################

    data = res.read().decode("utf-8")
    query_result = json.loads(data)

    thumbnail = query_result["data"][0]["product_photos"][0]
    link = query_result["data"][0]["offer"]["offer_page_url"]
    price = query_result["data"][0]["offer"]["price"]

    return thumbnail, link, price

search_output = search_product("adidas shoes")
