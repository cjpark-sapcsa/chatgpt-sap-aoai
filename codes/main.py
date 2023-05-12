import json
import re
import requests
import openai
import azure.functions as func
import logging
from fastapi import FastAPI
from azure.functions import HttpRequest, HttpResponse
from fastapi.responses import JSONResponse
import logging
from urllib.parse import quote
from urllib.parse import quote_plus
import urllib.parse
import httpx
import spacy
from typing import List, Dict, Any, Optional, Tuple, Set

# Load the spaCy model
nlp = spacy.load("en_core_web_sm")

# Azure OpenAI settings
openai.api_type = ""
openai.api_base = ""
openai.api_version = ""
openai.api_key = ""

# SAP ES5 Odata settings
ODATA_URL = ""
odata_user = ""
odata_password = ""


def fetch_product_data(product_filter: Optional[str] = None, property_filter: Optional[str] = None, question: Optional[str] = None) -> List[Dict[str, Any]]:
    headers = {'Accept': 'application/json'}
    
    # Build the filter string based on the user's input
    filter_list = []
    if product_filter:
        # Check if the provided filter is a product name or ID
        if product_filter.startswith("HT-") and len(product_filter) == 7: # Change here: Replace "HT_" with "HT-"
            filter_list.append(f"Id eq '{product_filter}'")
        else:
            filter_list.append(f"Name eq '{product_filter}'")
    if property_filter:
        capitalized_property_filter = property_filter[0].upper() + property_filter[1:]
        filter_list.append(f"{capitalized_property_filter} ne null")

    filter_string = " and ".join(filter_list)

    # Query the OData server using the filter string
    url = f"{ODATA_URL}?$filter={filter_string}"
    response = requests.get(url, headers=headers, auth=(odata_user, odata_password))
    response.raise_for_status()

    # Parse the JSON response and extract the product information
    data = response.json()
    products = data['d']['results']
    
    return products

def fetch_product_names() -> Set[str]:
    headers = {'Accept': 'application/json'}
    url = f"{ODATA_URL}?$select=Name"

    response = requests.get(url, headers=headers, auth=(odata_user, odata_password))
    response.raise_for_status()

    # Parse the JSON response and extract the product names
    data = response.json()
    products = data['d']['results']

    return {product['Name'] for product in products}


app = FastAPI()

@app.get("/api/query")
async def process_query_fastapi(question: str):
    if not question:
        return JSONResponse(content={"error": "Please provide a valid question in the request body"}, status_code=400)

    result = process_query(question, property_keyword_mapping)
    return result["answer"]


def process_query_http(req: func.HttpRequest) -> func.HttpResponse:
    question = req.params.get("question")

    if question is None:
        return func.HttpResponse(
            "Please provide a valid question in the request body",
            status_code=400
        )

    result = process_query(question, property_keyword_mapping)

    response_body = {
        'answer': result["answer"]
    }

    return func.HttpResponse(
        body=json.dumps(response_body, ensure_ascii=False),  # Add ensure_ascii=False to handle special characters
        status_code=200,
        headers={
            'Content-Type': 'application/json'
        }
    )


def process_query(question: str, property_keyword_mapping: dict):
    product_filter, property_filter = extract_filter_keyword(question)
    
    products = fetch_product_data(product_filter, property_filter, question)

    if not products:
        # If no matching products are found, use GPT-3.5-turbo to process the question
        result = process_product_data_with_gpt35turbo([], question)
        return {"answer": result["processed_data"]}

    if property_filter:
        # If a property filter is found, answer the question based on the property
        product_property_key = property_keyword_mapping[property_filter.lower()]
        product_property_values = []
        for product in products:
            value = product.get(product_property_key)
            if value is not None:
                product_property_values.append(str(value))
        if product_property_values:
            # Ensure that the answer is properly formatted
            product_name = products[0].get("Name")
            answer = f"The {property_filter} of the {product_name} is: {', '.join(product_property_values)}."
        else:
            answer = f"No {property_filter} information is available for the {product_filter}."
    else:
        # If no property filter is found, use GPT-3.5-turbo to process the question
        result = process_product_data_with_gpt35turbo(products, question)
        answer = result["processed_data"]

    return {"answer": answer}

def get_product_by_id(product_id: str) -> Optional[Dict]:
    all_products = get_products()

    # Check if the input product ID is a valid ID
    for product in all_products:
        if product["Id"] == product_id:
            return product

    # If the input product ID is not a valid ID, assume it is a product name and call get_product_by_name()
    return get_product_by_name(product_id)


def get_product_by_name(product_name: str):
    # Fetch all products
    all_products = get_products()

    # Find the product with the given name
    for product in all_products:
        if product["Name"].lower() == product_name.lower():
            return product

    # If the product is not found, return None
    return None

