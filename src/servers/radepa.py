import json
import httpx
import time


class RapedaConnect:
    def __init__(
            self,
            hostname: str,
            port: str = "2087",
            basepath: str = "/cpsess7945419007/frontend/jupiter/api/v1",
            login: str | None = None,
            password: str | None = None
    ):
        self.hostname = hostname
        self.port = port
        self.basepath = basepath
        self.login = login
        self.password = password
        self.session = httpx.AsyncClient()

    async def _login(self, login, password):
        target_url = f"http://{self.hostname}:{self.port}/login"
        header_data = {
            "username": login,
            "password": password,
            "LoginSecret": ""
        }
        response = await self.session.post(url=target_url, data=header_data)
        response.raise_for_status()  # Проверка на ошибки HTTP
        return self.session

    async def get_list(self):
        target_url = f"http://{self.hostname}:{self.port}{self.basepath}/list"
        response = await self.session.get(url=target_url)
        response.raise_for_status()
        content = response.json()
        return content["success"]

    async def get_ping(self) -> float:
        target_url = f"http://{self.hostname}:{self.port}"
        start_time = time.perf_counter()
        try:
            response = await self.session.get(url=target_url, follow_redirects=True)
            response.raise_for_status()
        except httpx.RequestError:
            return float('inf')  # Если сервер недоступен, возвращаем бесконечность
        end_time = time.perf_counter()
        return (end_time - start_time) * 1000  # Возвращаем время в миллисекундах

    async def get_status(self):
        target_url = f"http://{self.hostname}:{self.port}/server/status"
        response = await self.session.post(url=target_url)
        response.raise_for_status()
        content = response.json()
        return content

    async def close(self):
        await self.session.aclose()
