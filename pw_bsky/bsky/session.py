import requests
from requests import Response
from datetime import datetime, timezone
from typing import Tuple, Optional, Dict, Any, List
from bsky.skoot import Skoot

class Session:
    def __init__(self, username:str, password:str)->None:
        self.ATP_HOST = "https://bsky.social"
        self.HANDLE = username
        self.auth(username, password)

    def auth(self, username:str, password:str) -> None:
        data = {"identifier": username, "password": password}
        resp = requests.post(
            self.ATP_HOST + "/xrpc/com.atproto.server.createSession",
            json=data
        ).json()
        self.ATP_AUTH_TOKEN = resp['accessJwt']
        if self.ATP_AUTH_TOKEN == None:
            raise ValueError("No access token, is your password wrong?")
        self.REFRESH_TOKEN = resp['refreshJwt']
        self.EMAIL = resp['email']
        self.DID = resp["did"]

    def refresh(self):
        # TODO DIDs expire shortly and need to be refreshed for any long-lived sessions
        pass

    def get(self, xrpc:str, params:Optional[Dict[str, Any]]=None,)->Dict[str,Any]:
        url = f"{self.ATP_HOST}{xrpc}"
        headers = {"Authorization": "Bearer " + self.ATP_AUTH_TOKEN}
        
        resp = requests.get(url, params=params, headers=headers)
        
        try: 
            return resp.json()
        except requests.exceptions.HTTPError as e:
            return {"Error": e}
        
    def post(self, xrpc:str, params:Optional[Dict[str, Any]]=None, data:Optional[Dict[str, Any]]=None)->Dict[str,Any]:
        url = f"{self.ATP_HOST}{xrpc}"
        headers = {"Authorization": "Bearer " + self.ATP_AUTH_TOKEN}
        
        resp = requests.post(url, params=params, headers=headers, json=data)
        
        try: 
            return resp.json()
        except requests.exceptions.HTTPError as e:
            return {"Error": e}


    def reskoot(self,url:str)->Response:
        # sample url from desktop
        # POST https://bsky.social/xrpc/com.atproto.repo.createRecord
        # https://staging.bsky.app/profile/klatz.co/post/3jruqqeygrt2d
        '''
        {
            "collection":"app.bsky.feed.repost",
            "repo":"did:plc:n5ddwqolbjpv2czaronz6q3d",
            "record":{
                "subject":{
                        "uri":"at://did:plc:scx5mrfxxrqlfzkjcpbt3xfr/app.bsky.feed.post/3jszsrnruws27",
                        "cid":"bafyreiad336s3honwubedn4ww7m2iosefk5wqgkiity2ofc3ts4ii3ffkq"
                        },
                "createdAt":"2023-04-10T17:38:10.516Z",
                "$type":"app.bsky.feed.repost"
            }
        }
        '''

        person_youre_reskooting = self.resolveHandle(url.split('/')[-3]).json().get('did') # its a DID
        url_identifier = url.split('/')[-1]

        # import pdb; pdb.set_trace()
        skoot_cid = self.get_skoot_by_url(url).json().get('thread').get('post').get('cid')

        # subject -> uri is the maia one (thing rt'ing, scx)
        timestamp = datetime.now(timezone.utc)
        timestamp = timestamp.isoformat().replace('+00:00', 'Z')

        headers = {"Authorization": "Bearer " + self.ATP_AUTH_TOKEN}

        data = {
            "collection": "app.bsky.feed.repost",
            "repo": "{}".format(self.DID),
            "record": {
                "subject": {
                    "uri":"at://{}/app.bsky.feed.post/{}".format(person_youre_reskooting, url_identifier),
                    "cid":"{}".format(skoot_cid) # cid of the skoot to reskoot
                },
                "createdAt": timestamp,
                "$type": "app.bsky.feed.repost"
            }
        }

        resp = requests.post(
            self.ATP_HOST + "/xrpc/com.atproto.repo.createRecord",
            json=data,
            headers=headers
        )

        return resp

    def resolveHandle(self,username:str) -> Response: # aka getDid
        headers = {"Authorization": "Bearer " + self.ATP_AUTH_TOKEN}
        resp = requests.get(
            self.ATP_HOST + "/xrpc/com.atproto.identity.resolveHandle?handle={}".format(username),
            headers=headers
        )
        return resp

    def get_skoot_by_url(self,url:str) -> Skoot:
        "https://bsky.social/xrpc/app.bsky.feed.getPostThread?uri=at%3A%2F%2Fdid%3Aplc%3Ascx5mrfxxrqlfzkjcpbt3xfr%2Fapp.bsky.feed.post%2F3jszsrnruws27A"
        "at://did:plc:scx5mrfxxrqlfzkjcpbt3xfr/app.bsky.feed.post/3jszsrnruws27"
        "https://staging.bsky.app/profile/naia.bsky.social/post/3jszsrnruws27"

        headers = {"Authorization": "Bearer " + self.ATP_AUTH_TOKEN}

        did_of_person_in_link = url.split('/')[-3]
        if did_of_person_in_link[0:3]!="did":
            did_of_person_in_link = self.resolveHandle(did_of_person_in_link).json().get('did')            
        url_identifier = url.split('/')[-1] # the random stuf at the end

        uri = "at://{}/app.bsky.feed.post/{}".format(did_of_person_in_link, url_identifier)

        resp = requests.get(
            self.ATP_HOST + "/xrpc/app.bsky.feed.getPostThread?uri={}".format(uri),
            headers=headers
        )

        try: 
            return Post(resp.json())
        except requests.exceptions.HTTPError as e:
            return f"Error: {e}"

    def get_image_link(self, image: bytes)->Tuple[str, int]:
        url = "https://bsky.social/xrpc/com.atproto.repo.uploadBlob"
        size = len(image)
        headers = {
            "Authorization": "Bearer " + self.ATP_AUTH_TOKEN,
            "content-length": str(size),
            "content-type": "image/jpeg"}
        resp = requests.post(url, data = image, headers = headers)
        try: 
            link = resp.json() 
            link = link['blob']['ref']['$link']
            return link, size
        except requests.exceptions.HTTPError as e:
            return f"Error: {e}"

    def reply(self, root: Dict[str,str], url: str, post_content:str, image: Optional[bytes]=None, 
                   timestamp: Optional[datetime]=None) ->Response:
        post = self.get_skoot_by_url(url)
        if not timestamp:
            timestamp = datetime.now(timezone.utc)
        timestamp = timestamp.isoformat().replace('+00:00', 'Z')

        headers = {"Authorization": "Bearer " + self.ATP_AUTH_TOKEN}

        data = {
            "collection": "app.bsky.feed.post",
            "repo": "{}".format(self.DID),
            "record": {
                "text": post_content,
                "$type": "app.bsky.feed.post",
                "createdAt": timestamp,
                'reply':{
                    'root': root,
                    'parent': {
                        'cid': post.cid,
                        'uri': post.url
                    }
                }
            }
        }

        if image:
            image_link, size = self.get_image_link(image)
            data["record"]["embed"] = {
                "$type":"app.bsky.embed.images",
                "images": [
                    {
                        "image":{
                            "$type":"blob", 
                            "mimeType":"image/jpeg", 
                            "ref":{
                                "$link":image_link
                                },
                            "size": size,
                        },
                        "alt": "hey"
                    }
                ]
            }

        resp = requests.post(
            self.ATP_HOST + "/xrpc/com.atproto.repo.createRecord",
            json=data,
            headers=headers
        )

        return resp        


    def post_skoot(self, post_content:str, image: Optional[bytes]=None, 
                   timestamp: Optional[datetime]=None)->Response:
        if not timestamp:
            timestamp = datetime.now(timezone.utc)
        timestamp = timestamp.isoformat().replace('+00:00', 'Z')

        headers = {"Authorization": "Bearer " + self.ATP_AUTH_TOKEN}

        data = {
            "collection": "app.bsky.feed.post",
            "repo": "{}".format(self.DID),
            "record": {
                "text": post_content,
                "$type": "app.bsky.feed.post",
                "createdAt": timestamp,
            }
        }

        if image:
            image_link, size = self.get_image_link(image)
            data["record"]["embed"] = {
                "$type":"app.bsky.embed.images",
                "images": [
                    {
                        "image":{
                            "$type":"blob", 
                            "mimeType":"image/jpeg", 
                            "ref":{
                                "$link":image_link
                                },
                            "size": size,
                        },
                        "alt": "hey"
                    }
                ]
            }

        resp = requests.post(
            self.ATP_HOST + "/xrpc/com.atproto.repo.createRecord",
            json=data,
            headers=headers
        )

        return resp


    def get_car_file(self, did_of_car_to_fetch:Optional[str] = None)->Response:
        '''
        Get a .car file contain all skoots.
        TODO is there a putRepo?
        TODO save to file
        '''

        if did_of_car_to_fetch == None:
            did_of_car_to_fetch = self.DID

        headers = {"Authorization": "Bearer " + self.ATP_AUTH_TOKEN}

        resp = requests.get(
            self.ATP_HOST + "/xrpc/com.atproto.sync.getRepo?did={}".format(did_of_car_to_fetch),
            headers = headers
        )

        return resp

    def get_latest_skoot(self, accountname:str)->Response:
        return self.get_latest_n_skoots(accountname, 1)

    def get_latest_n_skoots(self, username:str, n=5)->Response:
        headers = {"Authorization": "Bearer " + self.ATP_AUTH_TOKEN}
        resp = requests.get(
            self.ATP_HOST + "/xrpc/app.bsky.feed.getAuthorFeed?actor={}&limit={}".format(username, n),
            headers = headers
        )

        return resp

    # [[API Design]] TODO one implementation should be highly ergonomic (comfy 2 use) and the other should just closely mirror the API's exact behavior?
    # idk if im super happy about returning requests, either, i kinda want tuples where the primary object u get back is whatever ergonomic thing you expect
    # and then you can dive into that and ask for the request. probably this means writing a class to encapsulate each of the
    # API actions, populating the class in the implementations, and making the top-level api as pretty as possible
    # ideally atproto lib contains meaty close-to-the-api and atprototools is a layer on top that focuses on ergonomics?
    def follow(self, username:Optional[str]=None, did_of_person_you_wanna_follow:Optional[str]=None)->Response:

        if username:
            did_of_person_you_wanna_follow = self.resolveHandle(username).json().get("did")

        if not did_of_person_you_wanna_follow:
            # TODO better error in resolveHandle
            raise ValueError("Failed; please pass a username or did of the person you want to follow (maybe the account doesn't exist?)")

        timestamp = datetime.now(timezone.utc)
        timestamp = timestamp.isoformat().replace('+00:00', 'Z')

        headers = {"Authorization": "Bearer " + self.ATP_AUTH_TOKEN}

        data = {
            "collection": "app.bsky.graph.follow",
            "repo": "{}".format(self.DID),
            "record": {
                "subject": did_of_person_you_wanna_follow,
                "createdAt": timestamp,
                "$type": "app.bsky.graph.follow"
            }
        }

        resp = requests.post(
            self.ATP_HOST + "/xrpc/com.atproto.repo.createRecord",
            json=data,
            headers=headers
        )

        return resp
    
    def unfollow(self):
        # TODO lots of code re-use. package everything into a API_ACTION class.
        raise NotImplementedError
    
    def getProfile(self, did:str)->Response:
        headers = {"Authorization": "Bearer " + self.ATP_AUTH_TOKEN}

        resp = requests.get(
            self.ATP_HOST + "/xrpc/app.bsky.actor.getProfile?actor={}".format(did),
            headers=headers
        )

        return resp



class BskyThing:
    def __init__(self, session: Session)->None:
        self.bsky = session

    