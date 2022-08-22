import datetime


class Timeframe:
    def __init__(self, start: datetime.datetime, end: datetime.datetime, customer):
        self.start = start
        self.end = end
        self.customer = customer

    def toHTMLRow(self):
        return f'<tr><td>{self.getDateString()}</td><td>{self.getStartString()}</td><td>{self.getEndString()}</td><td>{self.getTimeDeltaString()}</td></tr>'

    def getStartString(self):
        return str(self.start).split('.', 2)[0].split(' ')[1]
    
    def getEndString(self):
        return str(self.end).split('.', 2)[0].split(' ')[1]

    def getTimeDelta(self):
        return self.end - self.start
    
    def getTimeDeltaString(self):
        return str(self.getTimeDelta()).split('.', 2)[0]

    def getDateString(self):
        return str(self.start).split('.', 2)[0].split(' ')[0]

    def getTimeDeltaInMinutes(self):
        return float(self.getTimeDelta().seconds / 60)

    def getTimeDeltaInSeconds(self):
        return self.getTimeDelta().total_seconds()
