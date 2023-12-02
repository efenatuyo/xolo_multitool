import aiohttp, asyncio, os
from dataclasses import dataclass

class Run:
    def __init__(self, config) -> None:
        self.config = config
        
        try:
            proxies = open(input("Input proxy file to check: "), "r").read().split("\n")
            print(f"Checked proxies saved in: {asyncio.run(self.start(proxies))}")
        except Exception as e:
            print(e)

        
    async def start(self, proxies):
        semaphore = asyncio.Semaphore(self.config["max_threads"]) 
        
        async def process_proxy(session, proxy):
            async with semaphore:
                if len(proxy.split(":")) == 4:
                    username, password = proxy.split(":")[-2:]
                    proxy_checked = self.config["proxy"]["type"] + "://" + proxy.split(":")[:2]
                elif len(proxy.split(":")) == 2:
                    username = None
                    password = None
                    proxy_checked = self.config["proxy"]["type"] + "://" + proxy
                else:
                    return None
                
                try:
                    return await self.check_proxy(session, proxy_checked, username, password, proxy)
                except:
                    print(f"\033[91mInvalid Proxy: {proxy_checked}\033[0m")
                    return None
            
        async with aiohttp.ClientSession() as session:
            valid_proxies = await asyncio.gather(*[process_proxy(session, proxy) for proxy in proxies])
        
        open("valid_proxies.txt", "w+").write("\n".join([result for result in valid_proxies if result]))
        return os.path.dirname(os.path.abspath("valid_proxies.txt"))
    
    async def check_proxy(self, session, proxy, username, password, proxy_full):
        connector = aiohttp.TCPConnector(use_dns_cache=False)
        if username and password:
            auth = aiohttp.BasicAuth(login=username, password=password)
            response = await session.get(self.config["proxy"]["url"], proxy=proxy, proxy_auth=auth, timeout=self.config["proxy"]["timeout"], ssl=False)
        else:
            response = await session.get(self.config["proxy"]["url"], proxy=proxy, timeout=self.config["proxy"]["timeout"], ssl=False)
        
        print("\033[92m" + "Working Proxy: " + proxy + "\033[0m")
        return proxy_full