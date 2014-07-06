from datetime import date
import TrelloApiConstants

__author__ = 'yluft'

GAMELLO = 'Gamello'
LEADER_BOARD = 'LeaderBoard'

from AppPermissions import AppPermissions
from RequestsWrapper import RequestsWrapper


class Board:

    def __init__(self, boardId, appPermissions='../../resources/gamello.config'):
        self.boardId = boardId
        if type(appPermissions) is str:
            self.requests = RequestsWrapper(filename=appPermissions)
        elif type(appPermissions) is AppPermissions:
            self.requests = RequestsWrapper(permissions=appPermissions)

    def _getGamelloList(self):
        lists = RequestsWrapper().getAsPythonList(TrelloApiConstants.lists(self.boardId))
        for list in lists:
            if list.get('name') == GAMELLO:
                return list.get('id')
        else:
            return None

    def _addList(self):
        id = self._getGamelloList()
        if id is None:
            arguments = {
                'name': GAMELLO,
                'idBoard': self.boardId
            }
            response = self.requests.postAsPython("lists/", None, params=arguments)
            id = response['id']
        self._gamelloListId = id

    def _getLeaderBoardCard(self):
        lists = RequestsWrapper().getAsPythonList(TrelloApiConstants.cards(self._gamelloListId))
        for list in lists:
            if list.get('name') == LEADER_BOARD:
                return list.get('id')
        else:
            return None

    def _addLeaderBoard(self):
        id = self._getLeaderBoardCard()
        if id is None:
            arguments = {
                'idList': self._gamelloListId,
                'name': LEADER_BOARD
            }
            response = self.requests.postAsPython("cards/", None, params=arguments)
            id = response['id']
        self._leaderBoardCardId = id

    def _updateRules(self, rules):
        pass

    def initializeBoard(self):
        board = self.requests.get(TrelloApiConstants.board(self.boardId))
        print board
        self._addList()
        self._addLeaderBoard()
        self.leaderBoard = LeaderBoard(self._getMembers())

    def update(self, log, rules):
        deltas = rules.apply(log)
        self.leaderBoard.update(deltas, log.getLastUpdateTime())

    def _getMembers(self):
        return self.requests.getAsPythonList(TrelloApiConstants.boardMembers(self.boardId))


class LeaderBoard:
    def __init__(self, members):
        self.lastUpdate = date(1970, 1, 1)
        self.members = members
        self.scores = {memberObj['fullName']: 0 for memberObj in self.members}

    def update(self, deltas, time):
        for members in deltas:
            self.scores[members] += deltas[members]
        self.lastUpdate = time


def testLeaderBoardUpdate(board):
    print('testLeaderBoardUpdate')
    print(board._getMembers())
    members = [{'id': '1', 'fullName': 'Dude 1'}]
    leaderboard = LeaderBoard(members)
    assert leaderboard.lastUpdate == date(1970, 1, 1)
    assert len(leaderboard.scores) > 0
    print('testLeaderBoardUpdate: passed')



if __name__ == '__main__':
    board = Board('53b92a578425b1f0ae215cdd')
    board.initializeBoard()
    testLeaderBoardUpdate(board)

