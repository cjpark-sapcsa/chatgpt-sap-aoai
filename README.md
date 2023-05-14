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
![build flow](https://github.com/cjpark-sapcsa/aoai-sap/assets/60184856/2d787436-6039-4dba-947a-797797e23b94)


1. Setup the Local Project 
   - To use of Visual Studio Code, createa your local project for Azure Functions, https://learn.microsoft.com/en-us/azure/azure-functions/functions-develop-vs-code?tabs=csharp
   
2. Replace code (__init_.py, main.py, function.json, requirement.txt)  
![local project setup](https://github.com/cjpark-sapcsa/aoai-sap-usecase-1-Odata/assets/60184856/0cf8942f-e6a0-4cf6-b797-140405fad8cd)

2.1 Install the required packages: 
 Navigate to the project directory and install the required Python packages using the following commands
- `pip install -r requirements.txt`

2.2 Local project testing setup 
 The solution is using APP@FastAPI, in order to test in local, you need to install the below as well in the  (.venv)
- `pip install spacy`
- `python -m spacy download en_core_web_sm`
- `uvicorn main:app --reload`
- ![unicorn loading](https://github.com/cjpark-sapcsa/aoai-sap-usecase-1-Odata/assets/60184856/1354a2b8-9488-4873-9d1d-557fb7ece639)

2.3 Testing with Postman 
- `http://127.0.0.1:8000/api/query?question=does HT-1003  has a good rating count compare to others ? `
- ![postman test 1](https://github.com/cjpark-sapcsa/aoai-sap-usecase-1-Odata/assets/60184856/01f4f3ea-c48d-4203-ab85-e4c7d4e94ba5)

2.4 Deploy to Azure Functions
- ![deploy to Auzre Functions](https://github.com/cjpark-sapcsa/aoai-sap-usecase-1-Odata/assets/60184856/86e75ccc-24dc-407a-a8a2-6fa2b2106777)

2.4.1 Testign with Azure Function App 
- Menu -> Developer -> Code + Test
- ![auzre functio test](https://github.com/cjpark-sapcsa/aoai-sap-usecase-1-Odata/assets/60184856/1a01ab41-0cfd-4734-8ff5-78814793c47d)
- Output check
- ![Function output](https://github.com/cjpark-sapcsa/aoai-sap-usecase-1-Odata/assets/60184856/e036d949-5e50-4518-ada7-d7d7b22ec27e)

2.4.2 Get Function URL with KEY for the integration of AzureBot. 
- ![Get Function URL](https://github.com/cjpark-sapcsa/aoai-sap-usecase-1-Odata/assets/60184856/817047cc-69d0-4199-be5f-ee3cf7b0271a)

3. Setup Azure Bot connection to Teams 
- Make sure you have up and running AzureBot after you follow the reference blog AzureBot setup (reference URL : https://accessibleai.dev/post/create_and_deploy_bot/)
- Replace EchoBot.cs code 
- ![EchBot cs](https://github.com/cjpark-sapcsa/aoai-sap-usecase-1-Odata/assets/60184856/1978f2d6-09ed-4aef-b094-cb6021d21a41)
- Replace line 16 : Private readonly string _azureFunctionUrl = "";  with URL from section 2.4.2
- Save All
- Rebuild
- Publish 

4. Azure Bot Connection testing to Teams
![add Teams channel](https://github.com/cjpark-sapcsa/aoai-sap-usecase-1-Odata/assets/60184856/f9a4edc7-45a5-4e52-8cac-e684a3640f79)

![Test with teams](https://github.com/cjpark-sapcsa/aoai-sap-usecase-1-Odata/assets/60184856/6350ea38-419f-4cdf-abc2-94b1119e3b96)

## Code Overview
The main components of the code are:

main.py: This is the main script that runs the process query. It uses the OpenAI API to process user queries and returns the appropriate responses.

__init_.py: This script is responsible for connecting to the SAP system and fetching product data to HTTP trigger to AzureBot..


## Conclusion
With the SAP Bot, you can easily fetch and interact with your SAP data using natural language queries. Leveraging the power of OpenAI's GPT model and Azure's robust infrastructure, this bot can be a valuable tool for anyone needing quick and easy access to their SAP data.

Feel free to clone, modify, and use this project as you see fit. If you have any questions or suggestions, please open an issue or submit a pull request.
