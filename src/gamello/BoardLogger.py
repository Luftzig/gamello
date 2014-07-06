
import os
import sys
from RequestsWrapper import RequestsWrapper
from AppPermissions import AppPermissions

class BoardLogger:

    def __init__(self):
        self.boardLogger = {}
        self.timestampFilename = 'UpdateLoggerTime.txt'

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
            print "Exception received with error %s" % error
        finally:
            return boardFullLog
    ##--------------------------------------------------------------##
    def getBoardLog(self):
        boardFullLog = self.getAllBoardData()
        self.boardLogger = {}
        if os.path.exists(self.timestampFilename):
            self.filterBoardLog(boardFullLog)
        else:
            self.boardLogger = boardFullLog
        self.updateLoggerSampleTime(self.boardLogger)
        return self.boardLogger
    ##--------------------------------------------------------------##
    def filterBoardLog(self, boardFullLog):
        lastUpdateTime = self.getLastUpdateTime()
        filterByTimeGenerator = self.filterByTime(boardFullLog, lastUpdateTime)
        for result in filterByTimeGenerator:
            timeStamp = result[0]
            dictionaryEntry = result[1]
            self.boardLogger[timeStamp] = dictionaryEntry
    ##--------------------------------------------------------------##
    def filterByTime(self, boardFullLog, timeStamp):
        for k,v in boardFullLog.items():
            if k > timeStamp:
                yield k, v
    ##--------------------------------------------------------------##
    def updateLoggerSampleTime(self, boardFullLog):
        if boardFullLog != {}:
            lastUpdate = sorted(boardFullLog.keys())[-1]
            f = open(self.timestampFilename, 'w')
            f.write(lastUpdate)
            f.close()
    ##--------------------------------------------------------------##
    def getLastUpdateTime(self):
        f = open(self.timestampFilename, 'r')
        res = f.read()
        return res
    ##--------------------------------------------------------------##

if __name__ == '__main__':
    permissions = AppPermissions(file='../../resources/gamello.config')
    response = RequestsWrapper(permissions=permissions).getAsPythonList('boards/53b92a578425b1f0ae215cdd/actions')

    borderLoggerObj = BoardLogger()
    borderLoggerObj.getBoardLog()
    for k,v in borderLoggerObj.boardLogger.items():
        print k,v
    sys.exit(0)