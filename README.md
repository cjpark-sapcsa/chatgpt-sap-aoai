# Build SAP Bot with Azure OpenAI - Generative ChatGPT 

## Introduction
This repository hosts instructions and code needed to build a chatbot that integrates SAP data with Azure OpenAI's advanced GPT-35-turbo AI model, hosted on Azure. The bot is designed to address user queries regarding specific products available in an SAP system, including details about the product's name, ID, and other properties.

## Prerequisites
Before you start, make sure you have the following prerequisites:

Azure subscription
https://azure.microsoft.com/en-us/

Azure Cognitive Services Instance
https://azure.microsoft.com/en-us/products/cognitive-services/#overview

Azure OpenAI Service Instance 
https://azure.microsoft.com/en-us/products/cognitive-services/openai-service/

A SAP system with some product data 
- ES5 Demo system comes with a good setup of EPM data model with Odata service, https://developers.sap.com/tutorials/gateway-demo-signup.html, 

Python 3.7 or later installed on your machine (Visual Studio Code):

AzureBot setup (reference URL : https://accessibleai.dev/post/create_and_deploy_bot/)
- AzureBot service will be connected to Micrsoft Teams as Channel 

## Build Steps

Here is the overall build flow and solution desing for the SAP Bot with ChatGPT. 
![build flow](https://github.com/cjpark-sapcsa/chatgpt-sap-aoai/assets/60184856/7f531a62-3248-4a8c-986f-563748ab0632)


1. Setup the Local Project 
   - To use of Visual Studio Code, createa your local project for Azure Functions, https://learn.microsoft.com/en-us/azure/azure-functions/functions-develop-vs-code?tabs=csharp
   
2. Replace code (__init_.py, main.py, function.json, requirement.txt)  
![local project setup](https://github.com/cjpark-sapcsa/chatgpt-sap-aoai/assets/60184856/561dc53f-9575-4df9-af3a-51023b289275)


2.1 Install the required packages: 
 Navigate to the project directory and install the required Python packages using the following commands
- `pip install -r requirements.txt`

2.2 Local project testing setup 
 The solution is using APP@FastAPI, in order to test in local, you need to install the below as well in the  (.venv)
- `pip install spacy`
- `python -m spacy download en_core_web_sm`
- `uvicorn main:app --reload`
![unicorn loading](https://github.com/cjpark-sapcsa/chatgpt-sap-aoai/assets/60184856/3f495ab8-2301-42ec-b8f7-2b97fed937f1)

2.3 Testing with Postman 
- `http://127.0.0.1:8000/api/query?question=does HT-1003  has a good rating count compare to others ? `
![postman test 1](https://github.com/cjpark-sapcsa/chatgpt-sap-aoai/assets/60184856/d4ef0289-f9a7-4a8f-b37f-e51509eb2f92)

2.4 Deploy to Azure Functions
- ![deploy to Auzre Functions](https://github.com/cjpark-sapcsa/chatgpt-sap-aoai/assets/60184856/e9dd6612-dce7-43b4-b9f0-785bf28f44c2)

2.4.1 Testign with Azure Function App 
- Menu -> Developer -> Code + Test
- ![auzre functio test](https://github.com/cjpark-sapcsa/chatgpt-sap-aoai/assets/60184856/6e85b43f-2a7f-4b35-a19c-1a9764715f65)
- Output check
- ![Function output](https://github.com/cjpark-sapcsa/chatgpt-sap-aoai/assets/60184856/1224e5e3-d090-43ac-9b24-71f203898b3b)

2.4.2 Get Function URL with KEY for the integration of AzureBot. 
- ![Get Function URL](https://github.com/cjpark-sapcsa/chatgpt-sap-aoai/assets/60184856/7972e67c-8ece-4531-8c4f-da824d20557c)

3. Setup Azure Bot connection to Teams 
- Make sure you have up and running AzureBot after you follow the reference blog AzureBot setup (reference URL : https://accessibleai.dev/post/create_and_deploy_bot/)
- Replace EchoBot.cs code 
- ![EchBot cs](https://github.com/cjpark-sapcsa/chatgpt-sap-aoai/assets/60184856/8e4f88bd-d6dd-49d2-8ba0-c5b25da0610c)
- Replace line 16 : Private readonly string _azureFunctionUrl = "";  with URL from section 2.4.2
- Save All
- Rebuild
- Publish 

4. Azure Bot Connection testing to Teams
-![add Teams channel](https://github.com/cjpark-sapcsa/chatgpt-sap-aoai/assets/60184856/3283409d-55c7-4bd4-8113-641d8ded3856)
- ![Test with teams](https://github.com/cjpark-sapcsa/chatgpt-sap-aoai/assets/60184856/649c8044-7736-4d10-adf7-e13c9be3bca6)

## Code Overview
The main components of the code are:

main.py: This is the main script that runs the process query. It uses the OpenAI API to process user queries and returns the appropriate responses.

__init_.py: This script is responsible for connecting to the SAP system and fetching product data to HTTP trigger to AzureBot..


## Conclusion
With the SAP Bot, you can easily fetch and interact with your SAP data using natural language queries. Leveraging the power of OpenAI's GPT model and Azure's robust infrastructure, this bot can be a valuable tool for anyone needing quick and easy access to their SAP data.

Feel free to clone, modify, and use this project as you see fit. If you have any questions or suggestions, please open an issue or submit a pull request.
