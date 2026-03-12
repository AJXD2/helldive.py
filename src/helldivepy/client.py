from helldivepy.modules.war import WarModule
import httpx


class HelldiveAPIClient:
    def __init__(self, base_url: str = "https://api.helldivers2.dev/api", client: str = "helldivepy", contact: str = "github:ajxd2/helldive.py"):
        self.base_url = base_url
        self.headers = {
            "X-Super-Client": client,
            "X-Super-Contact": contact
        }
        self.client = httpx.Client()
        self.async_client = httpx.AsyncClient()
        self.modules = {
            "war": WarModule(self)
        }
    @property
    def war(self) -> WarModule:
        return self.modules['war']
