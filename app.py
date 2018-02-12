#!venv/bin/python3
'''#!venv\Scripts\pythonw.exe'''
'''#!/usr/bin/python3'''

#from flask_socketio import SocketIO, emit
from flask import Flask, render_template, request#, sessions
from core import *
from sys import platform

import subprocess
import webbrowser
import threading

class OsType(Enum):
    LINUX = 0
    OSX = 1
    WIN = 2

class StatInfo:
    appVersion = "linux-0.1.1"
    osType = None
    lastAlbums = None
    lastSearch = ""
    lastAction = -1   # -1-start, 0-explore, 1-search


app = Flask(__name__)
#socketio = SocketIO(app)

db = Database()
si = StatInfo()

htmlContentFile = "content.html"

@app.route('/', methods = ['POST', 'GET'])
def index():
    '''
    print(la.lastAction)
    if (la.lastAction == -1 and db.exploreOnStartup):
        print("asdf")
        la.lastAction = 0
        return explore()
    '''

    # nothing form / home page
    #-------------------------
    if request.method != 'POST':
        return render_template("index.html", appName = db.appName, lastSearch=si.lastSearch, content ="", version=si.appVersion)
    else:
        # save form (save tags)
        #----------------------
        if "saveTags" in request.form:
            for newOne in si.lastAlbums:
                if (newOne.name == request.form["subdirName"]):
                    tags = request.form["tags"].replace(" ", "").split(",")
                    col(PrintOutput.OK, tags)

                    if (si.lastAction == 0):
                        db.add_entry(newOne.name, request.form["date"], tags)
                    else:
                        db.change_entry(newOne.name, request.form["date"], tags)

                    # TODO save after search ???? > lastNewAlbums

                    # TODO font, setting, lib-flask,

            if (si.lastAction == 0):
                return explore()
            else:
                return search()

        # open form (open location in file manager)
        #------------------------------------------
        elif "openLocation" in request.form:
            for newOne in si.lastAlbums:
                if (newOne.name == request.form["subdirName"]):
                    if (si.osType == OsType.LINUX):
                        path = db.rootDir + "/" + newOne.name
                        os.system('xdg-open "%s"' % path)
                    elif (si.osType == OsType.WIN):
                        path = db.rootDir + "\\" + newOne.name
                        subprocess.Popen('explorer "' + path + '\\"')
                        #subprocess.Popen('explorer "C:\Users"')
                        #subprocess.Popen(r'explorer /select,"' + path + '"')
                        #os.system('start "' + path + '"')

                    # TODO open after search ???? > lastNewAlbums

            if (si.lastAction == 0):
                return explore()
            else:
                return search()

        # explore form (search for new albums)
        # -------------------------------------
        elif "explore" in request.form:
            si.lastAction = 0
            return explore()

        # search form (search for existing albums)
        #-----------------------------------------
        elif "search" in request.form:
            si.lastAction = 1
            si.lastSearch = request.form["searchTags"]
            return search()

        # close form (close app)
        # ----------------------
        elif "close" in request.form:
            close_app()

'''
@socketio.on('disconnect')
def close_tab():
    exit_app()
'''

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
    if (si.lastSearch == ""):
        primaryMatches = db.entries
    else:
        tags = si.lastSearch.replace(" ", "").split(",")
        primaryMatches, secondaryMatches = db.search(tags)

    if (len(primaryMatches) == 0 and len(secondaryMatches) == 0):
        content = "<h2>No items found</h2>"
        return render_template("index.html", appName=db.appName, lastSearch=si.lastSearch, content=content, version=si.appVersion)

    si.lastAlbums = list()
    si.lastAlbums.extend(primaryMatches)
    si.lastAlbums.extend(secondaryMatches)

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

    return render_template("index.html", appName=db.appName, lastSearch=si.lastSearch, content=content, version=si.appVersion)

def explore():
    reload_entry()

    newAlbums = db.explore()
    if (len(newAlbums) == 0):
        content = "<h2>Nothing new</h2>"
        return render_template("index.html", appName = db.appName, lastSearch=si.lastSearch, content=content, version=si.appVersion)

    si.lastAlbums = newAlbums

    content = "<h2>New albums:</h2>"
    content += get_content(newAlbums)
    return render_template("index.html", appName = db.appName, lastSearch=si.lastSearch, content=content, version=si.appVersion)

def reload_entry():
    db.close_entries()
    db.open_entries("entries.txt")
    db.load_entries()

def core_launch():
    rootDir = None

    db.open_config("config.txt")
    db.load_config()

    db.open_entries(db.entriesFileLocation)
    db.load_entries()

def close_app():
    db.close_config()
    db.close_entries()
    exit()

if __name__ == "__main__":
    # operating system check
    if platform == "linux" or platform == "linux2":
        si.osType = OsType.LINUX
    elif platform == "darwin":
        si.osType = OsType.OSX
    elif platform == "win32":
        si.osType = OsType.WIN

    col(PrintOutput.DEBUG, "Operating system: " + platform)

    # launch core (db, ...)
    core_launch()

    # run flask and open tab in browser
    port = 5000
    #port = 5000 + random.randint(0, 999)
    url = "http://127.0.0.1:{0}".format(port)
    threading.Timer(1.25, lambda: webbrowser.open(url)).start()
    app.run(port=port, debug=False)
