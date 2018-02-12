
import urllib.request

class Update:
    url = 'https://github.com/trainmaniak/imgs/blob/master/version.txt'
    currentVersion = None
    newVersion = None

    def __init__(self, currentVersion):
        self.currentVersion = currentVersion

    def check(self):
        response = urllib.request.urlopen(self.url)
        data = response.read()

    def download(self):
        pass

    def implement(self):
        pass

    