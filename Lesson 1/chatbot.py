import os
import json
from google import genai
from dotenv import load_dotenv

load_dotenv('.env')
client = genai.Client()

history_file = 'chat_history.json'

def load_history():
    if os.path.exists(history_file):
        with open(history_file, 'r') as f:
            return json.load(f)
    return []

def save_history(history):
    with open(history_file, 'w') as f:
        json.dump(history, f, indent=2)



history = load_history()
user_input = input("USER: ")
while user_input != "exit":
    
    history.append({"role": "user", "parts": [{"text": user_input}]})
    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=history,
    )
    print("AI:", response.text)
    history.append({"role": "model", "parts": [{"text": response.text}]})
    save_history(history)
    user_input = input("USER: ")

