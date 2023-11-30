import os
from PIL import Image
import gradio as gr
import prompt_generator_for_gpt
import query_amazon_firat


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
    amazon_search_queries = clothing_str_chatgpt.split('\n')[1:]
    gallery_list = []
    # for rows in range(3): ## current API runs out too fast.
    #     dict_amazon = query_amazon_firat.search_product(amazon_search_queries[rows], max_items=3)
    #     gallery_list += dict_amazon['thumbnails']
    # image = None
    hardcoded_image = 'images/generated_image.png'
    if os.path.isfile(hardcoded_image):
        image = Image.open(hardcoded_image)
    else:
        image = None
    output_im = image ## load image from images/ folder
    outputs = [output_im, date_start_info, date_end_info, logs_value, gallery_list]
    return outputs

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
            gallery_suggested_clothing = gr.Gallery(label="Our suggestions", rows=3, columns=3, allow_preview=True, show_download_button=False,)  
        
    l_inputs = [gender_str_box, ethnicity_str_box, age_str_box, destination_str_box, date_start_str_box, date_end_str_box]
    
    button_submit.click(run_the_process, inputs=l_inputs, outputs=[output_im, date_start_str_box, date_end_str_box, logs_box, gallery_suggested_clothing])

# data_start_parsed = parse_date_str(date_start_str)
    # if data_start_parsed == -1:
    #     logs_box.label = f"{date_start_str} does not match the format DD.MM.YYYY!"
    #     date_start_str_box.label = f'{date_start_str} does not match the format DD.MM.YYYY!'
    # date_end_parsed = parse_date_str(date_end_str)
    # dict_inputs = {
    #     'gender': gender_str_box.value,
    #     'ethnicity': ethnicity_str_box.value,
    #     'age': age_str_box.value,
    #     'destination': destination_str_box.value,
    #     'date_start': data_start_parsed,
    #     'date_end': date_end_parsed,
    # }

if __name__ == "__main__":
    demo.launch(share=False)