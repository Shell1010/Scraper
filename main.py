import os
from resources import Design
import asyncio
from resources import ReplIt
from aioconsole import aprint
from colorama import Fore as color



async def main(url: str, start: int = None, stop: int = None):
    repl = ReplIt()
    if os.path.isfile("./false_tokens.txt"):
        os.remove("./false_tokens.txt")

    if os.path.isfile("./tokens.txt"):
        os.remove("./tokens.txt")

    if os.path.isfile("./valid.txt"):
        os.remove("./valid.txt")


    await Design.ascii()
    await aprint(f"{color.GREEN}Scraping {url}...{color.RESET}")

    if start != None:
        id = await repl.get_id(url)

        urls, ids = await repl.get_forks(id)
        urls = urls[start:]
        ids = ids[start:]

        await aprint(f"{color.GREEN}Forks found: {len(urls)}{color.RESET}")
        full = []
        count = 0

        for i in range(0, len(urls), 50):
            await asyncio.gather(*(repl.get_zip(url, id) for url, id in zip(urls[i:i+50], ids[i:i+50]) ), return_exceptions=True)
        for id in ids:
            try:
                tokens = await repl.search_zip(id)
                await aprint(f"{color.GREEN}Finished fork {count+1}{color.RESET}")
                count += 1

                for token in tokens:
                    with open("./false_tokens.txt", "a+") as f:
                        f.write(f"{token}\n")
                full += tokens
            except:
                continue

        await repl.clean_dirs()


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
        await repl.bot_check()


    else:

        id = await repl.get_id(url)
        urls, ids = await repl.get_forks(id)
        await aprint(f"{color.GREEN}Forks found: {len(urls)}{color.RESET}")
        full = []
        count = 0
        for i in range(0, len(urls), 50):
            await asyncio.gather(*(repl.get_zip(url, id) for url, id in zip(urls[i:i+50], ids[i:i+50]) ), return_exceptions=True)
        for id in ids:
            try:
                tokens = await repl.search_zip(id)
                await aprint(f"{color.GREEN}Finished fork {count+1}{color.RESET}")
                count += 1
                for token in tokens:
                    with open("./false_tokens.txt", "a+") as f:
                        f.write(f"{token}\n")
                full += tokens
            except:
                continue

        await repl.clean_dirs()


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
        await repl.bot_check()




async def search_zips(url: str):
    repl = ReplIt()
    await Design.ascii()
    await aprint("Searching through zips...")
    id = await repl.get_id(url)
    urls, ids = await repl.get_forks(id)
    full = []
    count = 0
    for id in ids:
        try:
            tokens = await repl.search_zip(id)
            await aprint(f"{color.GREEN}Finished fork {count+1}{color.RESET}")
            count += 1

            for token in tokens:
                with open("./false_tokens.txt", "a+") as f:
                    f.write(f"{token}\n")
            full += tokens
        except:
            continue

    await repl.clean_dirs()


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
    await repl.bot_check()

# Scrapes from /community/discord
# Finds forks too

async def scrape():
    if os.path.isfile("./false_tokens.txt"):
        os.remove("./false_tokens.txt")

    if os.path.isfile("./tokens.txt"):
        os.remove("./tokens.txt")

    if os.path.isfile("./valid.txt"):
        os.remove("./valid.txt")

    repl = ReplIt()
    await Design.ascii()

    urls, ids = await repl.repl_scrape()

    await aprint(f"{color.GREEN}Urls found: {len(urls)}{color.RESET}")

    full = []
    count = 0
    for url, id in zip(urls, ids):

        with open("./false_tokens.txt", "a+") as f:
            try:
                await repl.get_zip(url, id)
                tokens = await repl.search_zip(id)
                for token in tokens:
                    f.write(f"{token}\n")
                full += tokens
                count += 1
                await aprint(f"{color.GREEN}Finished fork {count}{color.RESET}")
            except:
                continue

    for id in ids:
        count = 0
        urls, new_ids = await repl.get_forks(id)
        await aprint(f"{color.GREEN}Forks found: {len(urls)}{color.RESET}")
        for url, id in zip(urls, new_ids):
            with open("./false_tokens.txt", "a+") as f:
                try:
                    await repl.get_zip(url, id)
                    tokens = await repl.search_zip(id)
                    for token in tokens:
                        f.write(f"{token}\n")
                    full += tokens
                    count += 1
                    await aprint(f"{color.GREEN}Finished fork {count}{color.RESET}")
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
    # Bot check
    await repl.bot_check()

async def validate():
    repl = ReplIt()
    lines_seen = set()
    outfile = open("tokens.txt", "w")
    for line in open("false_tokens.txt", "r"):
        if line not in lines_seen:
            outfile.write(line)
            lines_seen.add(line)
    outfile.close()
    await repl.check()
    # Bot check
    await repl.bot_check()





if __name__ == "__main__":
    # Scrape forks from a url
    # asyncio.run(main("/@Remixstudio/Discord-MusicBot", start=1000))

    # Searches through each zip
    asyncio.run(search_zips("/@Remixstudio/Discord-MusicBot"))

    # Scrape from community/discord
    # asyncio.run(scrape())

    # Validate tokens in false_tokens.txt
    # asyncio.run(validate())
