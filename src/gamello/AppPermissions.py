from ConfigParser import ConfigParser

__author__ = 'yluft'


class AppPermissions:

    def __init__(self, **keys):
        if keys['file']:
            self.parseConfig(keys['file'])
        else:
            raise NotImplementedError('Cannot initialize without file')

    def parseConfig(self, fileName):
        configParser = ConfigParser()
        configParser.read(fileName)
        self.appKey = configParser.get('Permissions', 'appKey')
        self.userId = configParser.get('Permissions', 'userId')
        self.token = configParser.get('Permissions', 'userToken')


# Test
def testReading():
    permissions = AppPermissions(file='gamello.test.config')
    assert permissions.appKey == 'TestAppKey'
    assert permissions.userId == 'userId'


if __name__ == '__main__':
    testReading()