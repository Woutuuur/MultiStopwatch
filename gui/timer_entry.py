from tkinter import *
import gui.gui_manager as GUIManager
from config import DEFAULT_BUTTON_WIDTH


class TimerEntry:
    def __init__(self, timer):
        self.note = GUIManager.create_text_entry()
        self.start_button = GUIManager.create_button("Start", timer.start_timer)
        self.stop_button = GUIManager.create_button("Pause", timer.stop_timer)
        self.reset_button = GUIManager.create_button("Reset", timer.reset_timer)
        self.view_log_button = GUIManager.create_button("View log", timer.view_logs)
        self.remove_button = GUIManager.create_button("X", timer.remove, width=DEFAULT_BUTTON_WIDTH // 3)
        self.time_text = GUIManager.create_label("0:00:00")

    def render_at_row(self, row):
        self.note.grid(row=row, column=0, sticky=W, padx=5)
        self.start_button.grid(row=row, column=1)
        self.stop_button.grid(row=row, column=2)
        self.reset_button.grid(row=row, column=3)
        self.time_text.grid(row=row, column=4, padx=5)
        self.remove_button.grid(row=row, column=5)
        self.view_log_button.grid(row=row, column=6)

    def destroy(self):
        self.start_button.destroy()
        self.stop_button.destroy()
        self.note.destroy()
        self.reset_button.destroy()
        self.view_log_button.destroy()
        self.time_text.destroy()
        self.remove_button.destroy()

    def clear_note(self):
        self.note.delete(0, END)
