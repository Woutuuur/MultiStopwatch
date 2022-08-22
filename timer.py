from tkinter import *
import threading
from gui.timer_entry import TimerEntry
from datetime import datetime, timedelta
from gui.log_view import LogView
import application
from util.time_util import convert_time
import timeframe

class RepeatTimer(threading.Timer):
    def run(self):
        while not self.finished.wait(self.interval):
            self.function(*self.args, **self.kwargs)

class Timer:
    def __init__(self, row):
        self.row = row
        self.paused = True
        self.timeframes = []
        self.current_time = 0.0
        self.begin_time = datetime.now()
        self.timer_entry = TimerEntry(self)
        self.timerThread = RepeatTimer(1, self.update_timer)
        self.timer_entry.render_at_row(self.row)

    def clear_timeframes(self):
        self.timeframes.clear()

    def view_logs(self):
        log_view = LogView(f"Timer {self.row + 1} logs", self)
        log_view.display()

    def get_current_time(self):
        return self.current_time

    def log(self, context):
        if self.current_time > 0:
            if len(self.timer_entry.note.get()) > 0:
                application.write_log(f"{datetime.today().strftime('%Y-%m-%d %H:%M:%S')} stopwatch {self.row + 1} with label '{self.timer_entry.note.get()}' {context} at {self.timer_entry.time_text['text']}\n")
            else:
                application.write_log(f"{datetime.today().strftime('%Y-%m-%d %H:%M:%S')}"
                                      f" stopwatch {self.row + 1} {context}"
                                      f" at {self.timer_entry.time_text['text']}\n")

    def destroy(self):
        self.stop_timer()
        self.timer_entry.destroy()

    def remove(self):
        self.log('removed')
        self.destroy()
        application.instance.remove_timer(self.row)

    def update_timer(self):
        self.current_time += 1
        self.timer_entry.time_text['text'] = convert_time(self.current_time)
        application.instance.update_total_time()

    def start_timer(self):
        self.timer_entry.time_text['bg'] = '#e89595'
        if not self.timerThread.is_alive():
            self.begin_time = datetime.now()
            self.timerThread = RepeatTimer(1, self.update_timer)
            self.timerThread.start()

    def stop_timer(self):
        self.timer_entry.time_text['bg'] = '#f0f0f0'
        if self.timerThread.is_alive():
            new_timeframe = timeframe.Timeframe(self.begin_time, datetime.now(), self.timer_entry.note.get())
            self.timeframes.append(new_timeframe)
            self.timerThread.cancel()

    def reset_timer(self):
        self.stop_timer()
        self.log('reset')
        self.current_time = 0
        self.timer_entry.time_text['text'] = "0:00:00"
        application.instance.update_total_time()
