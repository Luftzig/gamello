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
        pass

    def _addLeaderBoard(self):
        pass

    def _updateRules(self):
        pass

    def initializeBoard(self):
        board = self.requests.get("boards/" + self.boardId)


if __name__ == '__main__':
    pass

