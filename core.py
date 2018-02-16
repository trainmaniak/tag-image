
import os
import os.path
import time

from tools import *

class Entry:
    name = None
    date = None
    tags = None

    def __init__(self, name, date, tags):
        self.name = name
        self.date = date
        self.tags = tags

    def get_matches(self, tags):
        degree = 0
        
        for tag in tags:
            if tag in self.tags:
                degree += 1

        return self, degree

class Database:
    fileConfig = None
    entriesFileLocation = None
    exploreOnStartup = False
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
            InfoPrinter.out(PrintOutput.WARNING, "cannot open entries file")

            # TODO rewrite old entries file because permission ???

            try:
                newFile = open(fileName, 'w')
                newFile.close()
                InfoPrinter.out(PrintOutput.OK, 'created new entries file')

                self.open_entries(fileName)
            except:
                InfoPrinter.out(PrintOutput.ERROR, 'cannot create new entries file')

        else:
            InfoPrinter.out(PrintOutput.OK, "open entries file")

    def load_entries(self):
        self.entries = list()

        for line in self.fileEntries:
            try:
                buffer = line.split(";")
                name = buffer[0]
                date = buffer[1]
                keys = list()

                for key in buffer[2].replace('\r', '').replace('\n', '').split("/"):
                    keys.append(key)
 
                self.entries.append(Entry(name, date, keys))
            except:
                InfoPrinter.out(PrintOutput.WARNING, "bad format of entries file")
            else:
                InfoPrinter.out(PrintOutput.DEBUG, name + " | " + date + " | " + ", ".join(keys))
        
        InfoPrinter.out(PrintOutput.OK, "load entries file")


    def close_entries(self):
        self.fileEntries.close()
        InfoPrinter.out(PrintOutput.OK, "close entries file")

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
                InfoPrinter.out(PrintOutput.DEBUG, subDir + " - " + date)
        
        return newAlbums
        
    def add_entry(self, name, date, tags):
        try:
            line = name + ";" + date + ";" + ('/'.join(tags))
            self.fileEntries.write(line+"\r\n")
        except IOError:
            InfoPrinter.out(PrintOutput.ERROR, "permissions to write file")
        else:
            InfoPrinter.out(PrintOutput.OK, "write to file")

    def change_entry(self, name, date, tags):
        for entry in self.entries:
            if (entry.name == name):
                entry.date = date
                entry.tags = tags

        try:
            #open('file.txt', 'w').close()
            self.close_entries()
            self.open_entries(self.entriesFileLocation)
            self.fileEntries.truncate()

            for entry in self.entries:
                self.add_entry(entry.name, entry.date, entry.tags)
        except IOError:
            InfoPrinter.out(PrintOutput.ERROR, "permissions to write file")
        else:
            InfoPrinter.out(PrintOutput.OK, "change entry in file")

    def open_config(self, fileName):
        try:
            self.fileConfig = open(fileName, 'r')
        except IOError:
            InfoPrinter.out(PrintOutput.ERROR, "open config file")
        else:
            InfoPrinter.out(PrintOutput.OK, "open config file")

    def load_config(self):
        for line in self.fileConfig:
            try:
                buffer = line.split("=")
                key = buffer[0]
                value = buffer[1].replace('\r', '').replace('\n', '')

                if (key == "rootDirectory"):
                    self.rootDir = value
                elif (key == "appName"):
                    self.appName = value
                elif (key == "entriesFileLocation"):
                    self.entriesFileLocation = value
                elif (key == "exploreOnStartup"):
                    if (value == "true"):
                        self.exploreOnStartup = True
                else:
                    InfoPrinter.out(PrintOutput.WARNING, "bad value in config file")
            except:
                InfoPrinter.out(PrintOutput.WARNING, "bad format of config file")
            else:
                InfoPrinter.out(PrintOutput.DEBUG, key + "=" + value)
        
        InfoPrinter.out(PrintOutput.OK, "load config file")

    def close_config(self):
        self.fileConfig.close()
        InfoPrinter.out(PrintOutput.OK, "close config file")
    
    def search(self, keys):
        matches = list()
        
        for entry in self.entries:
            print(keys)
            print("///" + str(entry.get_matches(keys)[1]))
            matches.append(entry.get_matches(keys))

        primaryMatches = list()
        for oneMatch in matches:
            if (oneMatch[1] == len(keys)):
                primaryMatches.append(oneMatch[0])

        secondaryMatches = list()
        degree = len(keys) - 1
        for oneMatch in matches:
            for oneMatch in matches:
                if (oneMatch[1] > 0 and oneMatch[1] == degree):
                    secondaryMatches.append(oneMatch[0])

            degree -= 1
            if (degree == 0):
                break

        return primaryMatches, secondaryMatches
