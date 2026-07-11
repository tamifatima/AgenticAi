from langchain_mcp_adapters import MultiServerMCPClient
from langgraph.prebuilt import create_react_agent
from langchain_groq import ChatGroq


from dotenv import load_dotenv
load_dotenv()

import asyncio

async def main():
    client=MultiServerMCPClient(
        {
            "math":{
                "command":"python",
                "args":["mathserver.py"],## ensure correct absolute path
                "transport":"stdio",
            },
            "weather":{
                "url":"http://localhost:8000",# Ensure server is running here
                "transport":"streamable-http",
            },
        }
    )

    import os
    os.environ["GROQ_API_KEY"] = os.getenv("GROQ_API_KEY")

    tools=await client.get_tools()
    model=ChatGroq(model="llama3-8b-8192")
    agent=create_react_agent(model,tools)


    math_response=await agent.ainvoke(
        {"messages":[{"role":"user","content":"What is 2+2?"}]}
    )

    print(math_response["messages"][-1].content)