PS C:\Users\JohnBlack\AresNet\ops\taiga-mcp> from mcp.client.streamable_http import streamablehttp_client
>> import asyncio, mcp
>>
>> MCP_URL = "https://taiga-mcp.politeground-c43f6662.eastus.azurecontainerapps.io/mcp"
>>
>> async def main():
>>     async with streamablehttp_client(MCP_URL) as (reader, writer, _):
>>         async with mcp.ClientSession(reader, writer) as session:
>>             await session.initialize()
>>             result = await session.call_tool("echo", {"message": "test"})
>>             print(result.model_dump())
>>
>> asyncio.run(main())
ParserError: 
Line |
   1 |  from mcp.client.streamable_http import streamablehttp_client
     |  ~~~~
     | The 'from' keyword is not supported in this version of the language.
PS C:\Users\JohnBlack\AresNet\ops\taiga-mcp> 