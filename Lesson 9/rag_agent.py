# type: ignore
import os
from openai import AzureOpenAI
from dotenv import load_dotenv
import json

load_dotenv()

from azure.core.credentials import AzureKeyCredential
from azure.search.documents import SearchClient

service_endpoint = os.environ["AZURE_SEARCH_SERVICE_ENDPOINT"]
index_name = os.environ["AZURE_SEARCH_INDEX_NAME"]
search_key = os.environ["AZURE_SEARCH_API_KEY"]

search_client = SearchClient(service_endpoint, index_name, AzureKeyCredential(search_key))

def az_ai_retrieve(query: str):
    results = search_client.search(search_text=query)
    text = ''
    for result in results:
        text += f"Source: {result['title']} \n Content: {result['chunk']}\n\n"
    
    return text

tools = [
    {
        "type": "function",
        "function": {
            "name": "az_ai_retrieve",
           "description": "Retrieves authoritative travel information from the knowledge base. Required for all travel queries.",
            "parameters": {
                "type": "object",
                "properties": {
                    "query": {
                        "type": "string",
                        "description": "The search query to find relevant travel documents"
                    }
                },
                "required": ["query"]
            }
        }
    }
]

available_functions = {
    "az_ai_retrieve": az_ai_retrieve
}

client = AzureOpenAI(
    api_key=os.environ["AZURE_OPENAI_API_KEY"],
    api_version="2024-10-21", 
    azure_endpoint=os.environ["AZURE_OPENAI_ENDPOINT"]
)

messages = [
    {
        "role": "system",
        "content": """You are a RAG assistant.
            You MUST always call the provided tool to answer the user's question.
            When answering, give references to the sources by the tool."""
    },
    {
        "role": "user",
        "content": "What is the best place to travel?"
    }
]

response = client.chat.completions.create(
    model=os.environ["AZURE_OPENAI_DEPLOYMENT_NAME"],
    messages=messages,
    tools=tools,
    tool_choice="auto"
)

response_message = response.choices[0].message

if response_message.tool_calls:
    messages.append(response_message)
    
    for tool_call in response_message.tool_calls:
        function_name = tool_call.function.name
        function_args = json.loads(tool_call.function.arguments)
        function_response = available_functions[function_name](**function_args)
        
        messages.append({
            "role": "tool",
            "tool_call_id": tool_call.id,
            "content": function_response
        })
    
    final_response = client.chat.completions.create(
        model=os.environ["AZURE_OPENAI_DEPLOYMENT_NAME"],
        messages=messages
    )
    
    print(final_response.choices[0].message.content)
else:
    print(response_message.content)