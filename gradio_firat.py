import os
from PIL import Image
import numpy as np
import pickle
import gradio as gr
import prompt_generator_for_gpt
import query_shopping_firat
import query_chatgpt_firat
import query_dalle_firat
import get_weather_data
import utils


shopping_image_urls = []
shopping_item_urls = []

hardcoded_shopping_results = {
    'row0': {'thumbnails': ['https://encrypted-tbn1.gstatic.com/shopping?q=tbn:ANd9GcSNB55HrfQe34rgvotn6kUHSMHNUKOji_5iaqYjk8y8m5rKyndVvnvWaZbSm3jvtJO12gJ7Uh5jN2LIe2D73dH_K3o8zpG3&usqp=CAE',
    'https://encrypted-tbn2.gstatic.com/shopping?q=tbn:ANd9GcQT7W2L8Tcht8JxngMU5N82PFoX24HK4BiLC63ZK6T4JVVRtpydXk1IHy8Ctb9Jo8WW6tC5AQRGlJwZDGDzmN0D_ZSXedgZ6w&usqp=CAE'],
    'links': ['https://www.the-british-shop.ch/Englische-Mode-fuer-Herren/Jacken-und-Maentel/Extrawarmer-Daunenparka?prod_number=82-0195-52&em_src=cp&em_cmp=free-listing',
    'https://www.amazon.de/bw-online-shop-Ladies-Fishtail-Winterparka-schwarz/dp/B0BHTXX1RY?source=ps-sl-shoppingads-lpcontext&ref_=fplfs&psc=1&smid=A38NTUAB4BA4TK'],
    'prices': ['CHF 389.00', 'CHF 85.72'],
    'query': 'Jacket,Winter Parka'},
    'row1': {'thumbnails': ['https://encrypted-tbn1.gstatic.com/shopping?q=tbn:ANd9GcTe7wxsra4DG7akvJgclhJNl_ynkGulQT3ulOAUrl_bgra5f_5F2Q60WuMDxI26aNoA5wjKYH0MwcKUJi_DJBzsx-fe87-ncQ&usqp=CAE',
    'https://encrypted-tbn1.gstatic.com/shopping?q=tbn:ANd9GcTpW_QBzImqOTP9PI7naEZaQX6gDgskm-7BKRi1-9FMxpJuidKq25LSz6gcD4kUCWdPNMFiThnDkDSQFm_QXi0hVxRNrUmg5w&usqp=CAE'],
    'links': ['https://www.amazon.de/Onsoyours-Strumpfhose-Thermoleggins-Freizeithose-Einheitsgr%C3%B6%C3%9Fe/dp/B09JZFKGJ7?source=ps-sl-shoppingads-lpcontext&ref_=fplfs&psc=1&smid=A24O97QQ6LZT0D',
    'https://gomilitar.com/products/genuine-swedish-army-pants-insulated-od-green-thermal-trousers-cold-weather?variant=47091590627670&currency=USD&utm_medium=product_sync&utm_source=google&utm_content=sag_organic&utm_campaign=sag_organic&srsltid=AfmBOop1S1l4IblnD_TBchfXn2O0HZxNYIuOWXR-atvVaFTAnwmi-Nl1fuM'],
    'prices': ['CHF 14.29', 'CHF 17.21'],
    'query': 'Pants,Thermal Trousers'},
    'row2': {'thumbnails': ['https://encrypted-tbn3.gstatic.com/shopping?q=tbn:ANd9GcRdjbj7SgrCKHYxHpLSwWgDIIrfP2seHaC-NQjbodQWBvwKl-T3ggunWgZ2SnuILPiG80QiP9_7TOBL6Djjqc0xcbiqYclm&usqp=CAE',
    'https://encrypted-tbn0.gstatic.com/shopping?q=tbn:ANd9GcSSxYkxxYItEEXWmZ6az3K8gzG5ZhJ5b8Lo5c77OH0_G5KVhD9kETPn2hy58IrtVcvpxIS9Mbfg6f67-dFOBlrNa79rHdZ4&usqp=CAE'],
    'links': ['https://www.ochsnersport.ch/de/shop/46-nord-nebraska-herren-winterboot-schwarz-42-0000200175448100000004-p.html',
    'https://www.amazon.de/CMP-Herren-Kinos-Snow-GRAFFITE-Nero/dp/B089XYCHKJ?source=ps-sl-shoppingads-lpcontext&ref_=fplfs&psc=1&smid=A3JWKAKR8XB7XF'],
    'prices': ['CHF 99.90', 'CHF 61.97'],
    'query': 'Boots,Insulated Snow Boots'}
}


hardcoded_params_1 = {
    'gender_str': 'male', 
    'ethnicity_str': 'european',
    'age_str': 30,
    'destination_str': 'Paris',
    'date_start_str': '05.01.2024',
    'date_end_str': '10.01.2024',
    'weather_params': [2, 5],
}

