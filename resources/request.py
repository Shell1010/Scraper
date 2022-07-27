import aiohttp
import asyncio
import uvloop




uvloop.install()



class RequestMaker:
    def __init__(self, loop=asyncio.get_event_loop(), *args, **kwargs):
        self.loop = loop

        self._await = self.loop.run_until_complete
        self.closed = False
        self.args, self.kwargs = args, kwargs


    # Creates original aiohttp session
    async def create_session(self, args, kwargs):
        self.closed = False
        self.session = aiohttp.ClientSession(*args, **kwargs)

    # Main thing you wanna use for sending reqs, returns [aiohttp.ClientResponse] Object
    async def request_pool(self, RequestContexts: list[aiohttp.RequestInfo]):
        return await asyncio.gather(*(self.request(**ctx) for ctx in RequestContexts ))


    # Helper method so session.request is async - isn't originally
    async def request(self, method: str, url: str, **kwargs):
        return await self.session.request(method, url, **kwargs)

    # Returns json response for every item in [aiohttp.ClientResponse]
    async def response_pool_json_sync(self, Response: list[aiohttp.ClientResponse]):
        return await asyncio.gather(*(resp.json() for resp in Response))


    # Returns text response for every item in [aiohttp.ClientResponse]
    async def response_pool_text_sync(self, Response: list[aiohttp.ClientResponse]):
        return await asyncio.gather(*(resp.text()for resp in Response))

    # Helper method so resp.status is async - isn't originally
    async def get_status(self, Response: aiohttp.ClientResponse):
        return Response.status

    # Returns status code response for every item in [aiohttp.ClientResponse]
    async def response_pool_status_sync(self, Response: list[aiohttp.ClientResponse]):
        return await asyncio.gather(*(self.get_status(resp) for resp in Response))





    # Used for the async with context manager, required for creating the original session and passing args to aiohttp.ClientSession
    async def __aenter__(self, *args, **kwargs):
        # print(self.args, self.kwargs, "HERE HERE HERE")
        await self.create_session(self.args, self.kwargs)

    # User upon exiting the context manager, required for closing all aiohttp sessions
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await self.session.close()
        self.session = None
        self.closed = True

    # Code for close, basically closes everything real



