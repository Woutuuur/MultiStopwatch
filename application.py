import os
import pickle
from GUI.gui_manager import GUIManager
from timer import Timer
from time_util import convert_time
from datetime import datetime
from config import *

class App():
    def __init__(self):
        self.__create_user_folder()
        self.__init_timers()
        self.add_timer_button = GUIManager.create_button("Add", self.add_timer)
        self.start_all_button = GUIManager.create_button("Start all", self.start_all_timers)
        self.stop_all_button = GUIManager.create_button("Pause all",  self.stop_all_timers)
        self.reset_all_button = GUIManager.create_button("Reset all",  self.reset_all_timers)
        self.clear_all_button = GUIManager.create_button("Clear notes",  self.clear_all_labels)
        self.remove_all_button = GUIManager.create_button("Remove all", self.remove_all_timers)
        self.total_time_label = GUIManager.create_label("0:00:00")

    def __init_timers(self):
        if os.path.isfile(os.path.join(FULL_PATH, DATA_FILENAME)):
            self.__load_from_data_file()
        else:
            self.timers = [Timer(i) for i in range(AMOUNT_OF_TIMERS)]

    def __load_from_data_file(self):
        global AMOUNT_OF_TIMERS

        with open(os.path.join(FULL_PATH, DATA_FILENAME), "rb") as f:
            data = pickle.load(f)
            AMOUNT_OF_TIMERS = len(data)
            self.timers = [Timer(i) for i in range(AMOUNT_OF_TIMERS)]
            for i, note_text, current_time, timeframes in data:
                self.timers[i].timer_entry.note.insert(1, note_text)
                self.timers[i].timer_entry.time_text['text'] = convert_time(current_time)
                self.timers[i].current_time = current_time
                self.timers[i].timeframes = timeframes
    
    def __write_to_data_file(self):
        with open(os.path.join(FULL_PATH, DATA_FILENAME), "wb") as f:
            timers_data = []
            for i, timer in enumerate(self.timers):
                timers_data.append([i, timer.timer_entry.note.get(), timer.current_time, timer.timeframes])
            pickle.dump(timers_data, f)
        for timer in self.timers:
            timer.stop_timer()

    def on_closing(self):
        self.__write_to_data_file()
        GUIManager.exit()

    def write_log(self, message):
        filename = f"log{datetime.today().strftime('%Y%m%d')}.txt"
        with open(os.path.join(FULL_PATH, filename), "a+") as f:
            f.write(message)

    def __reindex_timers(self):
        for i in range(len(self.timers)):
            self.timers[i].row = i
            self.timers[i].timer_entry.render_at_row(i)

    def update_grid(self):
        self.start_all_button.grid(row = AMOUNT_OF_TIMERS + 2, column = 1, pady=5)
        self.stop_all_button.grid(row = AMOUNT_OF_TIMERS + 2, column = 2, pady=5)
        self.reset_all_button.grid(row = AMOUNT_OF_TIMERS + 2, column = 3, pady=5)
        self.clear_all_button.grid(row = AMOUNT_OF_TIMERS + 2, column = 0, pady=5)
        self.remove_all_button.grid(row = AMOUNT_OF_TIMERS + 2, column = 4, pady=5)
        self.add_timer_button.grid(row = AMOUNT_OF_TIMERS + 1, column = 0)
        self.total_time_label.grid(row = AMOUNT_OF_TIMERS + 1, column = 4)

    def __create_user_folder(self):
        if not os.path.exists(FULL_PATH):
            os.makedirs(FULL_PATH)

    def update_total_time(self):
        self.total_time_label['text'] = convert_time(sum(map(lambda t: t.current_time, self.timers)))

    def remove_timer(self, i):
        global AMOUNT_OF_TIMERS

        self.timers.pop(i)
        AMOUNT_OF_TIMERS -= 1
        self.__reindex_timers()
        self.update_total_time()

    def stop_all_timers(self):
        for timer in self.timers:
            timer.stop_timer()

    def reset_all_timers(self):
        for timer in self.timers:
            timer.reset_timer()
        self.update_total_time()

    def clear_all_labels(self):
        for timer in self.timers:
            timer.timer_entry.clear_note()

    def start_all_timers(self):
        for timer in self.timers:
            timer.start_timer()

    def remove_all_timers(self):
        global AMOUNT_OF_TIMERS

        for timer in self.timers:
            timer.log('removed')
            timer.destroy()
        AMOUNT_OF_TIMERS = 0
        self.timers.clear()
        self.update_total_time()

    def add_timer(self):
        global AMOUNT_OF_TIMERS

        self.timers.append(Timer(len(self.timers)))
        AMOUNT_OF_TIMERS += 1
        self.__reindex_timers()
        self.update_grid()


instance = App()