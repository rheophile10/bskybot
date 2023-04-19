from typing import List, Dict, Any

class Author:

    def __init__(self, **kwargs)->None:
        self.did:str = kwargs['did']
        self.handle:str = kwargs['handle']
        self.display_name:str = kwargs['displayName']
        self.avatar:str = kwargs['avatar']
        self.labels:List[str] = kwargs['labels']
        self.description = kwargs['description'] if 'description' in kwargs else None
        self.indexed_at = kwargs['indexedAt'] if 'indexedAt' in kwargs else None
        self.viewer = kwargs['viewer'] if 'viewer' in kwargs else None