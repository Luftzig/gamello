
import sys
import requests


def prettyPrint(message, token ='*'):
    print len(message)* token
    print message
    print len(message)* token

#-----------------

if __name__ == "__main__":
    rc = 0
    url = "https://api.trello.com/1/boards/i8AxuVZG/cards"
    payload = {
        'fields': 'name',
        'key': 'b0bb19aa5adaa321f38ea1fee886c30f',
        'token': '5e41f24ad3e47dbf8d2ed3a9610ab923f73e1ce21f294afc4ddb333ae2ca087e',
        }
    try:
        r = requests.get(url, params=payload)
        for oneResult in r.json():
            print oneResult
        prettyPrint("Done printing all requests!")

    except  ValueError as error:
        print "ValueError caught with error: %s" % error
        rc = -1
    finally:
        sys.exit(rc)

