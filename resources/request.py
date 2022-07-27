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

        self._await = self.loop.run_until_complete

        self.closed = False

        self._await(self.create_session(*args, **kwargs))

    # Creates original aiohttp session
    async def create_session(self, *args, **kwargs):
        self.closed = False
        self.session = aiohttp.ClientSession(*args, **kwargs)

    # Main thing you wanna use for sending reqs, returns [aiohttp.ClientResponse] Object
    def request_pool_sync(self, RequestContexts: list[aiohttp.RequestInfo]):
        return self._await(
            asyncio.gather(*(self.request(**ctx) for ctx in RequestContexts)))


    # Request func that does the actual request, used in above func
    async def request(self, method: str, url: str, **kwargs):
        return await self.session.request(method, url, **kwargs)

    # Returns json response for every item in [aiohttp.ClientResponse]
    def response_pool_json_sync(self, Response: list[aiohttp.ClientResponse]):
        return self._await(
            asyncio.gather(*(self.resp_json(resp) for resp in Response)))


    # Returns text response for every item in [aiohttp.ClientResponse]
    def response_pool_text_sync(self, Response: list[aiohttp.ClientResponse]):
        return self._await(
            asyncio.gather(*(self.resp_text(resp) for resp in Response)))

    # Returns status code response for every item in [aiohttp.ClientResponse]
    def response_pool_status_sync(self, Response: list[aiohttp.ClientResponse]):
        return self._await(
            asyncio.gather(*(self.resp_status_code(resp) for resp in Response)))



    # Used in the response_pool_text func, used to actually turn the client response into text
    async def resp_text(self, Response: aiohttp.ClientResponse):
        return await Response.text()


    # Used in the response_pool_json func, used to actually turn the client response into json
    async def resp_json(self, Response: aiohttp.ClientResponse):
        return await Response.json()


    # Used in the response_pool_status func, used to actually turn the client response into status codes
    async def resp_status_code(self, Response: aiohttp.ClientResponse):
        return Response.status


    # Used for the with statement entry thing, basically upon doing with requestmaker: does code here, its pass because I don't really do anything important here
    def __enter__(self, *args, **kwargs):
        pass

    # Upon exiting the with statement it closes session
    def __exit__(self, exc_type, exc_val, exc_tb):
        self._await(self.session.close())


    # Code for close, basically closes everything real
    def close(self):
        self.closed = True
        self._await(self.session.close())
        self.session = None


