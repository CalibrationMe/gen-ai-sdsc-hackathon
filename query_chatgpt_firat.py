import os
from openai import AzureOpenAI


def query_chatgpt4_text(prompt_str):
    ## more details on https://github.com/openai/openai-python

    AZURE_CH_ENDPOINT = 'https://switzerlandnorth.api.cognitive.microsoft.com/'
    fname_CHATGPT_KEY = 'CHATGPT_TOKEN.txt' # TODO: change to your own API key. This is located under Home > Azure AI Services | Azure OpenAI > hackathon-hack-openai-10 > Keys and Endpoint > Key 1
    if os.path.isfile(fname_CHATGPT_KEY):
        with open(fname_CHATGPT_KEY, 'r') as fh:
            AZURE_CHATGPT_API_KEY = fh.read()
    else:
        print('Error: AZURE_CHATGPT_API_KEY file not found')

    client = AzureOpenAI(
    azure_endpoint = AZURE_CH_ENDPOINT, #os.getenv("AZURE_OPENAI_ENDPOINT"), 
    api_key = AZURE_CHATGPT_API_KEY, # os.getenv("AZURE_OPENAI_KEY"),  
    api_version="2023-05-15"
    )

    response = client.chat.completions.create(
        model="gpt-35-turbo", # model = "deployment_name".
        # model='gpt-4', ## better, but a lot slower, and more expensive
        messages=[
            # {"role": "system", "content": "You are a helpful assistant."},
            # {"role": "user", "content": "Does Azure OpenAI support customer managed keys?"},
            # {"role": "assistant", "content": "Yes, customer managed keys are supported by Azure OpenAI."},
            # {"role": "user", "content": "Do other Azure AI services support this too?"}
            {"role": "user", "content": prompt_str}
        ]
    )

    response_txt = response.choices[0].message.content
    return response_txt
