import aiohttp
import asyncio
import os

class Run:
    def __init__(self, config) -> None:
        self.config = config
        try:
            cookies = open(input("File with cookies to refresh: "), "r").read().split("\n")
            os.system("cls" if os.name == 'nt' else "clear")
            print(f"Refreshed cookies saved in: {asyncio.run(self.start(cookies))}")
        except Exception as e:
            print(e)

    async def start(self, cookies):
        semaphore = asyncio.Semaphore(self.config["max_threads"]) 

        async def process_cookie(cookie):
            async with semaphore:
                return await self.get_set_cookie(cookie)

        refreshed_cookies = await asyncio.gather(*[process_cookie(cookie) for cookie in cookies])

        open("refreshed_cookies.txt", "w+").write("\n".join(refreshed_cookies))

        return os.path.dirname(os.path.abspath("refreshed_cookies.txt"))

    async def get_set_cookie(self, cookie):
        async with aiohttp.ClientSession() as session:
            response = await session.post("https://auth.roblox.com/v1/authentication-ticket/redeem",
                                          headers={"rbxauthenticationnegotiation": "1"},
                                          json={"authenticationTicket": await self.get_rbx_authentication_ticket(cookie, session)})
            set_cookie_header = response.headers.getall("Set-Cookie")
            assert set_cookie_header, "An error occurred while getting the set_cookie"
            return set_cookie_header[1].split(".ROBLOSECURITY=")[1].split(";")[0]

    async def get_rbx_authentication_ticket(self, cookie, session):
            response = await session.post("https://auth.roblox.com/v1/authentication-ticket",
                                          headers={"rbxauthenticationnegotiation": "1",
                                                   "referer": "https://www.roblox.com/camel",
                                                   'Content-Type': 'application/json',
                                                   "x-csrf-token": await self.get_csrf_token(cookie, session)},
                                          cookies={".ROBLOSECURITY": cookie})
            assert response.headers.get("rbx-authentication-ticket"), "An error occurred while getting the rbx-authentication-ticket"
            return response.headers.get("rbx-authentication-ticket")

    async def get_csrf_token(self, cookie, session) -> str:
            response = await session.post("https://auth.roblox.com/v2/logout", cookies={".ROBLOSECURITY": cookie})
            xcsrf_token = response.headers.get("x-csrf-token")
            assert xcsrf_token, "An error occurred while getting the X-CSRF-TOKEN. Could be due to an invalid Roblox Cookie"
            return xcsrf_token