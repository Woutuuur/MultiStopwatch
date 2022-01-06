from tkinter import *
import tkinter.ttk as ttk
import os
from threading import Timer
import pickle
from PIL import ImageTk as itk
from datetime import datetime, timedelta
import html2clipboard as h2c
import copy
from functools import partial

AMOUNT_OF_TIMERS = 5
BUTTON_WIDTH = 10
DOC_PATH = os.path.join(os.path.expanduser('~'), "Documents")
FOLDER_NAME = "MultiStopWatch"
FULL_PATH = os.path.join(DOC_PATH, FOLDER_NAME)

ics_base = ''' 
BEGIN:VCALENDAR
VERSION:2.0
PRODID:-//woutervandenbroeke//MultiStopWatch 1.4//EN
BEGIN:VEVENT
UID:MultiStopWatch-1.4
TZID:Europe/Amsterdam
DTSTAMP:*DTSTAMP*
DTSTART:*DTSTART*
DTEND:*DTEND*
SUMMARY:*TITLE*
END:VEVENT
END:VCALENDAR
'''

root = Tk()
if not os.path.exists(FULL_PATH):
	os.makedirs(FULL_PATH)

def convert_time(seconds):
	seconds = seconds % (24 * 3600)
	hour = seconds // 3600
	seconds %= 3600
	minutes = seconds // 60
	seconds %= 60
	return "%d:%02d:%02d" % (hour, minutes, seconds)

class RepeatTimer(Timer):
    def run(self):
        while not self.finished.wait(self.interval):
            self.function(*self.args, **self.kwargs)

