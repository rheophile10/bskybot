from bsky.session import Session, BskyThing
from typing import List, Dict, Any


class Notifications(BskyThing): 
    xrpc:str = "/xrpc/app.bsky.notification.listNotifications"
    params:Dict[str, int] = {"limit":30}
    
    def __init__(self, session:Session)->None:
        super().__init__(session, self.xrpc, self.params)

    def get(self)->List['Notification']:
        result = self.bsky.get(self.xrpc, self.params)
        print(result)
        return result


class Notification:
    def __init__(self)->None:
        pass
