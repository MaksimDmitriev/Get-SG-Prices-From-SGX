import asyncio
import sys
from pathlib import Path

from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client

TICKERS = (
    "C2PU.SI",
    "A17U.SI",
)


async def main():
    uvx = Path(sys.executable).with_name("uvx")
    server_params = StdioServerParameters(command=str(uvx), args=["mcp-yahoo-finance"])

    async with stdio_client(server_params) as (read, write):
        async with ClientSession(read, write) as session:
            await session.initialize()

            for ticker in TICKERS:
                result = await session.call_tool("get_current_stock_price", {"symbol": ticker})
                print(f"{ticker}\t{result.content[0].text}")


if __name__ == "__main__":
    asyncio.run(main())
