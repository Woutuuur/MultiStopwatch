from tkinter import *
import tkinter.ttk as ttk
import os
from threading import Timer
import pickle
from PIL import ImageTk as itk
from datetime import datetime
import pyperclip

AMOUNT_OF_TIMERS = 5
BUTTON_WIDTH = 10
DOC_PATH = os.path.join(os.path.expanduser('~'), "Documents")
FOLDER_NAME = "MultiStopWatch"
FULL_PATH = os.path.join(DOC_PATH, FOLDER_NAME)

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
		
		def toString(self):
			return f'{self.getDateString()} | {self.getStartString()} | {self.getEndString()} | {self.getTimeDeltaString()}'

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
			return str(self.getTimeDelta().seconds / 60)

	def remove_all_logs(self):
		self.timeframes.clear()
		self.newWindow.destroy()
		self.view_logs()

	def view_logs(self):
		self.newWindow = Toplevel(root)
		self.newWindow.resizable(False, False)
		self.newWindow.title(f"Timer {self.i+1} logs")
		self.newWindow.minsize(250, 50)
		#self.newWindow.attributes("-toolwindow",1)
		self.newWindow.geometry(f"+{root.geometry().split('+', 1)[1]}")
		if len(self.timeframes) > 0:
			b = Label(self.newWindow, text="Customer")
			b.grid(row = 0, column = 0, sticky=W)
			b = Label(self.newWindow, text="Date")
			b.grid(row=0, column=1, sticky=W)
			b = Label(self.newWindow, text="Start")
			b.grid(row = 0, column = 2, sticky=W)
			b = Label(self.newWindow, text="End")
			b.grid(row = 0, column = 3, sticky=W)
			b = Label(self.newWindow, text="Duration")
			b.grid(row = 0, column = 4, sticky=W)
			b = Label(self.newWindow, text="Minutes")
			b.grid(row = 0, column = 5, sticky=W)
			for i in range(1, len(self.timeframes) + 1):
				b = Label(self.newWindow, text=self.timeframes[i-1].customer)
				b.grid(row=i, column=0, sticky=W)
				b = Label(self.newWindow, text=self.timeframes[i-1].getDateString())
				b.grid(row=i, column=1, sticky=W)
				b = Label(self.newWindow, text=self.timeframes[i-1].getStartString())
				b.grid(row=i, column=2, sticky=W)
				b = Label(self.newWindow, text=self.timeframes[i-1].getEndString())
				b.grid(row=i, column=3, sticky=W)
				b = Label(self.newWindow, text=self.timeframes[i-1].getTimeDeltaString())
				b.grid(row=i, column=4, sticky=W)
				b = Label(self.newWindow, text=round(float(self.timeframes[i-1].getTimeDeltaInMinutes())))
				b.grid(row=i, column=5, sticky=W)
				ttk.Separator(self.newWindow, orient=HORIZONTAL).grid(column=0, row=i-1, columnspan=6, sticky ='wes')
			for i in range(5):
				ttk.Separator(self.newWindow, orient=VERTICAL).grid(column=i+1, row=0, rowspan=len(self.timeframes) + 1, sticky='nsw')
			clear_logs_button = Button(self.newWindow, text="Remove all logs", command=self.remove_all_logs)
			clear_logs_button.grid(row=len(self.timeframes)+2, column=3, columnspan=2)
			copy_button = Button(self.newWindow, text="Copy to clipboard", command=self.copy_logs_to_clipboard)
			copy_button.grid(row=len(self.timeframes)+2, column=1, columnspan=2)
		else:
			b = Label(self.newWindow, text="Log is empty.")
			b.pack()
		
	def copy_logs_to_clipboard(self):
		text = ""
		text += " Datum      | Start    | Einde    | Duratie \n"
		text += "-" * 12 + "+" + "-" * 10 + "+" + "-" * 10 + "+" + "-" * 9 + "\n"
		total = 0
		for item in self.timeframes:
			text +=  " " + item.toString() + "\n"
			total += item.getTimeDelta().total_seconds()
		text += "\n" + " " * 25 + "Totaal:    " + convert_time(total)
		pyperclip.copy(text)

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
		self.time_text['text'] = convert_time(self.current_time)
		self.current_time += 1
		update_total_time()

	def start_timer(self):
		if not self.timerThread.is_alive():
			self.begin_time = datetime.now()
			self.timerThread = RepeatTimer(1, self.update_timer)
			self.timerThread.start()

	def stop_timer(self):
		if self.timerThread.is_alive():
			new_timeframe = self.timeframe(self.begin_time, datetime.now(), self.note.get())
			self.timeframes.append(new_timeframe)
			self.timerThread.cancel()

	def reset_timer(self):
		self.stop_timer()
		self.log('reset')
		self.current_time = 0
		self.time_text['text'] = "0:00:00"

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

def stop_all():
	for timer in timers:
		timer.stop_timer()

def reset_all():
	for timer in timers:
		timer.reset_timer()

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
