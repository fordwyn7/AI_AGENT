from langchain_community.document_loaders import TextLoader
from langchain_chroma import Chroma
from langchain_openai import AzureOpenAIEmbeddings
from langchain_text_splitters import RecursiveCharacterTextSplitter
from load_dotenv import load_dotenv

load_dotenv()

file_path = r"C:\Users\rsfor\Desktop\AI AGENT\chunk\tinyshakespeare.txt"
persistent_dir = "db"
az_emb = AzureOpenAIEmbeddings()

loader = TextLoader(file_path=file_path)
docs = loader.load()

# recursive way
# splitter = RecursiveCharacterTextSplitter(
#     chunk_size=1000,
#     chunk_overlap=0, 
#     separators=["\n\n", "\n", ". ", " ", ""]
# )
# chunks = splitter.split_documents(docs)



db = Chroma(persist_directory=persistent_dir,
             collection_name="azure_emb",
             embedding_function=az_emb)

query = "Who is Caius Marcius?"

retriever = db.as_retriever(
    search_type="similarity_score_threshold",
    search_kwargs={"k": 3, "score_threshold": 0.6}
)

selected_chunks = retriever.invoke(query)
print(len(selected_chunks))
# print(selected_chunks[0].page_content)