def run_the_process(gender_str, ethnicity_str, age_str, destination_str, date_start_str, date_end_str, is_online=False):
    if not is_online:
        ## load a random hardcoded one.
        l_hardcoded_pkl = ['hardcoded_params/affrican-american-23-stockholm-022024.pkl', 'middle-east-33-zermatt-012024.pkl']
        fname_pkl = np.random.choice(l_hardcoded_pkl)
        with open(fname_pkl, 'rb') as handle:
            d_hardcoded_params = pickle.load(handle)
        outputs = [d_hardcoded_params['dalle_image'], d_hardcoded_params['date_start_info'], d_hardcoded_params['date_end_info'], d_hardcoded_params['chat_gpt_prompt'], d_hardcoded_params['gallery_list'], d_hardcoded_params['url_display'], is_online]
        return outputs
        
    data_start_parsed = parse_date_str(date_start_str)
    if data_start_parsed == -1:
        date_start_info = f'{date_start_str} does not match the format DD.MM.YYYY!'
        return [None, date_start_info, date_end_str, None , None, None, is_online]
    else:
        date_start_info = date_start_str
    data_end_parsed = parse_date_str(date_end_str)
    if data_end_parsed == -1:
        date_end_info = f'{date_end_str} does not match the format DD.MM.YYYY!'
        return [None, date_start_str, date_end_info, None, None , None, is_online]
    else:
        date_end_info = date_end_str
        
    # if is_online:
    #     weather_params = get_weather_data.get_data(date_str='2023-11-20',days_before=30*5,location_name=destination_str)
    # else:
    #     ## weather params
    #     minTemp = 10
    #     maxTemp = 25
    #     minPrec = 0
    #     maxPrec = 15
    #     sunnyDays = 5
    minTemp = -15
    maxTemp = -10
    minPrec = 0
    maxPrec = 15
    sunnyDays = 2
    chat_gpt_prompt = prompt_generator_for_gpt.prompt_only_text(
            gender=gender_str, 
            ethnicity=ethnicity_str,
            age=age_str,
            destination=destination_str,
            minTemp=minTemp, maxTemp=maxTemp, minPrec=minPrec, maxPrec=maxPrec, sunnyDays=sunnyDays)
    ## call ChatGPT
    clothing_str_chatgpt = query_chatgpt_firat.query_chatgpt4_text(chat_gpt_prompt)
    # else:
    #     clothing_str_chatgpt = 'type of clothing,2-3 word description\nJacket,Winter Parka\nPants,Thermal Trousers\nBoots,Insulated Snow Boots\nGloves,Extreme Cold-Weather Gloves\nHat,Fleece-lined Beanie\nScarf,Thick Wool Scarf\nThermal Socks,Merino Wool Socks\nBase Layer,Long-sleeve Thermal Top\nOuter Layer,Waterproof Shell'
    logs_value = f'ChatGPT prompt: {chat_gpt_prompt}'
    ## call shopping API
    shopping_search_queries = clothing_str_chatgpt.split('\n')[1:]
    for rows in range(3): ## current API runs out too fast.
        dict_amazon = query_shopping_firat.search_product(shopping_search_queries[rows], max_items=3)
        if dict_amazon is None:
            dict_amazon = {'links': [], 'prices': [], 'thumbnails': []}
        if rows == 0: #great coding style
            row0 = dict_amazon
        elif rows == 1:
            row1 = dict_amazon
        elif rows == 2:
            row2 = dict_amazon
    # else:
    #     ## HARDCODED results from shopping search API
    #     row0, row1, row2 = hardcoded_shopping_results['row0'], hardcoded_shopping_results['row1'], hardcoded_shopping_results['row2']
    row0['links'] = [utils.shorten_url(link) for link in row0['links']]
    row1['links'] = [utils.shorten_url(link) for link in row1['links']]
    row2['links'] = [utils.shorten_url(link) for link in row2['links']]

    ## call DALL-E
    dalle_prompt = prompt_generator_for_gpt.prompt_string(gender=gender_str, 
            ethnicity=ethnicity_str,
            age=age_str,
            destination=destination_str,
            minTemp=minTemp, maxTemp=maxTemp, minPrec=minPrec, maxPrec=maxPrec, sunnyDays=sunnyDays, clothing_items=shopping_search_queries, with_text_output=False)
    dalle_image_arr = query_dalle_firat.get_dalle_image(dalle_prompt, image_save_name='images/generated_image.png')
    dalle_image = Image.open('images/generated_image.png')
    output_im = dalle_image
    # else:
    #     hardcoded_image = 'images/generated_image.png'
    #     if os.path.isfile(hardcoded_image):
    #         dalle_image = Image.open(hardcoded_image)
    #     else:
    #         dalle_image = None
    #     output_im = dalle_image ## load image from images/ folder
    
    ## Populate Gallery
    list_thumbnails = row0['thumbnails'] + row1['thumbnails'] + row2['thumbnails']
    list_prices = row0['prices'] + row1['prices'] + row2['prices']
    list_captions = [f'item {i+1}: {list_prices[i]}' for i in range(len(list_prices))]
    gallery_list = list(zip(list_thumbnails, list_captions))
    # gallery_list += list(zip(row0['thumbnails'], row0['prices']))
    # gallery_list += list(zip(row1['thumbnails'], row1['prices']))
    # gallery_list += list(zip(row2['thumbnails'], row2['prices']))
    shopping_image_urls = row0['thumbnails'] + row1['thumbnails'] + row2['thumbnails']
    shopping_item_urls = row0['links'] + row1['links'] + row2['links']
    
    url_display = [f"[item {i+1}]({shopping_item_urls[i]})" for i in range(len(shopping_item_urls))]
    url_display = '\n'.join(url_display)
    
    hardcoded_params = {
        'gender_str': gender_str,
        'ethnicity_str': ethnicity_str,
        'age_str': age_str,
        'destination_str': destination_str,
        'date_start_info': date_start_info,
        'date_end_info': date_end_info,
        'minTemp': minTemp,
        'maxTemp': maxTemp,
        'minPrec': minPrec,
        'maxPrec': maxPrec,
        'sunnyDays': sunnyDays,
        'shopping_search_queries': shopping_search_queries,
        'chat_gpt_prompt': chat_gpt_prompt,
        'clothing_str_chatgpt': clothing_str_chatgpt,
        'dalle_image': dalle_image,
        'gallery_list': gallery_list,
        'url_display': url_display,
    }
    # with open('hardcoded_params/affrican-american-23-stockholm-022024.pkl', 'wb') as handle:
    #     pickle.dump(hardcoded_params, handle, protocol=pickle.HIGHEST_PROTOCOL)
    
    outputs = [output_im, date_start_info, date_end_info, logs_value, gallery_list, url_display, is_online]
    return outputs

