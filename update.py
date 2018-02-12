
import urllib.request

class Update:
    url = 'https://github.com/trainmaniak/imgs/blob/master/version.txt'
    currentVersion = None
    newVersion = None

    def __init__(self, currentVersion):
        self.currentVersion = currentVersion

    def check(self):
        response = urllib.request.urlopen(self.url)
        self.newVersion = response.read()

        currentVersionArr = self.currentVersion.split('.')
        newVersionArr = self.newVersion.split('.')

        if (len(currentVersionArr) != len(newVersionArr)):
            return False

        if (newVersionArr[0] > currentVersionArr[0]):
            return True
        if (newVersionArr[1] > currentVersionArr[1]):
            return True
        if (newVersionArr[2] > currentVersionArr[2]):
            return True

        return False

    def download(self):

        pass

    def updateApp(self):
        pass

    