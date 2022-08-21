from tkinter import *
from tkinter import ttk as ttk

root = Tk()

class GUIManager():
    BUTTON_WIDTH = 10

    def init_gui():
        root.title('Multi Stopwatch')
        root.resizable(False, False)

    def start_gui():
        root.mainloop()

    def set_on_close_action(action):
        root.protocol("WM_DELETE_WINDOW", action)

    def create_button(text, command, width = BUTTON_WIDTH, window = root):
        return Button(window, text=text, takefocus=False, command=command, width=width)
    
    def create_text_entry(window = root):
        return Entry(window)
    
    def create_label(text, window = root):
        return Label(window, text = text)

    def create_checkbox(command, checked = False, window = root):
        value = IntVar(value = int(checked))
        button = Checkbutton(window, variable = value, command = command)

        return GUIManager.Checkbox(value, button)

    def create_separator(orientation, window = root):
        return ttk.Separator(window, orient=orientation)

    def exit():
        root.destroy()

    class Checkbox():
        def __init__(self, var, checkbutton):
            self.var = var
            self.checkbutton = checkbutton
        
        def getVar(self):
            return self.var