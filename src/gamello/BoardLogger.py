
import os
import sys
from PublicTools import prettyPrint
from RequestsWrapper import RequestsWrapper
from AppPermissions import AppPermissions

class BoardLogger:

    def __init__(self):
        self.dataDict = {}
        self.filename = 'UpdateLoggerTime.txt'

    ##--------------------------------------------------------------##
    def getAllBoardData(self):
        try:
            rc = 0
            boardFullLog = {}
            permissions = AppPermissions(file='../../resources/gamello.config')
            response = RequestsWrapper(permissions=permissions).getAsPythonList('boards/53b92a578425b1f0ae215cdd/actions')
            for entry in response:
                boardFullLog[entry["date"]] = entry
        except Exception as error:
            prettyPrint("Exception received with error %s" % error)
        finally:
            return boardFullLog
    ##--------------------------------------------------------------##
    def getBoardlogData(self):
        boardFullLog = self.getAllBoardData()
        self.dataDict = {}
        if os.path.exists(self.filename):
            lastUpdateTime = self.getLastUpdateTime()
            myGenerator = self.filterByTime(boardFullLog, lastUpdateTime)
            for entry in myGenerator:
                self.dataDict[entry[0]]= entry[1]
        else:
            self.dataDict = boardFullLog
        self.updateLoggerSampleTime(self.dataDict)
        return self.dataDict
    ##--------------------------------------------------------------##
    def filterByTime(self, boardFullLog, timeStamp):
        for k,v in boardFullLog.items():
            if k > timeStamp:
                yield k, v
    ##--------------------------------------------------------------##
    def updateLoggerSampleTime(self,boardFullLog):
        if boardFullLog != {}:
            lastUpdate = sorted(boardFullLog.keys())[-1]
            f = open(self.filename, 'w')
            f.write(lastUpdate)
            f.close()
    ##--------------------------------------------------------------##
    def getLastUpdateTime(self):
        f = open(self.filename, 'r')
        res = f.read()
        return res
    ##--------------------------------------------------------------##

if __name__ == '__main__':
    permissions = AppPermissions(file='../../resources/gamello.config')
    response = RequestsWrapper(permissions=permissions).getAsPythonList('boards/53b92a578425b1f0ae215cdd/actions')

    borderLoggerObj = BoardLogger()
    borderLoggerObj.getBoardlogData()
    for k,v in borderLoggerObj.dataDict.items():
        print k,v
    sys.exit(0)