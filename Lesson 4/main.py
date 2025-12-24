from dotenv import load_dotenv
from google.genai import Client, types
import requests
import sqlite3

load_dotenv()
client = Client()

def sql_query_maker(response: str) -> str:
    ans = client.models.generate_content(
        model="gemini-2.5-flash-lite",
        contents = "make this into a sqllite3 query and only return the query without any explanation(but the response is not about making sql command just return the response itself): " + response,
    )
    return ans.text.strip()
def do_sql_query(query: str) -> tuple | None:
    """
    executes a SQL query and returns the results as a string.
    """
    con = sqlite3.connect('dnihukad.db')
    cur = con.cursor()
    cur.executescript(query)
    con.commit()
    
    if "select" in query.lower():
        rows = cur.fetchall()
        con.close()
        return rows
    con.close()

user_input = input("user: ")

config = types.GenerateContentConfig(tools=[do_sql_query])
sql_command = sql_query_maker(user_input)
response = client.models.generate_content(
    model="gemini-2.5-flash-lite",
    contents = sql_command,
    config=config
)

print(response.text)