from typing import List, Dict, Any, Optional
from bsky.structs import Author, Record, SkootBase, Image
from bsky.session import Session, BskyThing


class Skoot(BskyThing):
    def __init__(self, 
                 session: Session,
                 skoot:SkootBase, 
                 parent:Optional[SkootBase], 
                 root:Optional[SkootBase],
                 author:Author,
                 text:Optional[str]='',
                 images:Optional[List[Image]]=[])->None:
        super().__init__(session)
        self.skoot = skoot
        self.parent = parent
        self.root = root
        self.author = author
        self.text= text
        self.images = images
    
    def delete(self, skoot:Optional[SkootBase])->None:
        data = {
            "collection":"app.bsky.feed.post",
            "repo":f"did:plc:{self.bsky.DID}",
            "rkey":skoot.rkey
            }
        result = self.bsky.post("/xrpc/com.atproto.repo.deleteRecord",data=data)
        print(result)

class Skoot_:
    url: str
    cid: str
    text: str
    root_cid:str
    author: Author
    record: Record
    embed: List[Dict[str, str]]
    reply_count: int
    repost_count: int
    like_count: int
    indexed_at: str
    labels: List[str]
    replies: List['Skoot']

    def __init__(self, response: Dict[str, Any]):
        if 'thread' in response:
            post = response['thread']['post']
            replies = response['thread']['replies']
        else:
            post = response['post']
            replies = response['replies']
        self.url = post['uri']
        self.cid = post['cid']
        self.author = Author(post['author'])
        self.record = Record(post['record'])
        if 'embed' in post:
            self.embed = [i for i in post['embed']['images']]
        self.reply_count = post['replyCount']
        self.like_count = post['likeCount']
        self.repost_count = post['repostCount']
        self.like_count = post['likeCount']
        self.indexed_at = post['indexedAt']
        self.labels = post['labels']
        self.replies = [Skoot(reply) for reply in replies]
    
