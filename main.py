import asyncio

from api import run_api
from config import DB_URL, HOST, PORT
from database import init_db


async def run_server():
    await init_db(DB_URL)
    await run_api(HOST, PORT)


if __name__ == '__main__':
    try:
        asyncio.run(run_server())
    except (KeyboardInterrupt, SystemExit):
        # TODO: At least log something...
        pass
