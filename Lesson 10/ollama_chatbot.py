# 1st way
from ollama import chat

history = []

while 1:
    user_input = input("User: ")
    if user_input.strip() == "/bye":
        break
    history.append(
        {
            "role" : "user",
            "content" : user_input
        }
    )
    res = chat(model="gemma2:2b", messages=history)
    history.append(
        {
            "role" : "assistant",
            "content" : res.message.content
        }
    )
    print(res.message.content)
    
#2nd way
import os
from dotenv import load_dotenv

load_dotenv()
from openai import OpenAI

client = OpenAI(base_url="http://localhost:11434/v1", api_key="gemma2:2b")

history = []

while 1:
    user_input = input("User: ")
    if user_input.strip() == "/bye":
        break

    history.append({"role": "user", "content": user_input})

    res = client.chat.completions.create(
        model="gemma2:2b", messages=history, stream=False
    )

    history.append({"role": "assistant", "content": res.choices[0].message.content})
    print("AI: ", res.choices[0].message.content)
