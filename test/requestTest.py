
import sys
import requests
import unittest


############################################################
############        Global Variables         ###############
############################################################
URL        = "https://api.trello.com/1/"
BOARD      = "boards/i8AxuVZG/cards"
USER_KEY   = "b0bb19aa5adaa321f38ea1fee886c30f"
TOKKEN_API = "5e41f24ad3e47dbf8d2ed3a9610ab923f73e1ce21f294afc4ddb333ae2ca087e"



############################################################
############       Helper Methods          #################
############################################################
def prettyPrint(message, token ='*'):
    print len(message)* token
    print message
    print len(message)* token
##--------------------------------------------------------##
def genericRequest(url, payload):
    r = requests.get(url, params=payload)
    for oneResult in r.json():
        print oneResult



############################################################
############        Main Methods           #################
############################################################
def getNameRequest():
    url = "%s%s" % (URL,BOARD)
    payload = {
                'fields': 'name',
                'key': USER_KEY,
                'token': TOKKEN_API,
              }
    genericRequest(url,payload)


class RequestTest(unittest.TestCase):

    def test(self):
        getNameRequest()


##---------------------------------------##
if __name__ == "__main__":
    rc = -1
    try:
        getNameRequest()
        prettyPrint("Done printing all requests!")
        rc = 0
    except  ValueError as error:
        print "ValueError caught with error: %s" % error
    finally:
        sys.exit(rc)

