import numpy as np



def prompt_string(gender = 'woman', ethnicity = 'korean', age = '50s', destination = 'Sahara', weather_lims = [35, 40], with_text_output=False):

    string_setup = f'A {gender}, {ethnicity}, aged {age} is flying to {destination}. The weather will be between {np.min(weather_lims):.1f} to {np.max(weather_lims):.1f} degrees celsius. '
    string_visual = f'Draw a hyper realistic picture of this person with clothing that is fitting for that weather. Make sure this person is facing the viewer. Make sure the surrounding of this person is fitting of the destionation:{destination}.' 
    if with_text_output: 
        string_text = f'As text output, list the outer set of clothes with basic descriptions (type of clothing, 2-3 word description) that would be fitting for searching this clothings online. Make sure that the text output is **only** a csv compatible output and no other text.'
        string_prompt = string_setup + string_visual + string_text
    else:
        string_prompt = string_setup + string_visual
    return string_prompt


def prompt_only_text(gender = 'man', ethnicity = 'european', age = '30s', destination = 'North Pole', weather_lims = [-35, -20]):
    string_setup = f'A {gender}, {ethnicity}, aged {age} is flying to {destination}. The weather will be between {np.min(weather_lims):.1f} to {np.max(weather_lims):.1f} degrees celsius. '
    
    string_text = f'As text output, list the outer set of clothes with basic descriptions (type of clothing, 2-3 word description) that would be fitting for searching this clothings online. Make sure that the text output is **only** a csv compatible output and no other text.'
    
    string_prompt = string_setup + string_text
    
    return string_prompt