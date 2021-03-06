import json
import requests
from AppPermissions import AppPermissions
import TrelloApiConstants

__author__ = 'yluft'


class RequestsWrapper:

    def __init__(self, **kwargs):
        if kwargs.has_key('permissions'):
            self.permissions = kwargs['permissions']
        elif kwargs.has_key('filename'):
            self.permissions = AppPermissions(file=kwargs['filename'])
        else:
            self.permissions = _defaultPermissions

    def _updateArguments(self, kwargs, target):
        kwargs['params'] = dict(kwargs.get('params', {}).items() + self._params().items())
        url = TrelloApiConstants.TRELLO_API_BASE + target
        return url

    def get(self, target, **kwargs):
        url = self._updateArguments(kwargs, target)
        return requests.get(url, **kwargs)

    def post(self, target, data, **kwargs):
        url = self._updateArguments(kwargs, target)
        return requests.post(url, data, **kwargs)

    def postAsPython(self, target, data, **kwargs):
        response = self.post(target, data, **kwargs)
        return json.loads(response.text)

    def _params(self):
        return {'key': self.permissions.appKey, 'token': self.permissions.token}

    def getAsPythonList(self, target, **kwargs):
        responseObj = self.get(target, **kwargs)
        return json.loads(responseObj.text)

    def put(self, target, data, **kwargs):
        url = self._updateArguments(kwargs, target)
        return requests.put(url, data, **kwargs)

    def putAsPythonObject(self, target, data, **kwargs):
        responseObj = self.put(target, data, **kwargs)
        return json.loads(responseObj.text)



_defaultPermissions = AppPermissions(file='../../resources/gamello.config')

#Test

def getAsPythonListTest():
    permissions = AppPermissions(file='../../resources/gamello.config')
    response = RequestsWrapper(permissions=permissions).getAsPythonList('boards/53b92a578425b1f0ae215cdd/actions')
    print response

if __name__ == '__main__':
    permissions = AppPermissions(file='../../resources/gamello.config')
    response = RequestsWrapper(permissions=permissions).get('members/me')
    assert response.status_code == 200

    response = RequestsWrapper().get('members/me')
    assert response.status_code == 200
