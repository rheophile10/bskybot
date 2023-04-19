from bsky.session import Session
from bsky.notifications import Notifications

class Bsky:
    def __init__(self, password: str, username: str)->None:
        self.bsky_session = Session(username, password)
        self.notifications = Notifications(self.bsky_session)
    


if __name__ == "__main__":
    from dotenv import dotenv_values
    from pathlib import Path

    env_path = Path(__file__).parent / '.env'
    config = dotenv_values(env_path)
    BSKY_USERNAME = config["BSKY_USERNAME"]
    BSKY_PASSWORD = config["BSKY_PASSWORD"]

    client = Bsky(BSKY_USERNAME, BSKY_PASSWORD)

    notifications = client.notifications.get()