from typing import List, Dict, Any

class Author:
    did: str
    handle: str
    display_name: str
    avatar: str
    labels: List[str] 
    
    def __init__(self, author: Dict[str, Any])->None:
        self.did = author['did']
        self.handle = author['handle']
        self.display_name = author['displayName']
        self.avatar = author['avatar']
        self.labels = author['labels']

class Image:
    
    def __init__(self, image: Dict[str, Any])->None:
        self.alt = image['alt']
        self.bsky_type= image['image']['$type']
        self.link= image['image']['ref']['$link']
        self.mimeType: image['image']['mimeType']
        self.size= image['image']['size']

class Record:
    text: str
    bsky_type:str
    images: List[Image]
    created_at: str

    def __init__(self, record: Dict[str, Any])->None:
        self.text = record['text']
        self.bsky_type = record['$type']
        self.images = []
        if 'embed' in record:
            if record['embed']['$type'] == 'app.bsky.embed.images':
                self.images = [Image(image) for image in record['embed']['images']]
            else:
                raise NotImplementedError
        self.created_at = record['createdAt']

class Skoot:
    url: str
    cid: str
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
    