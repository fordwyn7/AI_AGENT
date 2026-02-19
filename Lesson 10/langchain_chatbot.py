import os
from dotenv import load_dotenv

load_dotenv()
from langchain_core.messages import HumanMessage, AIMessage, SystemMessage

# gemini
# from langchain_google_genai import ChatGoogleGenerativeAI
# llm = ChatGoogleGenerativeAI(model="gemini-2.5-flash")

# azure openAI
# from langchain_openai import AzureChatOpenAI
# llm = AzureChatOpenAI(
#     api_key=os.getenv("AZURE_OPENAI_API_KEY"),
#     azure_endpoint=os.getenv("AZURE_OPENAI_ENDPOINT"),
#     api_version=os.getenv("AZURE_OPENAI_API_VERSION"),
#     deployment_name=os.getenv("AZURE_OPENAI_DEPLOYMENT_NAME"),
# )

#ollama
# from langchain_ollama import ChatOllama
# llm = ChatOllama(model="gemma2:2b")

#HuggingFace
import torch
from langchain_huggingface import HuggingFacePipeline
from transformers import pipeline, BitsAndBytesConfig 
from transformers import AutoTokenizer, AutoModelForCausalLM  

quantization_config = BitsAndBytesConfig(
    load_in_4bit=True,
    bnb_4bit_quant_type="nf4",
    bnb_4bit_use_double_quant=True,
    bnb_4bit_compute_dtype=torch.float16
)

tokenizer = AutoTokenizer.from_pretrained("microsoft/Phi-4-mini-instruct")
model = AutoModelForCausalLM.from_pretrained("microsoft/Phi-4-mini-instruct", quantization_config=quantization_config)

pipe = pipeline("text-generation", model=model, tokenizer=tokenizer)

llm = HuggingFacePipeline(pipeline=pipe)

history = [
    SystemMessage(content="You are a helpful assistant.")
]

while True:
    user_input = input("User: ")
    if user_input.strip() == "/bye":
        break

    history.append(HumanMessage(content=user_input))

    # LangChain → HF requires STRING
    prompt = "\n".join(m.content for m in history) + "\nAssistant:"
    response = llm.invoke(prompt)

    print("AI:", response)