def get_product_by_id_or_name(product_id_or_name: str) -> Optional[Dict[str, Any]]:
    headers = {'Accept': 'application/json'}
    filter_url = f"{ODATA_URL}?$filter=(Id eq '{product_id_or_name}' or Name eq '{product_id_or_name}')"
    
    response = requests.get(filter_url, headers=headers, auth=(odata_user, odata_password))
    response.raise_for_status()

    # Parse the JSON response and extract the product information
    data = response.json()
    products = data['d']['results']
    
    if len(products) > 0:
        return products[0]
    else:
        return None

property_keyword_mapping = {
    "average rating": "AverageRating",
    "stock quantity": "StockQuantity",
    "currency code": "CurrencyCode",
    "dimension depth": "DimensionDepth",
    "dimension height": "DimensionHeight",
    "dimension width": "DimensionWidth",
    "review": "Review",
    "product id": "Id",
    "image url": "ImageUrl",
    "is favorite": "IsFavoriteOfCurrentUser",
    "last modified": "LastModified",
    "main category": "MainCategoryId",
    "measure unit": "MeasureUnit",
    "price": "Price",
    "quantity unit": "QuantityUnit",
    "rating count": "RatingCount",
    "sub category": "SubCategoryId",
    "weight measure": "WeightMeasure",
    "weight unit": "WeightUnit",
    "description": "Description",
    "name": "Name",
    "supplier id": "SupplierId",
    "supplier name": "SupplierName"
}

def extract_filter_keyword(question: str) -> Tuple[Optional[str], Optional[str]]:
    question_lower = question.lower()

    # First, check if the question contains a product ID
    product_id = next((word for word in question.split() if (len(word) == 7 and word[:2].isalpha() and word[2] == '-' and word[3:].isdigit())), None)

    if product_id:
        product = get_product_by_id_or_name(product_id)
        if product:
            product_name = product['Name']
        else:
            product_name = None
    else:
        product_name = None

    property_keyword = None
    for kw in property_keyword_mapping.keys():
        kw_lower = kw.lower()
        if kw_lower in question_lower:
            # Check if there's a longer keyword that matches the question
            longer_keyword = next((long_kw for long_kw in property_keyword_mapping.keys() if long_kw.lower() != kw_lower and kw_lower in long_kw.lower() and long_kw.lower() in question_lower), None)
            if longer_keyword is None:
                property_keyword = kw
                break

    if property_keyword:
        property_keyword = next((kw for kw in property_keyword_mapping.keys() if kw.lower() == property_keyword.lower()), property_keyword)

    # If there is no product ID, check if the question contains a product name
    if not product_id:
        product_names = fetch_product_names()
        product_name = next((name for name in product_names if name.lower() in question_lower), product_name)

    return product_name, property_keyword



def get_products(filter_keyword=None, filter_id=None):
    headers = {'Accept': 'application/json'}

    if filter_id:
        filter_url = f"{ODATA_URL}?$filter=Id eq '{filter_id}'"
    elif filter_keyword:
        filter_url = f"{ODATA_URL}?$filter=Name eq '{filter_keyword}'"
    else:
        filter_url = ODATA_URL

    response = requests.get(filter_url, headers=headers, auth=(odata_user, odata_password))
    response.raise_for_status()

    # Parse the JSON response
    data = response.json()

    # Extract the product information and convert it into a list of dictionaries
    products = data['d']['results']

    return products

def process_product_data_with_gpt35turbo(products_info: list[dict], question: str):
    doc = nlp(question)
    intent = ''
    for token in doc:
        if token.pos_ == 'VERB':
            intent = token.lemma_
            break

    formatted_products_info = "\n".join([f"Product {i + 1}: {json.dumps(product_info)}" for i, product_info in enumerate(products_info)])

    openai_response = openai.Completion.create(
        engine="",
        prompt=f"Product data:\n{formatted_products_info}\n\nQuestion: {question}\n\nAnswer:",
        temperature=0.1,
        max_tokens=500,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0,
        n=1,
        stop=["\n"],
    )
        
    # Call the OpenAI AP
    if hasattr(openai_response, "choices"):
        choices = openai_response.choices   # type: ignore
        if choices:
            response_text = choices[0].text.strip()

            # Extract only the answer portion of the response
            answer_start = response_text.find("Answer:")
            if answer_start != -1:
                response_text = response_text[answer_start + 7:].strip()

            # Remove unrelated information
            irrelevant_info_start = response_text.find("In [ ]:")
            if irrelevant_info_start != -1:
                response_text = response_text[:irrelevant_info_start].strip()

            return {"processed_data": response_text}
        else:
            return {"processed_data": "No response from OpenAI"}
    else:
        return {"processed_data": "Response object has no 'choices' attribute"}