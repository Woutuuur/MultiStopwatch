import gui.gui_manager
from application import instance as app


def main():
	gui.gui_manager.init_gui()
	gui.gui_manager.set_on_close_action(app.on_closing)
	app.update_grid()
	app.update_total_time()
	gui.gui_manager.start_gui()


if __name__ == "__main__":
	main()
