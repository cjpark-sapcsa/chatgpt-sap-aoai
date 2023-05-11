// Copyright (c) Microsoft Corporation. All rights reserved.
// Licensed under the MIT License.
//
// Generated with Bot Builder V4 SDK Template for Visual Studio EchoBot v4.18.1

using System;
using System.Net.Http;
using System.Threading;
using System.Threading.Tasks;
using Microsoft.Bot.Builder;
using Microsoft.Bot.Schema;
using Microsoft.Extensions.Logging;
using Newtonsoft.Json;

namespace EPM_OData_Bot_GPT
{
    public class EchoBot : ActivityHandler
    {
        private readonly ILogger<EchoBot> _logger;
        private readonly IHttpClientFactory _httpClientFactory;

        public EchoBot(ILogger<EchoBot> logger, IHttpClientFactory httpClientFactory)
        {
            _logger = logger;
            _httpClientFactory = httpClientFactory;
        }

        protected override async Task OnMessageActivityAsync(ITurnContext<IMessageActivity> turnContext, CancellationToken cancellationToken)
        {
            string userMessage = turnContext.Activity.Text.Trim().ToLower();

            // Check if the user message starts with "product "
            if (userMessage.StartsWith("product "))
            {
                // Get the product ID from the user message
                string product_id = userMessage.Substring(8);

                string responseMessage = await CallLocalAPIAsync(product_id);
                await turnContext.SendActivityAsync(MessageFactory.Text(responseMessage), cancellationToken);
            }
            else
            {
                // If the user message does not start with "product ", send a default response
                await turnContext.SendActivityAsync(MessageFactory.Text("Please enter a valid product ID."), cancellationToken);
            }
        }

        private async Task<string> CallLocalAPIAsync(string product_id)
        {
            try
            {
                string apiUrl = $"";
                var httpClient = _httpClientFactory.CreateClient();

                // Log apiUrl here
                _logger.LogInformation("Request URL: {0}", apiUrl);
                _logger.LogDebug("Debug message: Request URL is logged.");

                var response = await httpClient.GetAsync(apiUrl, CancellationToken.None);

                if (response.IsSuccessStatusCode)
                {
                    string responseText = await response.Content.ReadAsStringAsync();
                    var responseObject = JsonConvert.DeserializeObject<dynamic>(responseText);

                    // Process the product data
                    string productName = responseObject.Name;
                    string productDescription = responseObject.Description;
                    string productPrice = responseObject.Price;
                    string currencyCode = responseObject.CurrencyCode;
                    string stockQuantity = responseObject.StockQuantity;

                    // Construct the response message
                    string responseMessage = $"Product Name: {productName}\nDescription: {productDescription}\nPrice: {productPrice} {currencyCode}\nStock Quantity: {stockQuantity}";

                    return responseMessage;
                }
                else
                {
                    _logger.LogWarning("Error in CallLocalAPIAsync - Status Code: {0}", response.StatusCode);
                    throw new Exception("Error: " + response.StatusCode);
                }
            }
            catch (Exception ex)
            {
                _logger.LogError(ex, "Error in CallLocalAPIAsync");
                throw;
            }
        }
    }
}