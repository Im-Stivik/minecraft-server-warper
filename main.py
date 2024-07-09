from fastapi import FastAPI, HTTPException, Request
from pydantic import BaseModel

from src.MinecaftServerManager import MinecraftServerInstance

app = FastAPI()
server_path = 'server/'  # Adjust the path to your Minecraft server directory
server_instance = MinecraftServerInstance(server_path)


class Command(BaseModel):
    command: str


@app.post("/server/start")
async def start_server():
    server_instance.start_server()
    return {"message": "Server started"}


@app.post("/server/stop")
async def stop_server():
    server_instance.stop_server()
    return {"message": "Server stopped"}


@app.post("/server/restart")
async def restart_server():
    server_instance.restart_server()
    return {"message": "Server restarted"}


@app.post("/server/world/recreate")
async def recreate_world():
    server_instance.recreate_world()
    return {"message": "World recreated"}


@app.post("/server/command")
async def send_command(command: Command):
    server_instance.execute_command(command.command)
    return {"message": f"Command '{command.command}' sent"}


@app.get("/server/output")
async def read_output():
    output = server_instance.read_output()
    return {"output": output}


@app.get("/server/output/tail/{lines}")
async def read_tail_specify_lines(lines: int):
    output = server_instance.read_tail(lines)
    return {"output": output}


@app.get("/server/output/tail/")
async def read_tail_default():
    output = server_instance.read_tail()
    return {"output": output}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="localhost", port=8000)