class timer:
	def __init__(self, i):
		self.i = i
		self.note = Entry(root)
		self.start_button = Button(root, text="Start", takefocus=0, command=self.start_timer, width = BUTTON_WIDTH)
		self.stop_button = Button(root, text = "Pause", takefocus=0, command=self.stop_timer, width = BUTTON_WIDTH)
		self.reset_button = Button(root, text="Reset", takefocus=0, command=self.reset_timer, width = BUTTON_WIDTH)
		self.view_log_button = Button(root, text="View log", takefocus=0, command=self.view_logs, width = BUTTON_WIDTH)
		self.time_text = Label(root, text="0:00:00")
		self.paused = True
		self.current_time = 0.0
		self.timerThread = RepeatTimer(1, self.update_timer)
		self.remove_button = Button(root, text = "X", takefocus = 0, width = BUTTON_WIDTH//3, command=self.remove)
		self.update_grid()
		self.timeframes = []
		self.begin_time = datetime.now()

	class timeframe:
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

	def remove_all_logs(self):
		self.timeframes.clear()
		self.newWindow.destroy()
		self.view_logs()

	def view_logs(self):
		self.newWindow = Toplevel(root)
		self.newWindow.resizable(False, False)
		self.newWindow.title(f"Timer {self.i+1} logs")
		self.newWindow.minsize(250, 50)
		self.checkbox_values = []
		#self.newWindow.attributes("-toolwindow",1)
		self.newWindow.geometry(f"+{root.geometry().split('+', 1)[1]}")
		if len(self.timeframes) > 0:
			b = Label(self.newWindow, text="Customer")
			b.grid(row = 0, column = 1, sticky=W)
			b = Label(self.newWindow, text="Date")
			b.grid(row=0, column=2, sticky=W)
			b = Label(self.newWindow, text="Start")
			b.grid(row = 0, column = 3, sticky=W)
			b = Label(self.newWindow, text="End")
			b.grid(row = 0, column = 4, sticky=W)
			b = Label(self.newWindow, text="Duration")
			b.grid(row = 0, column = 5, sticky=W)
			b = Label(self.newWindow, text="Minutes")
			b.grid(row = 0, column = 6, sticky=W)
			for i in range(1, len(self.timeframes) + 1):
				checkbox_value = IntVar()
				b = Checkbutton(self.newWindow, variable=checkbox_value)
				b.grid(row=i, column=0, sticky="nsew")
				self.checkbox_values.append(checkbox_value)
				b = Label(self.newWindow, text=self.timeframes[i-1].customer)
				b.grid(row=i, column=1, sticky=W)
				b = Label(self.newWindow, text=self.timeframes[i-1].getDateString())
				b.grid(row=i, column=2, sticky=W)
				b = Label(self.newWindow, text=self.timeframes[i-1].getStartString())
				b.grid(row=i, column=3, sticky=W)
				b = Label(self.newWindow, text=self.timeframes[i-1].getEndString())
				b.grid(row=i, column=4, sticky=W)
				b = Label(self.newWindow, text=self.timeframes[i-1].getTimeDeltaString())
				b.grid(row=i, column=5, sticky=W)
				b = Label(self.newWindow, text=round(self.timeframes[i-1].getTimeDeltaInMinutes()))
				b.grid(row=i, column=6, sticky=W)
				ttk.Separator(self.newWindow, orient=HORIZONTAL).grid(column=0, row=i-1, columnspan=7, sticky ='wes')
			for i in range(6):
				ttk.Separator(self.newWindow, orient=VERTICAL).grid(column=i+1, row=0, rowspan=len(self.timeframes) + 1, sticky='nsw')
			b = Button(self.newWindow, text="To Outlook", command=self.open_in_outlook)
			b.grid(row=len(self.timeframes)+2, column=0, columnspan=1, sticky=W)
			copy_button = Button(self.newWindow, text="Copy all to clipboard", command=lambda: self.copy_logs_to_clipboard(self.newWindow))
			copy_button.grid(row=len(self.timeframes)+2, column=2, columnspan=2)
			clear_logs_button = Button(self.newWindow, text="Remove all logs", command=self.remove_all_logs)
			clear_logs_button.grid(row=len(self.timeframes)+2, column=4, columnspan=2)

		else:
			b = Label(self.newWindow, text="Log is empty.")
			b.pack()
	
	def to_ics_timeformat(self, time):
		t = str(time.isoformat())
		t = t.replace('-', '').replace(':', '').split('.')[0]
		return t

	def open_in_outlook(self):
		timeframes = [timeframe for i, timeframe in enumerate(self.timeframes) if self.checkbox_values[i].get()]
		mins = 0
		dtstamp = self.to_ics_timeformat(datetime.now())
		dtstart = self.to_ics_timeformat(min([x.start for x in timeframes]))
		dtend = self.to_ics_timeformat(max([x.end for x in timeframes]))
		mins = int(round(sum([x.getTimeDeltaInMinutes() for x in timeframes])))
		customer = timeframes[0].customer
		hrs = mins // 60
		time_s = str(mins)
		if (hrs > 0):
			mins %= 60
			time_s = f"{hrs}:{mins:02}"
		filename = FULL_PATH + "/_tmp.ics"
		title = f"{time_s} - {customer}"
		s = ics_base.replace("*DTSTAMP*", dtstamp).replace("*DTSTART*", dtstart).replace("*DTEND*", dtend).replace("*TITLE*", title)
		with open(filename, "w") as f:
			f.write(s)
		os.startfile(filename)

	def timeframes_to_table(self, timeframes):
		text = '''<body><table cellspacing="0" border="1">'''
		text += "<tr><th>Datum</th><th>Start</th><th>Einde</th><th>Duratie</th></tr>"
		total = 0
		for item in timeframes:
			text  += item.toHTMLRow()
			total += item.getTimeDelta().total_seconds()
		text += f'''<tr><td colspan="3"><b>Totaal</b><td>{convert_time(total)}</td></tr>'''
		text += "</table></body>"
		text += "<style>table, th, td{ padding: 10px; border: 1px solid black; border-collapse: collapse; }</style>"
		return text

	def copy_logs_to_clipboard(self, logs_window):
		def handle_single_customer(customer, window):
			h2c.PutHtml(self.timeframes_to_table(timeframesByCustomer[customer]))
			window.destroy()
			
		if len(self.timeframes) == 0: h2c.PutHtml(""); return
		timeframesByCustomer = {}
		for timeframe in self.timeframes:
			if timeframe.customer in timeframesByCustomer:
				timeframesByCustomer[timeframe.customer].append(timeframe)
			else:
				timeframesByCustomer[timeframe.customer] = [timeframe]

		text = ""
		customers = list(timeframesByCustomer.keys())
		if len(timeframesByCustomer) == 1: 
			text = self.timeframes_to_table(self.timeframes)
			h2c.PutHtml(text)
		else:
			newWindow = Toplevel(logs_window)
			newWindow.resizable(False, False)
			newWindow.title("Which customer?")
			newWindow.geometry(f"+{root.geometry().split('+', 1)[1]}")
			for i, customer in enumerate(customers):
				b = Button(newWindow, text=customer, command=lambda c = customer: handle_single_customer(c, newWindow), width=40)
				b.grid(row=i, column=0, columnspan=10)

	def update_grid(self):
		self.view_log_button.grid(row = self.i, column = 6)
		self.reset_button.grid(row = self.i, column = 3)
		self.stop_button.grid(row = self.i, column = 2)
		self.start_button.grid(row = self.i, column = 1)
		self.remove_button.grid(row = self.i, column = 5)
		self.time_text.grid(row = self.i, column = 4, padx = 5)
		self.note.grid(row = self.i, column = 0, sticky=W, padx = 5)

	def log(self, context):
		if self.current_time > 0:
			if len(self.note.get()) > 0:
				write_log(f"{datetime.today().strftime('%Y-%m-%d %H:%M:%S')} stopwatch {self.i + 1} with label '{self.note.get()}' {context} at {self.time_text['text']}\n")
			else:
				write_log(f"{datetime.today().strftime('%Y-%m-%d %H:%M:%S')} stopwatch {self.i + 1} {context} at {self.time_text['text']}\n")

	def destroy(self):
		self.stop_timer()
		self.note.destroy()
		self.start_button.destroy()
		self.stop_button.destroy()
		self.time_text.destroy()
		self.reset_button.destroy()
		self.remove_button.destroy()
		self.view_log_button.destroy()

	def remove(self):
		self.log('removed')
		self.destroy()
		remove_timer(self.i)

	def update_timer(self):
		self.current_time += 1
		self.time_text['text'] = convert_time(self.current_time)
		update_total_time()

	def start_timer(self):
		self.time_text['bg'] = '#e89595'
		if not self.timerThread.is_alive():
			self.begin_time = datetime.now()
			self.timerThread = RepeatTimer(1, self.update_timer)
			self.timerThread.start()

	def stop_timer(self):
		self.time_text['bg'] = '#f0f0f0'
		if self.timerThread.is_alive():
			new_timeframe = self.timeframe(self.begin_time, datetime.now(), self.note.get())
			# new_timeframe = self.timeframe(self.begin_time - timedelta(hours=1, minutes=30), datetime.now(), self.note.get())
			self.timeframes.append(new_timeframe)
			self.timerThread.cancel()

	def reset_timer(self):
		self.stop_timer()
		self.log('reset')
		self.current_time = 0
		self.time_text['text'] = "0:00:00"
		update_total_time()

if os.path.isfile(os.path.join(FULL_PATH, "data.dat")):
	with open(os.path.join(FULL_PATH, "data.dat"), "rb") as f:
		data = pickle.load(f)
		AMOUNT_OF_TIMERS = len(data)
		timers = [timer(i) for i in range(AMOUNT_OF_TIMERS)]
		for timerdata in data:
			timers[timerdata[0]].note.insert(1, timerdata[1])
			timers[timerdata[0]].current_time = timerdata[2]
			timers[timerdata[0]].time_text['text'] = convert_time(timerdata[2])
			timers[timerdata[0]].timeframes = timerdata[3]
else:
	timers = [timer(i) for i in range(AMOUNT_OF_TIMERS)]

root.title('Multi Stopwatch')
root.resizable(False, False)

def write_log(message):
	with open(os.path.join(FULL_PATH, f"log{datetime.today().strftime('%Y%m%d')}.txt"), "a+") as f:
		f.write(message)

def reindex_timers():
	for n in range(len(timers)):
		timers[n].i = n
		timers[n].update_grid()

def remove_timer(i):
	global AMOUNT_OF_TIMERS
	timers.pop(i)
	AMOUNT_OF_TIMERS -= 1
	reindex_timers()
	update_total_time()

def stop_all():
	for timer in timers:
		timer.stop_timer()

def reset_all():
	for timer in timers:
		timer.reset_timer()
	update_total_time()

def clear_all():
	for timer in timers:
		timer.note.delete(0, END)

def start_all():
	for timer in timers:
		timer.start_timer()

def remove_all():
	global AMOUNT_OF_TIMERS
	for timer in timers:
		timer.log('removed')
		timer.destroy()
	AMOUNT_OF_TIMERS = 0
	timers.clear()
	update_total_time()

def add_timer():
	global AMOUNT_OF_TIMERS
	timers.append(timer(len(timers)))
	AMOUNT_OF_TIMERS += 1
	reindex_timers()
	update_grid()

def update_grid():
	start_all_button.grid(row = AMOUNT_OF_TIMERS+2, column = 1, pady=5)
	stop_all_button.grid(row = AMOUNT_OF_TIMERS+2, column = 2, pady=5)
	reset_all_button.grid(row = AMOUNT_OF_TIMERS+2, column = 3, pady=5)
	clear_all_button.grid(row = AMOUNT_OF_TIMERS+2, column = 0, pady=5)
	remove_all_button.grid(row = AMOUNT_OF_TIMERS+2, column = 4, pady=5)
	add_timer_button.grid(row = AMOUNT_OF_TIMERS+1, column = 0)
	total_time_label.grid(row = AMOUNT_OF_TIMERS + 1, column = 4)

add_timer_button = Button(root, text="Add", takefocus = 0, command=add_timer, width = BUTTON_WIDTH)
start_all_button = Button(root, text="Start all", takefocus = 0, command=start_all, width = BUTTON_WIDTH)
stop_all_button = Button(root, text="Pause all", takefocus = 0, command=stop_all, width = BUTTON_WIDTH)
reset_all_button = Button(root, text="Reset all", takefocus=0, command=reset_all, width = BUTTON_WIDTH)
clear_all_button = Button(root, text="Clear notes", takefocus = 0, command=clear_all, width = BUTTON_WIDTH)
remove_all_button = Button(root, text="Remove all", takefocus=0, command=remove_all, width = BUTTON_WIDTH)
total_time_label = Label(root, text="0:00:00", takefocus=0, width = BUTTON_WIDTH)

update_grid()

def on_closing():
	with open(os.path.join(FULL_PATH, "data.dat"), "wb") as f:
		timers_data = []
		for i, timer in enumerate(timers):
			timers_data.append([i, timer.note.get(), timer.current_time, timer.timeframes])
		pickle.dump(timers_data, f)
	for timer in timers:
		timer.stop_timer()
	root.destroy()

def update_total_time():
	total_time = 0
	for timer in timers:
		total_time += timer.current_time
	total_time_label['text'] = convert_time(total_time)

root.protocol("WM_DELETE_WINDOW", on_closing)
update_total_time()
root.mainloop()
