import os
from resources import Design
import asyncio
from resources import ReplIt
from aioconsole import aprint





async def main():
    if os.path.isfile("./false_tokens.txt"):
        os.remove("./false_tokens.txt")

    if os.path.isfile("./tokens.txt"):
        os.remove("./tokens.txt")

    repl = ReplIt()
    await Design.ascii()
    id = await repl.get_id("/@W1zz3d/Venom-Selfbot-2021-New-Selfbot")
    urls, ids = await repl.get_forks(id)
    await aprint(len(urls))
    full = []

    for url, id in zip(urls, ids):
        await repl.get_zip(url, id)
        tokens = await repl.search_zip(id)
        full += tokens


    for token in full:
        await aprint(token)
    with open('./false_tokens.txt', 'a+') as f:
        for token in full:
            f.write(f"{token}\n")

    lines_seen = set()
    outfile = open("tokens.txt", "w")
    for line in open("false_tokens.txt", "r"):
        if line not in lines_seen:
            outfile.write(line)
            lines_seen.add(line)
    outfile.close()

    await repl.check()








if __name__ == "__main__":
    asyncio.run(main())