from mcp.server.fastmcp import FastMCP
from dotenv import load_dotenv
from google.genai import Client, types
import sqlite3
import os


load_dotenv()
client = Client()
mcp = FastMCP('query_database')

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, "test.db")


def sql_query_maker(response: str) -> str:
    ans = client.models.generate_content(
        model="gemini-2.5-flash-lite",
        contents = "make this user query into a sqlite3 query and only return the sql query without any explanations(return the response itself that can be directly executed): " + response,
    )
    return ans.text.strip()
# @mcp.tool()
# def subtract(a: float, b: float) -> float:
#     """subtract two numbers. and return the result."""
#     return a - b
@mcp.tool()
def do_sql_query(query: str) -> list | None | str:
    """
    takes user query as input, and makes a sql query using an LLM, then
    executes a SQL query and returns the results.
    """
    con = sqlite3.connect(DB_PATH)
    cur = con.cursor()
    
    
    if "select" in query.lower():
        cur.execute(query)
        rows = cur.fetchall()
        con.close()
        return rows
    cur.executescript(query)
    con.commit()
    con.close()
    return "Query executed successfully."

if __name__ == '__main__':
    mcp.run(transport='stdio')