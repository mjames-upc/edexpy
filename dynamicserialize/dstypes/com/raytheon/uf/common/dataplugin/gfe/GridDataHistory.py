

class GridDataHistory(object):

    def __init__(self):
        self.origin = None
        self.originParm = None
        self.originTimeRange = None
        self.timeModified = None
        self.whoModified = None
        self.updateTime = None
        self.publishTime = None
        self.lastSentTime = None

    def __str__(self):
        return self.__repr__()

    def __repr__(self):
        retVal = "Origin: " + self.origin + '\n'
        retVal += "Origin Parm: " + str(self.originParm) + '\n'
        retVal += "Origin Time Range: " + str(self.originTimeRange) +\
                  " Time Modified: " + str(self.timeModified) +\
                  " Who Modified: " + str(self.whoModified) + '\n'
        retVal += "Update Time: " + str(self.updateTime) + '\n'
        retVal += "Publish Time: " + str(self.publishTime) + '\n'
        retVal += "Last Sent Time: " + str(self.lastSentTime) + '\n'
        return retVal

    def getOrigin(self):
        return self.origin

    def setOrigin(self, origin):
        self.origin = origin

    def getOriginParm(self):
        return self.originParm

    def setOriginParm(self, originParm):
        self.originParm = originParm

    def getOriginTimeRange(self):
        return self.originTimeRange

    def setOriginTimeRange(self, originTimeRange):
        self.originTimeRange = originTimeRange

    def getTimeModified(self):
        return self.timeModified

    def setTimeModified(self, timeModified):
        self.timeModified = timeModified

    def getWhoModified(self):
        return self.whoModified

    def setWhoModified(self, whoModified):
        self.whoModified = whoModified

    def getUpdateTime(self):
        return self.updateTime

    def setUpdateTime(self, updateTime):
        self.updateTime = updateTime

    def getPublishTime(self):
        return self.publishTime

    def setPublishTime(self, publishTime):
        self.publishTime = publishTime

    def getLastSentTime(self):
        return self.lastSentTime

    def setLastSentTime(self, lastSentTime):
        self.lastSentTime = lastSentTime
