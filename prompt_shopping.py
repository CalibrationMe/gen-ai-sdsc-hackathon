import http.client
import urllib.parse
import json

query = ["Red shoes woman", "green jeans woman", "black jacket woman", "gray hat", 
         "pink gloves", "blue scarf"]

API_keys = ["a6045d240bmsha035283f32634a5p17b44ejsna905ccfe27ae",'9545c1d755mshc6658fb8f9b6715p1255e6jsn57faa5927adf',
            'd40bbea9camsh1baecf3d4368123p1b66a6jsnca2a98e4cfe4']

def search_product(query, API_key):
    conn = http.client.HTTPSConnection("real-time-product-search.p.rapidapi.com")

    headers = {
        'X-RapidAPI-Key': API_key,
        'X-RapidAPI-Host': "real-time-product-search.p.rapidapi.com"
    }

    formatted_query = urllib.parse.quote(query)
    conn.request("GET", f"/search?q={formatted_query}&country=de&language=en", headers=headers)

    res = conn.getresponse()
    
    
    ######### custom output #########      
    #################################

    data = res.read().decode("utf-8")
    query_result = json.loads(data)

    # thumbnail = query_result["data"][0]["product_photos"][0]
    # link = query_result["data"][0]["offer"]["offer_page_url"]
    # price = query_result["data"][0]["offer"]["price"]

    # return thumbnail, link, price
    return query_result


results = {}  

for ii in range(len(API_keys)):
    for qq in range(1):
        current_query = query[ii*2+qq]
        print(current_query)
        try:

            query_result = search_product(current_query, API_keys[ii])
            thumbnail = query_result["data"][0]["product_photos"][0]
            link = query_result["data"][0]["offer"]["offer_page_url"]
            price = query_result["data"][0]["offer"]["price"]

            print(thumbnail, link, price)

            results[current_query] = {'thumbnail': thumbnail, 'link': link, 'price': price}
        except Exception as e:
            error_message = str(e)
            print(error_message)
            pass

        print("----------------")
                
query_result
