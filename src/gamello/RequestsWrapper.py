import requests
from AppPermissions import AppPermissions
import TrelloApiConstants

__author__ = 'yluft'


class RequestsWrapper:

    def __init__(self, **kwargs):
        if kwargs['permissions']:
            self.permissions = kwargs['permissions']
        elif kwargs['filename']:
            self.permissions = AppPermissions(file=kwargs['filename'])
        else:
            raise KeyError("Missing permissions object or file")

    def updateArguments(self, kwargs, target):
        kwargs['params'] = dict(kwargs.get('params', {}).items() + self._params().items())
        url = TrelloApiConstants.TRELLO_API_BASE + target
        return url

    def get(self, target, **kwargs):
        url = self.updateArguments(kwargs, target)
        return requests.get(url, **kwargs)

    def post(self, target, data, **kwargs):
        url = self.updateArguments(kwargs, target)
        return requests.post(url, data, **kwargs)

    def _params(self):
        return {'key': self.permissions.appKey, 'token': self.permissions.token}


#Test

if __name__ == '__main__':
    permissions = AppPermissions(file='../../resources/gamello.config')
    response = RequestsWrapper(permissions=permissions).get('members/me')
    print response.text
    print response.json()
