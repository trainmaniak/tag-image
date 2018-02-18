
import zipfile
import urllib
import os
import shutil
import stat

from distutils.dir_util import copy_tree

from tools import *

class Update:
    url = 'https://raw.githubusercontent.com/trainmaniak/tag-image-update/master/'

    updateAppName = 'tag-image.zip'
    updateFileName = 'version.txt'

    updateTempDir = 'updateTemp'
    updateTempDirZip = 'zip'
    updateTempDirUnpacked = 'unpacked'

    separator = None

    osType = None
    currentVersion = None
    newVersion = None

    def __init__(self, si):
        self.currentVersion = si.appVersion
        self.osType = si.osType

        if (si.osType == OsType.LINUX):
            self.separator = '/'
        elif (si.osType == OsType.WIN):
            self.separator = '\\'

        self.updateTempDirZip = self.updateTempDir + self.separator + self.updateTempDirZip
        self.updateTempDirUnpacked = self.updateTempDir + self.separator + self.updateTempDirUnpacked

    def check(self):
        try:
            self.newVersion = urllib.request.urlopen(self.url + self.updateFileName).read().decode('utf-8')
        except:
            InfoPrinter.out(PrintOutput.WARNING, 'check update failed')
            return False

        self.newVersion = self.newVersion.replace('\r', '').replace('\n', '')

        InfoPrinter.out(PrintOutput.DEBUG, 'update: {} -> {}'.format(self.currentVersion, self.newVersion))

        cVersionArray = self.currentVersion.split('.')
        nVersionArray = self.newVersion.split('.')

        if (len(cVersionArray) != len(nVersionArray)):
            InfoPrinter.out(PrintOutput.WARNING, 'bad format of version string')
            return False

        if (nVersionArray[0] > cVersionArray[0]):
            return True
        if (nVersionArray[1] > cVersionArray[1]):
            return True
        if (nVersionArray[2] > cVersionArray[2]):
            return True

        return False

    def download(self):
        try:
            if not os.path.exists(self.updateTempDirZip):
                os.makedirs(self.updateTempDirZip)

            urllib.request.urlretrieve(self.url + self.updateAppName, self.updateTempDirZip + self.separator + self.updateAppName)
        except:
            InfoPrinter.out(PrintOutput.WARNING, 'download update failed')
            return False
        else:
            InfoPrinter.out(PrintOutput.OK, 'successfully downloaded update')
            return True

    def updateApp(self):
        try:
            # unzip
            zip_ref = zipfile.ZipFile(self.updateTempDirZip + self.separator + self.updateAppName, 'r')
            zip_ref.extractall(self.updateTempDirUnpacked)
            zip_ref.close()

            InfoPrinter.out(PrintOutput.OK, 'successfully unpacked update')

            # copy and overwrite
            copy_tree(self.updateTempDirUnpacked + self.separator, '.')

            # for linux only - make launcher and interpreter executable
            if (self.osType == OsType.LINUX):
                st = os.stat('app-linux.py')
                os.chmod('app-linux.py', st.st_mode | stat.S_IEXEC)
                st = os.stat('venv-linux/bin/python3')
                os.chmod('venv-linux/bin/python3', st.st_mode | stat.S_IEXEC)

            InfoPrinter.out(PrintOutput.OK, 'update was successful')
        except:
            InfoPrinter.out(PrintOutput.WARNING, 'update failed')
        finally:
            # clean temp directory
            try:
                shutil.rmtree(self.updateTempDirZip)
                shutil.rmtree(self.updateTempDirUnpacked)
            except:
                InfoPrinter.out(PrintOutput.WARNING, 'temp directory can not clean')
            else:
                InfoPrinter.out(PrintOutput.OK, 'temp directory cleaned')
