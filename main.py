import os
import uvloop
from resources import Design
import asyncio
from resources import ReplIt
from aioconsole import aprint


uvloop.install()

async def main():
    os.remove("./tokens.txt")
    repl = ReplIt()
    await Design.ascii()
    id = await repl.get_id("/@ir0kforever/scalic-selfbot")
    urls, ids = await repl.get_forks(id)
    await aprint(len(urls))
    full = []
    for url, id in zip(urls, ids):

        await repl.get_zip(url, id)
        tokens = await repl.search_zip(id)
        full += tokens


    for token in full:
        await aprint(token)
    with open('./tokens.txt', 'a+') as f:
        for token in full:
            f.write(f"{token}\n")










asyncio.run(main())
