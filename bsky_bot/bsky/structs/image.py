from typing import Dict, Any


class Image:
    
    def __init__(self, image: Dict[str, Any])->None:
        self.alt = image['alt']
        self.bsky_type= image['image']['$type']
        self.link= image['image']['ref']['$link']
        self.mimeType: image['image']['mimeType']
        self.size= image['image']['size']

