import os
from PIL import Image
import gradio as gr
import prompt_generator_for_gpt
import query_shopping_firat
import utils


shopping_image_urls = []
shopping_item_urls = []

def run_the_process(gender_str, ethnicity_str, age_str, destination_str, date_start_str, date_end_str):
    data_start_parsed = parse_date_str(date_start_str)
    if data_start_parsed == -1:
        date_start_info = f'{date_start_str} does not match the format DD.MM.YYYY!'
    else:
        date_start_info = date_start_str
    data_end_parsed = parse_date_str(date_end_str)
    if data_end_parsed == -1:
        date_end_info = f'{date_end_str} does not match the format DD.MM.YYYY!'
    else:
        date_end_info = date_end_str
        
    # weather_params = get_weather_params(destination_str, data_start_parsed, data_end_parsed)
    weather_params = [[35, 40]]
    chat_gpt_prompt = prompt_generator_for_gpt.prompt_only_text(
        gender=gender_str, 
        ethnicity=ethnicity_str,
        age=age_str,
        destination=destination_str,
        weather_lims=weather_params[0])
    logs_value = f'ChatGPT prompt: {chat_gpt_prompt}'
    ## call ChatGPT
    ## call DALL-E
    ## call amazon API
    clothing_str_chatgpt = 'type of clothing,2-3 word description\nJacket,Winter Parka\nPants,Thermal Trousers\nBoots,Insulated Snow Boots\nGloves,Extreme Cold-Weather Gloves\nHat,Fleece-lined Beanie\nScarf,Thick Wool Scarf\nThermal Socks,Merino Wool Socks\nBase Layer,Long-sleeve Thermal Top\nOuter Layer,Waterproof Shell'
    shopping_search_queries = clothing_str_chatgpt.split('\n')[1:]
    gallery_list = []
    ## HARDCODED results from shopping search API
    row0 = {'thumbnails': ['https://encrypted-tbn1.gstatic.com/shopping?q=tbn:ANd9GcSNB55HrfQe34rgvotn6kUHSMHNUKOji_5iaqYjk8y8m5rKyndVvnvWaZbSm3jvtJO12gJ7Uh5jN2LIe2D73dH_K3o8zpG3&usqp=CAE',
    'https://encrypted-tbn2.gstatic.com/shopping?q=tbn:ANd9GcQT7W2L8Tcht8JxngMU5N82PFoX24HK4BiLC63ZK6T4JVVRtpydXk1IHy8Ctb9Jo8WW6tC5AQRGlJwZDGDzmN0D_ZSXedgZ6w&usqp=CAE'],
    'links': ['https://www.the-british-shop.ch/Englische-Mode-fuer-Herren/Jacken-und-Maentel/Extrawarmer-Daunenparka?prod_number=82-0195-52&em_src=cp&em_cmp=free-listing',
    'https://www.amazon.de/bw-online-shop-Ladies-Fishtail-Winterparka-schwarz/dp/B0BHTXX1RY?source=ps-sl-shoppingads-lpcontext&ref_=fplfs&psc=1&smid=A38NTUAB4BA4TK'],
    'prices': ['CHF 389.00', 'CHF 85.72'],
    'query': 'Jacket,Winter Parka'}
    row1 = {'thumbnails': ['https://encrypted-tbn1.gstatic.com/shopping?q=tbn:ANd9GcTe7wxsra4DG7akvJgclhJNl_ynkGulQT3ulOAUrl_bgra5f_5F2Q60WuMDxI26aNoA5wjKYH0MwcKUJi_DJBzsx-fe87-ncQ&usqp=CAE',
    'https://encrypted-tbn1.gstatic.com/shopping?q=tbn:ANd9GcTpW_QBzImqOTP9PI7naEZaQX6gDgskm-7BKRi1-9FMxpJuidKq25LSz6gcD4kUCWdPNMFiThnDkDSQFm_QXi0hVxRNrUmg5w&usqp=CAE'],
    'links': ['https://www.amazon.de/Onsoyours-Strumpfhose-Thermoleggins-Freizeithose-Einheitsgr%C3%B6%C3%9Fe/dp/B09JZFKGJ7?source=ps-sl-shoppingads-lpcontext&ref_=fplfs&psc=1&smid=A24O97QQ6LZT0D',
    'https://gomilitar.com/products/genuine-swedish-army-pants-insulated-od-green-thermal-trousers-cold-weather?variant=47091590627670&currency=USD&utm_medium=product_sync&utm_source=google&utm_content=sag_organic&utm_campaign=sag_organic&srsltid=AfmBOop1S1l4IblnD_TBchfXn2O0HZxNYIuOWXR-atvVaFTAnwmi-Nl1fuM'],
    'prices': ['CHF 14.29', 'CHF 17.21'],
    'query': 'Pants,Thermal Trousers'}
    row2 = {'thumbnails': ['https://encrypted-tbn3.gstatic.com/shopping?q=tbn:ANd9GcRdjbj7SgrCKHYxHpLSwWgDIIrfP2seHaC-NQjbodQWBvwKl-T3ggunWgZ2SnuILPiG80QiP9_7TOBL6Djjqc0xcbiqYclm&usqp=CAE',
    'https://encrypted-tbn0.gstatic.com/shopping?q=tbn:ANd9GcSSxYkxxYItEEXWmZ6az3K8gzG5ZhJ5b8Lo5c77OH0_G5KVhD9kETPn2hy58IrtVcvpxIS9Mbfg6f67-dFOBlrNa79rHdZ4&usqp=CAE'],
    'links': ['https://www.ochsnersport.ch/de/shop/46-nord-nebraska-herren-winterboot-schwarz-42-0000200175448100000004-p.html',
    'https://www.amazon.de/CMP-Herren-Kinos-Snow-GRAFFITE-Nero/dp/B089XYCHKJ?source=ps-sl-shoppingads-lpcontext&ref_=fplfs&psc=1&smid=A3JWKAKR8XB7XF'],
    'prices': ['CHF 99.90', 'CHF 61.97'],
    'query': 'Boots,Insulated Snow Boots'}
    row0['links'] = [utils.shorten_url(link) for link in row0['links']]
    row1['links'] = [utils.shorten_url(link) for link in row1['links']]
    row2['links'] = [utils.shorten_url(link) for link in row2['links']]
    gallery_list += list(zip(row0['thumbnails'], row0['prices']))
    gallery_list += list(zip(row1['thumbnails'], row1['prices']))
    gallery_list += list(zip(row2['thumbnails'], row2['prices']))
    shopping_image_urls = row0['thumbnails'] + row1['thumbnails'] + row2['thumbnails']
    shopping_item_urls = row0['links'] + row1['links'] + row2['links']
    
    for rows in range(3): ## current API runs out too fast.
        dict_amazon = query_shopping_firat.search_product(shopping_search_queries[rows], max_items=3)
        if dict_amazon is None:
            continue
        gallery_list += dict_amazon['thumbnails']
    url_display = [f"[item {i}]({shopping_item_urls[i]})" for i in range(len(shopping_item_urls))]
    url_display = '\n'.join(url_display)
    hardcoded_image = 'images/generated_image.png'
    if os.path.isfile(hardcoded_image):
        image = Image.open(hardcoded_image)
    else:
        image = None
    output_im = image ## load image from images/ folder
    outputs = [output_im, date_start_info, date_end_info, logs_value, gallery_list, url_display]
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
    'gender': 'male',
    'ethnicity': 'middle eastern',
    'age': '33',
    'destination': 'Zermatt',
    'travel_start': '05.01.2024',
    'travel_end': '10.01.2024',
}

with gr.Blocks() as demo:
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
        with gr.Column(scale=8):
            logs_box = gr.Textbox(info="Logs", interactive=False)
        with gr.Column(scale=2):
            button_submit = gr.Button(value="Find appropriate clothing!")
    with gr.Row():
        with gr.Column(scale=4):
            output_im = gr.Image(type="numpy", image_mode="L", label="Imagine!", interactive=False)
        with gr.Column(scale=6):
            with gr.Row():
                gallery_suggested_clothing = gr.Gallery(label="Our suggestions", rows=3, columns=3, allow_preview=True, show_download_button=False,)  
            with gr.Row():
                url_display = gr.Markdown()
        
    l_inputs = [gender_str_box, ethnicity_str_box, age_str_box, destination_str_box, date_start_str_box, date_end_str_box]
    
    button_submit.click(run_the_process, inputs=l_inputs, outputs=[output_im, date_start_str_box, date_end_str_box, logs_box, gallery_suggested_clothing, url_display])
    # gallery_suggested_clothing.change(fn=get_image_urls, inputs=gallery_suggested_clothing, outputs=url_display)

if __name__ == "__main__":
    demo.launch(share=False)