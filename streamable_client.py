"""Utility script to exercise the Taiga MCP Streamable HTTP endpoint."""

from __future__ import annotations

import argparse
import asyncio
from typing import Any

import mcp
from mcp.client.streamable_http import streamablehttp_client


async def call_echo(mcp_url: str, message: str) -> dict[str, Any]:
    async with streamablehttp_client(mcp_url) as (reader, writer, _):
        async with mcp.ClientSession(reader, writer) as session:
            await session.initialize()
            response = await session.call_tool("echo", {"message": message})
            return response.model_dump()


async def main() -> None:
    parser = argparse.ArgumentParser(description="Invoke the Taiga MCP echo tool over Streamable HTTP.")
    parser.add_argument(
        "mcp_url",
        nargs="?",
        default="https://taiga-mcp.politeground-c43f6662.eastus.azurecontainerapps.io/mcp",
        help="MCP Streamable HTTP endpoint to target.",
    )
    parser.add_argument("--message", default="test", help="Message to send to the echo tool.")
    args = parser.parse_args()

    result = await call_echo(args.mcp_url, args.message)
    print(result)


if __name__ == "__main__":
    asyncio.run(main())
