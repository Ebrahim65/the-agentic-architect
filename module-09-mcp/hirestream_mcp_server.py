"""
HireStream MCP Server - exposes CV processing tools via MCP protocol.
Run with: uv run hirestream_mcp_server.py
Inspect with: npx @modelcontextprotocol/inspector uv run hirestream_mcp_server.py
"""
 
import json
from mcp.server import Server
from mcp.server.stdio import stdio_server
from mcp.types import Tool, TextContent
import asyncio
 
# Create server instance
server = Server("hirestream")
 
# In-memory store for this example
JOB_DESCRIPTIONS = {
    "SWE-042": "Senior Software Engineer: 5+ years Python, cloud infrastructure (AWS/GCP), CI/CD pipelines..."
}
 
@server.list_tools()
async def list_tools() -> list[Tool]:
    """Declare all tools this server exposes."""
    return [
        Tool(
            name="get_job_description",
            description="Retrieve the full description for a job by its ID. Use when you need the requirements to score a candidate.",
            inputSchema={
                "type": "object",
                "properties": {
                    "job_id": {"type": "string", "description": "The job identifier, e.g. 'SWE-042'"}
                },
                "required": ["job_id"]
            }
        ),
        Tool(
            name="save_screening_result",
            description="Save a candidate screening result to the HireStream system.",
            inputSchema={
                "type": "object",
                "properties": {
                    "candidate_name": {"type": "string"},
                    "job_id": {"type": "string"},
                    "score": {"type": "integer", "minimum": 0, "maximum": 100},
                    "recommendation": {"type": "string", "enum": ["advance", "hold", "decline"]},
                    "notes": {"type": "string"}
                },
                "required": ["candidate_name", "job_id", "score", "recommendation"]
            }
        )
    ]
 
@server.call_tool()
async def call_tool(name: str, arguments: dict) -> list[TextContent]:
    """Handle tool calls from MCP clients."""
 
    if name == "get_job_description":
        job_id = arguments["job_id"]
        description = JOB_DESCRIPTIONS.get(job_id)
        if description:
            return [TextContent(type="text", text=f"Job {job_id}:\n{description}")]
        return [TextContent(type="text", text=f"Job ID '{job_id}' not found.")]
 
    elif name == "save_screening_result":
        # In production, this writes to a database
        result = json.dumps(arguments, indent=2)
        return [TextContent(type="text", text=f"Screening result saved:\n{result}")]
 
    return [TextContent(type="text", text=f"Unknown tool: {name}")]
 
async def main():
    async with stdio_server() as (read_stream, write_stream):
        await server.run(read_stream, write_stream, server.create_initialization_options())
 
if __name__ == "__main__":
    asyncio.run(main())
