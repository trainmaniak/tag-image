#!/usr/bin/python3

from flask import Flask, render_template, request
from core import *
import time
import webbrowser
import subprocess

app = Flask(__name__)

class LastActions:
    lastAlbums = None
    lastSearch = ""
    lastAction = 0   # 0-explore, 1-search

db = Database()
la = LastActions()

htmlContentFile = "content.html"

@app.route('/', methods = ['POST', 'GET'])
def index():
    # nothing form / home page
    #-------------------------
    if request.method != 'POST':
        return render_template("index.html", appName = db.appName, lastSearch=la.lastSearch, content = "")
    else:
        # save form (save tags)
        #----------------------
        if "saveTags" in request.form:
            for newOne in la.lastAlbums:
                if (newOne.name == request.form["subdirName"]):
                    tags = request.form["tags"].replace(" ", "").split(",")
                    col(PrintOutput.OK, tags)

                    if (la.lastAction == 0):
                        db.add_entry(newOne.name, request.form["date"], tags)
                    else:
                        db.change_entry(newOne.name, request.form["date"], tags)

                    # TODO save after search ???? > lastNewAlbums

            if (la.lastAction == 0):
                return explore()
            else:
                return search()

        # open form (open location in file manager)
        #------------------------------------------
        elif "openLocation" in request.form:
            for newOne in la.lastAlbums:
                if (newOne.name == request.form["subdirName"]):
                    path = db.rootDir + "/" + newOne.name
                    os.system('xdg-open "%s"' % path)

                    # TODO open after search ???? > lastNewAlbums

            if (la.lastAction == 0):
                return explore()
            else:
                return search()

        # search form (search for existing albums)
        #-----------------------------------------
        elif "search" in request.form:
            la.lastAction = 1
            la.lastSearch = request.form["searchTags"]
            return search()

        # explore form (search for new albums)
        #-------------------------------------
        elif "explore" in request.form:
            la.lastAction = 0
            return explore()

@app.errorhandler(404)
def page_not_found(error):
    return render_template('404.html'), 404

def get_content(items):
    content = ""
    for oneItem in items:
        tags = None
        if (oneItem.tags == None):
            tags = ""
        else:
            tags = " value=\"" + ", ".join(oneItem.tags) + "\" "

        content += "<div class=\"entry\">" \
                    "<form action=\"http://localhost:5000/\" method=\"post\">" \
                    "<label for=\"subdirName\">" + oneItem.name + "</label>" \
                    "<input type=\"hidden\" name=\"subdirName\" value=\"" + oneItem.name + "\">" \
                    "<input class=\"txt_tags\" type=\"text\" name=\"tags\" placeholder=\"Tags\"" + tags + ">" \
                    "<input class=\"txt_date\" type=\"text\" name=\"date\" value=\"" + oneItem.date + "\" placeholder=\"Date\">" \
                    "<input class=\"btn_save\" type=\"submit\" name=\"saveTags\" value=\"Save\">" \
                    "<input class=\"btn_open\" type=\"submit\" name=\"openLocation\" value=\"Open\"></form>" \
                    "</div>"

    return content

def search():
    primaryMatches = None
    secondaryMatches = list()
    if (la.lastSearch == ""):
        primaryMatches = db.entries
    else:
        tags = la.lastSearch.replace(" ", "").split(",")
        primaryMatches, secondaryMatches = db.search(tags)

    if (len(primaryMatches) == 0 and len(secondaryMatches) == 0):
        content = "<h2>No items found</h2>"
        return render_template("index.html", appName=db.appName, lastSearch=la.lastSearch, content=content)

    la.lastAlbums = list()
    la.lastAlbums.extend(primaryMatches)
    la.lastAlbums.extend(secondaryMatches)

    content = "<h2>Found items:</h2>"

    prim = get_content(primaryMatches)
    if (prim != ""):
        content += "<div id=\"prim\">"
        content += prim
        content += "</div>"

    sec = get_content(secondaryMatches)
    if (sec != ""):
        content += "<div id=\"sec\">"
        content += sec
        content += "</div>"

    return render_template("index.html", appName=db.appName, lastSearch=la.lastSearch, content=content)

def explore():
    reload_entry()

    newAlbums = db.explore()
    if (len(newAlbums) == 0):
        content = "<h2>Nothing new</h2>"
        return render_template("index.html", appName = db.appName, lastSearch=la.lastSearch, content=content)

    la.lastAlbums = newAlbums

    content = "<h2>New albums:</h2>"
    content += get_content(newAlbums)
    return render_template("index.html", appName = db.appName, lastSearch=la.lastSearch, content=content)

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