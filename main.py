from resources import Design
import asyncio
from resources import ReplIt
from aioconsole import aprint

async def main():
    repl = ReplIt()
    await Design.ascii()
    id = await repl.get_id("/@MatheusTeles1/Yuo-Selfbot")
    urls, ids = await repl.get_forks(id)
    await aprint(len(urls))



    await asyncio.gather(*(repl.get_zip(url, id) for url, id in zip(urls, ids)))
    tokens = await asyncio.gather(*(repl.search_zip(id) for id in ids))

    for lists in tokens:
        for token in lists:
            await aprint(token)








asyncio.run(main())