import asyncio
import json
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client
from openai import OpenAI
import os
from dotenv import load_dotenv
 
load_dotenv()
llm = OpenAI(base_url="https://openrouter.ai/api/v1", api_key=os.getenv("OPENROUTER_API_KEY"))
 
def mcp_tools_to_openai_format(mcp_tools) -> list[dict]:
    """Convert MCP tool definitions to OpenAI-compatible format."""
    return [
        {
            "type": "function",
            "function": {
                "name": t.name,
                "description": t.description,
                "parameters": t.inputSchema
            }
        }
        for t in mcp_tools
    ]
 
async def run_mcp_agent(user_request: str):
    server_params = StdioServerParameters(
        command="uv",
        args=["run", "hirestream_mcp_server.py"]
    )
 
    async with stdio_client(server_params) as (read, write):
        async with ClientSession(read, write) as session:
            await session.initialize()
 
            # Discover tools dynamically - no hardcoding
            mcp_tools = (await session.list_tools()).tools
            openai_tools = mcp_tools_to_openai_format(mcp_tools)
            print(f"Connected. Available tools: {[t.name for t in mcp_tools]}")
 
            messages = [
                {"role": "system", "content": "You are a HireStream screening assistant. Use the available tools to answer requests."},
                {"role": "user", "content": user_request}
            ]
 
            for _ in range(5):
                response = llm.chat.completions.create(
                    model="openai/gpt-oss-20b:free",
                    messages=messages,
                    tools=openai_tools,
                    tool_choice="auto"
                )
                msg = response.choices[0].message
                if not msg.tool_calls:
                    print(f"\nAgent: {msg.content}")
                    return
 
                messages.append({
                    "role": "assistant",
                    "content": msg.content,
                    "tool_calls": [{"id": tc.id, "type": "function", "function": {"name": tc.function.name, "arguments": tc.function.arguments}} for tc in msg.tool_calls]
                })
 
                for tc in msg.tool_calls:
                    args = json.loads(tc.function.arguments)
                    # Call through MCP session - not direct function call
                    result = await session.call_tool(tc.function.name, args)
                    result_text = result.content[0].text if result.content else "No result"
                    messages.append({"role": "tool", "tool_call_id": tc.id, "content": result_text})
 
if __name__ == "__main__":
    asyncio.run(run_mcp_agent("Get the job description for SWE-042"))
