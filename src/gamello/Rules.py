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


def mergeDeltasIntoFrom(pointsDeltas, ruleDeltas):
    for key in pointsDeltas:
        pointsDeltas[key] += ruleDeltas.get(key, 0)
    for key in ruleDeltas:
        if not pointsDeltas.has_key(key):
            pointsDeltas[key] = ruleDeltas[key]


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

    def apply(self, log):
        pointsDeltas = {}
        for rule in self.rules:
            ruleDeltas = rule.apply(log)
            mergeDeltasIntoFrom(pointsDeltas, ruleDeltas)
        return pointsDeltas


# Tests

def testGetFromBoard():
    _getFromBoard('53b92a578425b1f0ae215cdd')


def testDeltaMerging():
    print("testDeltaMerging")
    originalDelta = {
        'yoav': -5,
        'roy': 3
    }
    ruleDelta = {
        'yoav': 3,
        'daniel': 5
    }
    mergeDeltasIntoFrom(originalDelta, ruleDelta)
    assert originalDelta['yoav'] == -2
    assert originalDelta['roy'] == 3
    assert originalDelta['daniel'] == 5
    print("testDeltaMerging: passed")


def testRulesApply():
    print('testRulesApply')
    rules = Rules()

    class Rule:
        pass

    rule = Rule()
    rule.apply = lambda log: {'yoav': 5}
    rules.rules.append(rule)
    delta = rules.apply(None)
    assert delta['yoav'] == 5
    print('testRulesApply: passed')


if __name__ == '__main__':
    testGetFromBoard()

    testDeltaMerging()
    testRulesApply()
