TRELLO_API_BASE = "https://trello.com/1/"

AUTHORIZE = "authorize"


def lists(boardId):
    return "boards/{}/lists".format(boardId)


def cards(listId):
    return "lists/{}/cards".format(listId)