import pickle
import gui.gui_manager
from timer import Timer
from util.time_util import convert_time
from datetime import datetime
from config import *


def write_log(message):
    filename = f"log{datetime.today().strftime('%Y%m%d')}.txt"
    with open(os.path.join(FULL_PATH, filename), "a+") as f:
        f.write(message)


def create_user_folder():
    if not os.path.exists(FULL_PATH):
        os.makedirs(FULL_PATH)


class App:
    def __init__(self):
        create_user_folder()
        self.__init_timers()
        self.add_timer_button = gui.gui_manager.create_button("Add", self.add_timer)
        self.start_all_button = gui.gui_manager.create_button("Start all", self.start_all_timers)
        self.stop_all_button = gui.gui_manager.create_button("Pause all", self.stop_all_timers)
        self.reset_all_button = gui.gui_manager.create_button("Reset all", self.reset_all_timers)
        self.clear_all_button = gui.gui_manager.create_button("Clear notes", self.clear_all_labels)
        self.remove_all_button = gui.gui_manager.create_button("Remove all", self.remove_all_timers)
        self.total_time_label = gui.gui_manager.create_label("0:00:00")

    def get_amount_of_timers(self):
        return len(self.timers)

    def __init_timers(self):
        if os.path.isfile(os.path.join(FULL_PATH, DATA_FILENAME)):
            self.__load_from_data_file()
        else:
            self.timers = [Timer(i) for i in range(DEFAULT_AMOUNT_OF_TIMERS)]

    def __load_from_data_file(self):
        with open(os.path.join(FULL_PATH, DATA_FILENAME), "rb") as f:
            data = pickle.load(f)
            self.timers = [Timer(i) for i in range(len(data))]
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
        gui.gui_manager.close()

    def __reindex_timers(self):
        for i in range(len(self.timers)):
            self.timers[i].row = i
            self.timers[i].timer_entry.render_at_row(i)

    def update_grid(self):
        offset = self.get_amount_of_timers()

        self.add_timer_button.grid(row = offset + 1, column = 0)
        self.total_time_label.grid(row = offset + 1, column = 4)
        self.start_all_button.grid(row = offset + 2, column = 1, pady = 5)
        self.stop_all_button.grid(row = offset + 2, column = 2, pady = 5)
        self.reset_all_button.grid(row = offset + 2, column = 3, pady = 5)
        self.clear_all_button.grid(row = offset + 2, column = 0, pady = 5)
        self.remove_all_button.grid(row = offset + 2, column = 4, pady = 5)

    def update_total_time(self):
        self.total_time_label['text'] = convert_time(sum(map(Timer.get_current_time, self.timers)))

    def remove_timer(self, i):
        self.timers.pop(i)
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
        for timer in self.timers:
            timer.log('removed')
            timer.destroy()
        self.timers.clear()
        self.update_total_time()

    def add_timer(self):
        self.timers.append(Timer(len(self.timers)))
        self.__reindex_timers()
        self.update_grid()


instance = App()
