from tkinter import *

import gui.gui_manager
import log_manager


class LogView:
    WIDTH, HEIGHT = 250, 50

    def __init__(self, title, timer, window=gui.gui_manager.root):
        self.window = self.__create_window(title, window)
        self.checkboxes = []
        self.timer = timer
        self.main_checkbox = gui.gui_manager.create_checkbox(self.toggle_all_checkboxes, True, self.window)

    def display(self):
        if len(self.timer.timeframes) > 0:
            self.__display_headers()
            self.__display_timeframes()
        else:
            self.__display_empty_notif()

    def __display_headers(self):
        gui.gui_manager.create_label("Customer", self.window).grid(row = 0, column = 1, sticky = W)
        gui.gui_manager.create_label("Date", self.window).grid(row = 0, column = 2, sticky = W)
        gui.gui_manager.create_label("Start", self.window).grid(row = 0, column=3, sticky = W)
        gui.gui_manager.create_label("End", self.window).grid(row = 0, column = 4, sticky = W)
        gui.gui_manager.create_label("Duration", self.window).grid(row = 0, column = 5, sticky = W)
        gui.gui_manager.create_label("Minutes", self.window).grid(row = 0, column = 6, sticky = W)
        self.main_checkbox.checkbutton.grid(row = 0, column = 0, sticky = "nsew")

    def __display_timeframes(self):
        for i, timeframe in enumerate(self.timer.timeframes):
            checkbox = gui.gui_manager.create_checkbox(self.set_correct_value_main_checkbox, True, self.window)
            checkbox.checkbutton.grid(row = i + 1, column = 0, sticky = "nsew")
            self.checkboxes.append(checkbox)

            gui.gui_manager.create_label(timeframe.customer, self.window) \
                .grid(row = i + 1, column = 1, sticky = W)
            gui.gui_manager.create_label(timeframe.get_date_string(), self.window) \
                .grid(row = i + 1, column = 2, sticky = W)
            gui.gui_manager.create_label(timeframe.get_start_string(), self.window) \
                .grid(row = i + 1, column = 3, sticky = W)
            gui.gui_manager.create_label(timeframe.get_end_string(), self.window) \
                .grid(row = i + 1, column = 4, sticky = W)
            gui.gui_manager.create_label(timeframe.get_time_delta_string(), self.window) \
                .grid(row = i + 1, column = 5, sticky = W)
            gui.gui_manager.create_label(round(timeframe.get_time_delta_in_minutes()), self.window) \
                .grid(row = i + 1, column = 6, sticky = W)
            gui.gui_manager.create_separator(HORIZONTAL, self.window) \
                .grid(column = 0, row = i, columnspan = 7, sticky = 'wes')

        for i in range(1, 7):
            gui.gui_manager.create_separator(VERTICAL, self.window) \
                .grid(column = i, row = 0, rowspan=len(self.timer.timeframes) + 1, sticky = 'nsw')

        timeframes = self.__get_selected_timeframes()
        gui.gui_manager.create_button("To Outlook",
                                      lambda: log_manager.open_in_outlook(timeframes),
                                      window=self.window) \
            .grid(row = len(self.timer.timeframes) + 2, column = 0, columnspan = 1, sticky = W)
        gui.gui_manager.create_button("Copy to clipboard",
                                      lambda: log_manager.copy_logs_to_clipboard(timeframes),
                                      width=15,
                                      window=self.window) \
            .grid(row = len(self.timer.timeframes) + 2, column = 2, columnspan = 2)
        gui.gui_manager.create_button("Remove all logs",
                                      self.remove_all_logs,
                                      width=15,
                                      window=self.window) \
            .grid(row = len(self.timer.timeframes) + 2, column = 4, columnspan = 2)

        self.set_correct_value_main_checkbox()

    def __get_selected_timeframes(self):
        return [tf for i, tf in enumerate(self.timer.timeframes) if self.checkboxes[i].var.get()]

    def __display_empty_notif(self):
        self.window.columnconfigure(0, weight = 1)
        self.window.rowconfigure(0, weight = 1)
        gui.gui_manager.create_label("Log is empty.", self.window).grid(row = 0, column = 0)

    def remove_all_logs(self):
        self.timer.clear_timeframes()
        self.window.destroy()
        self.window = self.__create_window("Log cleared", gui.gui_manager.root)
        self.display()

    def __create_window(self, title, window):
        window = Toplevel(window)

        window.resizable(False, False)
        window.title(title)
        window.minsize(self.WIDTH, self.HEIGHT)
        window.geometry(f"+{window.geometry().split('+', 1)[1]}")

        return window

    def toggle_all_checkboxes(self):
        for checkbox in self.checkboxes:
            if self.main_checkbox.var.get():
                checkbox.checkbutton.select()
            else:
                checkbox.checkbutton.deselect()

    def set_correct_value_main_checkbox(self):
        self.main_checkbox.var.set(all(map(IntVar.get, map(gui.gui_manager.Checkbox.get_var, self.checkboxes))))
