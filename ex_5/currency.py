from typing import Dict
from datetime import datetime, timedelta
import asyncio
import aiohttp

class RequestException(Exception):
    pass
        
class Currency:    
    def __init__(self, base_url: str, session: aiohttp.ClientSession) -> None:
        self.base_url = base_url
        self.session = session
    
    async def get(self, url, params: Dict) -> str:
        try:
            async with self.session.get(f'{self.base_url}/{url}', params=params) as response:
                if response.status > 400:
                    raise RequestException
                return await response.json()
        except aiohttp.ClientConnectionError as e:
            raise RequestException
    
    async def get_currency(self, date: datetime = datetime.now(), currencies: list = [ "USD", "EUR" ]) -> dict:
        date_str = date.strftime("%d.%m.%Y")
        lst = await self.get("p24api/exchange_rates", { "date": date_str, "currecy": "USD" })
        rates = [ { item["currency"]: { "sale": item["saleRate"], "purchase": item["purchaseRate"] } } for item in lst["exchangeRate"] if item["currency"] in currencies ]
        return { lst["date"]: rates }
        
    
    async def get_currencies(self, days: int = 1, currencies: list = [ "USD", "EUR" ]) -> dict:
        try:
            handlers = [ self.get_currency(datetime.now() - timedelta(days=day), currencies) for day in range(0, days) ]
            return await asyncio.gather(*handlers)
        except RequestException:
            return "Something went wrong. Please try againe later!"    