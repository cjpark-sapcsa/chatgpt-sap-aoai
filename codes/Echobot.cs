// Copyright (c) Microsoft Corporation. All rights reserved.
// Licensed under the MIT License.
//
// Generated with Bot Builder V4 SDK Template for Visual Studio EchoBot v4.18.1
using Microsoft.Bot.Builder;
using Microsoft.Bot.Schema;
using Newtonsoft.Json;
using Newtonsoft.Json.Linq;
using System;
using System.Collections.Generic;
using System.Net.Http;
using System.Threading;
using System.Threading.Tasks;

namespace odata_es4_nlu.Bots
{
    public class EchoBot : ActivityHandler
    {
        private readonly HttpClient _httpClient = new HttpClient();
        private readonly string _azureFunctionUrl = ""; 

        protected override async Task OnMessageActivityAsync(ITurnContext<IMessageActivity> turnContext, CancellationToken cancellationToken)
        {
            var userInput = turnContext.Activity.Text;
            var response = await _httpClient.GetAsync($"{_azureFunctionUrl}&question={Uri.EscapeDataString(userInput)}");

            if (!response.IsSuccessStatusCode)
            {
                var errorMessage = "Error: Unable to connect to Azure Function.";
                await turnContext.SendActivityAsync(MessageFactory.Text(errorMessage, errorMessage), cancellationToken);
                return;
            }

            var jsonResponse = await response.Content.ReadAsStringAsync();
            Console.WriteLine("JSON response: " + jsonResponse);

            if (jsonResponse.StartsWith("{"))
            {
                try
                {
                    var responseObject = JObject.Parse(jsonResponse);

                    if (responseObject != null && responseObject["answer"] != null)
                    {
                        var replyText = responseObject["answer"].ToString();
                        await turnContext.SendActivityAsync(MessageFactory.Text(replyText, replyText), cancellationToken);
                    }
                    else
                    {
                        var errorMessage = "Error: Unexpected response from Azure Function.";
                        await turnContext.SendActivityAsync(MessageFactory.Text(errorMessage, errorMessage), cancellationToken);
                    }
                }
                catch (JsonReaderException)
                {
                    var errorMessage = "Error: The received JSON response is not in the correct format.";
                    await turnContext.SendActivityAsync(MessageFactory.Text(errorMessage, errorMessage), cancellationToken);
                }
                catch (Exception)
                {
                    var errorMessage = "Error processing response.";
                    await turnContext.SendActivityAsync(MessageFactory.Text(errorMessage, errorMessage), cancellationToken);
                }
            }
            else
            {
                var errorMessage = "Error: The received JSON response is not in the correct format.";
                await turnContext.SendActivityAsync(MessageFactory.Text(errorMessage, errorMessage), cancellationToken);
            }
        }

        protected override async Task OnMembersAddedAsync(IList<ChannelAccount> membersAdded, ITurnContext<IConversationUpdateActivity> turnContext, CancellationToken cancellationToken)
        {
            foreach (var member in membersAdded)
            {
                if (member.Id != turnContext.Activity.Recipient.Id)
                {
                    var welcomeText = "Hello and welcome to SAP ES5Bot Powered by GPT!";
                    await turnContext.SendActivityAsync(MessageFactory.Text(welcomeText, welcomeText), cancellationToken);
                }
            }
        }
    }
}
