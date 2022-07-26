from resources import Design
import asyncio

async def main():
    await Design.ascii()


asyncio.run(main())