import uvicorn

from api.app import app


async def run_api(host: str, port: int):
    uvicorn_config = uvicorn.Config(app, host=host, port=port)
    uvicorn_server = uvicorn.Server(uvicorn_config)
    await uvicorn_server.serve()
