from colorama import Fore as Color
from aioconsole import aprint
import os

class Design:


    @staticmethod
    async def ascii():
        os.system('cls' if os.name == 'nt' else 'clear')
        await aprint(f"""{Color.RED}
█▀ █▀▀ █▀█ ▄▀█ █▀█ █▀▀ █▀█
▄█ █▄▄ █▀▄ █▀█ █▀▀ ██▄ █▀▄
______________________________
Made by sexy shell
        {Color.RESET}""")
