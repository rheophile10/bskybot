from typing import List, Dict, Any
from bsky.structs.image import Image
from dataclasses import dataclass

@dataclass
class SkootBase:
    cid: str
    uri: str

    def __post_init__(self)->None:
        self.rkey = self.uri.split('/')[-1]

class Record:

    def __init__(self, **kwargs)->None:        
        self.bsky_type = kwargs['$type']
        self.created_at = kwargs['createdAt']
        self.text = kwargs['text'] if 'text' in kwargs else None
        if 'reply' in kwargs:
            self.root = SkootBase(kwargs['reply']['root']['cid'],
                                  kwargs['reply']['root']['uri'])
            self.parent = SkootBase(kwargs['reply']['parent']['cid'],
                                    kwargs['reply']['parent']['uri'])
        if 'embed' in kwargs:
            self.images = []
            if kwargs['embed']['$type'] == 'app.bsky.embed.images':
                self.images = [Image(image) for image in kwargs['embed']['images']]
            else:
                raise NotImplementedError
