import asyncio
import sys
from pathlib import Path

from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client

TICKER_LIST = """
DBS Group Holdings Ltd (D05.SI)
Oversea-Chinese Banking Corporation Limited (O39.SI)
Singapore Exchange Limited (S68.SI)
United Overseas Bank Limited (U11.SI)
NetLink NBN Trust (CJLU.SI)
Sembcorp Industries Ltd (U96.SI)
Sheng Siong Group Ltd (OV8.SI)
Singapore Technologies Engineering Ltd (S63.SI)
Singapore Telecommunications Limited (Z74.SI)
Amova-StraitsTrading Asia ex Japan REIT Index ETF (CFA.SI)
CapitaLand Ascendas REIT (A17U.SI)
CapitaLand Integrated Commercial Trust (C38U.SI)
CSOP iEdge S-REIT Leaders Index ETF (SRT.SI)
ESR REIT (9A4U.SI)
Frasers Centrepoint Trust (J69U.SI)
Keppel DC REIT (AJBU.SI)
Lion-Phillip S-REIT ETF (CLR.SI)
Mapletree Industrial Trust (ME8U.SI)
Mapletree Pan Asia Commercial Trust (N2IU.SI)
Parkway Life Real Estate Investment Trust (C2PU.SI)
Suntec Real Estate Investment Trust (T82U.SI)
"""


async def main():
    uvx = Path(sys.executable).with_name("uvx")
    server_params = StdioServerParameters(command=str(uvx), args=["mcp-yahoo-finance"])

    async with stdio_client(server_params) as (read, write):
        async with ClientSession(read, write) as session:
            await session.initialize()

            for ticker in extract_tickers(TICKER_LIST):
                result = await session.call_tool("get_current_stock_price", {"symbol": ticker})
                print(f"{result.content[0].text}")


def extract_tickers(ticker_list: str) -> list[str]:
    tickers = []
    for line in ticker_list.splitlines():
        line = line.strip()
        if line:
            tickers.append(line.rsplit("(", 1)[1].rstrip(")"))
    return tickers


if __name__ == "__main__":
    asyncio.run(main())
