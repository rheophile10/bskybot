from pw_bsky.bsky import Bsky
from dotenv import dotenv_values
from pathlib import Path

env_path = Path(__file__).parents[1] / '.env'
config = dotenv_values(env_path)
BSKY_USERNAME = config["BSKY_USERNAME"]
BSKY_PASSWORD = config["BSKY_PASSWORD"]

client = Bsky(BSKY_USERNAME, BSKY_PASSWORD)

replies, likes, follows = client.notifications.get()
for reply in replies:
    print(reply.text)