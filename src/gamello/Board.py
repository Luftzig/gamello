from datetime import date, datetime
import operator
import TrelloApiConstants
from Rules import Rules

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
        self._postLeaderboard()

    def _getMembers(self):
        return self.requests.getAsPythonList(TrelloApiConstants.boardMembers(self.boardId))

    def _postLeaderboard(self):
        payload = {"value": str(self.leaderBoard)}
        self.requests.putAsPythonObject(TrelloApiConstants.cardDesc(self._leaderBoardCardId), None, params=payload)



class LeaderBoard:
    def __init__(self, members):
        # TODO support adding new users
        self.lastUpdate = date(1970, 1, 1)
        self.members = members
        self.usernamesToFullnames = {memberObj['username']: memberObj['fullName'] for memberObj in self.members}
        self.maxUserName = len(max(self.usernamesToFullnames.values(), key=lambda n: len(n)))
        self.scores = {memberObj['username']: 0 for memberObj in self.members}

    def update(self, deltas, time):
        for members in deltas:
            self.scores[members] += deltas[members]
        self.lastUpdate = time

    def __str__(self):
        result = ""
        sorted_scores = sorted(self.scores, key=lambda x: x[1])
        for score in enumerate(sorted_scores, start=1):
            fullname = self.usernamesToFullnames[score[1]].ljust(self.maxUserName)
            result += "{num}. {fullname}  {score}\n".format(num=score[0], fullname=fullname, score=self.scores[score[1]])
        result += "\nLast updated: " + str(self.lastUpdate)
        return result


class Empty():
    pass


def testLeaderBoardUpdate():
    print('testLeaderBoardUpdate')
    members = [{'id': '1', 'fullName': 'Dude 1', 'username': 'dude1'},
               {'id': '2', 'fullName': 'I gotta really long name', 'username': 'dude2'}]
    leaderboard = LeaderBoard(members)
    assert leaderboard.lastUpdate == date(1970, 1, 1)
    assert len(leaderboard.scores) > 0
    deltas = {'dude1': 4, 'dude2': 2}
    newTime = datetime.today()
    leaderboard.update(deltas, newTime)
    assert leaderboard.scores['dude1'] == 4
    assert leaderboard.lastUpdate == newTime
    print('testLeaderBoardUpdate: passed')


def testLeaderBoardPrinting():
    print("src.gamello.Board.testLeaderBoardPrinting")
    members = [{'id': '1', 'fullName': 'Dude 1', 'username': 'dude1'},
               {'id': '3', 'fullName': 'Dude 3', 'username': 'dude3'},
               {'id': '2', 'fullName': 'I gotta really long name', 'username': 'dude2'}]
    leaderboard = LeaderBoard(members)
    deltas = {'dude2': 4, 'dude1': 1}
    newTime = datetime.today()
    leaderboard.update(deltas, newTime)
    print(str(leaderboard))
    print("src.gamello.Board.testLeaderBoardPrinting")


def testPostToBoard():
    print('testPostToBoard')
    board = Board('53b92a578425b1f0ae215cdd')
    board.initializeBoard()
    rules = Rules()
    rules.apply = lambda ignored: {'gamello': 2}
    log = Empty()
    log.getLastUpdateTime = lambda : datetime.today()
    board.update(log, rules)
    print('testPostToBoard: passed')


if __name__ == '__main__':
    # board = Board('53b92a578425b1f0ae215cdd')
    # board.initializeBoard()
    # testLeaderBoardUpdate()
    testLeaderBoardPrinting()
    # testPostToBoard()

