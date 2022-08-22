import gui.gui_manager as GUIManager
from application import instance as app


def main():
	GUIManager.init_gui()
	GUIManager.set_on_close_action(app.on_closing)
	app.update_grid()
	app.update_total_time()
	GUIManager.start_gui()


if __name__ == "__main__":
	main()
