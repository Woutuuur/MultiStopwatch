class Timeframe:
    def __init__(self, start, end, customer):
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
        
    def convert_time(seconds):
        seconds = seconds % (24 * 3600)
        hour = seconds // 3600
        seconds %= 3600
        minutes = seconds // 60
        seconds %= 60
        return "%d:%02d:%02d" % (hour, minutes, seconds)