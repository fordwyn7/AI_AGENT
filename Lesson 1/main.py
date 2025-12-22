from dotenv import load_dotenv

load_dotenv('.env')

from google import genai

client = genai.Client()

user_input = input("USER: ")
while user_input != "exit":
    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=user_input,
    )
    print("AI:", response.text)
    user_input = input("USER: ")