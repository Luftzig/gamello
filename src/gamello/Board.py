__author__ = 'yluft'

from AppPermissions import AppPermissions
from RequestsWrapper import RequestsWrapper


class Board:

    def __init__(self, boardId, appPermissions='../../resources/gamello.config'):
        self.boardId = boardId
        if type(appPermissions) is str:
            self.requests = RequestsWrapper(filename=appPermissions)
        elif type(appPermissions) is AppPermissions:
            self.requests = RequestsWrapper(permissions=appPermissions)

    def _addList(self):
        arguments = {
            'name': 'Gamello',
            'idBoard': self.boardId
        }
        self.requests.post("lists/", None, params=arguments)

    def _addLeaderBoard(self, idList):
        arguments = {
            'idList': idList,
            'name': 'LeaderBoard'
        }
        self.requests.post("cards/", None, params=arguments)

    def _updateRules(self):
        pass

    def initializeBoard(self):
        board = self.requests.get("boards/" + self.boardId)
        print board
        self._addList()
        self._addLeaderBoard()

if __name__ == '__main__':
    board = Board('53b92a578425b1f0ae215cdd')
    board.initializeBoard()

