#!/usr/bin/python3

from enum import Enum
import os
import os.path
import time

class Entry:
    name = None
    date = None
    tags = None

    def __init__(self, name, date, tags):
        self.name = name
        self.date = date
        self.tags = tags

    def get_matches(self, keys):
        degree = 0
        
        for tag in self.tags:
            if tag == keys:
                degree += 1

        return self.name, degree

class Database:
    fileConfig = None
    fileEntries = None

    rootDir = None
    appName = None

    entries = list()
    
    def __init__(self):
        pass

    def open_entries(self, fileName):
        try:
            self.fileEntries = open(fileName, 'r+')
        except IOError:
            col(PrintOutput.ERROR, "open entries file")
        else:
            col(PrintOutput.OK, "open entries file")

    def load_entries(self):
        self.entries = list()

        for line in self.fileEntries:
            try:
                buffer = line.split(";")
                name = buffer[0]
                date = buffer[1]
                keys = list()

                for key in buffer[2].replace('\n', '').split("/"):
                    keys.append(key)
 
                self.entries.append(Entry(name, date, keys))
            except:
                col(PrintOutput.WARNING, "bad format of entries file")
            else:
                col(PrintOutput.DEBUG, name + " | " + date + " | " + ", ".join(keys))
        
        col(PrintOutput.OK, "load entries file")


    def close_entries(self):
        self.fileEntries.close()
        col(PrintOutput.OK, "close entries file")

    def explore(self):
        newAlbums = list()

        subDirs = next(os.walk(self.rootDir))[1]
        for subDir in subDirs:
            add = True

            if (self.entries != None):
                for entry in self.entries:
                    if (subDir == entry.name):
                        add = False

            if (add):
                # get time of current album
                epochDate = os.path.getctime(self.rootDir + "/" + subDir)
                date = time.strftime('%Y.%m.%d', time.localtime(epochDate))

                newAlbums.append(Entry(subDir, date, None))
                col(PrintOutput.DEBUG, subDir + " - " + date)
        
        return newAlbums
        
    def add_entry(self, path, date, keys):
        try:
            line = path+";"+date+";"+('/'.join(keys))
            self.fileEntries.write(line+"\n")
        except IOError:
            col(PrintOutput.ERROR, "perrmisions to write file")
        else:
            col(PrintOutput.OK, "write to file")

    def open_config(self, fileName):
        try:
            self.fileConfig = open(fileName, 'r')
        except IOError:
            col(PrintOutput.ERROR, "open config file")
        else:
            col(PrintOutput.OK, "open config file")

    def load_config(self):
        for line in self.fileConfig:
            try:
                buffer = line.split("=")
                key = buffer[0]
                value = buffer[1].replace('\n', '')

                if (key == "rootDirectory"):
                    self.rootDir = value
                elif (key == "appName"):
                    self.appName = value
                else:
                    col(PrintOutput.WARNING, "bad value in config file")
            except:
                col(PrintOutput.WARNING, "bad format of config file")
            else:
                col(PrintOutput.DEBUG, key + "=" + value)
        
        col(PrintOutput.OK, "load config file")

    def close_config(self):
        self.fileConfig.close()
        col(PrintOutput.OK, "close config file")
    
    def search(self, keys):
        matches = list()
        
        for entry in self.entries:
            matches.append(entry.get_matches(keys))

        primaryMatches = list()
        for oneMatch in matches:
            if (oneMatch[1] == len(keys)):
                primaryMatches.append(oneMatch)

        secondaryMatches = list()
        degree = len(keys)
        for oneMatch in matches:
            for oneMatch in matches:
                if (oneMatch[1] > 0 and oneMatch[1] == degree):
                    secondaryMatches.append(oneMatch)

            degree -= 1
            if (degree == 0):
                break

        return primaryMatches, secondaryMatches

class PrintOutput(Enum):
    ERROR = 0
    OK = 1
    WARNING = 2
    DEBUG = 3
    INPUT = 4

def col(y, text):
    W  = "\033[0m"  # white (normal)
    R  = "\033[31m" # red
    G  = "\033[32m" # green
    O  = "\033[33m" # orange
    B  = "\033[34m" # blue
    P  = "\033[35m" # purple

    # fatal error
    if (y == PrintOutput.ERROR):
        print("["+R+"  Error"+W+"] - ", end="")
        print(text)
        exit()
    # task ok
    elif (y == PrintOutput.OK):
        print("["+G+"     Ok"+W+"] - ", end="")
        print(text)
    # ignorable error
    elif (y == PrintOutput.WARNING):
        print("["+O+"Warning"+W+"] - ", end="")
        print(text)
    # debug info
    elif (y == PrintOutput.DEBUG):
        print("["+B+"  Debug"+W+"] - ", end="")
        print(text)
    # input
    elif (y == PrintOutput.INPUT):
        print("["+P+"  Input"+W+"] - ", end="")
        print(text+": ", end="")
        try:
            return input()
        except:
            print()
            col(PrintOutput.ERROR, "Keyboard Interrupt")
            exit()
    # nothing
    else:
        col(PrintOutput.ERROR, "Bad \"col\" function call")

'''
def test():
    db = Database()
    rootDir = None

    db.open_config("config")
    db.open_entries("entries")

    db.load_config()
    db.load_entries()

    #db.add_entry("cesta", "datum", {"tagA", "tagB"})
    newAlbums = db.explore()

    for newOne in newAlbums:
        keys = col(PrintOutput.INPUT, newOne + " - type tags").split("/")
        col(PrintOutput.OK, keys)
        if keys[0] == 'a':
            break;
        db.add_entry(newOne, "datum", keys)

    db.close_config()
    db.close_entries()

test()
'''