import os


class Repo(object):
    def __init__(self):
        pass

    def getall(self):
        current = os.getcwd()
        os.chdir('repository')
        file = os.listdir(os.getcwd())
        os.chdir(current)
        return file

    def getCount(self):
        repoList = self.getall()
        repoIDs = 0
        contentIDs = set()
        for each in repoList:
            repoID, contentID = each.split('_')
            contentIDs.add(contentID)
            repoIDs += 1
        tu = (repoIDs, len(contentIDs))
        return tu
