# from dotenv import load_dotenv
# from google.genai import Client, types
# import requests

# load_dotenv()
# # res = requests.get("https://jsonplaceholder.typicode.com/users")
# # info = res.json()

# def mul(a: float, b: float) -> float:
#     return a * b
# mul_fc_def = {
#     "name": "mul",
#     "description": "Multiplies two numbers together.",
#     "parameters": {
#         "type": "object",
#         "properties": {
#             "a": {
#                 "type": "number",
#                 "description": "First number",
#             },
#             "b": {
#                 "type": "number",
#                 "description": "second number",
#             },
#         },
#         "required": ["a", "b"],
#     },
# } 
# user_input = "what is 324325324 times 43254325?"
# tools = types.Tool(function_declarations=[mul_fc_def])
# config = types.GenerateContentConfig(tools=[tools])
# client = Client()
# response = client.models.generate_content(
#     model="gemini-2.5-flash",
#     contents = user_input,
#     config=config
# )
# res = response.candidates[0].content.parts[0]
# print(res.function_call)
# if res.function_call is None:
#     print(res.text)
# else:
#     print(res.function_call.name)
#     print(mul(**res.function_call.args))









# from dotenv import load_dotenv
# from google.genai import Client, types
# import requests

# load_dotenv()
# client = Client()

# # res = requests.get("https://jsonplaceholder.typicode.com/users")
# # info = res.json()

# def mul(a: float, b: float) -> float:
#     """
#     Multiplys two numbers together and returns the result.
#     """
#     return int(a * b)

# user_input = "what is 324325324 times 43254325?"

# config = types.GenerateContentConfig(tools=[mul])

# response = client.models.generate_content(
#     model="gemini-2.5-flash",
#     contents = user_input,
#     config=config
# )

# print(response.text)