def get_image_urls(image_url):
    i = shopping_image_urls.index(image_url)
    url = shopping_item_urls[i]
    markdown_url = f"[See item]({url})"
    return markdown_url

def parse_date_str(date_str):
    '''Expects date in format: 'DD.MM.YYYY'
    Returns date in the format: 'YYYY-MM-DD'
    '''
    date_split = str(date_str).split('.')
    if len(date_split) != 3:
        return -1
    day = date_split[0]
    if int(day) < 0 or int(day) > 31:
        return -1
    month = date_split[1]
    if int(month) < 0 or int(month) > 12:
        return -1
    year = date_split[2]
    if int(year) < 2023 or int(year) > 9999:
        return -1
    date_parsed = f'{year}-{month}-{day}'
    return date_parsed
    
d_defaults = {
    'gender': 'female',
    'ethnicity': 'middle eastern',
    'age': '33',
    'destination': 'Zermatt',
    'travel_start': '05.01.2024',
    'travel_end': '10.01.2024',
}

with gr.Blocks() as demo:
    with gr.Row():
        # gr.Column(scale=99)
        with gr.Column(scale=1):
            logo = gr.Image(value="images/Logo_TravelTailor.png", interactive=False, width=100)
    with gr.Row():
        with gr.Column(scale=1):
            gender_str_box = gr.Textbox(info="Gender", value=d_defaults['gender'], interactive=True)
        with gr.Column(scale=1):
            ethnicity_str_box = gr.Textbox(info="Ethnicity", value=d_defaults['ethnicity'], interactive=True)
        with gr.Column(scale=1):
            age_str_box = gr.Textbox(info="Age", value=d_defaults['age'], interactive=True)
        with gr.Column(scale=1):
            destination_str_box = gr.Textbox(info="Destination", value=d_defaults['destination'], interactive=True)
        with gr.Column(scale=1):
            date_start_str_box = gr.Textbox(info="Travel start [DD.MM.YYYY]", value=d_defaults['travel_start'], interactive=True)
        with gr.Column(scale=1):
            date_end_str_box = gr.Textbox(info="Travel end [DD.MM.YYYY]", value=d_defaults['travel_end'], interactive=True)
    with gr.Row():
        with gr.Column(scale=50):
            logs_box = gr.Textbox(info="Logs", interactive=False, visible=False)
        with gr.Column(scale=5):
            button_submit = gr.Button(value="Find appropriate clothing!")
        with gr.Column(scale=2):
            checkbox_online = gr.Checkbox(label="Online", value=False, interactive=True)
    with gr.Row():
        with gr.Column(scale=4):
            output_im = gr.Image(type="numpy", image_mode="L", label="Imagine!", interactive=False)
        with gr.Column(scale=6):
            with gr.Row():
                gallery_suggested_clothing = gr.Gallery(label="Our suggestions", rows=3, columns=3, allow_preview=True, show_download_button=False,)  
            with gr.Row():
                url_display = gr.Markdown()
        
    l_inputs = [gender_str_box, ethnicity_str_box, age_str_box, destination_str_box, date_start_str_box, date_end_str_box, checkbox_online]
    
    button_submit.click(run_the_process, inputs=l_inputs, outputs=[output_im, date_start_str_box, date_end_str_box, logs_box, gallery_suggested_clothing, url_display])
    # gallery_suggested_clothing.change(fn=get_image_urls, inputs=gallery_suggested_clothing, outputs=url_display)

if __name__ == "__main__":
    demo.launch(share=False)