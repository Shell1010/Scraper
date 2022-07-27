import aiohttp
import asyncio
import time
import uvloop
import inspect
import nest_asyncio


# nest_asyncio.apply()
uvloop.install()



class RequestMaker:
    def __init__(self, loop=asyncio.get_event_loop(), *args, **kwargs):
        self.loop = loop
        # assuming you're going to use https, not socks.
        # self.sema = self.sema = asyncio.BoundedSemaphore(4000)
        # Like await but works in sync
        self._await = self.loop.run_until_complete
        # self._nowait = self.loop.create_task
        self.closed = False
        self.args, self.kwargs = args, kwargs
        

    # Creates original aiohttp session
    async def create_session(self, args, kwargs):
        self.closed = False
        self.session = aiohttp.ClientSession(*args, **kwargs)

    # Main thing you wanna use for sending reqs, returns [aiohttp.ClientResponse] Object
    async def request_pool(self, RequestContexts: list[aiohttp.RequestInfo]):
        return await asyncio.gather(*(self.session.request(**ctx) for ctx in RequestContexts))


    # Returns json response for every item in [aiohttp.ClientResponse]
    async def response_pool_json_sync(self, Response: list[aiohttp.ClientResponse]):
        return await asyncio.gather(resp.json() for resp in Response)


    # Returns text response for every item in [aiohttp.ClientResponse]
    async def response_pool_text_sync(self, Response: list[aiohttp.ClientResponse]):
        return await asyncio.gather(resp.text() for resp in Response)

    # Returns status code response for every item in [aiohttp.ClientResponse]
    async def response_pool_status_sync(self, Response: list[aiohttp.ClientResponse]):
        return await asyncio.gather(resp.status for resp in Response)

    
    


    # Used for the with statement entry thing, basically upon doing with requestmaker: does code here, its pass because I don't really do anything important here
    async def __aenter__(self, *args, **kwargs):
        # print(self.args, self.kwargs, "HERE HERE HERE")
        await self.create_session(self.args, self.kwargs)

    # Upon exiting the with statement it closes session
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await self.session.close()
        self.session = None
        self.closed = True

    # Code for close, basically closes everything real
    


