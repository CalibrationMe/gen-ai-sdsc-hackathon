import numpy as np



def prompt_string(gender = 'woman', ethnicity = 'korean', age = '50s', destination = 'Sahara', minTemp=-35, maxTemp=25, minPrec=0, maxPrec=15, sunnyDays=5, clothing_items=None, with_text_output=False):

    string_setup = f'A {gender}, {ethnicity}, aged {age} is travelling to {destination}. The temperature will be between {minTemp} to {maxTemp} degrees celsius. Precipitation will be between {minPrec} and {maxPrec} (in case you want to draw rain). '
    string_visual = f'Draw a hyper realistic picture of this person with clothing that is fitting for that weather. Make sure this person is facing the viewer. Make sure the surrounding of this person is fitting of the destionation:{destination}. **NO** text and **NO** numbers on the picture. ' 
    if clothing_items is not None:
        string_clothing = f'This person is wearing the following clothing items among other things: {clothing_items}. '
        string_visual =  string_visual + string_clothing
    if with_text_output: 
        string_text = f'As a CSV compatible text output, list the outer set of clothes with basic descriptions (type of clothing, 3-4 word description for searching product online) that would be fitting for searching this clothings online. Make sure that the text output is **only** a csv compatible output and **no** other text. For example, the output format should look like the following ```\nJacket, lightweight, waterproof\nHoodie, comfortable, casual\nT-shirt, short-sleeved, breathable\nButton-down shirt, long-sleeved, versatile\nSweater, warm, cozy\nWindbreaker, travel-friendly, windproof'
        string_prompt = string_setup + string_visual + string_text
    else:
        string_prompt = string_setup + string_visual
    return string_prompt


def prompt_only_text(gender = 'man', ethnicity = 'european', age = '30s', destination = 'North Pole', minTemp=-35, maxTemp=25, minPrec=0, maxPrec=15, sunnyDays=5):
    string_setup = f'A {gender}, {ethnicity}, aged {age} is travelling to {destination}. The temperature will be between {minTemp} to {maxTemp} degrees celsius. Precipitation between {minPrec} and {maxPrec} and {sunnyDays} sunny days. '
    string_text = f'As a CSV compatible text output, list the outer set of clothes with basic descriptions (type of clothing, 3-4 word description for searching product online) that would be fitting for searching this clothings online. Make sure that the text output is **only** a csv compatible output and **no** other text. For example, the output format should look like the following ```\nJacket, lightweight, waterproof\nHoodie, comfortable, casual\nT-shirt, short-sleeved, breathable\nButton-down shirt, long-sleeved, versatile\nSweater, warm, cozy\nWindbreaker, travel-friendly, windproof'
    
    string_prompt = string_setup + string_text
    
    return string_prompt