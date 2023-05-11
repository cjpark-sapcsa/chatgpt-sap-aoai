# Build SAP Bot with Azure OpenAI - Generative ChatGPT 

## Introduction
This repository contains a proof-of-concept (POC) for a chatbot that integrates SAP data with Azure OpenAI's powerful GPT-35-turbo AI model, hosted on Azure. The purpose of this bot is to answer user queries related to specific products stored in an SAP system, such as details about the product's name, ID, and other properties.

![chatgpt-image](https://github.com/cjpark-sapcsa/aoai-sap/assets/60184856/2dbcf287-1fac-4cfb-8fb0-ae9351628dc1)


## Prerequisites
Before you start, make sure you have the following prerequisites:

Azure subscription https://azure.microsoft.com/en-us/
Azure Cognitive Services Instance https://azure.microsoft.com/en-us/products/cognitive-services/#overview
Azure OpenAI Service Instance https://azure.microsoft.com/en-us/products/cognitive-services/openai-service/
A SAP system with some product data e.g https://developers.sap.com/tutorials/gateway-demo-signup.html, ES5 Demo system comes with a good setup of EPM data model with Odata service. 
Python 3.7 or later installed on your machine (Visual Studio Code) 
AzureBot setup (reference URL : https://accessibleai.dev/post/create_and_deploy_bot/)

## Build Steps

Here is the overall build flow and solution desing for the SAP Bot with ChatGPT. 
![build flow](https://github.com/cjpark-sapcsa/aoai-sap/assets/60184856/2d787436-6039-4dba-947a-797797e23b94)


Follow these steps to build the SAP Bot:

Clone the repository: Use the following command to clone this repository to your local machine.

git clone https://github.com/cjpark-sapcsa/Odata-ES5.git
Install the required packages: Navigate to the project directory and install the required Python packages using the following commands:

cd Odata-ES5
pip install -r requirements.txt
Set up your environment variables: Create a .env file in the root directory of the project, and add the following environment variables:

AZURE_KEY: Your Azure API key
Odata_URL: Your SAP connection string to ES5 Odata 

## Code Overview
The main components of the code are:

main.py: This is the main script that runs the bot. It uses the OpenAI API to process user queries and returns the appropriate responses.

__init_.py: This script is responsible for connecting to the SAP system and fetching product data.


## Conclusion
With the SAP Bot, you can easily fetch and interact with your SAP data using natural language queries. Leveraging the power of OpenAI's GPT model and Azure's robust infrastructure, this bot can be a valuable tool for anyone needing quick and easy access to their SAP data.

Feel free to clone, modify, and use this project as you see fit. If you have any questions or suggestions, please open an issue or submit a pull request.
