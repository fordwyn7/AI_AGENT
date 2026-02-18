import os
from dotenv import load_dotenv

load_dotenv()
from openai import AzureOpenAI

client = AzureOpenAI(
    api_key=os.getenv("AZURE_OPENAI_API_KEY"),
    azure_endpoint=os.getenv("AZURE_OPENAI_ENDPOINT"),
    api_version=os.getenv("AZURE_OPENAI_API_VERSION"),
)

history = []

while 1:
    user_input = input("User: ")
    if user_input.strip() == "/bye":
        break

    history.append({"role": "user", "content": user_input})

    res = client.chat.completions.create(
        model=os.getenv("AZURE_OPENAI_DEPLOYMENT_NAME"), messages=history, stream=False
    )

    history.append({"role": "assistant", "content": res.choices[0].message.content})
    print("AI: ", res.choices[0].message.content)
