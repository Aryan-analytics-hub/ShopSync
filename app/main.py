"""Desktop application entry point."""

import customtkinter as ctk

from gui.login import LoginWindow
from gui.main_window import MainWindow


ctk.set_appearance_mode("Dark")
ctk.set_default_color_theme("blue")


def launch_main_window(user):
    app = MainWindow(user)
    app.mainloop()


def main():
    login = LoginWindow(launch_main_window)
    login.mainloop()


if __name__ == "__main__":
    main()
