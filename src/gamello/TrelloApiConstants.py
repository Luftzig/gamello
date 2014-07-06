TRELLO_API_BASE = "https://trello.com/1/"

AUTHORIZE = "authorize"


def lists(boardId):
    return "boards/{}/lists".format(boardId)


def cards(listId):
    return "lists/{}/cards".format(listId)


def board(boardId):
    return "boards/{}".format(boardId)


def boardMembers(boardId):
    return "boards/{}/members".format(boardId)