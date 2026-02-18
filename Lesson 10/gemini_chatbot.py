import os
from dotenv import load_dotenv;load_dotenv()
from google.genai import Client

client = Client()
chat = client.chats.create(model="gemini-2.5-flash", history=[])

while 1:
    user_input = input("User: ")
    if user_input.strip() == "/bye":
        break
    res = chat.send_message(message=user_input)
    print("Ai:", res.text)
