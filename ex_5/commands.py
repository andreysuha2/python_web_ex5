from ex_5.core.commands import CommandList, Command
from ex_5.currency import Currency
from ex_5.server.main import Server as WSServer
import websockets
import asyncio
import aiohttp

class CurrencyUtil(Command):
    DEFAULT_CURRENCIES = [ "USD", "EUR" ]
    
    async def run(self, days, currencies):
        async with aiohttp.ClientSession() as session:
            currency = Currency(base_url='https://api.privatbank.ua', session=session)
            result = await currency.get_currencies(days, currencies)
            return result
            
    
    def execute(self, *args):
        days = int(args[0] if len(args) > 0 else 1)
        currencies = args[1:]
        if days > 10:
            return 'Max days 10'
        return asyncio.run(self.run(days, [ *currencies, *self.DEFAULT_CURRENCIES ]))
    
class Server(Command):
    async def run(self):
        server = WSServer()
        async with websockets.serve(server.ws_handler, "localhost", 8000):
            await asyncio.Future()
            
    
    def execute(self):
        asyncio.run(self.run())
    
commands_list = CommandList(commands={ "currency": CurrencyUtil(), "serve": Server() })