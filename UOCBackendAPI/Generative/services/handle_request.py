import os
import requests

class HandleRequest:
    def __init__(self):
        pass

    def get(self, url: str, params):
        return requests.get(
            url=url,
            params=params,
        )
    
    def getdata(self, url: str, params, data):
        return requests.get(
            url=url,
            params=params,
            json=data
        )

    def post(self, url: str, body):
        return requests.request(
            "POST",
            url,
            data=body,
        )
    
    def put(self, url: str, body):
        return requests.request(
            "PUT",
            url,
            data=body,
        )