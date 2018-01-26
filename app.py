#!/usr/bin/python3

from flask import Flask, render_template, request
from core import *
import time
import webbrowser
import subprocess

app = Flask(__name__)

db = Database()
htmlContentFile = "content.html"

@app.route('/', methods = ['POST', 'GET'])
def index():
    # nothing form / home page
    #-------------------------
    if request.method != 'POST':
        return render_template("index.html", content = "")
    else:
        # save form (save tags)
        #----------------------
        if "saveTags" in request.form:

            # TODO save

            return explore()

        # explore form (search for new albums)
        #-------------------------------------
        elif "explore" in request.form:
            return explore()

@app.errorhandler(404)
def page_not_found(error):
    return render_template('404.html'), 404

def explore():
    reload_entry()

    '''
    htmlContent = open(htmlContentFile, 'r')
    content = htmlContent.read()
    htmlContent.close()
    '''
    content = "<div id=\"content\">"
    newAlbums = db.explore()
    if (len(newAlbums) == 0):
        content = "<div id=\"empty-content\">Nothing new</div>"
        return render_template("index.html", content=content)

    for newOne in newAlbums:
        content += "<div class=\"entry\">" \
                   "<p>" + newOne[0] + "</p>" \
                                       "<form><input type=\"text\" name=\"tags\" placeholder=\"Tags\">" \
                                       "<input type=\"text\" name=\"date\" value=\"" + newOne[
                       1] + "\" placeholder=\"Date\">" \
                            "<input type=\"submit\" name=\"saveTags\" value=\"Save\"></form>" \
                            "</div>"

    for newOne in newAlbums:
        # keys = keys = col(PrintOutput.INPUT, newOne[0] + " - type tags").split("/")
        keys = ["neco1", "neco2"]
        col(PrintOutput.OK, keys)

        db.add_entry(newOne[0], newOne[1], keys)

    content += "</div>"
    return render_template("index.html", content=content)

def reload_entry():
    db.close_entries()
    db.open_entries("entries.txt")
    db.load_entries()

def core_launch():
    rootDir = None

    db.open_config("config.txt")
    db.open_entries("entries.txt")

    db.load_config()
    db.load_entries()

def exit_app():
    db.close_config()
    db.close_entries()
    exit()

if __name__ == "__main__":
    core_launch()
    app.run()
    #webbrowser.open("http://example.com/")
    #subprocess.Popen(['xdg-open', 'http://example.com/'])




'''
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
'''