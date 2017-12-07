#!/usr/bin/python3

from appJar import gui
import database

class MainWindow:
    window = None

    def __init__(self):
        self.windows = gui()

        self.windows.addLabel("title", "Photo Manager", 0, 0, 1) # Row 0,Column 0,Span 1
        self.windows.addButtons(["Search", "Add new"], self.press_btn, 1, 0, 1) # Row 1,Column 0,Span 1
        self.windows.addButtons(["Exit"], self.press_btn, 2, 1, 0) # Row 2,Column 1
        self.windows.go()

    def press_btn(self, btn):
        if (btn == "Exit"):
            self.window.stop()
        elif (btn == "Search"):
            pass
        elif (btn == "Add new"):
            pass

def main():
    window = MainWindow()

main()