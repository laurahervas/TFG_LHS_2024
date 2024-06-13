import string
import unicodedata

class UserQueryStatement:
    def __init__(self, query: str):
        self.query = self._processUserQuery(query)


    def _processUserQuery(self, query: str):
        for p in string.punctuation:
            query = query.replace(p,'')
        return unicodedata.normalize('NFKD', query).encode('ascii', 'ignore').decode('utf-8', 'ignore').lower()