import asyncio
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client

server_params = StdioServerParameters(command="mcp", args=["run", "server.py"], env=None)


def extract_content(payload):
    """Best-effort to pull text from MCP responses."""
    if hasattr(payload, "contents"):
        contents = payload.contents
        if contents:
            first = contents[0]
            if hasattr(first, "text"):
                return first.text
            if isinstance(first, dict) and "text" in first:
                return first["text"]
            return str(first)
    if hasattr(payload, "content"):
        content = payload.content
        if isinstance(content, list) and content:
            first = content[0]
            if hasattr(first, "text"):
                return first.text
            return str(first)
        return str(content)
    return str(payload)


async def run():
    async with stdio_client(server_params) as (read, write):
        async with ClientSession(read, write) as session:
            await session.initialize()

            resources = await session.list_resources()
            print("Resources:")
            for resource in resources.resources:
                print(f"- {resource.uri}")

            templates = await session.list_resource_templates()
            print("\nResource templates:")
            for tmpl in templates.resourceTemplates:
                print(f"- {tmpl.uriTemplate}")

            tools = await session.list_tools()
            print("\nTools:")
            for tool in tools.tools:
                print(f"- {tool.name}")

            greeting_payload = await session.read_resource("greeting://hello")
            print(f"\nGreeting: {extract_content(greeting_payload)}")

            add_result = await session.call_tool("add", arguments={"a": 1, "b": 7})
            print(f"\nAdd result: {extract_content(add_result)}")


if __name__ == "__main__":
    asyncio.run(run())
