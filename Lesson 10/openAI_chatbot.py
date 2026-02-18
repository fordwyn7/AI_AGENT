import os
from dotenv import load_dotenv

load_dotenv()
from openai import OpenAI

client = OpenAI()

history = []

while 1:
    user_input = input("User: ")
    if user_input.strip() == "/bye":
        break

    history.append({"role": "user", "content": user_input})

    res = client.chat.completions.create(
        model="gpt-4.1-mini", messages=history, stream=False
    )

    history.append({"role": "assistant", "content": res.choices[0].message.content})
    print("AI: ", res.choices[0].message.content)
