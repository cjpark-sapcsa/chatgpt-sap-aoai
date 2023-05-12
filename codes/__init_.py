import azure.functions as func
import json
from .main import process_query_http  # Make sure to import the process_query_http function

async def main(req: func.HttpRequest) -> func.HttpResponse:
    question = req.params.get("question")
    if not question:
        return func.HttpResponse(
            "Please pass a question in the query string",
            status_code=400
        )

    response = process_query_http(req)

    return func.HttpResponse(
        response.get_body(),
        status_code=response.status_code,
        headers={"Content-Type": "application/json"}
    )

