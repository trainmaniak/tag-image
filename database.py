#!/usr/bin/python3

import os

class Entry:
    path = None
    date = None
    tags = None

    def __init__(self, path, date, tags):
        self.path = path
        self.date = date
        self.tags = tags

    def get_matches(self, keys):
        degree = 0
        
        for i in tags:
            if i == keys:
                degree += 1

        return index, degree

class Database:
    fileConfig = None
    fileEntries = None
    rootDir = None
    entries = list()
    
    def __init__(self):
        pass

    def open_entries(self, fileName):
        try:
            self.fileEntries = open(fileName, 'r+')
        except IOError:
            col(0, "open entries file")
        else:
            col(1, "open entries file")

    def load_entries(self):
        for line in self.fileEntries:
            try:
                buffer = line.split(";")
                path = buffer[0]
                date = buffer[1]
                keys = buffer[2].replace('\n', '').split("/")
 
                self.entries.append(Entry(path, date, keys))
            except:
                col(2, "bad format of entries file")
            else:
                col(3, path)
                col(3, date)
                col(3, keys)
        
        col(1, "load entries file")


    def close_entries(self):
        self.fileEntries.close()

    def explore(self):
        newAlbums = list()

        subDirs = next(os.walk(self.rootDir))[1]
        for subDir in subDirs:
            add = True

            for entry in self.entries:
                if (subDir == entry.path):
                    add = False;
            
            if (add):
                newAlbums.append(subDir)
                col(3, subDir)
        
        return newAlbums
        
    def add_entry(self, path, date, keys):
        try:
            line = path+";"+date+";"+('/'.join(keys))
            self.fileEntries.write(line+"\n")
        except IOError:
            col(0, "perrmisions to write file")
        else:
            col(1, "write to file")

    def open_config(self, fileName):
        try:
            self.fileConfig = open(fileName, 'r')
        except IOError:
            col(0, "open config file")
        else:
            col(1, "open config file")

    def load_config(self):
        for line in self.fileConfig:
            try:
                buffer = line.split("=")
                key = buffer[0]
                value = buffer[1].replace('\n', '')

                if (key == "rootDirectory"):
                    self.rootDir = value
                else:
                    col(2, "bad value in config file")
            except:
                col(2, "bad format of config file")
            else:
                col(3, key)
                col(3, value)
        
        col(1, "load config file")

    def close_config(self):
        self.fileConfig.close()
    
    def search(self, keys):
        matches = list()
        
        for i in self.entries:
            matches.append(i.get_matches(keys))

        return matches

def col(y, text):
    W  = "\033[0m"  # white (normal)
    R  = "\033[31m" # red
    G  = "\033[32m" # green
    O  = "\033[33m" # orange
    B  = "\033[34m" # blue
    P  = "\033[35m" # purple

    # fatal error
    if (y == 0):
        print("["+R+"Error"+W+"] - ", end="")
        print(text)
        exit()
    # task ok
    elif (y == 1):
        print("["+G+"Ok"+W+"] - ", end="")
        print(text)
    # ignorable error
    elif (y == 2):
        print("["+O+"Warning"+W+"] - ", end="")
        print(text)
    # debug info
    elif (y == 3):
        print("["+B+"Debug"+W+"] - ", end="")
        print(text)
    # input
    elif (y == 4):
        print("["+P+"Input"+W+"] - ", end="")
        print(text+": ", end="")
        try:
            return input()
        except:
            print()
            col(0, "Keyboard Interrupt")
            exit()

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
        keys = col(4, "type tags").split("/")
        col(1, keys)
        if keys[0] == 'a':
            break;
        db.add_entry(newOne, "datum", keys)

    db.close_config()
    db.close_entries()

#test()