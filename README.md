# Build SAP Bot with Azure OpenAI - Generative ChatGPT 

## Introduction
This repository contains a proof-of-concept (POC) for a chatbot that integrates SAP data with Azure OpenAI's powerful GPT-35-turbo AI model, hosted on Azure. The purpose of this bot is to answer user queries related to specific products stored in an SAP system, such as details about the product's name, ID, and other properties.

![chatgpt-image](https://github.com/cjpark-sapcsa/aoai-sap/assets/60184856/2dbcf287-1fac-4cfb-8fb0-ae9351628dc1)


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
- the solution is using APP@FastAPI, in order to test in local, you need to install the below as well in the  (.venv).
- `pip install spacy`
- `python -m spacy download en_core_web_sm`
- `uvicorn main:app --reload`
- ![unicorn loading](https://github.com/cjpark-sapcsa/aoai-sap-usecase-1-Odata/assets/60184856/1354a2b8-9488-4873-9d1d-557fb7ece639)


Azure Bot connection to Teams 
- code  (see the EchoBot.cs)
- open the Teams channel within AzureBot. 

## Code Overview
The main components of the code are:

main.py: This is the main script that runs the process query. It uses the OpenAI API to process user queries and returns the appropriate responses.

__init_.py: This script is responsible for connecting to the SAP system and fetching product data to HTTP trigger to AzureBot..


## Conclusion
With the SAP Bot, you can easily fetch and interact with your SAP data using natural language queries. Leveraging the power of OpenAI's GPT model and Azure's robust infrastructure, this bot can be a valuable tool for anyone needing quick and easy access to their SAP data.

Feel free to clone, modify, and use this project as you see fit. If you have any questions or suggestions, please open an issue or submit a pull request.
