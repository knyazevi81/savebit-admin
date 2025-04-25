from fastapi import APIRouter, Depends, status
from fastapi.exceptions import HTTPException
import httpx

from src.users.models import Users
from src.users.dependencies import get_current_user
from src.servers.schemas import ServerData
from src.exceptions import IncorrectLoginOrPasswordException
from src.servers.service import ServerService
from src.servers.radepa import RapedaConnect
from src.exceptions import ServerDisconnect



router = APIRouter(
    prefix="/servers_api",
    tags=["server connection api"]
)

@router.get("/list")
async def get_all_servers(
    user: Users = Depends(get_current_user)
):
    servers = await ServerService.find_all()
    output_data = []
    for serv in servers:
        connector = RapedaConnect(
            hostname=serv.hostname,
            port=serv.port,
            basepath=serv.basepath,
            login=serv.login,
            password=serv.password
        )
        ping = await connector.get_ping()
        output_data.append({
            "id": serv.id,
            "hostname": serv.hostname,
            "name": serv.server_name,
            "ping": f"{ping:.2f}ms"
        })

    return output_data


@router.post('/add_server')
async def add_new_server(
    server: ServerData,
    user: Users = Depends(get_current_user)
):
    if not user:
        raise IncorrectLoginOrPasswordException

    server_exist_check = await ServerService.find_one_or_none(
        hostname=server.hostname
    )
    if server_exist_check:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Server has already been added"
        )
    try:
        connector = RapedaConnect(
            hostname=server.hostname,
            port=server.port,
            basepath=server.basepath,
            login=server.login,
            password=server.password
        )
        await connector._login(server.login, server.password)
        await ServerService.add(
            hostname=server.hostname,
            server_name=server.server_name,
            port=server.port,
            basepath=server.basepath,
            login=server.login,
            password=server.password
        )
        ping = await connector.get_ping()
        return {"status": "Server connected successfully", "ping": f"{ping:.2f}"}
    except Exception as e:
        print(e)
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="disconnected"
        )



