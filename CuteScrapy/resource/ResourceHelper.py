# coding:utf8
__author__ = 'modm'
import json
import os

try:
    from scrapy.settings import Settings
    from scrapy.utils import project
except:
    pass


class ResourceHelper():
    def __init__(self):
        self.path = self._script_path()
        try:
            self.settings = project.get_project_settings()  # get settings
            self.configPath = self.settings.get("RESOURCE_DIR")
        except:
            pass
        if 'configPath' in self.__dict__:
            self.path = self.configPath

    def _script_path(self):
        import inspect, os
        this_file = inspect.getfile(inspect.currentframe())
        return os.path.abspath(os.path.dirname(this_file))

    def getPath(self, resourceName):
        return self.path + os.path.sep + resourceName

    def loadJson(self, resourceName):
        with open(self.path + os.path.sep + resourceName, 'r')as f:
            data = json.load(f)
        f.close
        return data

    def readStrings(self, resourceName):
        with open(self.path + os.path.sep + resourceName, 'r')as f:
            data = [line[:-1] for line in f.readlines()]
        f.close
        return data

    def get(self, key, resourceData):
        return resourceData[key]

    def write(self, resourceName, content):
        with open(self.path + os.path.sep + resourceName, 'w')as f:
            f.write(content)
        f.close

    def append(self, resourceName, content):
        with open(self.path + os.path.sep + resourceName, 'a')as f:
            f.write(content)
        f.close


if __name__ == '__main__':
    print ResourceHelper().readStrings("proxy.txt")
