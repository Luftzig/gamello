from RequestsWrapper import RequestsWrapper
import TrelloApiConstants

__author__ = 'yluft'

import os.path


def _getRulesCard(listId):
    cards = RequestsWrapper().getAsPythonList(TrelloApiConstants.cards(listId))


def _getFromBoard(boardId):
    lists = RequestsWrapper().getAsPythonList(TrelloApiConstants.lists(boardId))
    for list in lists:
        # TODO Gamello should be a constant
        if list.get('name') == 'Gamello':
            return _getRulesCard(list.get('id'))




class Rules:

    def __init__(self):
        self.rules = []

    def readFrom(self, source):
        if os.path.isfile(source):
            self._parseRules(file(source).readlines())
        else:
            lines = _getFromBoard(source)

    def _parseRules(self, lines):
        pass


def testGetFromBoard():
    _getFromBoard('53b92a578425b1f0ae215cdd')


if __name__ == '__main__':
    testGetFromBoard()
