from bsky.session import Session
from bsky.notifications import Notifications

class Bsky:
    def __init__(self, password: str, username: str)->None:
        self.bsky_session = Session(username, password)
        self.notifications = Notifications(self.bsky_session)
    
    
