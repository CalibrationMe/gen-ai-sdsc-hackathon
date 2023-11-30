# gen-ai-sdsc-hackathon


Instructions for using scripts from Firat:   
All scripts look for a specific file that won't be on github that contain tokens for corresponding APIs. 
Please create corresponding files in your own deployment with your own tokens/keys. 

Otherwise, you can use `environment-firat.yml` to install the conda environment to get these scripts working: 
`conda env create -f environment-firat.yml`  

Additional requirements:   
Running DALL-E:
```python 
ENDPOINT = 'https://rhaetian-poppy-sweden.openai.azure.com/'
# You need to create a local file `DALLE_TOKEN.txt` that contains your Key for the server in Sweden. 
```

Running ChatGPT: 
```python
AZURE_CH_ENDPOINT = 'https://switzerlandnorth.api.cognitive.microsoft.com/'
## You need to create a local file `CHATGPT_TOKEN.txt` that contains your key for the server in Switzerland North. This is located under Home > Azure AI Services | Azure OpenAI > hackathon-hack-openai-10 > Keys and Endpoint > Key 1