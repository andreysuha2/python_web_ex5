from websockets import WebSocketServerProtocol
from websockets.exceptions import ConnectionClosedOK
from ex_5.currency import Currency
import json
import aiohttp
import logging
import names

logging.basicConfig(level=logging.INFO)

class Server:
    clients = set()
    
    def __init__(self) -> None:
        self.commands = { "/exchange": self.exchange } 
    
    async def register(self, ws: WebSocketServerProtocol):
        ws.name = names.get_full_name()
        self.clients.add(ws)
        logging.info(f'{ws.remote_address} connects')
    
    async def exchange(self, *args):
        days = int(args[0] if len(args) > 0 else 1)
        currencies = [ "USD", "EUR" ]
        if days > 10:
            return 'Max days 10'
        async with aiohttp.ClientSession() as session:
            currency = Currency(base_url='https://api.privatbank.ua', session=session)
            result = await currency.get_currencies(days, currencies)
            print(result)
            return json.dumps(result)
    
    async def unregister(self, ws: WebSocketServerProtocol):
        self.clients.remove(ws)
        logging.info(f'{ws.remote_address} disconnects')
        
    async def send_to_clients(self, message: str):
        if self.clients:
            [ await client.send(message) for client in self.clients ]
            
    async def distrubute(self, ws: WebSocketServerProtocol):
        async for message in ws:
            data = message
            words = message.split(" ")
            if words[0] in self.commands:
                data = await self.commands[words[0]](*words[1:])
                await self.send_to_clients(f"{ws.name}: {message}")
            await self.send_to_clients(f"{ws.name}: {data}")        
            
    async def ws_handler(self, ws: WebSocketServerProtocol):
        await self.register(ws)
        try:
            await self.distrubute(ws)
        except ConnectionClosedOK:
            pass
        finally:
            await self.unregister(ws)
            