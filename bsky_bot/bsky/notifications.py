from bsky_bot.bsky.session import Session, BskyThing
from bsky_bot.bsky.structs import Author, Record, SkootBase
from bsky_bot.bsky.skoot import Skoot
from typing import List, Dict, Any, Optional, Tuple

class Notification:
    def __init__(self, **kwargs)->None:
        self._skoot_base = SkootBase(kwargs['cid'], kwargs['uri'])
        self._reasonSubject = kwargs["reasonSubject"] if "reasonSubject" in kwargs else None
        self.author = Author(**kwargs['author'])
        self._reason = kwargs['reason']
        self._record = Record(**kwargs['record'])
        self._is_read = kwargs['isRead']
        self._indexed_at = kwargs['indexedAt']
        self._labels = kwargs['labels']
class Notifications(BskyThing): 
    xrpc:str = "/xrpc/app.bsky.notification.listNotifications"
    params:Dict[str, int] = {"limit":30}

    def __init__(self, session:Session)->None:
        super().__init__(session)

    def get(self, limit:Optional[int]=None)->Tuple[List[Skoot], Any, Any]:
        if limit:
            self.params['limit'] = limit
        replies = []
        likes = []
        follows = []
        for n in self.bsky.get(self.xrpc, self.params)['notifications']:
            n = Notification(**n)
            if n._record.bsky_type == 'app.bsky.feed.post':
                replies.append(
                    Skoot(n._skoot_base, n._record.parent, 
                          n._record.root, n.author, n._record.text)
                    )
        return replies, likes, follows

