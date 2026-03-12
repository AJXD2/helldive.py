from helldivepy.models import War
import httpx
from rich import print

def hello():
    client = httpx.Client()
    resp = client.get("https://api.helldivers2.dev/api/v1/war", headers={"X-Super-Client": "helldivepy/rewrite", "X-Super-Contact": "mailto:aj@ajxd2.dev,github:ajxd2,discord:ajxd2"})
    war = War(**resp.json())
    print(war.statistics.automaton_kills)

if __name__ == "__main__":
    hello()
