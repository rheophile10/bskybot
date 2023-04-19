from bsky_bot.bsky.session import Session
from bsky_bot.bsky.notifications import Notifications
from bsky_bot.bsky.skoot import Skoot
from typing import List, Dict, Any, Optional, Tuple

class Bsky:
    def __init__(self, username: str, password: str)->None:
        self.bsky_session = Session(username, password)
        self.notifications = Notifications(self.bsky_session)
    
    def get_notifications(self, limit:Optional[int]=None)->Tuple[List[Skoot], Any, Any]:
        return self.notifications.get(limit)