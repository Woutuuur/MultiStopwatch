import datetime


class Timeframe:
    def __init__(self, start: datetime.datetime, end: datetime.datetime, customer):
        self.start = start
        self.end = end
        self.customer = customer

    def to_html_row(self):
        return f'<tr><td>{self.get_date_string()}</td><td>{self.get_start_string()}</td>' \
               f'<td>{self.get_end_string()}</td><td>{self.get_time_delta_string()}</td></tr>'

    def get_start_string(self):
        return str(self.start).split('.', 2)[0].split(' ')[1]
    
    def get_end_string(self):
        return str(self.end).split('.', 2)[0].split(' ')[1]

    def get_time_delta(self):
        return self.end - self.start
    
    def get_time_delta_string(self):
        return str(self.get_time_delta()).split('.', 2)[0]

    def get_date_string(self):
        return str(self.start).split('.', 2)[0].split(' ')[0]

    def get_time_delta_in_minutes(self):
        return float(self.get_time_delta().seconds / 60)

    def get_time_delta_in_seconds(self):
        return self.get_time_delta().total_seconds()
